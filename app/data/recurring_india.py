RECURRING_INDIA = [
    # Home & Utilities
    {"Field Name": "LocalGroceryVeg", "Field Description": "Groceries", "Field Default Value": 8000},
    {"Field Name": "LocalWaterElectricity", "Field Description": "Water & Electricity", "Field Default Value": 3000},
    {"Field Name": "LocalHouseRepairs", "Field Description": "House Repairs", "Field Default Value": 1500},
    {"Field Name": "LocalMaidServices", "Field Description": "Maid Services", "Field Default Value": 2500},

    # Transport
    {"Field Name": "LocalInsuranceVehicle", "Field Description": "Vehicle Insurance", "Field Default Value": 1500},
    {"Field Name": "LocalTransportFuel", "Field Description": "Fuel", "Field Default Value": 3000},
    {"Field Name": "LocalVehicleMaintenance", "Field Description": "Vehicle Maintenance", "Field Default Value": 1500},

    # Lifestyle
    {"Field Name": "LocalEntertainment", "Field Description": "Entertainment", "Field Default Value": 2000},
    {"Field Name": "LocalInternetMobileTelecom", "Field Description": "Internet & Mobile", "Field Default Value": 1500},
    {"Field Name": "LocalTVOTT", "Field Description": "TV & OTT", "Field Default Value": 1000},
    {"Field Name": "LocalTravelLeisureInland", "Field Description": "Domestic Travel", "Field Default Value": 3000},
    {"Field Name": "LocalFunctionsEtc", "Field Description": "Functions & Events", "Field Default Value": 2000},

    # Taxes & Insurance
    {"Field Name": "LocalPropertyTax", "Field Description": "Property Tax", "Field Default Value": 1500},
    {"Field Name": "LocalMedicalInsurance", "Field Description": "Medical Insurance", "Field Default Value": 3500},
    {"Field Name": "LocalMiscellaneousTax", "Field Description": "Other Taxes", "Field Default Value": 1000},

    # Optional
    {"Field Name": "LocalTravelLeisureForeignOpt", "Field Description": "Foreign Travel", "Field Default Value": 5000},
    {"Field Name": "LocalOthersOpt", "Field Description": "Other Optional Expenses", "Field Default Value": 2000},

    # Totals
    {"Field Name": "GLTotalYearlyExpensesMust", "Field Input":
        "={LocalGroceryVeg}+{LocalWaterElectricity}+{LocalHouseRepairs}+{LocalMaidServices}"
        "+{LocalInsuranceVehicle}+{LocalTransportFuel}+{LocalVehicleMaintenance}"
        "+{LocalPropertyTax}+{LocalMedicalInsurance}+{LocalMiscellaneousTax}"
        "+{LocalEntertainment}+{LocalInternetMobileTelecom}+{LocalTVOTT}"
        "+{LocalTravelLeisureInland}+{LocalFunctionsEtc}"
    },
    {"Field Name": "GLTotalYearlyExpensesOptional", "Field Input":
        "+{LocalTravelLeisureForeignOpt}+{LocalOthersOpt}"
    }
]
