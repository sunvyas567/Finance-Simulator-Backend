def india_investment_fn(
    starting_corpus: float,
    scenario: dict,
    prev_year: dict,
    year: int,
    country: str,
):
    """
    India investment behaviour model

    Instruments supported:
    - SWP (growth compounding)
    - FD (interest income + compounding)
    - SCSS (income only, 5-year renewable, quarterly payout)
    - POMIS (income only, 5-year renewable, monthly payout)

    Notes:
    - SCSS & POMIS auto renew every 5 years
    - Principal reinvested automatically
    - Income never stops unless allocation changes
    """
    #print(f"India investment_fn called with starting_corpus={starting_corpus}, year={year}")
    allocations = scenario.get("allocations", {})
    rates = scenario.get("rates", {})

    result = {}

    # -------------------------------------------------
    # Allocation %
    # -------------------------------------------------
    swp_pct = allocations.get("SWP", 0) / 100
    fd_pct = allocations.get("FD", 0) / 100
    scss_pct = allocations.get("SCSS", 0) / 100
    pomis_pct = allocations.get("POMIS", 0) / 100

    # -------------------------------------------------
    # Rates
    # -------------------------------------------------
    swp_rate = rates.get("SWP", 0) / 100
    fd_rate = rates.get("FD", 0) / 100
    scss_rate = rates.get("SCSS", 0) / 100
    pomis_rate = rates.get("POMIS", 0) / 100

    # =====================================================
    # SWP (growth compounding)
    # =====================================================
    if year == 1:
        swp_balance = starting_corpus * swp_pct
    else:
        swp_balance = prev_year.get("SWPBalance", 0)

    swp_growth = swp_balance * swp_rate
    swp_balance_end = swp_balance + swp_growth

    result["SWPGrowth"] = round(swp_growth, 2)
    result["SWPIncome"] = 0.0
    result["SWPBalance"] = round(swp_balance_end, 2)

    # =====================================================
    # FD (interest income + compounding)
    # =====================================================
    if year == 1:
        fd_balance = starting_corpus * fd_pct
    else:
        fd_balance = prev_year.get("FDBalance", 0)

    fd_income = fd_balance * fd_rate
    fd_balance_end = fd_balance + fd_income

    result["FDIncome"] = round(fd_income, 2)
    result["FDBalance"] = round(fd_balance_end, 2)

    # =====================================================
    # SCSS (income only, 5-year renewable)
    # =====================================================
    if year == 1:
        scss_corpus = starting_corpus * scss_pct
    else:
        scss_corpus = prev_year.get("SCSSCorpus", 0)
    #scss_corpus = starting_corpus * scss_pct

    # Cycle tracking
    scss_cycle = ((year - 1) // 5) + 1
    scss_year_in_cycle = ((year - 1) % 5) + 1

    scss_annual_income = scss_corpus * scss_rate
    scss_quarterly_income = scss_annual_income / 4

    result["SCSSIncome"] = round(scss_annual_income, 2)
    result["SCSSQuarterlyPayout"] = round(scss_quarterly_income, 2)
    result["SCSSCorpus"] = round(scss_corpus, 2)
    result["SCSSCycle"] = scss_cycle
    result["SCSSYearInCycle"] = scss_year_in_cycle

    # Flag maturity year (informational only — auto renewed)
    if scss_year_in_cycle == 5:
        result["SCSSMaturityEvent"] = True
    else:
        result["SCSSMaturityEvent"] = False

    # =====================================================
    # POMIS (income only, 5-year renewable)
    # =====================================================

    if year == 1:
        pomis_corpus = starting_corpus * pomis_pct
    else:
        pomis_corpus = prev_year.get("POMISCorpus", 0)
    #print(f"Year {year}: POMIS corpus from previous year: {pomis_corpus}")
    #pomis_corpus = starting_corpus * pomis_pct

    pomis_cycle = ((year - 1) // 5) + 1
    pomis_year_in_cycle = ((year - 1) % 5) + 1

    pomis_annual_income = pomis_corpus * pomis_rate
    pomis_monthly_income = pomis_annual_income / 12

    result["POMISIncome"] = round(pomis_annual_income, 2)
    result["POMISMonthlyPayout"] = round(pomis_monthly_income, 2)
    result["POMISCorpus"] = round(pomis_corpus, 2)
    result["POMISCycle"] = pomis_cycle
    result["POMISYearInCycle"] = pomis_year_in_cycle

    if pomis_year_in_cycle == 5:
        result["POMISMaturityEvent"] = True
    else:
        result["POMISMaturityEvent"] = False

    # =====================================================
    # Total Investment Income (optional)
    # =====================================================
    result["TotalInvestmentIncome"] = round(
        result["FDIncome"]
        + result["SCSSIncome"]
        + result["POMISIncome"],
        2,
    )

    return result

def india_investment_fn_old(
    starting_corpus: float,
    scenario: dict,
    prev_year: dict,
    year: int,
    country: str
):
    """
    Scenario-aware India investment computation
    """

    allocations = scenario.get("allocations", {})
    rates = scenario.get("rates", {})

    result = {}

    # -------------------------------
    # Allocation percentages
    # -------------------------------
    swp_pct = allocations.get("SWP", 0) / 100
    fd_pct = allocations.get("FD", 0) / 100
    scss_pct = allocations.get("SCSS", 0) / 100
    pomis_pct = allocations.get("POMIS", 0) / 100

    # -------------------------------
    # Rates
    # -------------------------------
    swp_rate = rates.get("SWP", 0) / 100
    fd_rate = rates.get("FD", 0) / 100
    scss_rate = rates.get("SCSS", 0) / 100
    pomis_rate = rates.get("POMIS", 0) / 100

    # =====================================================
    # SWP (Growth-only, no withdrawal in v1)
    # =====================================================
    if year == 1:
        swp_balance = starting_corpus * swp_pct
    else:
        swp_balance = prev_year.get("SWPBalance", 0)

    swp_growth = swp_balance * swp_rate
    swp_balance_end = swp_balance + swp_growth

    result["SWPGrowth"] = round(swp_growth, 2)
    result["SWPIncome"] = 0.0
    result["SWPBalance"] = round(swp_balance_end, 2)

    # =====================================================
    # FD
    # =====================================================
    if year == 1:
        fd_balance = starting_corpus * fd_pct
    else:
        fd_balance = prev_year.get("FDBalance", 0)

    fd_growth = fd_balance * fd_rate
    fd_balance_end = fd_balance + fd_growth

    result["FDIncome"] = round(fd_growth, 2)
    result["FDBalance"] = round(fd_balance_end, 2)

    # =====================================================
    # SCSS (income only, corpus static)
    # =====================================================
    
    if year == 1:
        scss_corpus = starting_corpus * scss_pct
    else:
        scss_corpus = prev_year.get("SCSSCorpus", 0)
    scss_income = scss_corpus * scss_rate #if year <= 5 else 0

    result["SCSSIncome"] = round(scss_income, 2)
    result["SCSSCorpus"] = scss_corpus
    # =====================================================
    # POMIS (income only, 5 years)
    # =====================================================
    if year == 1:
        pomis_corpus = starting_corpus * pomis_pct
    else:
        pomis_corpus = prev_year.get("POMISCorpus", 0)
    #print(f"Year {year}: POMIS corpus from previous year: {pomis_corpus}")
    #pomis_corpus = starting_corpus * pomis_pct
    pomis_income = pomis_corpus * pomis_rate #if year <= 5 else 0

    result["POMISIncome"] = round(pomis_income, 2)
    result["POMISCorpus"] = pomis_corpus

    if year == 6:
        result["POMISMaturedPrincipal"] = round(pomis_corpus, 2)

    # =====================================================
    # Total Investment Income
    # =====================================================
    #result["TotalInvestmentIncome"] = round(
    #    result["FDIncome"]
    #    + result["SCSSIncome"]
    #    + result["POMISIncome"],
    #    2
    #)

    return result

