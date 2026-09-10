---
name: ship-change
description: Prepare a factual commit or PR handoff for an accepted and reviewed Bitewiz change.
argument-hint: <plan-path>
disable-model-invocation: true
---

Read `$ARGUMENTS`, the diff, review findings, and observed verification. Stop if blocking findings or required failed checks remain. Inspect for secrets and unrelated files. Draft a commit/PR summary with behavior, architecture impact, commands run, checks not run, residual risk, and rollback. Do not commit, push, merge, or deploy without explicit human approval.
