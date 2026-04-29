from app.api.tax.india import india_tax
from app.api.tax.us import us_tax
from app.api.tax.uk import uk_tax

def calculate_tax(income_breakup: dict, user_data: dict, country: str):
    taxable_income = sum(income_breakup.values())

    if taxable_income <= 0:
        return {
            "total_tax": 0.0,
            "effective_rate": 0.0,
            "components": {}
        }

    if country == "IN":
        return india_tax(taxable_income, user_data)
    elif country == "US":
        return us_tax(taxable_income, user_data)
    elif country == "UK":
        return uk_tax(taxable_income, user_data)
    else:
        return {
            "total_tax": 0.0,
            "effective_rate": 0.0,
            "components": {}
        }
