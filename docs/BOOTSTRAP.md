# Bootstrap — ใช้ Repo นี้กับโปรเจคใหม่ (3 ขั้นตอน)

> Clone → Config → Loop — จบภายใน 5 นาที

---

## 1. Clone & Install (1 นาที)

```bash
git clone https://github.com/tuit2542/agentic-demo.git my-project
cd my-project

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt && cd ..

# Frontend
cd frontend && npm install && cd ..

# Env
cp .env.example .env   # แก้ค่า DB_URL / JWT_SECRET ตามจริง
```

## 2. Config ให้เป็นโปรเจคของตัวเอง (2 นาที)

แก้ **3 จุดนี้** ให้เป็นโปรเจคใหม่:

| ไฟล์ | ต้องแก้ | ตัวอย่าง |
|------|---------|----------|
| `AGENTS.md` | `## Project Goal` บรรทัดแรก | เปลี่ยนจาก "URL Shortener" → "Todo App ของคุณ" |
| `.hermes/specs/TEMPLATE.md` | User story / API contract | ใส่ spec ของ feature แรกที่จะให้ AI ทำ |
| `docs/TRACKING.md` | Checklist | ใส่ feature list ของโปรเจคใหม่ |

```bash
# สร้าง feature แรกให้ AI ทำ
cp .hermes/specs/TEMPLATE.md .hermes/specs/my-first-feature.md
# เปิดไฟล์แล้วใส่ story + acceptance criteria + API contract
```

## 3. สั่ง AI ทำ Loop (1 บรรทัด)

```bash
# เลือก AI ที่ชอบ — แค่เปลี่ยนตัวเรียก, prompt เดียวกันหมด
agy -p "$(cat docs/AI_PROMPT_TEMPLATE.md)" --dangerously-skip-permissions
# หรือ
claude -p "$(cat docs/AI_PROMPT_TEMPLATE.md)" --dangerously-skip-permissions
# หรือ
codex --approval-mode full-auto "$(cat docs/AI_PROMPT_TEMPLATE.md)"
```

AI จะทำเอง: `RED → GREEN → REFACTOR → lint → type check → commit → push → PR → dev` ✅

---

## ไฟล์สำคัญที่ต้องรู้

```
agentic-demo/
├── AGENTS.md                      ← กฎโปรเจค (AI อ่านทุกครั้ง)
├── .hermes.md                     ← กฎ monorepo
├── backend/.hermes.md             ← กฎ backend
├── frontend/.hermes.md            ← กฎ frontend
├── .hermes/specs/
│   ├── TEMPLATE.md                ← แบบฟอร์ม spec ให้ AI ทำตาม
│   └── my-first-feature.md        ← spec feature แรก (สร้างเอง)
├── docs/
│   ├── AI_PROMPT_TEMPLATE.md      ← copy ไปสั่ง AI ได้เลย
│   ├── TRACKING.md                ← checklist ทุก feature
│   └── WORKFLOW.md                ← Flow: feat → dev → qa → sit → uat → main
├── backend/src/                   ← code
└── frontend/src/                  ← code
```

## Quality Gates (AI จะทำเองก่อน commit ทุกครั้ง)

| Gate | Backend | Frontend |
|------|---------|----------|
| Lint | `ruff check` | `eslint` |
| Type | `mypy` | `tsc --noEmit` |
| Test | `pytest` | `vitest` |
| Validate all | `python scripts/pre_commit_validate.py` | `npm run lint && npx tsc --noEmit && npm run test` |

## Branching

```
feat/my-feature → dev → qa → sit → uat → main
     ↑ AI ทำถึง dev แล้วหยุด — Human ค่อย promote ต่อ (1-2 approvals)
```

## ลบของเก่า (ถ้าอยากเริ่ม clean)

```bash
# ลบ code URL Shortener เก่า แต่เก็บโครง + scripts + workflow
rm -rf backend/src/* backend/tests/* frontend/src/app/* .hermes/specs/*.md
# เหลือ: AGENTS.md, WORKFLOW, CI, scripts, TEMPLATE — แล้วเริ่มใหม่ได้เลย
```

## Troubleshooting

| ปัญหา | แก้ |
|------|-----|
| `mypy` fail | `mypy src/ --ignore-missing-imports` |
| `ruff` fail | `ruff format src/ tests/ && ruff check --fix` |
| `gh pr create` fail | `gh auth login` ก่อน |
| Port ชน | `.env` แก้ `BACKEND_PORT` |
| DB ไม่ขึ้น | `DATABASE_URL=""` = in-memory (ไม่ต้องมี DB ก็รันได้) |
