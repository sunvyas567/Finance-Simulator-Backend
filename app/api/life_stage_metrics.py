
def detect_life_stage(user_data: dict) -> str:
    age = user_data.get("GLAge", {}).get("input")
    #print(f"Detecting life stage for age: {age}")
    #print(f"User data for life stage detection: {user_data}")
    if age < 35:
        return "EARLY_ACCUMULATION"   # FIRE oriented
    elif age < 50:
        return "WEALTH_BUILDING"
    elif age < 60:
        return "PRE_RETIREMENT"
    else:
        return "RETIREMENT"

def calculate_fire_metrics(user_data: dict, projections: list):
    """
    FIRE readiness metrics
    """

    if not projections:
        return {}

    age = user_data.get("age", 30)

    # annual expenses year 1
    y1 = projections[0]
    annual_expense = y1["TotalExpenses"]

    # FIRE number (25x rule)
    fire_number = annual_expense * 25

    current_corpus = user_data.get("initial_corpus", {})
    current_total = sum(current_corpus.values())

    fire_progress = (current_total / fire_number) * 100 if fire_number else 0

    # years to FIRE from projection
    years_to_fire = None
    for row in projections:
        if row["EndingCorpus"] >= fire_number:
            years_to_fire = row["Year"]
            break

    return {
        "life_stage": "FIRE_TRACK",
        "fire_number": round(fire_number, 2),
        "current_progress_pct": round(fire_progress, 1),
        "years_to_fire": years_to_fire,
    }

def calculate_wealth_builder_metrics(user_data: dict, projections: list):

    if not projections:
        return {}

    y1 = projections[0]

    savings_rate = (
        y1["NetIncomeAfterTax"] - y1["TotalExpenses"]
    ) / max(y1["NetIncomeAfterTax"], 1)

    corpus_growth = (
        projections[-1]["EndingCorpus"] - projections[0]["StartingCorpus"]
    ) / max(projections[0]["StartingCorpus"], 1)

    return {
        "life_stage": "WEALTH_BUILDING",
        "savings_rate_pct": round(savings_rate * 100, 1),
        "projected_corpus_growth_pct": round(corpus_growth * 100, 1),
    }

def calculate_pre_retirement_metrics(user_data: dict, projections: list):

    if not projections:
        return {}

    retirement_year = len(projections)
    final_corpus = projections[-1]["EndingCorpus"]

    y1 = projections[0]
    required_corpus = y1["TotalExpenses"] * 25

    readiness = (final_corpus / required_corpus) * 100 if required_corpus else 0

    return {
        "life_stage": "PRE_RETIREMENT",
        "required_corpus": round(required_corpus, 2),
        "projected_corpus": round(final_corpus, 2),
        "readiness_pct": round(readiness, 1),
    }

def calculate_retirement_metrics(user_data: dict, projections: list):

    if not projections:
        return {}

    corpus_depletion_year = None

    for row in projections:
        if row["EndingCorpus"] <= 0:
            corpus_depletion_year = row["Year"]
            break

    sustainable = corpus_depletion_year is None

    return {
        "life_stage": "RETIRED",
        "corpus_lasts_full_projection": sustainable,
        "depletion_year": corpus_depletion_year,
    }

def calculate_life_stage_metrics(user_data: dict, projections: list):

    stage = detect_life_stage(user_data)

    if stage == "EARLY_ACCUMULATION":
        return calculate_fire_metrics(user_data, projections)

    if stage == "WEALTH_BUILDING":
        return calculate_wealth_builder_metrics(user_data, projections)

    if stage == "PRE_RETIREMENT":
        return calculate_pre_retirement_metrics(user_data, projections)

    return calculate_retirement_metrics(user_data, projections)
