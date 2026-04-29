from copy import deepcopy
from app.api.assumption_normalizer import normalize_assumptions
from app.api.assumption_diff import diff_assumptions


def run_scenario(
    *,
    baseline_assumptions: dict,
    scenario_overrides: dict,
    user: dict,
    country: str,
    total_monthly_expenses: float | None = None
):
    """
    Runs a scenario branch from baseline assumptions.
    """

    # 1. Merge baseline + overrides
    merged = deepcopy(baseline_assumptions)

    for key, val in scenario_overrides.items():
        merged[key] = {
            "input": val["input"],
            "source": "scenario",
            "locked": True
        }

    # 2. Normalize assumptions
    normalized = normalize_assumptions(
        merged,
        user=user,
        country=country,
        total_monthly_expenses=total_monthly_expenses
    )

    # 3. Diff vs baseline
    assumption_diff = diff_assumptions(
        baseline=baseline_assumptions,
        current=normalized
    )

    return normalized, assumption_diff
