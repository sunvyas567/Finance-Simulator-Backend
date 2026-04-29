import json
from app.api.config import (
    BASE_DATA_CONFIG,
    ONETIME_EXPENSES_CONFIG,
    RECURRING_EXPENSES_CONFIG,
)

def hydrate_user_data(user_data: dict) -> dict:
    """
    Ensures user_data has all default inputs before projections.
    Mirrors main3 behavior.
    """
    ctx = json.loads(json.dumps(user_data))

    all_configs = (
        BASE_DATA_CONFIG
        + ONETIME_EXPENSES_CONFIG
        + RECURRING_EXPENSES_CONFIG
    )

    for item in all_configs:
        key = item.get("Field Name")
        default = item.get("Field Default Value")

        
        # ✅ DO NOT OVERRIDE EXISTING INPUT
        if key not in user_data:
            user_data[key] = {"input": default}
            
        if not key:
            continue

        if key not in ctx:
            # Skip formulas, only seed base values
            if isinstance(default, str) and default.startswith("="):
                continue
            ctx[key] = {"input": default}

        elif "input" not in ctx[key]:
            ctx[key]["input"] = default

    return ctx
