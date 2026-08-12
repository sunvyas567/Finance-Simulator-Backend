# app/api/advisor/engine.py

import os
import json
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import google.generativeai as genai

router = APIRouter()

# -------------------------------------------------
# 🎯 PYDANTIC STRUCURED AI OUTPUT SCHEMAS
# -------------------------------------------------
class AdvisorAIResponse(BaseModel):
    summary: str = Field(..., description="A 2-3 sentence friendly, plain-English overview of the user's plan longevity.")
    positives: List[str] = Field(..., description="Bullet points highlighting what parts of the portfolio or cashflow strategies are working well.")
    warnings: List[str] = Field(..., description="Risk vectors, shortfall warnings, or inflation traps detected down the timeline.")
    recommendations: List[str] = Field(..., description="Actionable updates the user can make to their allocations or savings rate right now.")


# Configure your global Google API client layer
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_KEY:
    genai.configure(api_key=GOOGLE_KEY)


# app/api/advisor/engine.py (Update only the advisor_ai endpoint)

@router.post("/advisorAI", response_model=AdvisorAIResponse)
def advisor_ai(payload: dict):
    """
    Advanced Generative AI Advisor powered by Google Gemini.
    Implements a resilient multi-model waterfall loop to eliminate 404 deprecation errors.
    """
    if not GOOGLE_KEY:
        raise HTTPException(
            status_code=500, 
            detail="GOOGLE_API_KEY environment variable is missing on this backend container node."
        )

    projections = payload.get("projections", [])
    base_context = payload.get("base_context", {}).get("_meta", {}) # Safe multi-nest read
    scenario = payload.get("scenario", {})
    user_data = payload.get("user_data", {})

    if not projections:
        raise HTTPException(status_code=400, detail="Cannot generate AI insights without raw projection data streams.")

    # 1. Extract metadata context layers safely
    currency = base_context.get("currency", "₹")
    country = base_context.get("country", "IN")
    scenario_name = base_context.get("scenario", "Realistic")
    current_age = user_data.get("GLAge", {}).get("input", 35)

    # 2. Pull timeline boundary values
    year1 = projections[0]
    last_year = projections[-1]
    starting_wealth = year1.get("EndingCorpus", 0) or year1.get("StartingCorpus", 0)
    terminal_wealth = last_year.get("EndingCorpus", 0)

    system_instruction = (
        "You are an elite, highly empathetic retirement portfolio engineer and wealth strategist. "
        "Analyze the year-by-year financial projection array matrix and demographic context provided. "
        "Deliver a conversational, encouraging, yet highly accurate wealth audit report. "
        "You MUST strictly structure your output according to the requested JSON response schema."
    )

    user_prompt = f"""
    User Location Node: {country} Node
    Active Market Simulation Path: {scenario_name} Volatility Track
    Current Age Coordinate: {current_age} years old
    Timeline Projection Window: {len(projections)} Years Horizon
    
    Starting Pool Liquid Net Worth: {currency}{starting_wealth:,.2f}
    Final Terminal Capital Position at end of horizon: {currency}{terminal_wealth:,.2f}
    
    Active Portfolio Asset Allocations Mix:
    {scenario.get('allocations', {})}
    
    Secondary External Inflow Revenue Stream Map:
    {scenario.get('income_sources', {})}
    
    Review the complete chronological dataset logs below:
    {projections}
    """

    # 🟢 3. ACTIVE WATERFALL TIMELINE: Sequential backup options for cost-effective structured tasks
    candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]
    
    response = None
    last_error_msg = ""
    selected_model_name = ""

    # 🟢 4. TRIAL PIPELINE RUN: Loops through candidates until one clears validation cleanly
    for model_name in candidate_models:
        try:
            print(f"🧬 Attempting secure pipeline hook via: {model_name}...")
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            
            # Fire inference payload structure configuration
            response = model.generate_content(
                user_prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=AdvisorAIResponse,
                    temperature=0.3
                )
            )
            
            # If the response cleared the gateway with content, confirm success and break loop
            if response and response.text:
                selected_model_name = model_name
                print(f"✅ Successful compilation container match established using: {selected_model_name}")
                break
                
        except Exception as model_err:
            last_error_msg = str(model_err)
            print(f"⚠️ Version Miss: {model_name} returned an exception block. Cascading to next candidate...")
            continue

    # 5. Fallback circuit-breaker logic if all endpoints are completely offline
    if not response or not response.text:
        raise HTTPException(
            status_code=500,
            detail=f"All available Gemini model endpoints rejected this transaction block. Last trace error: {last_error_msg}"
        )

    try:
        # Parse the verified schema payload dictionary back to your frontend
        parsed_insights = json.loads(response.text)
        
        # Inject the active model signature tag so your UI debug dashboard updates accurately
        parsed_insights["source"] = "live"
        return parsed_insights
        
    except Exception as parse_err:
        raise HTTPException(
            status_code=500,
            detail=f"AI returned invalid structure formatting limits. Trace: {str(parse_err)}"
        )
