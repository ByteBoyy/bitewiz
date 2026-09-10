# Bitewiz agent instructions

## Purpose

Maintain Bitewiz as a real-time voice application. Preserve call isolation, explicit tool contracts, and coordinated shutdown.

## Repository map

- `app.py`: routes, connection IDs, and task assembly.
- `lib_infrastructure/dispatcher.py`: typed per-call pub/sub.
- `lib_socket_handler/`: client I/O and disconnect handling.
- `lib_stt/`: Deepgram speech-to-text.
- `lib_llm/`: relevance gate, model streaming, prompts, and tools.
- `lib_tts/`: Deepgram text-to-speech.
- `public/` and `templates/`: browser client.

## Invariants

- Scope every pipeline event to the connection `guid`.
- Keep OpenAI and Deepgram credentials in server-side environment variables.
- Resolve model tool requests only through the explicit `tool_implementations` map.
- Treat audio, transcripts, model output, and tool arguments as untrusted data.
- Bound retained conversational state.
- Dispose every task created for a disconnected call.
- Do not claim an external integration worked unless it was run and observed.

## Workflow

1. Trace both publishers and subscribers for every affected `MessageType`.
2. Use an ExecPlan governed by `.agent/PLANS.md` for multi-file, risky, or architectural work.
3. Obtain human acceptance of the plan before implementation.
4. Delegate a bounded file set; never allow concurrent agents to edit the same file.
5. Review the complete diff separately from implementation.
6. Record commands actually run and checks not run.
7. Do not commit, push, merge, or deploy without explicit human approval.

## Review focus

Check blocking work inside async paths, task cancellation, cross-call state, unbounded model/tool recursion, schema/implementation drift, secrets, user-content logging, and claims that exceed the prototype's actual behavior.

## ExecPlans

For substantial work, create a self-contained living plan under `plans/` and maintain it according to `.agent/PLANS.md`.
