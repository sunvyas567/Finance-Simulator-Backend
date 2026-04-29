from typing import Dict, Any


# Fields that should NEVER be diffed (derived / outputs)
EXCLUDED_FIELDS = {
    "GLTotalYearlyExpensesMust",
    "GLTotalYearlyExpensesOptional",
    "GrandTotalOneTime",
    "GLTotalIncomeOverallFDs"
}


def diff_assumptions(
    baseline: Dict[str, Dict[str, Any]],
    current: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Returns a structured diff between baseline and current assumptions.
    """

    diffs = {}

    for key, base_val in baseline.items():
        if key in EXCLUDED_FIELDS:
            continue

        if key not in current:
            continue

        base_input = base_val.get("input")
        curr_input = current[key].get("input")

        if base_input == curr_input:
            continue

        diff_entry = {
            "from": base_input,
            "to": curr_input,
            "source": current[key].get("source", "unknown"),
            "impact_type": classify_impact(key)
        }

        # Numeric delta
        if _is_number(base_input) and _is_number(curr_input):
            diff_entry["delta"] = round(curr_input - base_input, 2)

            # Monthly / yearly hint
            if key.startswith("Local") and "Monthly" not in key:
                diff_entry["delta_monthly"] = diff_entry["delta"]
                diff_entry["delta_yearly"] = round(diff_entry["delta"] * 12, 2)

        diffs[key] = diff_entry

    return diffs


# -----------------------------
# Helpers
# -----------------------------

def _is_number(val):
    return isinstance(val, (int, float))


def classify_impact(field_name: str) -> str:
    """
    Tags the assumption for explanation & UI grouping.
    """
    if field_name.startswith("Local"):
        return "expense_or_income"

    if "Rate" in field_name or "Growth" in field_name:
        return "market_return"

    if "Years" in field_name or "Age" in field_name:
        return "horizon"

    return "other"
