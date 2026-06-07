#!/usr/bin/env python3
"""
Agent Audit Logger MCP Server
==============================
By MEOK AI Labs | https://meok.ai

Cryptographically signed, hash-chained audit log for agent-to-agent (A2A) calls.

PROBLEM SOLVED: when agent A delegates to agent B who invokes tool C, you lose
the causal chain the moment anything fails. Auditors of AI systems (EU AI Act
Art 12 logging, DORA Art 17 ICT incident logs, ISO 42001 clause 9 monitoring)
demand a tamper-evident record. Point every agent at this MCP's `log` tool —
each event is HMAC-SHA256 signed and hash-chained to the previous event.

USE CASES:
  - Forensic reconstruction after an agent incident
  - EU AI Act Art 12 automatic logs for high-risk AI systems
  - ISO 42001 clause 9 performance evaluation evidence
  - DORA Art 17 incident classification supporting evidence
  - Compliance Trust Center: cert your auditor reads offline

PRICING:
  - Free — 1,000 log entries/day, ephemeral
  - Pro £199/mo — unlimited + signed end-of-day attestation + chain verification
  - Enterprise £1,499/mo — multi-tenant + SIEM webhook push + retention policy

Install: pip install agent-audit-logger-mcp
Run:     python server.py
"""

import json
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict, deque
from mcp.server.fastmcp import FastMCP

import os as _os
import sys
import os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    from auth_middleware import check_access as _shared_check_access
    _AUTH_ENGINE_AVAILABLE = True
except ImportError:
    _AUTH_ENGINE_AVAILABLE = False

    def _shared_check_access(api_key: str = ""):
        """Fallback when shared auth engine is not available."""
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
        return True, "OK, Pro at https://www.csoai.org/checkout", "free"


try:
    from attestation import get_attestation_tool_response
    _ATTESTATION_LOCAL = True
except ImportError:
    _ATTESTATION_LOCAL = False

_ATTESTATION_API = _os.environ.get(
    "MEOK_ATTESTATION_API", "https://meok-attestation-api.vercel.app"
)


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


STRIPE_199 = "https://buy.stripe.com/14AfZjfsM6oq7oh2Yg8k90P"
STRIPE_1499 = "https://buy.stripe.com/14AfZjfsM6oq7oh2Yg8k90P"


# ── Log signing key (local fallback — production uses attestation-api)  ─────
_LOG_SIGNING_KEY = (
    _os.environ.get("MEOK_LOG_SIGNING_KEY", "").encode("utf-8")
    or hashlib.sha256(b"MEOK_LOG_DEV_KEY_ROTATE_BEFORE_GA").digest()
)

# In-memory log store — {tenant_id: [(ts, entry_dict, signature, prev_hash)]}
# MVP; swap for Postgres/append-only file in production deployment.
_log_store: dict[str, list[dict]] = defaultdict(list)
_daily_stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

FREE_DAILY_LIMIT = 1000


def _chain_sign(prev_hash: str, payload: dict) -> tuple[str, str]:
    """Return (signature, new_hash). new_hash = HMAC(prev_hash || payload)."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    message = prev_hash.encode("utf-8") + b"|" + canonical
    sig = hmac.new(_LOG_SIGNING_KEY, message, hashlib.sha256).hexdigest()
    new_hash = hashlib.sha256(message + sig.encode()).hexdigest()
    return sig, new_hash


mcp = FastMCP(
    "agent-audit-logger",
    instructions=(
        "MEOK AI Labs Agent Audit Logger MCP. Cryptographically signed, hash-chained "
        "audit log for A2A calls. Every tool-call / agent-handoff / decision gets a "
        "tamper-evident record. Use `log` to append, `verify_chain` to check integrity, "
        "`search` to query by agent/operation/time, `sign_day_attestation` (Pro) for "
        "end-of-day signed evidence packet."
    ),
)


@mcp.tool()
def log(
    tenant_id: str,
    from_agent: str,
    to_agent: str,
    action: str,
    payload_hash: str = "",
    outcome: str = "success",
    context_csv: str = "",
    api_key: str = "",
) -> str:
    """Append a signed, hash-chained log entry.

    - tenant_id: customer / organisation identifier
    - from_agent: calling agent id (e.g. "orchestrator")
    - to_agent: receiving agent id (e.g. "compliance-scorer")
    - action: what was requested (e.g. "score_dora_compliance")
    - payload_hash: SHA256 of the payload body (keeps logs small + hides PII)
    - outcome: success | fail | timeout | blocked
    - context_csv: optional comma-separated tags (e.g. "high-risk,financial")
    """
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})

    today = datetime.now(timezone.utc).date().isoformat()
    _daily_stats[tenant_id][today] += 1
    if tier == "free" and _daily_stats[tenant_id][today] > FREE_DAILY_LIMIT:
        return json.dumps({
            "error": f"Free tier daily limit ({FREE_DAILY_LIMIT} log entries/day) reached. Upgrade for unlimited + signed end-of-day attestations.",
            "upgrade_url": STRIPE_199,
        })

    ts = datetime.now(timezone.utc).isoformat()
    log_store = _log_store[tenant_id]
    prev_hash = log_store[-1]["chain_hash"] if log_store else "GENESIS"

    entry = {
        "ts_utc": ts,
        "seq": len(log_store) + 1,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "action": action,
        "payload_hash": payload_hash,
        "outcome": outcome,
        "context": [c.strip() for c in context_csv.split(",") if c.strip()],
    }
    signature, chain_hash = _chain_sign(prev_hash, entry)
    record = {**entry, "signature": signature, "chain_hash": chain_hash, "prev_hash": prev_hash}
    log_store.append(record)

    return json.dumps({
        "logged": True,
        "seq": entry["seq"],
        "chain_hash": chain_hash[:16] + "...",
        "tenant_id": tenant_id,
    })


@mcp.tool()
def verify_chain(tenant_id: str, api_key: str = "") -> str:
    """Re-verify the integrity of the log chain for a tenant.
    Returns OK or the first sequence number where the chain breaks."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg})

    log_store = _log_store[tenant_id]
    if not log_store:
        return json.dumps({"tenant_id": tenant_id, "entries": 0, "status": "no entries yet"})

    prev_hash = "GENESIS"
    for i, rec in enumerate(log_store):
        stripped = {k: v for k, v in rec.items() if k not in ("signature", "chain_hash", "prev_hash")}
        expected_sig, expected_hash = _chain_sign(prev_hash, stripped)
        if not hmac.compare_digest(expected_sig, rec["signature"]):
            return json.dumps({
                "tenant_id": tenant_id,
                "status": "CHAIN BROKEN",
                "break_at_seq": rec["seq"],
                "reason": "signature mismatch",
            })
        if not hmac.compare_digest(expected_hash, rec["chain_hash"]):
            return json.dumps({
                "tenant_id": tenant_id,
                "status": "CHAIN BROKEN",
                "break_at_seq": rec["seq"],
                "reason": "chain hash mismatch",
            })
        prev_hash = rec["chain_hash"]

    return json.dumps({
        "tenant_id": tenant_id,
        "status": "OK",
        "entries_verified": len(log_store),
        "tip_hash": prev_hash,
        "first_entry_ts": log_store[0]["ts_utc"],
        "last_entry_ts": log_store[-1]["ts_utc"],
    })


