import json


def generate_agent_spec(memo_file):

    with open(memo_file, "r") as f:
        memo = json.load(f)

    agent = {
        "agent_name": f"{memo.get('company_name','Company')} Receptionist",
        "voice_style": "professional",

        "key_variables": {
            "business_hours": memo.get("business_hours", ""),
            "address": memo.get("office_address", ""),
            "services": memo.get("services_supported", []),
            "emergency_definition": memo.get("emergency_definition", [])
        },

        "system_prompt": f"""
You are the receptionist for {memo.get('company_name','the company')}.

BUSINESS HOURS FLOW
- greet caller
- ask purpose
- collect name and phone
- route call appropriately
- confirm next steps
- ask if anything else is needed
- close politely

AFTER HOURS FLOW
- greet caller
- ask purpose
- determine if emergency
- if emergency collect name, number and address immediately
- attempt transfer
- if transfer fails reassure caller someone will follow up
""",

        "call_transfer_protocol": memo.get("call_transfer_rules", ""),

        "fallback_protocol": "If transfer fails apologize and promise callback.",

        "version": "v1"
    }

    with open("agent_spec_v1.json", "w") as f:
        json.dump(agent, f, indent=4)

    print("Agent Spec v1 Generated")


generate_agent_spec("account_memo_v1.json")
