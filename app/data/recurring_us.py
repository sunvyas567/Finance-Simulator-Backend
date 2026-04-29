RECURRING_US = [
    # Housing & Utilities
    {"Field Name": "USHousing", "Field Description": "Housing (Rent / Mortgage)", "Field Default Value": 1800},
    {"Field Name": "USUtilities", "Field Description": "Utilities", "Field Default Value": 300},
    {"Field Name": "USGroceries", "Field Description": "Groceries", "Field Default Value": 600},
    {"Field Name": "USHealthInsurance", "Field Description": "Health Insurance", "Field Default Value": 450},

    # Transport & Connectivity
    {"Field Name": "USTransport", "Field Description": "Transport", "Field Default Value": 350},
    {"Field Name": "USPhoneInternet", "Field Description": "Phone & Internet", "Field Default Value": 150},

    # Lifestyle
    {"Field Name": "USEntertainment", "Field Description": "Entertainment", "Field Default Value": 200},
    {"Field Name": "USMisc", "Field Description": "Miscellaneous", "Field Default Value": 150},

    # Totals
    {"Field Name": "GLTotalYearlyExpensesMust",
     "Field Input": "=USHousing+USUtilities+USGroceries+USHealthInsurance+USTransport+USPhoneInternet"},

    {"Field Name": "GLTotalYearlyExpensesOptional",
     "Field Input": "=USEntertainment+USMisc"}
]
