#from fastapi import APIRouter
#from app.data.config_data import (
#    BASE_DATA_CONFIG,
#    ONETIME_EXPENSES_CONFIG,
#    RECURRING_EXPENSES_CONFIG,
#    INVESTMENT_PLAN_CONFIG,
#    KNOWLEDGEBASE_FAQ_DATA,
#    ABOUT_APP_TEXT
#)

#router = APIRouter(prefix="/config", tags=["Config"])

#@router.get("/")
#def get_all_config():
#    return {
#    "about": ABOUT_APP_TEXT,
#    "base_data": BASE_DATA_CONFIG,
#    "onetime_expenses": ONETIME_EXPENSES_CONFIG,
#    "recurring_expenses": RECURRING_EXPENSES_CONFIG,
#    "investment_plan": INVESTMENT_PLAN_CONFIG
#}

from fastapi import APIRouter, Query
from app.api.country_resolver import resolve_country_configs

router = APIRouter(prefix="/config", tags=["Config"])

@router.get("/")
def get_config(country: str = Query(default="IN")):
    configs = resolve_country_configs(country)
    return {
        "about": "Multi-country retirement planner",
        "base_data": configs["base_data"],
        "onetime_expenses": configs["onetime"],
        "recurring_expenses": configs["recurring"],
        "investment_plan": configs["investment"]
    }



