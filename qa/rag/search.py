"""검색 3종. 어떤 방식을 쓸지는 측정(eval)으로 정한다.

- vector : 로컬 임베딩 + Redis KNN — 표현이 달라도 뜻이 같으면 찾는다
- keyword: BM25 (한국어는 형태소 분석기 없이 글자 2-gram으로 근사) — 단순·빠름
- agentic: Claude Code가 vault를 직접 grep/read — 구성 요소 없음, 호출마다 시간·토큰
"""

import math
import re
from collections import Counter
from dataclasses import dataclass

from redis.commands.search.query import Query

from qa.intent import claude
from qa.jobs.queue import redis
from qa.rag import index


@dataclass
class Hit:
    path: str
    title: str
    heading: str
    text: str
    score: float


def _source_filter(source: str | None) -> str:
    return f"@source:{{{source}}}" if source else "*"


def vector(query: str, k: int = 5, source: str | None = None) -> list[Hit]:
    q = index.embed([query], "query")[0]
    res = redis().ft(index.INDEX).search(
        Query(f"({_source_filter(source)})=>[KNN {k} @embedding $vec AS dist]")
        .sort_by("dist").return_fields("path", "title", "heading", "text", "dist").dialect(2),
        query_params={"vec": q.tobytes()},
    )
    return [Hit(d.path, d.title, d.heading, d.text, 1 - float(d.dist)) for d in res.docs]


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[0-9A-Za-z_]+|[가-힣]+", text.lower())
    out = []
    for w in words:
        if re.match(r"[가-힣]", w):
            out += [w[i:i + 2] for i in range(len(w) - 1)] or [w]  # 조사·어미가 붙어도 겹치도록 2-gram
        else:
            out.append(w)
    return out


def keyword(query: str, k: int = 5, source: str | None = None, k1: float = 1.5, b: float = 0.75) -> list[Hit]:
    docs = [c for c in index.all_chunks() if not source or c["source"] == source]
    toks = [_tokens(d["text"]) for d in docs]
    avg = sum(map(len, toks)) / max(len(toks), 1)
    df = Counter(t for ts in toks for t in set(ts))
    q = _tokens(query)
    scored = []
    for d, ts in zip(docs, toks):
        tf = Counter(ts)
        s = sum(math.log(1 + (len(docs) - df[t] + 0.5) / (df[t] + 0.5))
                * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(ts) / avg)) for t in q if t in tf)
        if s > 0:
            scored.append(Hit(d["path"], d["title"], d["heading"], d["text"], s))
    return sorted(scored, key=lambda h: -h.score)[:k]


AGENTIC_SYSTEM = """너는 문서 검색기다. vault 폴더의 마크다운 노트에서 질문과 관련된 노트를 찾는다.
Grep·Glob·Read 도구로 직접 찾아 읽고, 관련도가 높은 순서로 노트 경로(vault 기준 상대 경로)를 돌려준다.
표현이 달라도 같은 뜻이면 관련 있는 것으로 본다(예: '이름 안 보임' ≈ '개인정보 파기')."""


def agentic(query: str, k: int = 5, source: str | None = None) -> list[Hit]:
    scope = f"{source}/ 폴더 안에서만 " if source else ""
    out = claude.structured(
        f"{scope}다음과 관련된 노트를 최대 {k}개 찾아라: {query}",
        {"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}},
         "required": ["paths"], "additionalProperties": False},
        AGENTIC_SYSTEM, tools="Grep,Glob,Read", effort="low", timeout=180,
        extra_args=["--allowedTools", "Grep,Glob,Read"], cwd=index.VAULT,
    )
    return [Hit(p, p, "", "", 1.0 / (i + 1)) for i, p in enumerate(out["paths"][:k])]


METHODS = {"vector": vector, "keyword": keyword, "agentic": agentic}


def unique_notes(hits: list[Hit]) -> list[Hit]:
    """같은 노트의 여러 청크는 가장 높은 것 하나만 남긴다 (근거 링크는 노트 단위)."""
    seen, out = set(), []
    for h in hits:
        if h.path not in seen:
            seen.add(h.path)
            out.append(h)
    return out
