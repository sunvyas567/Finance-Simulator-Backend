RECURRING_UK = [
    # Housing & Utilities
    {"Field Name": "UKHousing", "Field Description": "Housing", "Field Default Value": 1300},
    {"Field Name": "UKCouncilTax", "Field Description": "Council Tax", "Field Default Value": 150},
    {"Field Name": "UKUtilities", "Field Description": "Utilities", "Field Default Value": 250},
    {"Field Name": "UKGroceries", "Field Description": "Groceries", "Field Default Value": 500},

    # Transport & Connectivity
    {"Field Name": "UKTransport", "Field Description": "Transport", "Field Default Value": 300},
    {"Field Name": "UKInternet", "Field Description": "Internet & Mobile", "Field Default Value": 120},

    # Lifestyle
    {"Field Name": "UKEntertainment", "Field Description": "Entertainment", "Field Default Value": 180},
    {"Field Name": "UKMisc", "Field Description": "Miscellaneous", "Field Default Value": 150},

    # Totals
    {"Field Name": "GLTotalYearlyExpensesMust",
     "Field Input": "=UKHousing+UKCouncilTax+UKUtilities+UKGroceries+UKTransport+UKInternet"},

    {"Field Name": "GLTotalYearlyExpensesOptional",
     "Field Input": "=UKEntertainment+UKMisc"}
]
