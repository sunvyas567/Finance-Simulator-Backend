def uk_investment_fn(
    starting_corpus: float,
    scenario: dict,
    prev_year: dict,
    year: int,
    country: str
):
    """
    Scenario-aware UK investment computation
    """

    allocations = scenario.get("allocations", {})
    rates = scenario.get("rates", {})
    income_sources = scenario.get("income_sources", {})

    result = {}

    # -------------------------------
    # Allocation percentages
    # -------------------------------
    pension_pct = allocations.get("PENSION", 0) / 100
    isa_pct = allocations.get("ISA", 0) / 100

    # -------------------------------
    # Rates
    # -------------------------------
    pension_rate = rates.get("PENSION", 0) / 100
    isa_rate = rates.get("ISA", 0) / 100

    # =====================================================
    # Pension pot (corpus only)
    # =====================================================
    if year == 1:
        pension_balance = starting_corpus * pension_pct
    else:
        pension_balance = prev_year.get("UKPensionBalance", 0)

    pension_growth = pension_balance * pension_rate
    result["UKPensionBalance"] = round(pension_balance + pension_growth, 2)

    # =====================================================
    # ISA (corpus only)
    # =====================================================
    if year == 1:
        isa_balance = starting_corpus * isa_pct
    else:
        isa_balance = prev_year.get("UKISABalance", 0)

    isa_growth = isa_balance * isa_rate
    result["UKISABalance"] = round(isa_balance + isa_growth, 2)

    # =====================================================
    # Income Sources (cash)
    # =====================================================
    state_pension = income_sources.get("state_pension", 0) * 12
    annuity_income = income_sources.get("annuity", 0) * 12
    dividend_income = income_sources.get("dividends", 0)

    result["UKStatePensionIncome"] = round(state_pension, 2)
    result["UKAnnuityIncome"] = round(annuity_income, 2)
    result["DividendIncome"] = round(dividend_income, 2)

    # =====================================================
    # Total Investment Income (cash only)
    # =====================================================
    #result["TotalInvestmentIncome"] = round(
    #    state_pension + annuity_income + dividend_income,
     #   2
    #)

    return result
