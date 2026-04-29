# allocation_engine.py

from typing import Dict
#from allocation_rules import COUNTRY_RULES

# allocation_rules.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class InstrumentRule:
    name: str
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    max_allocation_pct: Optional[float] = None
    max_investment_amount: Optional[float] = None
    enabled: bool = True


INDIA_RULES = {
    "SWP": InstrumentRule("SWP", max_allocation_pct=100),

    "FD": InstrumentRule("FD", max_allocation_pct=100),

    "SCSS": InstrumentRule(
        "SCSS",
        min_age=60,
        max_allocation_pct=100,
        max_investment_amount=30_00_000  # ₹30 lakh govt cap
    ),

    "POMIS": InstrumentRule(
        "POMIS",
        max_allocation_pct=100,
        max_investment_amount=4_50_000  # single holder cap
    )
}


US_RULES = {
    "SWP": InstrumentRule("SWP"),
    "401K": InstrumentRule("401K"),
    "IRA": InstrumentRule("IRA"),
    "BROKERAGE": InstrumentRule("BROKERAGE"),
}


UK_RULES = {
    "SWP": InstrumentRule("SWP"),
    "PENSION": InstrumentRule("PENSION"),
    "ISA": InstrumentRule("ISA"),
}


COUNTRY_RULES = {
    "IN": INDIA_RULES,
    "US": US_RULES,
    "UK": UK_RULES,
}


class AllocationEngine:

    def __init__(self, country: str, age: int, investable_amount: float):
        self.country = country
        self.age = age
        self.amount = investable_amount
        self.rules = COUNTRY_RULES[country]

    # ---------------------------------------------------
    # STEP 1 — Remove ineligible instruments
    # ---------------------------------------------------
    def filter_eligible(self, allocations: Dict[str, float]):

        valid = {}

        for instrument, pct in allocations.items():

            rule = self.rules.get(instrument)

            if not rule or not rule.enabled:
                continue

            if rule.min_age and self.age < rule.min_age:
                continue

            if rule.max_age and self.age > rule.max_age:
                continue

            valid[instrument] = pct

        return valid

    # ---------------------------------------------------
    # STEP 2 — Normalize to 100%
    # ---------------------------------------------------
    def normalize(self, allocations: Dict[str, float]):

        total = sum(allocations.values())

        if total == 0:
            return allocations

        return {
            k: v * 100 / total
            for k, v in allocations.items()
        }

    # ---------------------------------------------------
    # STEP 3 — Apply investment caps
    # ---------------------------------------------------
    def apply_caps(self, allocations: Dict[str, float]):

        final = {}
        leftover_pct = 0

        for inst, pct in allocations.items():

            rule = self.rules[inst]
            amount = self.amount * pct / 100

            if rule.max_investment_amount and amount > rule.max_investment_amount:
                capped_pct = rule.max_investment_amount * 100 / self.amount
                final[inst] = capped_pct
                leftover_pct += pct - capped_pct
            else:
                final[inst] = pct

        # redistribute leftover
        if leftover_pct > 0:
            eligible = [k for k in final if final[k] > 0]
            if eligible:
                add = leftover_pct / len(eligible)
                for k in eligible:
                    final[k] += add

        return self.normalize(final)

    # ---------------------------------------------------
    # STEP 4 — Convert % → money
    # ---------------------------------------------------
    def to_amounts(self, allocations):

        return {
            k: round(self.amount * v / 100, 2)
            for k, v in allocations.items()
        }

    # ---------------------------------------------------
    # MASTER FUNCTION
    # ---------------------------------------------------
    def build(self, raw_allocations):

        step1 = self.filter_eligible(raw_allocations)
        step2 = self.normalize(step1)
        step3 = self.apply_caps(step2)
        amounts = self.to_amounts(step3)

        return {
            "final_percentages": step3,
            "final_amounts": amounts
        }
