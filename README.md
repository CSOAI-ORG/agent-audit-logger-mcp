# Agent Audit Logger MCP


> ## Buy Starter — £29/mo
> **Signed attestations + unlimited audits + email support.**
> 👉 **[Subscribe at meok.ai](https://buy.stripe.com/8x2eVf1BW9ACaAt1Uc8k842)** — instant HMAC signing key + Stripe-managed billing.
>
> Free tier remains MIT-licensed and zero-config. Upgrade only when you need signed compliance artefacts for audit.

[![PyPI](https://img.shields.io/pypi/v/agent-audit-logger-mcp)](https://pypi.org/project/agent-audit-logger-mcp/) [![Python](https://img.shields.io/pypi/pyversions/agent-audit-logger-mcp)](https://pypi.org/project/agent-audit-logger-mcp/)


**Hash-chained, HMAC-signed audit log for A2A agent calls.** Tamper-evident by construction. EU AI Act Art 12 / DORA Art 17 / ISO 42001 clause 9 auditor-ready.

By [MEOK AI Labs](https://meok.ai).

## Why

When agent A delegates to agent B who invokes tool C, the causal chain disappears the moment anything fails. Auditors need a record that proves:

- The event actually happened (cryptographic signature)
- The record wasn't modified after the fact (hash chain)
- The chain is continuous (no deletions)

Point every agent at this MCP's `log` tool. Each entry is HMAC-SHA256 signed and hash-chained to the previous entry.

## Tools

- `log` — append a new (from_agent, to_agent, action, outcome) entry, signed + chained
- `verify_chain` — re-verify the entire chain for a tenant; flags the first break
- `search` — query by agent, operation, outcome
- `daily_stats` — per-day log volume
- `sign_day_attestation` — Pro: signed end-of-day evidence packet with tip hash

## Install

```bash
pip install agent-audit-logger-mcp
```

## Claude Desktop

```json
{
  "mcpServers": {
    "audit": { "command": "agent-audit-logger-mcp" }
  }
}
```

## Example

```python
# In your orchestrator MCP, immediately after an A2A delegation:
log(
    tenant_id="acme-corp",
    from_agent="orchestrator",
    to_agent="compliance-scorer",
    action="score_dora_article_9",
    payload_hash=sha256(payload),
    outcome="success",
    context_csv="high-risk,financial"
)

# End of day: emit signed attestation for auditor
sign_day_attestation(
    tenant_id="acme-corp",
    date_utc="2026-04-23",
    api_key="meok_pro_..."
)
```

## Tiers

- **Free** — 1,000 log entries/day, ephemeral, chain verification
- **Pro £199/mo** — unlimited + signed end-of-day attestations + chain integrity reports — [subscribe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
- **Enterprise £1,499/mo** — multi-tenant + SIEM webhook push + retention policy — [subscribe](https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837)

## Related MEOK MCPs

- [`agent-rate-limiter-mcp`](https://pypi.org/project/agent-rate-limiter-mcp/) — fleet-wide shared rate limiter
- [`agent-policy-enforcement-mcp`](https://pypi.org/project/agent-policy-enforcement-mcp/) — per-agent-pair IAM
- [`a2a-governance-bridge-mcp`](https://pypi.org/project/a2a-governance-bridge-mcp/) — map A2A to compliance frameworks
- [`meok-attestation-verify`](https://pypi.org/project/meok-attestation-verify/) — verify signed certs anywhere

## License

MIT — MEOK AI Labs, 2026.


## Sister MCPs

Part of the MEOK **A2a** pack — designed to work together as a fleet. Install the whole pack with `npx meok-setup --pack a2a`, or pick the ones you need:

- **Prompt Injection Firewall** → `uvx agent-prompt-injection-firewall-mcp` · [PyPI](https://pypi.org/project/agent-prompt-injection-firewall-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-prompt-injection-firewall-mcp)
- **Data Residency** → `uvx agent-data-residency-mcp` · [PyPI](https://pypi.org/project/agent-data-residency-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-data-residency-mcp)
- **Certified Handoff** → `uvx agent-handoff-certified-mcp` · [PyPI](https://pypi.org/project/agent-handoff-certified-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-handoff-certified-mcp)
- **Policy Enforcement** → `uvx agent-policy-enforcement-mcp` · [PyPI](https://pypi.org/project/agent-policy-enforcement-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-policy-enforcement-mcp)
- **Rate Limiter** → `uvx agent-rate-limiter-mcp` · [PyPI](https://pypi.org/project/agent-rate-limiter-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-rate-limiter-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

<!-- mcp-name: io.github.CSOAI-ORG/agent-audit-logger-mcp -->
