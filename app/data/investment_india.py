INVESTMENT_INDIA = [
    # Total Investment Corpus
    {"Field Name": "LocalStartingCorpus",
     "Field Input": "={GLPFBalance}+{GLPPFBalance}+{GLSuperannuationBalance}"},

    # Income from investments
    {"Field Name": "GLFDIncome",
     "Field Input": "=({GLPFBalance}+{GLPPFBalance}+{GLSuperannuationBalance})*{GLNormalFDRate}/100"},

    {"Field Name": "GLSCSSIncome",
     "Field Input": "={GLPFBalance}*{GLSCSSRate}/100"},

    {"Field Name": "GLPOMISIncome",
     "Field Input": "={GLPPFBalance}*{GLPOMISRate}/100"},

    # Total Income
    {"Field Name": "GLTotalIncomeOverallFDs",
     "Field Input": "={GLFDIncome}+{GLSCSSIncome}+{GLPOMISIncome}+{GLDividendIncome}+{GLRealStateIncome}"},
]
