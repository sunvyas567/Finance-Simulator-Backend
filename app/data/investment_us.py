INVESTMENT_US = [
    # Starting Corpus
    {"Field Name": "LocalStartingCorpus",
     "Field Input": "={GL401kCorpus}+{GLRothIRACorpus}"},

    # Income from investments
    {"Field Name": "GL401kIncome",
     "Field Input": "={GL401kCorpus}*{GL401kRate}/100"},

    {"Field Name": "GLRothIRAIncome",
     "Field Input": "={GLRothIRACorpus}*{GLRothIRARate}/100"},

    # Total Income
    {"Field Name": "GLTotalIncomeOverallFDs",
     "Field Input": "={GL401kIncome}+{GLRothIRAIncome}+{GLSocialSecurityIncome}+{GLDividendIncome}+{GLRentalIncome}"}
]
