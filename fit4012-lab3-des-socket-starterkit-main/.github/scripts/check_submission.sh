#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "[CHECK] Kiem tra cau truc nop bai..."
required=(
  sender.py
  receiver.py
  des_socket_utils.py
  README.md
  report-1page.md
  threat-model-1page.md
  peer-review-response.md
  tests
  logs
)
echo "[CHECK] Kiem tra so luong test..."
count=$(find tests -maxdepth 1 -type f | wc -l | tr -d ' ')
[[ "$count" -ge 5 ]] || { echo "[FAIL] Can it nhat 5 file test trong tests/"; exit 1; }

echo "[CHECK] Kiem tra negative tests..."
ls tests/*tamper* >/dev/null 2>&1 || { echo "[FAIL] Thieu test tamper"; exit 1; }
ls tests/*wrong*key* >/dev/null 2>&1 || { echo "[FAIL] Thieu test wrong key"; exit 1; }

echo "[CHECK] Kiem tra cac muc bat buoc trong README..."
grep -qi "How to run" README.md || { echo "[FAIL] README thieu How to run"; exit 1; }
grep -qi "Input / Output" README.md || { echo "[FAIL] README thieu Input / Output"; exit 1; }
grep -qi "Threat-model awareness" README.md || { echo "[FAIL] README thieu Threat-model awareness"; exit 1; }
grep -qi "Ethics & Safe use" README.md || { echo "[FAIL] README thieu Ethics & Safe use"; exit 1; }
grep -qi "Team members" README.md || { echo "[FAIL] README thieu Team members"; exit 1; }
grep -qi "Task division" README.md || { echo "[FAIL] README thieu Task division"; exit 1; }
grep -qi "Demo roles" README.md || { echo "[FAIL] README thieu Demo roles"; exit 1; }

echo "[CHECK] Kiem tra README da khai bao du 2 thanh vien va phan cong..."
for token in TODO_MEMBER_1 TODO_MEMBER_1_ID TODO_MEMBER_2 TODO_MEMBER_2_ID TODO_ROLE_MEMBER_1 TODO_ROLE_MEMBER_2 TODO_SHARED_WORK TODO_DEMO_ROLE_1 TODO_DEMO_ROLE_2 TODO_DEMO_ROLE_SHARED; do
  if grep -q "$token" README.md; then
    echo "[FAIL] README van con placeholder $token"
    exit 1
  fi
done

echo "[CHECK] Kiem tra cac file OBE co con placeholder khong..."
for doc in report-1page.md threat-model-1page.md peer-review-response.md; do
  if grep -q "TODO_STUDENT" "$doc"; then
    echo "[FAIL] $doc van con TODO_STUDENT"
    exit 1
  fi
done

echo "[CHECK] Kiem tra logs minh chung..."
real_logs=$(find logs -maxdepth 1 -type f ! -name '.gitkeep' ! -name 'README.md' | wc -l | tr -d ' ')
[[ "$real_logs" -ge 1 ]] || { echo "[FAIL] logs/ chua co log minh chung that"; exit 1; }

echo "[PASS] Submission contract hop le."