# -------------------------------------------------
# 🤖 NEW ENDPOINT: GOOGLE GEMINI AI ADVISOR
# -------------------------------------------------
@router.post("/advisorAI", response_model=AdvisorAIResponse)
def advisor_ai(payload: dict):
    """
    Advanced Generative AI Advisor powered by Google Gemini.
    Ingests full timeline array data to output hyper-personalized optimization feedback.
    """
    if not GOOGLE_KEY:
        raise HTTPException(
            status_code=500, 
            detail="GOOGLE_API_KEY environment variable is missing on this backend container node."
        )

    projections = payload.get("projections", [])
    base_context = payload.get("base_context", {})
    scenario = payload.get("scenario", {})
    user_data = payload.get("user_data", {})

    if not projections:
        raise HTTPException(status_code=400, detail="Cannot generate AI insights without raw projection data streams.")

    try:
        # Extract metadata metrics context layers
        meta = base_context.get("_meta", {})
        currency = meta.get("currency", "₹")
        country = meta.get("country", "IN")
        scenario_name = meta.get("scenario", "Realistic")
        current_age = user_data.get("GLAge", {}).get("input", 35)

        # Pull terminal boundaries values
        year1 = projections[0]
        last_year = projections[-1]
        starting_wealth = year1.get("EndingCorpus", 0) or year1.get("StartingCorpus", 0)
        terminal_wealth = last_year.get("EndingCorpus", 0)

        # Engineering a context-dense system instruction prompt for the model
        system_instruction = (
            "You are an elite, highly empathetic retirement portfolio engineer and wealth strategist. "
            "Analyze the year-by-year financial projection array matrix and demographic context provided. "
            "Deliver a conversational, encouraging, yet highly accurate wealth audit report. "
            "You MUST strictly structure your output according to the requested JSON response schema."
        )

        user_prompt = f"""
        User Location Node: {country} Node
        Active Market Simulation Path: {scenario_name} Volatility Track
        Current Age Coordinate: {current_age} years old
        Timeline Projection Window: {len(projections)} Years Horizon
        
        Starting Pool Liquid Net Worth: {currency}{starting_wealth:,.2f}
        Final Terminal Capital Position at end of horizon: {currency}{terminal_wealth:,.2f}
        
        Active Portfolio Asset Allocations Mix:
        {scenario.get('allocations', {})}
        
        Secondary External Inflow Revenue Stream Map:
        {scenario.get('income_sources', {})}
        
        Review the complete chronological dataset logs below:
        {projections}
        """

        # Initialize the target generation instance configuration
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Highly scalable, low-latency structured output model
            system_instruction=system_instruction
        )

        # Trigger content loop generation with native JSON Schema constraints enforced
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=AdvisorAIResponse,
                temperature=0.3  # Keeps hallucination rates extremely low
            )
        )

        # Parse the verified JSON string back into a standard Python dictionary object structure
        parsed_insights = json.loads(response.text)
        return parsed_insights

    except Exception as e:
        print(f"❌ Gemini Advisor Engine Crash Sequence: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Secure AI pipeline processing failed context trace: {str(e)}"
        )


