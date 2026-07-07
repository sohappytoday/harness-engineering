---
name: commit-message
description: "스테이징된 변경을 바탕으로 AngularJS Commit Convention 형식의 커밋 메시지를 2인 팀(author, reviewer) 협업으로 작성한다. '커밋 메시지', 'commit message' '커밋 메시지 만들어줘' 같은 자연어 요청 시 반드시 사용한다. 단, 이미 메시지가 작성된 `git commit -m` 대체는 아니다."
allowed-tools: Bash, Read, Write, Task
---

# Commit Message Skill
2인 팀을 순차로 호출해 AngularJS Commit Convention 형식의 커밋 메시지를 생성한다.

## Workflow
1. Precondition 체크.
  `git diff --cached --quiet`를 실행해 스테이징된 변경이 없으면 문구와 함께 종료한다.
2. Author 에이전트 호출.
  `commit-msg-author` 에이전트를 Agent 도구로 호출.
  출력은 `_workspace/commit-message-draft.md`에 작성.
3. Reviewer 에이전트 호출.
  `commit-msg-reviewer` 에이전트를 Agent 도구로 호출.
  출력은 `_workspace/commit-message-review.md`에 작성.
4. 판정 분기.
  - PASS: `_workspace/commit-message-draft.md` 내용을 사용자에게 제시하고 완료.
  - REDO: reviewer 수정 지시를 프롬프트에 포함해 author를 재호출한 뒤, 3번(Reviewer)으로 복귀해 재검토한다 (최대 2회).
5. 루프 종료.
  2회 재작성 후에도 REDO면 "자동 승인 한계 도달 - 수동 검토 권장" 경고와 함께 마지막 draft를 반환하고 종료한다 (무한 루프 방지).