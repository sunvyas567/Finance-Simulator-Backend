import re
import unicodedata
import math

def clean_formula(formula):
    if not isinstance(formula, str) or not formula.startswith("="):
        return formula
    formula = formula[1:].strip()
    formula = unicodedata.normalize("NFKC", formula).strip()
    formula = formula.replace("−", "-").replace("\u2212", "-")
    return formula

def eval_formula(formula, data_context):
    expression = clean_formula(formula)

    def replacer(match):
        var_name = match.group(1)
        val = data_context.get(var_name, {}).get("input", 0)
        try:
            return str(float(val))
        except:
            return "0"

    expression = re.sub(r"\{([^}]+)\}", replacer, expression)
    return eval(
        expression,
        {"__builtins__": {"math": math, "min": min, "max": max}},
        {}
    )
