# app/api/projection_engine.py

import copy
from app.api.country_resolver import resolve_country_configs
from app.api.tax.engine import calculate_tax
from app.api.life_stage_metrics import calculate_life_stage_metrics, detect_life_stage



# -------------------------------------------------
# Recurring Expenses (COUNTRY-SCOPED)
# -------------------------------------------------
def compute_yearly_recurring_expenses(user_data: dict, inflation: float, year: int):
    country = user_data.get("country")
    expenses = user_data.get("recurring_expenses", {}).get(country, {})

    must_monthly = 0.0
    optional_monthly = 0.0

    for k, v in expenses.items():
        monthly = v.get("monthly", 0)
        if k.endswith("Opt"):
            optional_monthly += monthly
        else:
            must_monthly += monthly

    factor = (1 + inflation) ** (year - 1)

    return (
        round(must_monthly * 12 * factor, 2),
        round(optional_monthly * 12 * factor, 2),
    )


# -------------------------------------------------
# One-time expenses (COUNTRY-SCOPED)
# -------------------------------------------------
def compute_grand_total_onetime(user_data: dict) -> float:
    country = user_data.get("country")
    expenses = user_data.get("onetime_expenses", {}).get(country, {})
    return round(sum(v.get("input", 0) for v in expenses.values()), 2)


# -------------------------------------------------
# SINGLE SCENARIO ENGINE (PURE)
# -------------------------------------------------
def run_projection_engine_for_scenario(
    *,
    user_data: dict,
    scenario_name: str,
):
    country = user_data.get("country", "IN")
    years = int(user_data.get("GLProjectionYears", {}).get("input", 1))

    config = resolve_country_configs(country)
    if not config:
        raise ValueError(f"Unsupported country: {country}")

    #plan = user_data.get("investment_plan", {})
    plan = user_data["investment_plan"][country]
    scenario = copy.deepcopy(plan["scenarios"][scenario_name])

    # Safety
    scenario.setdefault("allocations", {})
    scenario.setdefault("rates", {})
    scenario.setdefault("income_sources", {})
    withdrawal_cfg = scenario.setdefault("withdrawal", {})

    # Initial corpus
    #corpus = user_data.get("initial_corpus", {})
    corpus = user_data["initial_corpus"][country]
    initial_corpus_total = round(sum(corpus.values()), 2)

    inflation = user_data.get("GLInflationRate", {}).get("input", 0) / 100

    #external_income_annual = sum(
    #    v * 12 for v in scenario.get("income_sources", {}).values()
    #)
    # External income (correct frequency handling)
    external_income_annual = 0

    for key, value in scenario.get("income_sources", {}).items():
        if key in ["dividends", "other"]:
            external_income_annual += value  # yearly
        else:
            external_income_annual += value * 12  # monthly

    monthly_withdrawal = withdrawal_cfg.get(
        "monthly",
        10000 if country == "IN" else 2000 if country == "US" else 1000,
    )

    projections = []
    prev = {}

    for year in range(1, years + 1):
        starting_corpus = (
            initial_corpus_total if year == 1 else prev.get("EndingCorpus", 0)
        )

        annual_must, annual_optional = compute_yearly_recurring_expenses(
            user_data, inflation, year
        )
        annual_expense = annual_must + annual_optional
        withdrawal_yearly = monthly_withdrawal * 12

        investment_result = config["investment_fn"](
            starting_corpus=starting_corpus,
            scenario=scenario,
            prev_year=prev,
            year=year,
            country=country,
        )

        investment_income = sum(
            v for k, v in investment_result.items() if k.endswith("Income")
        )

        total_income = investment_income + external_income_annual

        taxable = {}
        for k, v in investment_result.items():
            if k.endswith("Income"):
                taxable[k] = v
        #for k, v in scenario.get("income_sources", {}).items():
        #    taxable[f"EXT_{k.upper()}"] = v * 12
        for k, v in scenario.get("income_sources", {}).items():
            if k in ["dividends", "other"]:
                taxable[f"EXT_{k.upper()}"] = v
            else:
                taxable[f"EXT_{k.upper()}"] = v * 12


        tax = round(
            calculate_tax(taxable, user_data, country).get("total_tax", 0),
            2,
        )

        net_income_after_tax = round(total_income - tax, 2)
        one_time = compute_grand_total_onetime(user_data) if year == 1 else 0

        ending_corpus = round(
            starting_corpus
            + net_income_after_tax
            - annual_expense
            - withdrawal_yearly
            - one_time,
            2,
        )

        year_data = {
            "Year": year,
            "StartingCorpus": starting_corpus,
            "AnnualMustExpenses": annual_must,
            "AnnualOptionalExpenses": annual_optional,
            "TotalExpenses": annual_expense,
            "TotalIncome": round(total_income, 2),
            "TotalTax": tax,
            "NetIncomeAfterTax": net_income_after_tax,
            "TotalWithdrawal": withdrawal_yearly,
            "EndingCorpus": ending_corpus,
        }

        year_data.update(investment_result)

        projections.append(year_data)
        prev = year_data

    return {
        "scenario": scenario_name,
        "projections": projections,
        "ending_corpus": projections[-1]["EndingCorpus"] if projections else 0,
    }


# -------------------------------------------------
# MULTI-SCENARIO WRAPPER (PUBLIC API)

def run_projection_engine(user_data: dict, user: dict):
    country = user_data.get("country", "IN")
    config = resolve_country_configs(country)

    plan = user_data.setdefault("investment_plan", {})[country] #added country scoping
    scenarios = plan.get("scenarios", {})
    active = plan.get("active_scenario", "Base")

    results_by_scenario = {}

    for name in scenarios:
        results_by_scenario[name] = run_projection_engine_for_scenario(
            user_data=user_data,
            scenario_name=name,
        )

    active_result = results_by_scenario.get(active)

    base_context = {
        "_meta": {
            "country": country,
            "country_label": config["label"],
            "currency": config["currency"],
            "scenario": active,
        },
        "initial_corpus": {
            "components": user_data.get("initial_corpus", {})[country],
            "total": sum(user_data.get("initial_corpus", {})[country].values()),
        },
        "one_time": {
            "total": compute_grand_total_onetime(user_data),
        },
    }

    life_stage = detect_life_stage(user_data)

    life_stage_metrics = calculate_life_stage_metrics(
        user_data,
        active_result["projections"]
    )

    return {
          # 🔙 BACKWARD COMPAT (DO NOT BREAK UI)
    "projections": active_result["projections"],
    
    # 🆕 NEW – scenario-aware data
    "results_by_scenario": results_by_scenario,
    "active_result": active_result,

    # 🔒 SINGLE SOURCE CONTEXT
    "base_context": {
        **base_context,
        "scenario_results": {
            name: res["projections"]
            for name, res in results_by_scenario.items()
        },
     },
    "life_stage_metrics": life_stage_metrics,   # ⭐ NEW
    "life_stage": life_stage,
    }
