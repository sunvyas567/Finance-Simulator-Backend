BASE_DATA_UK = [
    # ----------------------------
    # Personal
    # ----------------------------
    {"Field Name": "GLAge", "Field Description": "Current Age", "Field Default Value": 60},
    {"Field Name": "GLGender", "Field Description": "Gender", "Field Default Value": "Male"},

    # ----------------------------
    # Core Assumptions
    # ----------------------------
    {"Field Name": "GLProjectionYears", "Field Description": "Projection Years", "Field Default Value": 2,"assumption": True,"scenario": True},
    {"Field Name": "GLInflationRate", "Field Description": "Inflation Rate (%)", "Field Default Value": 2.8,"assumption": True,"scenario": True},

    # ----------------------------
    # Investment Rates
    # ----------------------------
    {"Field Name": "GLISARate", "Field Description": "ISA Return (%)", "Field Default Value": 6.0,"assumption": True,"scenario": True},

    # ----------------------------
    # SWP
    # ----------------------------
    {"Field Name": "GLSWPGrowthRate", "Field Description": "Portfolio Growth Rate (%)", "Field Default Value": 6.0,"assumption": True,"scenario": True},
    {"Field Name": "GLSWPMonthlyWithdrawal", "Field Description": "Monthly Withdrawal", "Field Default Value": 1800,"assumption": True,"scenario": True},

    # ----------------------------
    # Retirement Corpus
    # ----------------------------
    {"Field Name": "GLISACorpus", "Field Description": "ISA Corpus", "Field Default Value": 180000,"assumption": True,"scenario": True},
    {"Field Name": "GLPrivatePensionCorpus", "Field Description": "Private Pension Corpus", "Field Default Value": 220000,"assumption": True,"scenario": True},

    # ----------------------------
    # Other Income
    # ----------------------------
    {"Field Name": "GLStatePension", "Field Description": "State Pension (Annual)", "Field Default Value": 10500,"assumption": True,"scenario": True},
    {"Field Name": "GLDividendIncome", "Field Description": "Dividend Income (Annual)", "Field Default Value": 10000,"assumption": True,"scenario": True},
    {"Field Name": "GLRentalIncome", "Field Description": "Rental Income (Annual)", "Field Default Value": 20000,"assumption": True,"scenario": True}
]
