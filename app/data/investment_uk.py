INVESTMENT_UK = [
    # Starting Corpus
    {"Field Name": "LocalStartingCorpus",
     "Field Input": "={GLISACorpus+GLPrivatePensionCorpus}"},

    # Income from investments
    {"Field Name": "GLISAIncome",
     "Field Input": "={GLISACorpus*GLISARate}/100"},

    # Total Income
    {"Field Name": "GLTotalIncomeOverallFDs",
     "Field Input": "={GLISAIncome}+{GLStatePension}+{GLDividendIncome}+{GLRentalIncome}"}
]
