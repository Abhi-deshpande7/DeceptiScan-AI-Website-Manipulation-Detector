LEGAL_RULES = {
    "Roach Motel": {
        "gdpr": {
            "risk": "High",
            "rule": "Article 7(3) — withdrawal of consent must be as easy as giving it"
        },
        "dpdp": {
            "risk": "High",
            "rule": "Section 6 — consent must be freely withdrawable at any time"
        },
        "ftc": {
            "risk": "High",
            "rule": "FTC Act Section 5 — unfair or deceptive acts or practices"
        }
    },
    "Hidden costs": {
        "gdpr": {"risk": "Low",  "rule": "Not directly covered"},
        "dpdp": {"risk": "Low",  "rule": "Not directly covered"},
        "ftc":  {"risk": "High", "rule": "FTC Dot Com Disclosures — all material costs must be clear"}
    },
    "Trick questions": {
        "gdpr": {"risk": "High", "rule": "Article 7 — consent must be unambiguous and specific"},
        "dpdp": {"risk": "High", "rule": "Section 6 — consent must be free from ambiguity"},
        "ftc":  {"risk": "Medium","rule": "FTC Act Section 5 — deceptive practices"}
    },
    "Forced continuity": {
        "gdpr": {"risk": "High", "rule": "Article 7(3) — must notify before charging"},
        "dpdp": {"risk": "High", "rule": "Section 6 — consent required before recurring charge"},
        "ftc":  {"risk": "High", "rule": "Restore Online Shoppers Confidence Act (ROSCA)"}
    },
    "Privacy zuckering": {
        "gdpr": {"risk": "High", "rule": "Article 5 — data minimisation and purpose limitation"},
        "dpdp": {"risk": "High", "rule": "Section 8 — data must be used only for stated purpose"},
        "ftc":  {"risk": "Medium","rule": "FTC Privacy guidelines"}
    },
    "Fake urgency": {
        "gdpr": {"risk": "Low",  "rule": "Not directly covered"},
        "dpdp": {"risk": "Low",  "rule": "Not directly covered"},
        "ftc":  {"risk": "High", "rule": "FTC Act Section 5 — false urgency is deceptive"}
    },
    "Confirmshaming": {
        "gdpr": {"risk": "Medium","rule": "Article 7 — consent must be freely given"},
        "dpdp": {"risk": "Medium","rule": "Section 6 — consent must not be coerced"},
        "ftc":  {"risk": "Medium","rule": "FTC Act Section 5 — manipulative language"}
    },
    "Disguised ads": {
        "gdpr": {"risk": "Low",  "rule": "Not directly covered"},
        "dpdp": {"risk": "Low",  "rule": "Not directly covered"},
        "ftc":  {"risk": "High", "rule": "FTC Native Advertising Guidelines — ads must be clearly labelled"}
    }
}

def assess_legal_risk(patterns):
    results = []
    for pattern in patterns:
        name = pattern.get("pattern_name", "")
        matched_key = None
        for key in LEGAL_RULES:
            if key.lower() in name.lower() or name.lower() in key.lower():
                matched_key = key
                break

        if matched_key:
            rules = LEGAL_RULES[matched_key]
        else:
            rules = {
                "gdpr": {"risk": "Unknown", "rule": "Manual review required"},
                "dpdp": {"risk": "Unknown", "rule": "Manual review required"},
                "ftc":  {"risk": "Unknown", "rule": "Manual review required"}
            }

        results.append({
            "pattern_name": name,
            "severity": pattern.get("severity", "Low"),
            "gdpr_risk":  rules["gdpr"]["risk"],
            "gdpr_rule":  rules["gdpr"]["rule"],
            "dpdp_risk":  rules["dpdp"]["risk"],
            "dpdp_rule":  rules["dpdp"]["rule"],
            "ftc_risk":   rules["ftc"]["risk"],
            "ftc_rule":   rules["ftc"]["rule"]
        })
    return results