# Candidate Review Report

```yaml
review_id:
reviewer_id:
project_id:
policy_id:
status: needs_revision
promoted_count: 0
rejected_count: 0
```

## Reviewed Candidates

| Agent | Decision | Checks | Notes |
|-------|----------|--------|-------|
| | promote/reject | frontmatter_complete, project_scoped, source_path_relative, boundary_declared | |

## Promoted Team Pack

```yaml
pack_id:
include_candidate_agents: []
```

## Boundaries

- Candidate review does not invoke any subagent.
- Promotion is project-scoped and does not modify the global registry.
- Rejected candidates can be reconsidered with a new selection policy or manual review.
