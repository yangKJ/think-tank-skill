# Minimal Conclusion

```yaml
minimal_conclusion:
  request: "{the concrete question this run answered}"
  route:
    selected_intent: "{intent}"
    selected_mode: "{research|council|review|strategy}"
    selected_recipe: "{recipe}"
    trigger_status: "{explicit|inferred|fallback}"
  conclusion: "{specific conclusion}"
  decision: "{what should be done next or accepted now}"
  evidence:
    summary: "{what evidence types or sources support this}"
    evidence_state: "{selected|invoked|recovered|verified_partial|verified|blocked|failed|tracking}"
    confidence: "{low|medium|high}"
  risks:
    - "{residual risk}"
  next_step: "{single best next action}"
  boundaries:
    - "{what this conclusion does not cover}"
```

## Quality Check

```yaml
minimal_conclusion_quality_check:
  request_explicit: true
  route_explicit: true
  conclusion_specific: true
  decision_actionable: true
  evidence_state_labeled: true
  confidence_labeled: true
  next_step_present: true
  boundaries_present: true
```
