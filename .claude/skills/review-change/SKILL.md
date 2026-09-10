---
name: review-change
description: Independently review a Bitewiz diff against its accepted plan and runtime invariants.
argument-hint: <plan-path>
context: fork
agent: voice-pipeline-reviewer
disable-model-invocation: true
---

Review the current diff against `$ARGUMENTS` and `AGENTS.md`. Return blocking findings, non-blocking findings, scope drift, and missing verification. Do not edit files.
