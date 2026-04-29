# app/api/advisor/engine.py

from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException
#from app.api.projection_engine import run_projection_engine

router = APIRouter()


@router.post("/advisor")
def advisor(payload: dict):
    return generate_advisor_recommendations(
        projections=payload.get("projections", []),
        base_context=payload.get("base_context", {}),
        scenario=payload.get("scenario", {}),
        user_data=payload.get("user_data", {}),
    )

#@router.post("/advisor")
#def advisor(payload: dict):
#    return generate_advisor_recommendations(**payload)

def generate_advisor_recommendations(
    projections: list,
    base_context: dict,
    scenario: dict,
    user_data: Optional[dict] = None,
    #projections: List[dict],
    #user_data: Dict,
    #base_context: Dict,
    #scenario: Dict,
    #user_data: dict | None = None,   # ✅ accept but optional
):
    """
    Rules-based, scenario-aware advisor engine.
    """

    if not projections:
        return _empty_advice("No projection data available.")

    year1 = projections[0]
    last_year = projections[-1]

    
    currency = base_context["_meta"].get("currency", "₹")
    country = base_context["_meta"].get("country", "IN")
    scenario_name = base_context["_meta"].get("scenario", "Base")

    advice = {
        "health_score": 100,
        "alerts": [],
        "recommendations": [],
        "positives": [],
        "scenario_insights": []
    }

    # -------------------------------------------------
    # Core Financial Signals
    # -------------------------------------------------
    starting_corpus = year1.get("StartingCorpus", 0)
    ending_corpus = last_year.get("EndingCorpus", 0)
    net_surplus_y1 = year1.get("NetSurplus", 0)
    tax_y1 = year1.get("TotalTax", 0)
    income_y1 = year1.get("TotalIncome", 0)

    mandatory = year1.get("AnnualMustExpenses", 0)
    optional = year1.get("AnnualOptionalExpenses", 0)
    
    expense_ratio = (
        mandatory / income_y1 if income_y1 > 0 else 1.0
    )

    #print("Expense ratio", expense_ratio)
    # -------------------------------------------------
    # RULE 1: Sustainability Check
    # -------------------------------------------------
    if net_surplus_y1 < 0:
        advice["alerts"].append({
            "severity": "high",
            "message": "Your expenses exceed your income in the first year."
        })
        advice["recommendations"].append(
            "Reduce discretionary expenses or rebalance investments to improve income."
        )
        advice["health_score"] -= 25
    else:
        advice["positives"].append(
            "Your income comfortably covers expenses in the first year."
        )

    # -------------------------------------------------
    # RULE 2: Corpus Depletion Risk
    # -------------------------------------------------
    if ending_corpus < starting_corpus * 0.7:
        advice["alerts"].append({
            "severity": "high",
            "message": "Your corpus depletes significantly over the projection period."
        })
        advice["recommendations"].append(
            "Consider lowering withdrawals or increasing growth-oriented allocations."
        )
        advice["health_score"] -= 30
    elif ending_corpus > starting_corpus:
        advice["positives"].append(
            "Your corpus grows over time, indicating a sustainable plan."
        )

    # -------------------------------------------------
    # RULE 3: Expense Load
    # -------------------------------------------------
    if expense_ratio > 0.7:
        advice["alerts"].append({
            "severity": "medium",
            "message": "Mandatory expenses consume a large portion of income."
        })
        advice["recommendations"].append(
            "Build a higher income buffer or reduce fixed costs."
        )
        advice["health_score"] -= 15

    # -------------------------------------------------
    # RULE 4: Tax Efficiency
    # -------------------------------------------------
    if income_y1 > 0 and tax_y1 / income_y1 > 0.25:
        advice["alerts"].append({
            "severity": "medium",
            "message": "Tax outgo is relatively high."
        })
        advice["recommendations"].append(
            "Explore more tax-efficient income sources or allocations."
        )
        advice["health_score"] -= 10
    else:
        advice["positives"].append(
            "Your tax burden appears manageable."
        )

    # -------------------------------------------------
    # RULE 5: Scenario Allocation Review
    # -------------------------------------------------
    allocations = scenario.get("allocations", {})

    equity_like = sum(
        v for k, v in allocations.items()
        if k.upper() in {"SWP", "BROKERAGE", "401K", "IRA", "ISA"}
    )

    debt_like = sum(
        v for k, v in allocations.items()
        if k.upper() in {"FD", "SCSS", "POMIS", "PENSION"}
    )

    if equity_like < 30:
        advice["scenario_insights"].append(
            "Your allocation is heavily tilted towards conservative instruments."
        )
        advice["recommendations"].append(
            "Consider increasing growth assets slightly to hedge inflation."
        )
        advice["health_score"] -= 10

    if equity_like > 70:
        advice["alerts"].append({
            "severity": "low",
            "message": "High exposure to market-linked assets."
        })
        advice["recommendations"].append(
            "Ensure sufficient stable income to manage market volatility."
        )

    # -------------------------------------------------
    # RULE 6: Longevity Buffer
    # -------------------------------------------------
    if ending_corpus <= 0:
        advice["alerts"].append({
            "severity": "critical",
            "message": "Your corpus runs out before the projection ends."
        })
        advice["recommendations"].append(
            "Immediate restructuring required: reduce withdrawals or extend working years."
        )
        advice["health_score"] = max(advice["health_score"] - 40, 10)

    # -------------------------------------------------
    # Clamp Health Score
    # -------------------------------------------------
    advice["health_score"] = max(0, min(100, advice["health_score"]))

    advice["summary"] = (
        f"Scenario '{scenario_name}' results in a "
        f"health score of {advice['health_score']}/100."
    )
    #print("Advice :", advice)
    return advice


def _empty_advice(reason: str) -> dict:
    return {
        "health_score": 0,
        "alerts": [{"severity": "info", "message": reason}],
        "recommendations": [],
        "positives": [],
        "scenario_insights": [],
        "summary": reason
    }
