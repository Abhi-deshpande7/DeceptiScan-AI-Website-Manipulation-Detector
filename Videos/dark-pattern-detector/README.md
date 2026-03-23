# Dark Pattern Detector

An AI-powered tool that detects manipulative design patterns on any website 
using Llama 3 running locally via Ollama — no API key required.

## Features
- Scrapes any website URL automatically
- Detects 8+ types of dark patterns
- Severity ranking — High / Medium / Low
- Downloadable CSV report
- Fully local — no internet needed for AI analysis

## Tech Stack
Python · Streamlit · BeautifulSoup · Llama 3 · Ollama · pandas

## How to Run
1. Install Ollama from ollama.com
2. Run: `ollama run llama3`
3. Then:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author
Abhishek Deshpande — Manipal University Jaipur