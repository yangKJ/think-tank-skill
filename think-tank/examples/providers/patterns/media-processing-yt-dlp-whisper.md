# Media Processing Provider Pattern

This example documents a media-processing pattern using `yt-dlp` and `openai-whisper` as representative peer skills. It does not grant download rights, transcription rights, or provider availability.

```yaml
pattern_status:
  pattern_documented: true
  available_if_user_installs_provider: true
  requires_user_environment: network access, media rights, local storage, transcription runtime
  not_bundled: true
```

## User Intent

Turn a user-provided media URL or local file into a transcript and structured research notes.

## think-tank Role

- Confirm the user has rights to process the media.
- Define output artifacts: transcript, timestamps, quotes, summary, and known gaps.
- Route to `media-processing` only when provider preflight passes.
- Keep downloaded media and transcripts out of the public skill core.

## Provider Boundary

```yaml
provider_boundary:
  route_selected: media-processing
  provider_preflight: check media rights, tool availability, storage path, and expected output
  dispatch_decision: invoke only after permission and artifact location are clear
  invoked_providers: []
  not_invoked_providers:
    - yt-dlp
    - openai-whisper
  recovery: no provider output recovered in this pattern document
  boundaries:
    - media download is never a default think-tank capability
    - generated media artifacts belong in user workspace outputs, not public core
    - transcript accuracy must be labeled when generated
  verification_status: pattern_documented
```

## Expected Output Shape

```yaml
selected_intent: media_research
selected_mode: research
selected_capabilities:
  - media-processing
invoked_providers: []
not_invoked_providers:
  - yt-dlp: available_if_user_installs_provider
  - openai-whisper: available_if_user_installs_provider
boundaries:
  - Media rights and local runtime are user-owned.
verification_status: pattern_documented
```
