from fastapi import APIRouter
from app.api.scenario_engine import run_scenario
from app.api.projection_engine import run_projection_engine

router = APIRouter()

@router.post("/")
def run_scenarios(payload: dict):
    baseline = payload["baseline"]
    scenarios = payload["scenarios"]
    user = payload["user"]

    output = {}

    for s in scenarios:
        normalized, diff = run_scenario(
            baseline_assumptions=baseline,
            scenario_overrides=s["overrides"],
            user=user,
            country=user["country"]
        )
        df, _ = run_projection_engine(normalized)
        output[s["id"]] = {
            "projection": df,
            "diff": diff
        }

    return output
