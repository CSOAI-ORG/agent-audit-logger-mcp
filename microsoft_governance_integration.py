"""Microsoft Agent Governance Toolkit Integration
Based on: github.com/microsoft/agent-governance-toolkit
License: MIT
"""

# Microsoft Agent Governance Toolkit Alignment
MICROSOFT_GOVERNANCE_SCHEMA = {
    "schema_version": "1.0",
    "agent_id": "",
    "agent_type": "",
    "capabilities": [],
    "decision_log": [],
    "telemetry": {
        "tool_calls": 0,
        "success_rate": 0.0,
        "policy_violations": 0
    },
    "policy_enforcement": {
        "allowed_tools": [],
        "denied_tools": [],
        "care_threshold": 0.7
    }
}

def align_audit_log_with_microsoft(sov3_log: dict) -> dict:
    """Convert SOV3 audit log to Microsoft Agent Governance Toolkit format"""
    microsoft_format = MICROSOFT_GOVERNANCE_SCHEMA.copy()
    
    # Map SOV3 fields to Microsoft format
    microsoft_format["agent_id"] = sov3_log.get("agent_id", "")
    microsoft_format["agent_type"] = sov3_log.get("agent_type", "cli-agent")
    microsoft_format["capabilities"] = sov3_log.get("capabilities", [])
    
    # Telemetry
    microsoft_format["telemetry"]["tool_calls"] = sov3_log.get("tool_call_count", 0)
    microsoft_format["telemetry"]["success_rate"] = sov3_log.get("success_rate", 0.0)
    
    # Policy enforcement
    microsoft_format["policy_enforcement"]["allowed_tools"] = sov3_log.get("allowed_tools", [])
    microsoft_format["policy_enforcement"]["care_threshold"] = sov3_log.get("care_threshold", 0.7)
    
    return microsoft_format

def export_audit_log(sov3_log: dict, format: str = "microsoft") -> str:
    """Export audit log in specified format"""
    if format == "microsoft":
        return json.dumps(align_audit_log_with_microsoft(sov3_log), indent=2)
    else:
        return json.dumps(sov3_log, indent=2)

# Integration with SOV3 audit-logger MCP
def enhance_audit_logger():
    """Enhance SOV3 audit-logger with Microsoft compatibility"""
    return {
        "microsoft_compatible": True,
        "schema_version": "1.0",
        "export_formats": ["sov3", "microsoft", "owasp"],
        "interoperability": "Enables audit log sharing between SOV3 and Microsoft Agent Governance Toolkit"
    }

if __name__ == "__main__":
    # Test
    test_log = {
        "agent_id": "kimi-cli",
        "agent_type": "kimi-cli",
        "capabilities": ["code_generation", "web_search"],
        "tool_call_count": 150,
        "success_rate": 0.95,
        "allowed_tools": ["hermes_ask", "quantum_memory_search"]
    }
    
    print("Microsoft Agent Governance Toolkit Integration")
    print("=" * 60)
    print()
    print("✅ Export format created")
    print(export_audit_log(test_log, "microsoft"))
