# Troubleshooting

## Release checks fail

Run the failing check directly:

```bash
python3 checks/open_source_release_suite.py
python3 checks/stable_release_check.py
```

Then run the specific check named in the error output.

## Image links fail

Run:

```bash
python3 checks/markdown_image_links_check.py
python3 checks/visual_assets_check.py
```

Common causes:

- README points to a missing PNG.
- A new visual lacks a prompt record.
- An SVG was reintroduced as a primary README visual.

## Provider claims look too strong

Use the provider boundary vocabulary:

```text
pattern_documented
available_if_user_installs_provider
requires_user_environment
not_bundled
selected
preflight_checked
invoked
recovered
verified_partial
verified
blocked
```

If a provider was not called, list it under `not_invoked_providers`.

## Research OS data should not be public

Only templates and contracts belong in this repository. Real workspace data belongs in a user-local project workspace.

## Memory promotion is unclear

Start local. Promote only when the candidate is public-safe, platform-neutral, evidence-backed, and has a staleness rule.
