📞 Day 5 — FAQ SDR + Lead Capture Voice Agent

A voice-based Sales Development Representative (SDR) that answers company FAQs and automatically captures lead information during a natural conversation. The agent uses company-provided content (FAQs, product details, pricing) and avoids adding any unprovided details.

🧭 Overview

This agent acts as a Sales Development Representative for a chosen Indian company or startup.
It greets visitors, understands their needs, answers product/company questions using your provided FAQ data, and collects key lead fields.
When the conversation ends, the agent generates a structured lead summary and stores the captured information in JSON format.

✨ Features

Warm SDR-style voice interaction

Answers company FAQ, pricing, and product questions

Natural inquiry about user needs

Lead field capture (name, company, role, email, use case, etc.)

JSON storage of all responses

End-of-call lead summary generation

Keyword-based or simple matching for FAQ lookup

Avoids hallucinating — only uses provided content

🤖 Agent Capabilities
1. SDR Persona

Greets users politely

Asks what they’re working on

Keeps the conversation business-focused

Guides them naturally to discuss their needs

Asks for missing lead details smoothly

2. FAQ Answering

Loads company content (FAQ, product info, pricing)

Matches user questions to relevant FAQ entries

Responds only with provided content

No made-up details or assumptions

3. Lead Capture

Collects fields such as:

Name

Company

Email

Role

Use case

Team size

Timeline (now / soon / later)

4. End-of-Call Summary

When user says “That’s all”, “I’m done”, etc., the agent:

Summarizes who the lead is

Summarizes their needs

Summarizes urgency

Saves all data to a JSON file

🛠️ Function Tools
Tool	Purpose
load_company_faq()	Loads FAQs/content provided by you
find_faq_answer()	Keyword-based FAQ lookup
set_lead_field()	Stores a single lead field
save_lead_json()	Saves collected data to JSON file
generate_summary()	Creates conversation summary
📊 Metrics Tracked

Lead personal details

Company name

User’s needs / use-case

Team size

Timeline

FAQ question types asked

Summary of conversation

🗣 Conversational Flow

Greet warmly

Ask what brought them here

Understand needs

Answer FAQs using provided content

Collect lead fields in natural dialogue

Detect end-of-call phrases like:

“That’s all”

“I’m done”

“Thanks, that’s it”

Generate lead summary

Save JSON file

💾 Data Persistence

All collected lead information is stored in:

backend/leads/lead_data.json


Format includes:

Name

Company

Email

Role

Use case

Team size

Timeline

🔗 External Integrations

You can integrate:

LiveKit (voice agent)

Deepgram / Google STT

Murf / ElevenLabs TTS

Optional CRM integration (HubSpot, Zoho — if added later)

(Current README covers only your provided requirements.)

🧱 Tech Stack

Backend: Python

Voice: LiveKit Agents

STT/TTS: Deepgram, Google, Murf Falcon (optional)

Storage: JSON

NLP: Simple keyword search for FAQ

Frontend: Any client or LiveKit UI (if added)

🎤 Example User Flow

Agent: Hi there, welcome! What brings you here today?
User: I want to know your pricing.
Agent: (Finds pricing info in FAQ → answers)

Agent: Great! Can I know your name so I can help you better?
User: I’m Rohan.

Agent: Sure Rohan. What company are you with?
→ Continues collecting email, role, use case, team size, timeline

User: That’s all for now.
Agent: Thanks! Here is a quick summary of your requirements…
→ Saves JSON file

📝 JSON Entry Structure
{
  "name": "Rohan",
  "company": "TechLabs",
  "email": "rohan@example.com",
  "role": "Product Manager",
  "use_case": "Integrating AI voice support",
  "team_size": "12",
  "timeline": "soon",
  "summary": "Rohan from TechLabs wants AI voice support…"
}

🧠 Advice / Output Logic

FAQ answers come strictly from the provided FAQ text

Keyword-based matching (e.g., “pricing”, “cost”, “features”)

Does NOT generate info outside provided content

Lead questions asked only if field is not yet stored

Natural transitions between answers and questions

End-of-call detection based on stop phrases

⚙️ Setup Instructions
🔧 Backend Setup
cd Day_5/backend
uv sync
cp .env.example .env.local


Add API keys:

LIVEKIT_URL

LIVEKIT_API_KEY

LIVEKIT_API_SECRET

STT/TTS provider keys

Run agent:

uv run python src/agent.py dev

💻 Frontend Setup (if included)
cd Day_5/frontend
pnpm install
cp .env.example .env.local
pnpm dev

🔑 Third Party Services

Configure in .env.local:

LiveKit credentials

STT API keys (Deepgram/Google)

TTS API keys (Murf/ElevenLabs)

✅ MVP Completion Checklist

You are done when:

✔ Agent behaves like an SDR
✔ Answers product/company/pricing FAQs
✔ Collects & stores lead details
✔ Generates end-of-call summary
✔ Saves everything in JSON
