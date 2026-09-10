# Add an inspectable agent operating layer

This ExecPlan is governed by `.agent/PLANS.md`.

## Purpose / Big Picture

Let a reviewer see how substantial Bitewiz work is investigated, planned, delegated, reviewed, and prepared for shipping. The setup must be grounded in the existing voice pipeline and must not imply that earlier commits used a workflow added later.

## Scope and exclusions

Add shared agent instructions, Claude-specific routing, three project roles, four reusable skills, this living plan, and an architecture-accurate README. Do not change application behavior, add tests or CI, install Claude Code, fabricate transcripts, or publish without approval.

## Progress

- [x] (2026-09-11 00:00Z) Audited repository structure and history.
- [x] (2026-09-11 00:00Z) Researched current official Claude Code and OpenAI conventions.
- [x] (2026-09-11 00:00Z) Added shared and Claude-specific instruction entrypoints.
- [x] (2026-09-11 00:00Z) Added bounded explorer, implementer, and reviewer roles.
- [x] (2026-09-11 00:00Z) Added planning, tracing, review, and shipping workflows as skills.
- [x] (2026-09-11 00:00Z) Replaced the one-line README with an honest architecture and repository guide.
- [x] (2026-09-11 00:00Z) Reviewed every agent/skill frontmatter block, the instruction import, the README against repository paths, secret patterns, scope, and whitespace; no blocking finding remained.
- [ ] Obtain human approval before commit and push.

## Surprises & Discoveries

Claude Code now treats project skills as custom slash workflows; `.claude/commands/` remains compatible but is no longer the preferred structure. Claude Code reads `CLAUDE.md`, not `AGENTS.md`, so `CLAUDE.md` imports the shared file.

## Decision Log

- **2026-09-11:** Add no application code, tests, or CI because the accepted task is the orchestration evidence layer.
- **2026-09-11:** Use project skills instead of legacy command files.
- **2026-09-11:** State when this layer was added and avoid claims of earlier use.
- **2026-09-11:** Keep implementation agents worktree-isolated and review agents read-only.

## Milestones

The first milestone establishes one cross-tool source of truth through `AGENTS.md` and `CLAUDE.md`. The second adds repository-specific agents and skills. The third makes the project itself understandable through an accurate README and completes a documentation-only review.

## Validation and acceptance

Inspect all frontmatter for unique names and required descriptions. Confirm `CLAUDE.md` begins with `@AGENTS.md`. Confirm the README's architecture maps to actual paths and no production integration, verification, or historical-use claim exceeds the repository evidence. Run `git diff --check` and inspect `git status --short` for scope.

## Safety and recovery

The changes are documentation and agent configuration only. They can be reverted without changing runtime behavior. Commit and push remain separate human-approved actions.

## Outcomes & Retrospective

The repository now exposes a truthful agent operating layer tied to its actual asynchronous voice architecture. The change is limited to documentation and agent configuration; application behavior, tests, and CI are unchanged. Static review passed, but Claude Code runtime discovery was not run because the CLI is unavailable. Commit and push remain pending human approval.
