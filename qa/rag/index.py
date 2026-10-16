"""vault 노트 → 청크 → 로컬 임베딩 → Redis 벡터 인덱스.

원본은 vault(git)이고 인덱스는 언제든 다시 만들 수 있는 파생물이다.
파일 단위 해시로 바뀐 노트만 다시 임베딩한다(QA 리포트가 계속 쌓이므로).
"""

import hashlib
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from redis.commands.search.field import TagField, TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition, IndexType

from qa.config import ROOT, settings
from qa.jobs.queue import redis

VAULT = ROOT / "vault"
INDEX = "qa-docs"
PREFIX = "qa:doc:"
FILE_HASHES = "qa:docfiles"  # path → 파일 해시
MODEL = "intfloat/multilingual-e5-large"
DIM = 1024
MAX_CHARS = 1200  # e5 입력 한도(512 토큰) 안에 들도록 자른다


@dataclass
class Chunk:
    path: str        # vault 기준 상대 경로 — Obsidian 링크로 그대로 쓴다
    title: str
    heading: str
    source: str      # 기획서 | 이력 | QA 리포트
    repo: str
    text: str


@lru_cache(maxsize=1)
def model():
    from fastembed import TextEmbedding  # 로딩이 무거워 실제로 쓸 때만 불러온다
    # 기본 캐시는 OS 임시 폴더라 재부팅 시 2GB를 다시 내려받는다 — 작업 폴더에 둔다.
    return TextEmbedding(MODEL, cache_dir=str(settings.work_dir / "models"))


def embed(texts: list[str], kind: str) -> np.ndarray:
    # e5 계열은 질문과 문서에 서로 다른 접두어를 붙여야 성능이 나온다.
    prefixed = [f"{kind}: {t}" for t in texts]
    return np.array(list(model().embed(prefixed)), dtype=np.float32)


def _split_frontmatter(raw: str) -> tuple[dict, str]:
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        return yaml.safe_load(fm) or {}, body
    return {}, raw


def chunk_note(path: Path) -> list[Chunk]:
    fm, body = _split_frontmatter(path.read_text())
    rel = str(path.relative_to(VAULT))
    title_match = re.search(r"^# (.+)$", body, re.M)
    title = title_match.group(1).strip() if title_match else path.stem
    source = fm.get("type") or rel.split("/")[0]
    repo = fm.get("repo", "")
    chunks = []
    # ## 단위로 나눈다. 제목은 모든 청크 앞에 붙여 맥락을 잃지 않게 한다.
    for section in re.split(r"\n(?=## )", body):
        heading = section.strip().splitlines()[0].lstrip("# ").strip() if section.strip() else ""
        text = re.sub(r"\n{3,}", "\n\n", section).strip()
        for i in range(0, max(len(text), 1), MAX_CHARS):
            piece = text[i:i + MAX_CHARS].strip()
            if piece:
                chunks.append(Chunk(rel, title, heading, source, repo, f"{title}\n{piece}"))
    return chunks


def ensure_index() -> None:
    r = redis()
    try:
        r.ft(INDEX).info()
    except Exception:
        r.ft(INDEX).create_index(
            [TagField("path"), TagField("source"), TagField("repo"),
             TextField("title"), TextField("text"),
             VectorField("embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": DIM, "DISTANCE_METRIC": "COSINE"})],
            definition=IndexDefinition(prefix=[PREFIX], index_type=IndexType.HASH),
        )


def sync() -> dict:
    """vault와 인덱스를 맞춘다. 바뀐 파일만 다시 임베딩하고, 지워진 파일은 인덱스에서도 지운다."""
    ensure_index()
    r = redis()
    known = {k.decode(): v.decode() for k, v in r.hgetall(FILE_HASHES).items()}
    current = {str(p.relative_to(VAULT)): p for p in VAULT.rglob("*.md") if not p.name.startswith(".")}
    stats = {"added": 0, "updated": 0, "removed": 0, "unchanged": 0, "chunks": 0}

    for rel in set(known) - set(current):
        _delete_file(rel)
        stats["removed"] += 1

    for rel, path in current.items():
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        if known.get(rel) == digest:
            stats["unchanged"] += 1
            continue
        _delete_file(rel)
        chunks = chunk_note(path)
        vectors = embed([c.text for c in chunks], "passage") if chunks else []
        pipe = r.pipeline()
        for i, (c, v) in enumerate(zip(chunks, vectors)):
            pipe.hset(f"{PREFIX}{hashlib.sha1(rel.encode()).hexdigest()[:12]}:{i}", mapping={
                "path": rel, "title": c.title, "heading": c.heading, "source": c.source,
                "repo": c.repo, "text": c.text, "embedding": v.tobytes(),
            })
        pipe.hset(FILE_HASHES, rel, digest)
        pipe.execute()
        stats["updated" if rel in known else "added"] += 1
        stats["chunks"] += len(chunks)
    return stats


def _delete_file(rel: str) -> None:
    r = redis()
    keys = list(r.scan_iter(f"{PREFIX}{hashlib.sha1(rel.encode()).hexdigest()[:12]}:*"))
    if keys:
        r.delete(*keys)
    r.hdel(FILE_HASHES, rel)


def all_chunks() -> list[dict]:
    r = redis()
    out = []
    for key in r.scan_iter(f"{PREFIX}*"):
        h = r.hgetall(key)
        out.append({k.decode(): v.decode() for k, v in h.items() if k != b"embedding"})
    return out
