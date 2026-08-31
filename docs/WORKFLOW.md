# Development Workflow

> Flow ปัจจุบันของ Agentic Demo — Agent ทำ code, Human approve + promote

---

## Overview

```mermaid
flowchart TD
    A["🧑 Human: สร้าง feature spec"] --> B["🤖 Agent: implement (TDD)"]
    B --> C["🤖 Agent: validate"]
    C --> D["🤖 Agent: commit + push"]
    D --> E["🤖 Agent: create PR → dev"]
    E --> F{"CI Pass?"}
    F -->|❌| B
    F -->|✅| G["🧑 Human: approve PR → dev"]
    G --> H["🧑 Human: PR dev → qa"]
    H --> I{"CI Pass?"}
    I -->|❌| B
    I -->|✅| J["🧑 Human: approve (1)"]
    J --> K["🧑 Human: PR qa → sit"]
    K --> L{"CI Pass?"}
    L -->|❌| B
    L -->|✅| M["🧑 Human: approve (1)"]
    M --> N["🧑 Human: PR sit → uat"]
    N --> O{"CI Pass?"}
    O -->|❌| B
    O -->|✅| P["🧑 Human: approve (1)"]
    P --> Q["🧑 Human: PR uat → main"]
    Q --> R{"CI Pass?"}
    R -->|❌| B
    R -->|✅| S["🧑 Human: approve (2)"]
    S --> T["🎉 Production"]
```

---

## Responsibility Split

| Phase | Agent | Human |
|-------|:-----:|:-----:|
| Design (spec) | - | ✅ |
| Implement (TDD) | ✅ | - |
| Validate (lint/type/test) | ✅ | - |
| Commit + push | ✅ | - |
| Create PR → dev | ✅ | - |
| Approve PR | - | ✅ |
| Promote ข้าม env | - | ✅ |

---

## Branch Protection Rules

| Branch | Required Approvals | CI Required |
|--------|:------------------:|:-----------:|
| dev | 0 | ✅ |
| qa | 1 | ✅ |
| sit | 1 | ✅ |
| uat | 1 | ✅ |
| main | 2 | ✅ |

---

## Agent Workflow (สิ่งที่ Agent ทำ)

```bash
# 1. Implement
# TDD: RED → GREEN → REFACTOR

# 2. Validate
cd backend && python scripts/pre_commit_validate.py
cd frontend && python scripts/validate.py

# 3. Commit + push
git add -A
git commit -m "feat: feature-name"
git push -u origin HEAD

# 4. Create PR
gh pr create --title "feat: feature-name" --body "..." --base dev

# DONE — agent ไม่ต้องทำอะไรต่อ
```

---

## Human Workflow (สิ่งที่ Human ทำ)

```bash
# 1. Approve PR → dev (GitHub UI)
# 2. Create PR dev → qa
gh pr create --title "promote: dev → qa" --base qa --head dev
# 3. Approve PR qa → sit (1 approval)
# 4. Create PR sit → uat
# 5. Approve PR uat → main (2 approvals)
```

---

## Diagram แยก Agent vs Human

```mermaid
flowchart LR
    subgraph Agent["🤖 Agent"]
        A1[Implement] --> A2[Validate]
        A2 --> A3[Commit]
        A3 --> A4[Push]
        A4 --> A5[Create PR → dev]
    end
    
    subgraph Human["🧑 Human"]
        H1[Approve PR] --> H2[Create PR → next env]
        H2 --> H3[Approve PR]
    end
    
    A5 -->|PR ready| H1
```

---

*Last updated: 2026-08-31*
