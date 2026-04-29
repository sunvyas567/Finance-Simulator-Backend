def us_tax(taxable_income: float, user_data: dict):
    slabs = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
        (float("inf"), 0.32)
    ]

    remaining = taxable_income
    prev_limit = 0
    total_tax = 0
    components = {}

    for limit, rate in slabs:
        slab_income = min(limit - prev_limit, remaining)
        if slab_income <= 0:
            break
        tax = slab_income * rate
        components[f"{prev_limit}-{limit}@{rate*100}%"] = tax
        total_tax += tax
        remaining -= slab_income
        prev_limit = limit

    return {
        "total_tax": round(total_tax, 2),
        "effective_rate": round(total_tax / taxable_income, 4),
        "components": components
    }
