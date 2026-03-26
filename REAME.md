# Customer Support Agent with LangGraph + Google Gemini

## Overview
AI-powered customer support agent for TechTrend Innovations using LangGraph and Google Gemini.

## Features
- Google Gemini LLM integration
- Short-term & long-term memory
- State management with LangGraph
- Human-in-the-loop escalation
- Streamlit UI

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
setx GOOGLE_API_KEY "your_key"
streamlit run app.py
