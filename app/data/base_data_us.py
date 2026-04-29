BASE_DATA_US = [
    # ----------------------------
    # Personal
    # ----------------------------
    {"Field Name": "GLAge", "Field Description": "Current Age", "Field Default Value": 60},
    {"Field Name": "GLGender", "Field Description": "Gender", "Field Default Value": "Male"},

    # ----------------------------
    # Core Assumptions
    # ----------------------------
    {"Field Name": "GLProjectionYears", "Field Description": "Projection Years", "Field Default Value": 2,"assumption": True,"scenario": True},
    {"Field Name": "GLInflationRate", "Field Description": "Inflation Rate (%)", "Field Default Value": 3.0,"assumption": True,"scenario": True},

    # ----------------------------
    # Investment Rates
    # ----------------------------
    {"Field Name": "GL401kRate", "Field Description": "401(k) Return (%)", "Field Default Value": 7.0,"assumption": True,"scenario": True},
    {"Field Name": "GLRothIRARate", "Field Description": "Roth IRA Return (%)", "Field Default Value": 6.5,"assumption": True,"scenario": True},

    # ----------------------------
    # SWP / Withdrawal
    # ----------------------------
    {"Field Name": "GLSWPGrowthRate", "Field Description": "Portfolio Growth Rate (%)", "Field Default Value": 6.5,"assumption": True,"scenario": True},
    {"Field Name": "GLSWPMonthlyWithdrawal", "Field Description": "Monthly Withdrawal", "Field Default Value": 2000,"assumption": True,"scenario": True},

    # ----------------------------
    # Initial Corpus
    # ----------------------------
    {"Field Name": "GL401kCorpus", "Field Description": "401(k) Corpus", "Field Default Value": 250000,"assumption": True,"scenario": True},
    {"Field Name": "GLRothIRACorpus", "Field Description": "Roth IRA Corpus", "Field Default Value": 180000,"assumption": True,"scenario": True},

    # ----------------------------
    # Other Income
    # ----------------------------
    {"Field Name": "GLSocialSecurityIncome", "Field Description": "Social Security (Annual)", "Field Default Value": 18000,"assumption": True,"scenario": True},
    {"Field Name": "GLDividendIncome", "Field Description": "Dividend Income (Annual)", "Field Default Value": 12000,"assumption": True,"scenario": True},
    {"Field Name": "GLRentalIncome", "Field Description": "Rental Income (Annual)", "Field Default Value": 24000,"assumption": True,"scenario": True}
]
