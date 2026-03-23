import ollama
import json
import base64

def detect_dark_patterns(page_data):
    prompt = f"""
You are a UX researcher specialising in dark patterns.

Analyse the following website content and identify dark patterns.

Website: {page_data.get('url')}
Title: {page_data.get('title')}
Button texts: {page_data.get('buttons')}
Link texts: {page_data.get('links')}
Checkboxes: {page_data.get('checkboxes')}
Headings: {page_data.get('headings')}
Paragraphs: {page_data.get('paragraphs')}

Return a JSON array only:
[
  {{
    "pattern_name": "name",
    "category": "urgency/privacy/subscription/pricing/consent/misdirection",
    "evidence": "exact text from page",
    "severity": "High/Medium/Low",
    "explanation": "why manipulative",
    "recommendation": "ethical alternative"
  }}
]

Return ONLY the JSON array, nothing else.
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return _parse_json(response["message"]["content"])


def detect_visual_dark_patterns(screenshot_b64):
    prompt = """
You are a UX researcher analysing a website screenshot for dark patterns.

Look carefully at the visual layout and identify:
- Misleading button colours (e.g. decline button is grey and tiny, accept is bright)
- Hidden or tiny unsubscribe/cancel links
- Fake urgency indicators like countdown timers
- Confusing checkbox states
- Disguised advertisements that look like content
- Visual misdirection — important info in small grey text

Return a JSON array only:
[
  {
    "pattern_name": "name",
    "category": "visual/urgency/consent/misdirection",
    "evidence": "describe what you see visually",
    "severity": "High/Medium/Low",
    "explanation": "why this is manipulative",
    "recommendation": "ethical alternative"
  }
]

Return ONLY the JSON array, nothing else.
"""
    response = ollama.chat(
        model="llava",
        messages=[{
            "role": "user",
            "content": prompt,
            "images": [screenshot_b64]
        }]
    )
    return _parse_json(response["message"]["content"])


def _parse_json(raw):
    try:
        start = raw.find("[")
        end   = raw.rfind("]") + 1
        if start != -1 and end != 0:
            return json.loads(raw[start:end])
        return []
    except:
        return []