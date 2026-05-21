# Image2 Prompt: Provider Invocation Ledger

Create a README infographic for think-tank 2.0 explaining the Provider Invocation Ledger.

Visual goal: make it visually obvious that "selected" is not the same as "invoked".

Composition:
- 16:9 horizontal image
- title: "Provider Invocation Ledger"
- state machine across the center:
  "candidate" -> "discovered" -> "selected" -> "preflight" -> "dispatched" -> "invoked" -> "recovered" -> "verified"
- add clear boundary markers:
  - after "selected": "not invoked yet"
  - after "preflight": "not a result yet"
  - after "recovered": "needs evidence"
- side panel: "Blocked provider" with reasons:
  "permission", "login", "rights", "runtime", "security"
- side panel: "Ledger entry" with fields:
  "capability", "provider", "state", "dispatch", "recovery", "verification"
- footer: "selected != invoked != recovered != verified"

Style:
- polished technical product graphic
- clean PNG bitmap, not SVG-like
- light documentation background, sharp cards, readable text
- use distinct but restrained status colors

Constraints:
- Do not imply any provider is bundled.
- Do not show real provider logos or private account state.
- Avoid dense tiny text.
- Aspect ratio 16:9.
