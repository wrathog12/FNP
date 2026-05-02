"""
═══════════════════════════════════════════════════════════════
  Agent 1: Context Agent — Event Intelligence
  
  Detects the most relevant upcoming High-Value Gifting Event
  within the next 30 days using the current date + Gemini AI.
  
  Core function: get_current_event()
═══════════════════════════════════════════════════════════════
"""

import json
from dataclasses import dataclass, asdict
from datetime import date, datetime

from google import genai
from google.genai import types

import config
from utils import log_agent_start, log_agent_complete, log_step, log_result, Timer


@dataclass
class EventContext:
    """Structured output from the Context Agent."""
    event_name: str              # e.g., "Mother's Day"
    event_date: str              # e.g., "2026-05-10"
    days_until: int              # e.g., 8
    cultural_significance: str   # Brief cultural context
    gifting_urgency: str         # "Peak" | "Building" | "Early"
    target_emotion: str          # e.g., "Gratitude, warmth, maternal love"

    def to_dict(self) -> dict:
        return asdict(self)


def get_current_event() -> EventContext:
    """
    Detect the next High-Value Gifting Event within 30 days.
    
    Uses Python's datetime for the current date, then sends it
    to Gemini to identify the most commercially relevant upcoming
    gifting event for a premium flower & gifting brand (FNP).
    
    Returns:
        EventContext with event details and emotional direction.
    """
    log_agent_start("Context Agent - Event Intelligence", "[CTX]")

    # Step 1: Get today's date
    today = date.today()
    today_str = today.strftime("%B %d, %Y")  # e.g., "May 02, 2026"
    log_step(f"[DATE] Today's date: {today_str}")

    # Step 2: Query Gemini for event detection
    log_step("[SEARCH] Querying Gemini for upcoming gifting events...")

    client = genai.Client(api_key=config.GEMINI_API_KEY)

    prompt = f"""You are an event intelligence system for FNP (Ferns N Petals), India's leading premium flower and gifting brand.

Today's date is: {today_str}

TASK: Identify the single most commercially relevant "High-Value Gifting Event" occurring within the NEXT {config.EVENT_LOOKAHEAD_DAYS} days.

Consider these events (and any other culturally significant ones):
- Mother's Day (2nd Sunday of May)
- Father's Day (3rd Sunday of June)  
- Valentine's Day (February 14)
- Diwali (varies — Hindu lunar calendar)
- Raksha Bandhan (varies — Hindu lunar calendar)
- Christmas (December 25)
- New Year (January 1)
- Women's Day (March 8)
- Anniversary (general — if no specific event is near)
- Eid (varies)
- Holi (varies)

RULES:
1. Pick the SINGLE most important event within {config.EVENT_LOOKAHEAD_DAYS} days
2. If multiple events exist, pick the one with highest commercial value for a flower/gifting brand
3. If NO major event is within {config.EVENT_LOOKAHEAD_DAYS} days, return "Default / General Gifting"
4. Calculate the exact number of days until the event

Respond ONLY with valid JSON in this exact format (no markdown, no code blocks):
{{
    "event_name": "Mother's Day",
    "event_date": "2026-05-10",
    "days_until": 8,
    "cultural_significance": "A day to honor mothers and maternal figures. Peak gifting occasion in India with flowers, cakes, and personalized gifts.",
    "gifting_urgency": "Peak",
    "target_emotion": "Gratitude, warmth, maternal love, tenderness"
}}

gifting_urgency must be one of:
- "Peak" = event is within 7 days (urgent buying window)
- "Building" = event is 8-20 days away (awareness + early orders)
- "Early" = event is 21-30 days away (teaser campaigns)
"""

    with Timer("Event detection"):
        response = client.models.generate_content(
            model=config.TEXT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,  # Low temp for factual accuracy
                response_mime_type="application/json",
            ),
        )

    # Step 3: Parse the response
    try:
        raw_text = response.text.strip()
        # Clean potential markdown code block wrappers
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0]
        
        event_data = json.loads(raw_text)
        event = EventContext(**event_data)
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        log_step(f"[WARN] Parse error: {e}. Using fallback event.")
        event = _get_fallback_event(today)

    # Step 4: Log results
    log_result("Event", event.event_name)
    log_result("Date", event.event_date)
    log_result("Days Until", str(event.days_until))
    log_result("Urgency", event.gifting_urgency)
    log_result("Target Emotion", event.target_emotion)

    log_agent_complete("Context Agent")
    return event


def _get_fallback_event(today: date) -> EventContext:
    """Fallback event when Gemini fails or no event is detected."""
    return EventContext(
        event_name="Default / General Gifting",
        event_date=today.strftime("%Y-%m-%d"),
        days_until=0,
        cultural_significance="Everyday premium gifting — celebrating life's beautiful moments.",
        gifting_urgency="Building",
        target_emotion="Joy, appreciation, thoughtful elegance",
    )