# -------------------------------------------------
# 🔁 LEGACY ENDPOINT: RULE-BASED ADVISOR
# -------------------------------------------------
def generate_advisor_recommendations(
    projections: list,
    base_context: dict,
    scenario: dict,
    user_data: Optional[dict] = None,
):
    """
    Rules-based, scenario-aware advisor engine.
    """
    if not projections:
        return _empty_advice("No projection data available.")

    year1 = projections[0]
    last_year = projections[-1]
    
    currency = base_context.get("_meta", {}).get("currency", "₹")
    country = base_context.get("_meta", {}).get("country", "IN")
    scenario_name = base_context.get("_meta", {}).get("scenario", "Base")

    advice = {
        "health_score": 100,
        "alerts": [],
        "recommendations": [],
        "positives": [],
        "scenario_insights": []
    }

    starting_corpus = year1.get("StartingCorpus", 0)
    ending_corpus = last_year.get("EndingCorpus", 0)
    net_surplus_y1 = year1.get("NetSurplus", 0)
    tax_y1 = year1.get("TotalTax", 0)
    income_y1 = year1.get("TotalIncome", 0)

    mandatory = year1.get("AnnualMustExpenses", 0)
    expense_ratio = mandatory / income_y1 if income_y1 > 0 else 1.0

    if net_surplus_y1 < 0:
        advice["alerts"].append({"severity": "high", "message": "Your expenses exceed your income in the first year."})
        advice["recommendations"].append("Reduce discretionary expenses or rebalance investments to improve income.")
        advice["health_score"] -= 25
    else:
        advice["positives"].append("Your income comfortably covers expenses in the first year.")

    if ending_corpus < starting_corpus * 0.7:
        advice["alerts"].append({"severity": "high", "message": "Your corpus depletes significantly over the projection period."})
        advice["recommendations"].append("Consider lowering withdrawals or increasing growth-oriented allocations.")
        advice["health_score"] -= 30
    elif ending_corpus > starting_corpus:
        advice["positives"].append("Your corpus grows over time, indicating a sustainable plan.")

    if expense_ratio > 0.7:
        advice["alerts"].append({"severity": "medium", "message": "Mandatory expenses consume a large portion of income."})
        advice["recommendations"].append("Build a higher income buffer or reduce fixed costs.")
        advice["health_score"] -= 15

    if income_y1 > 0 and tax_y1 / income_y1 > 0.25:
        advice["alerts"].append({"severity": "medium", "message": "Tax outgo is relatively high."})
        advice["recommendations"].append("Explore more tax-efficient income sources or allocations.")
        advice["health_score"] -= 10
    else:
        advice["positives"].append("Your tax burden appears manageable.")

    allocations = scenario.get("allocations", {})
    equity_like = sum(v for k, v in allocations.items() if k.upper() in {"SWP", "BROKERAGE", "401K", "IRA", "ISA"})

    if equity_like < 30:
        advice["scenario_insights"].append("Your allocation is heavily tilted towards conservative instruments.")
        advice["recommendations"].append("Consider increasing growth assets slightly to hedge inflation.")
        advice["health_score"] -= 10

    if equity_like > 70:
        advice["alerts"].append({"severity": "low", "message": "High exposure to market-linked assets."})
        advice["recommendations"].append("Ensure sufficient stable income to manage market volatility.")

    if ending_corpus <= 0:
        advice["alerts"].append({"severity": "critical", "message": "Your corpus runs out before the projection ends."})
        advice["recommendations"].append("Immediate restructuring required: reduce withdrawals or extend working years.")
        advice["health_score"] = max(advice["health_score"] - 40, 10)

    advice["health_score"] = max(0, min(100, advice["health_score"]))
    advice["summary"] = f"Scenario '{scenario_name}' results in a health score of {advice['health_score']}/100."
    return advice


def _empty_advice(reason: str) -> dict:
    return {
        "health_score": 0,
        "alerts": [{"severity": "info", "message": reason}],
        "recommendations": [],
        "positives": [],
        "scenario_insights": [],
        "summary": reason
    }