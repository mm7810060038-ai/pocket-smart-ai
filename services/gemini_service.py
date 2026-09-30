import json
from .fallback import home_fallback, party_fallback, jewelry_fallback
from ..config import GEMINI_API_KEY, GEMINI_MODEL


def _client():
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return None


def _ask(prompt: str):
    client = _client()
    if client is None:
        return None
    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        text = getattr(response, "text", "") or ""
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
    except Exception:
        return None
    return None


def home(data):
    prompt = f"""You are PocketSmart AI. Create budget-aware home interior recommendations. Return ONLY valid JSON with keys title, summary, items. items must be an array of objects with name, platform, price, url. Budget: {data['budget']}. Room: {data['room']}. Style: {data['style']}. Requested items: {data['items']}. Platforms: IKEA, Amazon, Flipkart."""
    return _ask(prompt) or home_fallback(data)


def party(data):
    prompt = f"""You are PocketSmart AI. Create a party budget plan. Return ONLY valid JSON with keys title, summary, allocation, items. allocation is an array of category and amount. items must contain name, platform, price, url. Budget: {data['budget']}. Guests: {data['guests']}. Event: {data['event_type']}. Venue/location: {data['venue']}. Platforms: Swiggy, Zomato, OYO."""
    return _ask(prompt) or party_fallback(data)


def jewelry(data):
    prompt = f"""You are PocketSmart AI. Recommend jewelry based on budget, occasion and style. Return ONLY valid JSON with keys title, summary, items. items must contain name, platform, price, url. Budget: {data['budget']}. Occasion: {data['occasion']}. Style: {data['style']}. Outfit notes: {data.get('outfit') or 'not provided'}. Platforms: Amazon, Flipkart."""
    return _ask(prompt) or jewelry_fallback(data)
