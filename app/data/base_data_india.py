BASE_DATA_INDIA = [
    # ----------------------------
    # Personal
    # ----------------------------
    {"Field Name": "GLAge", "Field Description": "Current Age", "Field Default Value": 58},
    {"Field Name": "GLGender", "Field Description": "Gender", "Field Default Value": "Male"},

    # ----------------------------
    # Core Assumptions
    # ----------------------------
    {"Field Name": "GLProjectionYears", "Field Description": "Projection Years", "Field Default Value": 2,"assumption": True,"scenario": True},
    {"Field Name": "GLInflationRate", "Field Description": "Inflation Rate (%)", "Field Default Value": 6.0,"assumption": True,"scenario": True},

    # ----------------------------
    # Interest & Investment Rates
    # ----------------------------
    {"Field Name": "GLNormalFDRate", "Field Description": "Normal FD Rate (%)", "Field Default Value": 6.5,"assumption": True,"scenario": True},
    {"Field Name": "GLSrCitizenFDRate", "Field Description": "Senior Citizen FD Rate (%)", "Field Default Value": 7.5,"assumption": True,"scenario": True},
    {"Field Name": "GLSCSSRate", "Field Description": "SCSS Rate (%)", "Field Default Value": 8.,"assumption": True,"scenario": True},
    {"Field Name": "GLPOMISRate", "Field Description": "Post Office MIS Rate (%)", "Field Default Value": 7.4,"assumption": True,"scenario": True},

    # ----------------------------
    # SWP
    # ----------------------------
    {"Field Name": "GLSWPGrowthRate", "Field Description": "SWP Growth Rate (%)", "Field Default Value": 6.5,"assumption": True,"scenario": True},
    {"Field Name": "GLSWPMonthlyWithdrawal", "Field Description": "SWP Monthly Withdrawal", "Field Default Value": 25000,"assumption": True,"scenario": True},

    # ----------------------------
    # Initial Corpus
    # ----------------------------
    {"Field Name": "GLPFBalance", "Field Description": "Provident Fund Accumulation", "Field Default Value": 1500000,"assumption": True,"scenario": True},
    {"Field Name": "GLPPFBalance", "Field Description": "PPF Accumulation", "Field Default Value": 800000,"assumption": True,"scenario": True},
    {"Field Name": "GLSuperannuationBalance", "Field Description": "Superannuation Corpus", "Field Default Value": 500000,"assumption": True,"scenario": True},

    # ----------------------------
    # Other Income
    # ----------------------------
    {"Field Name": "GLDividendIncome", "Field Description": "Dividend Income (Annual)", "Field Default Value": 60000,"assumption": True,"scenario": True},
    {"Field Name": "GLRealStateIncome", "Field Description": "Rental Income (Annual)", "Field Default Value": 180000,"assumption": True,"scenario": True},

    {"Field Name": "GLSWPInvestmentPercentage","Field Description": "SWP Allocation (%)","Field Default Value": 60,"assumption": True,"scenario": True},
    {"Field Name": "GLNonSWPInvestmentPercentage","Field Description": "Non-SWP Allocation (%)","Field Default Value": 40,"assumption": True,"scenario": True},
    {"Field Name": "GLNormalFDExcludingPOMISSCSS","Field Description": "Normal FD Allocation (%)","Field Default Value": 50},
    {"Field Name": "GLSrCitizenFDExcludingPOMISSCSS","Field Description": "Senior Citizen FD Allocation (%)","Field Default Value": 50},
    {
    "Field Name": "GLPOMISSingle",
    "Field Description": "Post Office MIS Monthly Income",
    "Field Default Value": 2000
    },
    {
    "Field Name": "GLSCSSSingle",
    "Field Description": "SCSS Monthly Income",
    "Field Default Value": 3000
    },
    {
    "Field Name": "GLCurrentMonthlyRental",
    "Field Description": "Current Monthly Rental Income",
    "Field Default Value": 20000
    },
    {
    "Field Name": "GLMaxMonthlyRental",
    "Field Description": "Maximum Rental Income",
    "Field Default Value": 30000
    },
    {
    "Field Name": "GLAnnuityExistingMonthly",
    "Field Description": "Existing Monthly Annuity",
    "Field Default Value": 1500
    },
    {
    "Field Name": "GLPensionEPS",
    "Field Description": "EPS Pension Income",
    "Field Default Value": 2000
    },


]
