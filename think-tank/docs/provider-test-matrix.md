# Provider Test Matrix

Provider test matrix connects v1.1 provider patterns with the v2.0 provider invocation ledger.

It does not claim these providers are bundled or verified by default.

## Required Test Columns

| capability slot | pattern doc | preflight | permission gate | invocation evidence | recovery artifact | failure boundary | sample ledger |
|---|---|---|---|---|---|---|---|
| source-acquisition | `think-tank/examples/providers/patterns/source-acquisition-web-access.md` | provider exists, network allowed | source scope | command or tool ref | source notes | use user-provided material | `think-tank/examples/providers/ledgers/source-acquisition-web-access.json` |
| social-listening | `think-tank/examples/providers/patterns/social-listening-xiaohongshu.md` | service health, login state | platform permission | command or tool ref | sample summary | no social collection | `think-tank/examples/providers/ledgers/social-listening-xiaohongshu.json` |
| media-processing | `think-tank/examples/providers/patterns/media-processing-yt-dlp-whisper.md` | tool exists, media reachable | rights confirmation | command or tool ref | transcript or metadata | user-provided transcript | `think-tank/examples/providers/ledgers/media-processing-yt-dlp-whisper.json` |
| knowledge-persistence | `think-tank/examples/providers/patterns/knowledge-persistence-obsidian.md` | vault path known | explicit write confirmation | command or tool ref | note path | propose-only memory | `think-tank/examples/providers/ledgers/knowledge-persistence-obsidian.json` |
| media-production | `think-tank/examples/providers/patterns/media-production-research-to-video.md` | production provider ready | asset rights and scope | command or tool ref | production package | storyboard-only output | `think-tank/examples/providers/ledgers/media-production-research-to-video.json` |

## State Rule

```text
selected != invoked != recovered != verified
```

## Ledger Entry Requirements

Each sample ledger must include:

```yaml
capability_slot:
provider_name:
state:
preflight:
dispatch:
invocation:
recovery:
verification:
failure_boundary:
```

## Public Boundary

Provider test samples are public-safe structure examples. They must not contain credentials, private URLs, account identifiers, private source data, or real login state.
