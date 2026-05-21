# Security Policy

## Supported Scope

Security reports are accepted for the public `think-tank` Skill core, including:

- protocol documents
- schemas
- templates
- public examples
- release checks
- provider boundary documentation
- Research OS and memory runtime contracts

This repository does not bundle provider credentials, private runtime state, user workspaces, or closed-source provider implementations.

## Reporting A Vulnerability

Please report security issues privately through GitHub Security Advisories when available. If that is not available, open a minimal issue that does not disclose exploit details and ask for a private contact path.

Do not publish:

- secrets or tokens
- private workspace contents
- account identifiers
- provider login state
- private source ledgers
- unredacted prompt injection payloads that target a live user system

## Security Boundaries

`think-tank` treats the following as high-risk operations:

- external provider invocation
- MCP or tool execution
- private knowledge-base writes
- media download or transformation
- social platform collection
- publishing, sending, deleting, or modifying remote content
- promoting private memory to public docs

High-risk operations require permission gates, privacy gates, recovery boundaries, and evidence labels.

## Disclosure Expectations

Reports should include:

- affected file or protocol area
- expected behavior
- observed risk
- minimal reproduction or scenario
- whether private data, provider state, or external systems are involved
- suggested mitigation if known

## Maintainer Response

Maintainers should:

- acknowledge the report
- assess public-core impact
- avoid requesting secrets or private data
- patch protocol, schema, examples, or checks as appropriate
- add a regression check when practical
