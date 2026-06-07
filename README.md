[![MCP Scorecard: 78/100](https://img.shields.io/badge/proofof.ai-78%2F100-5b21b6)](https://proofof.ai/scorecard/agent-audit-logger-mcp.html)

# Agent Audit Logger MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-22c55e)](https://councilof.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/agent_audit_logger_mcp/)

> Hash-chained HMAC-signed audit log MCP for A2A (agent-to-agent) calls

Hash-chained HMAC-signed audit log MCP for A2A (agent-to-agent) calls. Every tool-call, agent-handoff, decision gets a tamper-evident signed record. EU AI Act Art 12 automatic logs, DORA Art 17 ICT incident logs, ISO 42001 clause 9 monitoring — auditor-ready end-of-day attestations. By MEOK AI Labs.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install agent_audit_logger_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install agent-audit-logger-mcp --client claude
```

## ✨ Features

- HMAC-signed audit logs
- Hash-chained integrity
- A2A agent tracking
- Compliance reporting
- Tamper-proof records

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/agent-audit-logger-mcp)
- [API Reference](https://meok-attestation-api.vercel.app)
- [EU AI Act Compliance Guide](https://councilof.ai)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)
- **Free** — 1,000 log entries/day, ephemeral, chain verification
- **Pro £199/mo** — unlimited + signed end-of-day attestations + chain integrity reports — [subscribe](https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j)
- **Enterprise £1,499/mo** — multi-tenant + SIEM webhook push + retention policy — [subscribe](https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j)

Need help getting compliant? **[Book a free 15-min diagnostic →](mailto:nicholas@meok.ai?subject=Compliance%20diagnostic)**

## 🏢 Enterprise

Need custom development, SLA guarantees, or white-label deployment?

- **Pro:** £79/mo — Full MCP suite + EU AI Act tracking
- **Enterprise:** £499/mo — Custom dev + SLA + Dedicated support

[View Pricing →](https://councilof.ai/payg) | [Contact Sales →](mailto:sales@meok.ai)

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 26 PyPI packages · ~16,300 monthly installs.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
- **Prompt Injection Firewall** → `uvx agent-prompt-injection-firewall-mcp` · [PyPI](https://pypi.org/project/agent-prompt-injection-firewall-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-prompt-injection-firewall-mcp)
- **Data Residency** → `uvx agent-data-residency-mcp` · [PyPI](https://pypi.org/project/agent-data-residency-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-data-residency-mcp)
- **Certified Handoff** → `uvx agent-handoff-certified-mcp` · [PyPI](https://pypi.org/project/agent-handoff-certified-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-handoff-certified-mcp)
- **Policy Enforcement** → `uvx agent-policy-enforcement-mcp` · [PyPI](https://pypi.org/project/agent-policy-enforcement-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-policy-enforcement-mcp)
- **Rate Limiter** → `uvx agent-rate-limiter-mcp` · [PyPI](https://pypi.org/project/agent-rate-limiter-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-rate-limiter-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)


## Protocol coverage + Universal PAYG

This MCP is part of MEOK's 47-MCP fleet that bridges every active agent-interop protocol
and 30+ regulatory frameworks. See the full coverage matrix at [meok.ai/protocols](https://meok.ai/protocols).

**Agent interop protocols supported (8 live):**

- ✅ **MCP** (Anthropic) — native
- ✅ **A2A** (Google + Linux Foundation, absorbed IBM ACP Sept 2025)
- ✅ **IBM ACP** — covered via A2A merge
- ◐ **Stripe ACP** (Agentic Commerce Protocol) — Q3 bridge via [agent-commerce-protocol-mcp](https://github.com/CSOAI-ORG/agent-commerce-protocol-mcp)
- ◐ **AP2** (Google Agent Payments) — partial via [agent-commerce-payments-mcp](https://github.com/CSOAI-ORG/agent-commerce-payments-mcp)
- ◐ **x402** (Coinbase HTTP 402) — partial via api.meok.ai gateway
- → **OASF / AGNTCY** (Cisco Outshift + Linux Foundation) — Q3 bridge
- 👁 **ANP** (Cisco Agent Network) — watch-list

**Pricing options:**

| Option | Price | Best for |
|---|---|---|
| Self-host (this MCP) | £0 — MIT | Devs |
| This MCP Starter | £29/mo | One-MCP teams |
| This MCP Pro | £79/mo | Production + 24h SLA |
| [Universal PAYG](https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j) | £29/mo + £0.0002/call | Spiky usage across many MCPs |
| Substrate bundle (this category) | £99-£499/mo | A whole pack |
| [MEOK Universe](https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j) | £1,499/mo | All 47 MCPs, 500K calls |

Each tier above the free self-host adds HMAC-signed attestations verifiable at
`verify.meok.ai`. Linux Foundation governance on the A2A spine means EU regulated
buyers can deploy without vendor-lock-in objections.

<!-- mcp-name: io.github.CSOAI-ORG/agent-audit-logger-mcp -->

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->

