#!/usr/bin/env bash
# n8n/workflows/*.json을 실행 중인 n8n에 등록하고 게시(활성화)한다.
# 워크플로 JSON은 자격증명 ID 대신 SLACK_CREDENTIAL_ID 자리표시자를 갖는다 —
# ID는 n8n 인스턴스마다 다르므로 이름("Slack · Library QA")으로 찾아 치환한다.
set -euo pipefail
cd "$(dirname "$0")/.."
COMPOSE=(docker compose -f compose.qa.yml)
CRED_NAME="Slack · Library QA"

cred_id=$("${COMPOSE[@]}" exec -T n8n sh -c '
  n8n export:credentials --all --output=/tmp/c.json >/dev/null 2>&1
  node -e "const c=require(\"/tmp/c.json\").find(x=>x.name===process.argv[1]); console.log(c?c.id:\"\")" "$1"
  rm -f /tmp/c.json' _ "$CRED_NAME")
if [[ -z "$cred_id" ]]; then
  echo "n8n에 '$CRED_NAME' 자격증명이 없습니다. n8n 화면에서 먼저 만드세요." >&2
  exit 1
fi

for wf in n8n/workflows/*.json; do
  id=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$wf")
  sed "s/SLACK_CREDENTIAL_ID/$cred_id/g" "$wf" | "${COMPOSE[@]}" exec -T n8n sh -c "cat > /tmp/wf.json && n8n import:workflow --input=/tmp/wf.json && n8n publish:workflow --id=$id && rm /tmp/wf.json"
  echo "등록·게시: $(basename "$wf") ($id)"
done

# CLI로 바꾼 게시 상태는 실행 중인 프로세스에 반영되지 않으므로 재시작한다.
"${COMPOSE[@]}" restart n8n >/dev/null
echo "n8n 재시작 완료"
