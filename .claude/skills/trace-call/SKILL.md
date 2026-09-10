---
name: trace-call
description: Trace one Bitewiz call behavior across WebSocket, dispatcher, STT, LLM, tools, TTS, and cleanup.
argument-hint: <behavior-or-event>
context: fork
agent: call-flow-explorer
disable-model-invocation: true
---

Investigate `$ARGUMENTS`. Return the concrete entry point, every relevant publisher/subscriber, mutable state, trust boundary, external call, and disconnect/error behavior. Do not edit files.
