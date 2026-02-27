# Tool Contract Standard (MVP)

## Purpose
A **tool contract** is the single source of truth for:
- what a tool is called (versioned name)
- what inputs it accepts
- what outputs it returns
- what errors it may emit
- what risk controls apply (read-only vs transactional, sensitivity, timeouts)

This reference implementation is **deny-by-default**:
- tools must exist in `tools/tool_registry.json`
- policy must allow the tool for the intent
- transactional tools must require an `approvalId` (HITL binding)

## Naming + Versioning
- `toolName` format: `domain.action.v<MAJOR>`
  - Examples: `claims.read.v1`, `case.create.v1`
- Backward incompatible changes → bump MAJOR (`v2`)
- Backward compatible changes → keep MAJOR, add optional fields only

## Required Tool Metadata
Each tool entry in `tools/tool_registry.json` MUST include:
- `name` (string)
- `type` (enum: `READ_ONLY` | `TRANSACTIONAL`)
- `dataSensitivity` (enum: `NONE` | `PII` | `PHI`)
- `riskTier` (enum: `LOW` | `MEDIUM` | `HIGH`)
- `idempotent` (boolean)
- `timeoutMs` (int >= 1000)
- `rateLimitPerMin` (int >= 1)
- `schema.input` (object with at least one key)
- `schema.output` (object with at least one key)
- `errors` (array of strings)

### Transactional Tool Rule
If `type = TRANSACTIONAL`, then:
- `requiresApprovalId = true`
- `schema.input` MUST contain `approvalId`
- `schema.input` SHOULD contain `idempotencyKey` for retry-safe writes.

For demo implementations, idempotency can be stubbed at the tool boundary (for example, in-memory key cache).  
Production implementations should enforce idempotency keys with durable storage and replay-window checks.

## Allowed Error Codes (recommended baseline)
- `VALIDATION_ERROR`
- `AUTHZ_DENIED`
- `NOT_FOUND`
- `CONFLICT`
- `RATE_LIMITED`
- `TIMEOUT`
- `DEPENDENCY_FAILURE`
- `UNKNOWN`

## Validation
- `scripts/validate_tools.py` validates `tools/tool_registry.json` against
  `standards/schemas/tool-contract.schema.json`
- CI should run this validation (post-MVP)

## Example (good)
`claims.read.v1` with input `claimId`, output `status`, `lastUpdated`

## Example (bad)
- tool referenced in allowlist but missing in tool registry
- transactional tool without `approvalId` requirements
