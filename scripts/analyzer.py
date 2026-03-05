import json
import re


def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = text.split("--- CHUNK")
    return chunks


def analyze_chunks(chunks):

    memo = {
        "account_id": "account_001",
        "company_name": "",
        "business_hours": "",
        "office_address": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": "",
        "non_emergency_routing_rules": "",
        "call_transfer_rules": "",
        "integration_constraints": [],
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": []
    }

    service_keywords = [
        "pressure washing",
        "sprinkler",
        "fire alarm",
        "electrical",
        "inspection",
        "maintenance",
        "repair"
    ]

    emergency_keywords = [
        "emergency",
        "urgent",
        "sprinkler leak",
        "alarm going off"
    ]

    for chunk in chunks:

        text = chunk.lower()

        # detect services
        for service in service_keywords:
            if service in text and service not in memo["services_supported"]:
                memo["services_supported"].append(service)

        # detect emergencies
        for emergency in emergency_keywords:
            if emergency in text and emergency not in memo["emergency_definition"]:
                memo["emergency_definition"].append(emergency)

        # detect routing rules
        if "after hours" in text:
            memo["after_hours_flow_summary"] = chunk

        if "transfer" in text or "dispatch" in text:
            memo["call_transfer_rules"] = chunk

        # detect phone numbers
        phones = re.findall(r"\+?\d[\d\s\-]{8,}\d", chunk)
        if phones:
            memo["notes"].append(f"phone detected: {phones}")

        # detect emails
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", chunk)
        if emails:
            memo["notes"].append(f"email detected: {emails}")

    return memo


def save_memo(memo):
    with open("account_memo_v1.json", "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=4)


def main():

    chunks = load_chunks("chunks.txt")

    memo = analyze_chunks(chunks)

    save_memo(memo)

    print("Account Memo Generated")


if __name__ == "__main__":
    main()
