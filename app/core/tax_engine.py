def calculate_tax(country: str, income: float) -> float:
    if country == "IN":
        return tax_india(income)
    elif country == "US":
        return tax_us(income)
    elif country == "UK":
        return tax_uk(income)
    return 0.0

def tax_india(income):
    slabs = [
        (250000, 0.0),
        (500000, 0.05),
        (1000000, 0.20),
        (float("inf"), 0.30)
    ]
    return slab_tax(income, slabs)

def tax_us(income):
    slabs = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
        (float("inf"), 0.32)
    ]
    return slab_tax(income, slabs)

def tax_uk(income):
    slabs = [
        (12570, 0.0),
        (50270, 0.20),
        (125140, 0.40),
        (float("inf"), 0.45)
    ]
    return slab_tax(income, slabs)

def slab_tax(income, slabs):
    tax = 0.0
    prev = 0
    for limit, rate in slabs:
        if income > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (income - prev) * rate
            break
    return tax
