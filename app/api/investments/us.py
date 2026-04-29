def us_investment_fn(
    starting_corpus: float,
    scenario: dict,
    prev_year: dict,
    year: int,
    country: str
):
    """
    Scenario-aware US investment computation
    """

    allocations = scenario.get("allocations", {})
    rates = scenario.get("rates", {})
    income_sources = scenario.get("income_sources", {})

    result = {}

    # -------------------------------
    # Allocation percentages
    # -------------------------------
    k401_pct = allocations.get("401K", 0) / 100
    ira_pct = allocations.get("IRA", 0) / 100
    brokerage_pct = allocations.get("BROKERAGE", 0) / 100

    # -------------------------------
    # Rates
    # -------------------------------
    k401_rate = rates.get("401K", 0) / 100
    ira_rate = rates.get("IRA", 0) / 100
    brokerage_rate = rates.get("BROKERAGE", 0) / 100

    # =====================================================
    # 401(k) – corpus only
    # =====================================================
    if year == 1:
        k401_balance = starting_corpus * k401_pct
    else:
        k401_balance = prev_year.get("US401KBalance", 0)

    k401_growth = k401_balance * k401_rate
    result["US401KBalance"] = round(k401_balance + k401_growth, 2)

    # =====================================================
    # IRA – corpus only
    # =====================================================
    if year == 1:
        ira_balance = starting_corpus * ira_pct
    else:
        ira_balance = prev_year.get("USIRABalance", 0)

    ira_growth = ira_balance * ira_rate
    result["USIRABalance"] = round(ira_balance + ira_growth, 2)

    # =====================================================
    # Brokerage – corpus only
    # =====================================================
    if year == 1:
        brokerage_balance = starting_corpus * brokerage_pct
    else:
        brokerage_balance = prev_year.get("USBrokerageBalance", 0)

    brokerage_growth = brokerage_balance * brokerage_rate
    result["USBrokerageBalance"] = round(
        brokerage_balance + brokerage_growth, 2
    )

    # =====================================================
    # Income Sources (cash)
    # =====================================================
    ss_income = income_sources.get("social_security", 0) * 12
    dividend_income = income_sources.get("dividends", 0)

    result["USSocialSecurityIncome"] = round(ss_income, 2)
    result["DividendIncome"] = round(dividend_income, 2)

    # =====================================================
    # Total Investment Income (cash only)
    # =====================================================
    #result["TotalInvestmentIncome"] = round(
    #    ss_income + dividend_income,
    #    2
    #)

    return result
