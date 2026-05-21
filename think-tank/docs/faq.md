# FAQ

## Is think-tank an agent runtime?

No. `think-tank` is a protocol-first Skill core. It defines modes, profiles, capability slots, provider boundaries, run records, memory runtime contracts, handoff packets, guardrails, and eval fixtures.

Platform adapters or external runtimes may implement parts of the protocol.

## Are providers bundled?

No. Provider examples are optional patterns. A provider must be installed, permissioned, invoked, recovered, and verified in the user's environment before it can be reported as working.

## Does selected mean invoked?

No.

```text
selected != invoked != recovered != verified
```

## Does think-tank store my project memory?

The public core does not store user project memory. Research OS defines a local workspace contract. User projects own their own workspace data.

## Can I use only the Skill core?

Yes. The core docs, schemas, templates, examples, and checks are useful even without optional providers.

## Is 2.0 stable?

2.0 is stable for the public protocol-first release scope. It does not claim every provider, every platform runtime, or every true multi-agent workflow is production-ready.
