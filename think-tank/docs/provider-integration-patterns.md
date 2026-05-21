# Provider Integration Patterns

`think-tank` documents provider integration patterns. It does not bundle peer skills, perform provider login, or guarantee that a provider can be invoked in a user's environment.

This document is a v1.1 pattern pack for optional provider ecosystems. It is meant to help users connect their own tools without confusing `route selection` with `provider invocation`.

Core evidence boundary:

```text
selected != dispatched != invoked != recovered != verified
```

## Status Vocabulary

Use these states when writing examples, reports, or provider notes:

```yaml
pattern_documented: The integration shape is described.
available_if_user_installs_provider: The provider can be used only when the user installs and exposes it.
requires_user_environment: Runtime, account, permissions, paths, or services are user-owned.
not_bundled: The provider is not shipped by think-tank.
selected_not_invoked: Policy selected a provider, but no tool call happened.
invoked: A concrete tool or skill call happened in this run.
recovered: think-tank received provider output and used it in the final result.
verified_partial: A scoped path has evidence, but coverage is incomplete.
```

## Required Boundary Block

Every provider-assisted example should include this block, adapted to the task:

```yaml
provider_boundary:
  route_selected:
  provider_preflight:
  dispatch_decision:
  invoked_providers:
  not_invoked_providers:
  recovery:
  boundaries:
  verification_status:
```

## Pattern Families

| pattern | example provider class | what think-tank does | what the provider does |
|---|---|---|---|
| source acquisition | web access skill | define evidence needs and source quality gates | fetch or read sources if available |
| social listening | social platform skill | define sample shape and consent boundary | collect platform samples if logged in and allowed |
| media processing | download or transcription skill | define media rights, artifact plan, and transcript needs | download, extract, or transcribe when permitted |
| knowledge persistence | local notes or vault skill | propose memory candidates and write boundary | write only after explicit user confirmation |
| media production | production workflow skill | convert research into storyboard and acceptance criteria | create production package or render artifacts |

## Non-Claims

Do not write:

- `think-tank supports xiaohongshu`
- `think-tank integrates yt-dlp`
- `think-tank provides Obsidian persistence`
- `All peer skills are invoked automatically`

Write instead:

- `think-tank documents a social-listening provider pattern using xiaohongshu as an example`
- `think-tank documents a media-processing provider pattern that can use yt-dlp if the user installs and authorizes it`
- `think-tank can propose knowledge-persistence writes, while the user's provider performs the write after confirmation`

## Example Index

- [`examples/provider-patterns/source-acquisition-web-access.md`](../examples/provider-patterns/source-acquisition-web-access.md)
- [`examples/provider-patterns/social-listening-xiaohongshu.md`](../examples/provider-patterns/social-listening-xiaohongshu.md)
- [`examples/provider-patterns/media-processing-yt-dlp-whisper.md`](../examples/provider-patterns/media-processing-yt-dlp-whisper.md)
- [`examples/provider-patterns/knowledge-persistence-obsidian.md`](../examples/provider-patterns/knowledge-persistence-obsidian.md)
- [`examples/provider-patterns/media-production-research-to-video.md`](../examples/provider-patterns/media-production-research-to-video.md)
