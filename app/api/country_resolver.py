# app/api/country_resolver.py
from app.data.base_data_india import BASE_DATA_INDIA
from app.data.base_data_us import BASE_DATA_US
from app.data.base_data_uk import BASE_DATA_UK

from app.data.onetime_india import ONETIME_INDIA
from app.data.onetime_us import ONETIME_US
from app.data.onetime_uk import ONETIME_UK

from app.data.recurring_india import RECURRING_INDIA
from app.data.recurring_us import RECURRING_US
from app.data.recurring_uk import RECURRING_UK

from app.data.investment_india import INVESTMENT_INDIA
from app.data.investment_us import INVESTMENT_US
from app.data.investment_uk import INVESTMENT_UK
from app.api.investments.india import india_investment_fn
from app.api.investments.us import us_investment_fn
from app.api.investments.uk import uk_investment_fn


COUNTRY_META = {
    "IN": {
        "label": "India",
        "currency": "₹",
        "investment_fn": india_investment_fn,
        "default_inflation": 0.06,
        "base_data": BASE_DATA_INDIA,
        "onetime": ONETIME_INDIA,
        "recurring": RECURRING_INDIA,
        "investment": INVESTMENT_INDIA
    },
    "US": {
        "label": "United States",
        "currency": "$",
        "investment_fn": us_investment_fn,
        "default_inflation": 0.03,
        "base_data": BASE_DATA_US,
        "onetime": ONETIME_US,
        "recurring": RECURRING_US,
        "investment": INVESTMENT_US
    },
    "UK": {
        "label": "United Kingdom",
        "currency": "£",
        "investment_fn": uk_investment_fn,
        "default_inflation": 0.025,
        "base_data": BASE_DATA_UK,
        "onetime": ONETIME_UK,
        "recurring": RECURRING_UK,
        "investment": INVESTMENT_UK
    },
}


def resolve_country_configs(country: str) -> dict:
    """
    🔒 Single source of country behavior.
    NO data defaults.
    NO UI fields.
    NO expenses.
    """
    if country not in COUNTRY_META:
        raise ValueError(f"Unsupported country: {country}")

    return COUNTRY_META[country].copy()
