@AGENTS.md

# Claude Code routing

Keep always-loaded instructions here minimal. Use project skills for procedures.

- `/plan-change` creates a living ExecPlan before substantial work.
- `/trace-call` investigates the event flow without editing.
- `/review-change` delegates an independent read-only review.
- `/ship-change` prepares evidence only after review; repository actions require human approval.

Use the project agents in `.claude/agents/`. Do not create or edit Claude's runtime files under `~/.claude/teams/` or `~/.claude/tasks/`.