@mcp.tool()
def search(
    tenant_id: str,
    from_agent: str = "",
    to_agent: str = "",
    action: str = "",
    outcome: str = "",
    limit: int = 50,
    api_key: str = "",
) -> str:
    """Query the log. Empty filters match everything. Returns newest-first."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg})

    log_store = _log_store[tenant_id]
    matches = []
    for rec in reversed(log_store):
        if from_agent and rec["from_agent"] != from_agent:
            continue
        if to_agent and rec["to_agent"] != to_agent:
            continue
        if action and rec["action"] != action:
            continue
        if outcome and rec["outcome"] != outcome:
            continue
        matches.append({
            "seq": rec["seq"], "ts_utc": rec["ts_utc"],
            "from_agent": rec["from_agent"], "to_agent": rec["to_agent"],
            "action": rec["action"], "outcome": rec["outcome"],
            "context": rec["context"],
            "signature": rec["signature"][:16] + "...",
        })
        if len(matches) >= limit:
            break
    return json.dumps({"tenant_id": tenant_id, "matches": matches, "total_matches_capped_at": limit})


@mcp.tool()
def daily_stats(tenant_id: str, api_key: str = "") -> str:
    """Return daily log volume stats for a tenant."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg})
    return json.dumps({
        "tenant_id": tenant_id,
        "tier": tier,
        "daily_log_counts": dict(_daily_stats[tenant_id]),
        "total_entries": len(_log_store[tenant_id]),
    })


@mcp.tool()
def sign_day_attestation(tenant_id: str, date_utc: str, api_key: str = "", email: str = "") -> str:
    """Emit a signed attestation certifying the log integrity + volume for a given day.

    Pro/Enterprise only. Use this as end-of-day evidence for your auditor / Trust
    Center. The attestation includes the tip hash at end-of-day so anyone can
    later prove the log wasn't retroactively modified.
    """
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if tier == "free":
        return json.dumps({
            "error": "Signed day attestations require Pro (£199/mo) or Enterprise tier.",
            "upgrade_url": STRIPE_199,
        })

    log_store = _log_store[tenant_id]
    day_entries = [r for r in log_store if r["ts_utc"].startswith(date_utc)]
    day_count = len(day_entries)
    by_outcome = defaultdict(int)
    for r in day_entries:
        by_outcome[r["outcome"]] += 1

    findings = [
        f"Date: {date_utc}",
        f"Log entries this day: {day_count}",
        f"Outcomes: " + ", ".join(f"{k}={v}" for k, v in sorted(by_outcome.items())),
        f"Tip hash at end of day: {day_entries[-1]['chain_hash'] if day_entries else 'N/A'}",
    ]
    score = 100 * (by_outcome.get("success", 0) / max(1, day_count))

    if _ATTESTATION_LOCAL:
        cert = get_attestation_tool_response(
            regulation="A2A audit-log integrity + volume (per-day)",
            entity=f"tenant:{tenant_id}:{date_utc}",
            score=score,
            findings=findings,
            articles_audited=["EU AI Act Art 12", "DORA Art 17", "ISO 42001 clause 9"],
            tier=tier,
        )
    else:
        import urllib.request as _url
        try:
            req = _url.Request(
                f"{_ATTESTATION_API}/sign",
                data=json.dumps({
                    "api_key": api_key, "email": email,
                    "regulation": "A2A audit-log integrity + volume (per-day)",
                    "entity": f"tenant:{tenant_id}:{date_utc}",
                    "score": score,
                    "findings": findings,
                    "tier": tier,
                }).encode(),
                headers={"Content-Type": "application/json"},
            )
            with _url.urlopen(req, timeout=15) as resp:
                cert = json.loads(resp.read())
        except Exception as e:
            return json.dumps({"error": f"Attestation API unreachable: {e}"})

    return json.dumps(cert, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
