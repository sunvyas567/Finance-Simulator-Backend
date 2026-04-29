def india_tax(taxable_income: float, user_data: dict):
    slabs = [
        (250000, 0.0),
        (500000, 0.05),
        (1000000, 0.20),
        (float("inf"), 0.30)
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
