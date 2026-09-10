# Bitewiz execution plans

An ExecPlan is a self-contained, living design that a contributor can execute using only the working tree and the plan.

Use one for changes spanning multiple pipeline components, event types, third-party integrations, schemas, or more than about an hour of work.

Every plan must explain the user-visible purpose, exact affected paths and event flow, scope and exclusions, milestones, acceptance commands, safety, and recovery. Maintain `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` throughout execution.

The plan must name every changed publisher and subscriber, state how per-call isolation is preserved, and distinguish deterministic checks from credentialed OpenAI/Deepgram verification. A plan is complete only when its observable acceptance is recorded or an unmet condition is explicit.
