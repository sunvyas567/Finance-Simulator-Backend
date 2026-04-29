from copy import deepcopy

# -----------------------------
# Country Profiles (v1)
# -----------------------------

COUNTRY_PROFILES = {
    "IN": {
        "inflation": 6.0,
        "swp_return": 10.0,
        "expense_weights": {
            "LocalGroceryVeg": 0.22,
            "LocalWaterElectricity": 0.04,
            "LocalTransportFuel": 0.10,
            "LocalMedicalInsurance": 0.06,
            "LocalInsuranceVehicle": 0.04,
            "LocalHouseRepairs": 0.04,
            "LocalVehicleMaintenance": 0.03,
            "LocalEntertainment": 0.08,
            "LocalInternetMobileTelecom": 0.03,
            "LocalTVOTT": 0.02,
            "LocalTravelLeisureInland": 0.12,
            "LocalFunctionsEtc": 0.04,
            "LocalMiscellaneousTax": 0.08
        }
    },

    "US": {
        "inflation": 3.0,
        "swp_return": 7.0,
        "expense_weights": {
            "LocalGroceryVeg": 0.18,
            "LocalWaterElectricity": 0.08,
            "LocalTransportFuel": 0.12,
            "LocalMedicalInsurance": 0.14,
            "LocalHouseRepairs": 0.05,
            "LocalEntertainment": 0.10,
            "LocalInternetMobileTelecom": 0.05,
            "LocalTravelLeisureInland": 0.12,
            "LocalMiscellaneousTax": 0.11
        }
    },

    "UK": {
        "inflation": 3.2,
        "swp_return": 6.5,
        "expense_weights": {
            "LocalGroceryVeg": 0.20,
            "LocalWaterElectricity": 0.10,
            "LocalTransportFuel": 0.10,
            "LocalMedicalInsurance": 0.06,
            "LocalHouseRepairs": 0.05,
            "LocalEntertainment": 0.10,
            "LocalInternetMobileTelecom": 0.04,
            "LocalTravelLeisureInland": 0.10,
            "LocalMiscellaneousTax": 0.15
        }
    }
}


# -----------------------------
# Normalizer
# -----------------------------

def normalize_assumptions_old(
    user_data: dict,
    *,
    user: dict,
    country: str,
    total_monthly_expenses: float | None = None
) -> dict:
    """
    Returns engine-ready user_data with:
    - country defaults applied
    - expenses auto-distributed
    - premium entitlements enforced
    """

    data = deepcopy(user_data)
    profile = COUNTRY_PROFILES.get(country, COUNTRY_PROFILES["IN"])

    # -----------------------------
    # Inflation & Market Defaults
    # -----------------------------

    _set_default(data, "GLInflationRate", profile["inflation"], country)
    _set_default(data, "GLSWPGrowthRate", profile["swp_return"], country)

    # -----------------------------
    # Projection Years (ENTITLEMENT)
    # -----------------------------

    if not user.get("is_premium"):
        projection_years = 2
    else:
        raw = data.get("GLProjectionYears", {}).get("input")
        projection_years = int(raw or 1)

    data["GLProjectionYears"] = {
        "input": projection_years,
        "source": "system",
        "locked": True
    }

    # -----------------------------
    # Expense Auto Distribution
    # -----------------------------

    if total_monthly_expenses:
        _distribute_expenses(
            data,
            total_monthly_expenses,
            profile["expense_weights"]
        )

    return data


# -----------------------------
# Helpers
# -----------------------------

def _set_default(data, key, value, country):
    if key not in data or data[key].get("source") != "user":
        data[key] = {
            "input": value,
            "source": f"country:{country}",
            "locked": False
        }


def _distribute_expenses(data, total, weights):
    remaining_total = total
    unlocked_weights = {}

    # Respect locked fields
    for field, weight in weights.items():
        if data.get(field, {}).get("locked"):
            remaining_total -= data[field]["input"]
        else:
            unlocked_weights[field] = weight

    if remaining_total <= 0 or not unlocked_weights:
        return

    weight_sum = sum(unlocked_weights.values())

    for field, weight in unlocked_weights.items():
        amount = round((weight / weight_sum) * remaining_total, 2)
        data[field] = {
            "input": amount,
            "source": "auto",
            "locked": False
        }

from app.api.country_profiles import COUNTRY_PROFILES

def normalize_assumptions(user_data: dict, user: dict):
    country_code = user_data.get("country", "IN")
    profile = COUNTRY_PROFILES[country_code]

    normalized = dict(user_data)  # shallow copy

    # ---- Defaults (only if user didn't override) ----
    normalized.setdefault(
        "InflationRate",
        {"input": profile["inflation_default"] * 100}
    )

    normalized.setdefault(
        "RetirementAge",
        {"input": profile["retirement_age_default"]}
    )

    # ---- Investment assumptions ----
    for k, v in profile["investment_returns"].items():
        key = f"Return_{k.upper()}"
        normalized.setdefault(key, {"input": v * 100})

    # ---- Meta ----
    normalized["_meta"] = {
        "country": country_code,
        "currency": profile["currency"]
    }

    return normalized
