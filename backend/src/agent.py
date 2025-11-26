# ======================================================
# 💼 DAY 5: AI SALES DEVELOPMENT REP (SDR)
# 🚀 MegaFlow - Auto-Lead Capture Agent
# Features: FAQ Retrieval, Lead Qualification, JSON Database
# ======================================================

import logging
import json
import os
import asyncio
from datetime import datetime
from typing import Annotated, Literal, Optional, List
from dataclasses import dataclass, asdict

print("\n" + "💼" * 50)
print("🚀 AI SDR AGENT - DAY 5 TUTORIAL")
print("📚 SELLING: MegaFlow — Business Automation SaaS")
print("💡 agent.py LOADED SUCCESSFULLY!")
print("💼" * 50 + "\n")

from dotenv import load_dotenv
from pydantic import Field
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)

# 🔌 PLUGINS (kept same as your environment)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
load_dotenv(".env.local")

# ======================================================
# 📂 1. KNOWLEDGE BASE (FAQ) — MEGAFLOW
# ======================================================

FAQ_FILE = "megaflow_faq.json"
LEADS_FILE = "leads_db.json"

# MegaFlow FAQ content (simple, factual — no hallucinations)
MEGAFLOW_DEFAULT_FAQ = [
    {
        "question": "What does MegaFlow do?",
        "answer": "MegaFlow helps businesses manage inventory, orders, and billing in one place."
    },
    {
        "question": "Do you have a free plan?",
        "answer": "MegaFlow does not have a free plan. Only paid plans."
    },
    {
        "question": "Who is MegaFlow for?",
        "answer": "Small businesses, D2C brands, local sellers, and online shop owners use MegaFlow."
    },
    {
        "question": "How does pricing work?",
        "answer": "Pricing depends on business size and features needed. Please contact sales for a custom quote."
    },
    {
        "question": "What features does MegaFlow offer?",
        "answer": "MegaFlow provides inventory tracking, order management, billing & invoices, reports & analytics, customer record management, and multi-channel order support."
    }
]

def load_knowledge_base():
    """Generates FAQ file if missing, then loads it."""
    try:
        path = os.path.join(os.path.dirname(__file__), FAQ_FILE)
        if not os.path.exists(path):
            with open(path, "w", encoding='utf-8') as f:
                json.dump(MEGAFLOW_DEFAULT_FAQ, f, indent=4)
        with open(path, "r", encoding='utf-8') as f:
            # Return as string (JSON text) to embed into the agent instructions
            return json.dumps(json.load(f))
    except Exception as e:
        print(f"⚠️ Error loading FAQ: {e}")
        return ""

MEGAFLOW_FAQ_TEXT = load_knowledge_base()

# ======================================================
# 💾 2. LEAD DATA STRUCTURE
# ======================================================

@dataclass
class LeadProfile:
    name: str | None = None
    company: str | None = None
    email: str | None = None
    role: str | None = None
    use_case: str | None = None
    team_size: str | None = None
    timeline: str | None = None
   
    def is_qualified(self):
        """Returns True if we have the minimum info (Name + Email + Use Case)"""
        return all([self.name, self.email, self.use_case])

@dataclass
class Userdata:
    lead_profile: LeadProfile

# ======================================================
# 🛠️ 3. SDR TOOLS
# ======================================================

@function_tool
async def update_lead_profile(
    ctx: RunContext[Userdata],
    name: Annotated[Optional[str], Field(description="Customer's name")] = None,
    company: Annotated[Optional[str], Field(description="Customer's company name")] = None,
    email: Annotated[Optional[str], Field(description="Customer's email address")] = None,
    role: Annotated[Optional[str], Field(description="Customer's job title")] = None,
    use_case: Annotated[Optional[str], Field(description="What they want to build or use MegaFlow for")] = None,
    team_size: Annotated[Optional[str], Field(description="Number of people in their team")] = None,
    timeline: Annotated[Optional[str], Field(description="When they want to start (e.g., Now, next month)")] = None,
) -> str:
    """
    ✍️ Captures lead details provided by the user during conversation.
    Only call this when the user explicitly provides information.
    """
    profile = ctx.userdata.lead_profile
   
    # Update only fields that are provided (not None)
    if name: profile.name = name
    if company: profile.company = company
    if email: profile.email = email
    if role: profile.role = role
    if use_case: profile.use_case = use_case
    if team_size: profile.team_size = team_size
    if timeline: profile.timeline = timeline
   
    print(f"📝 UPDATING LEAD: {profile}")
    return "Lead profile updated. Continue the conversation."

@function_tool
async def submit_lead_and_end(
    ctx: RunContext[Userdata],
) -> str:
    """
    💾 Saves the lead to the database and signals the end of the call.
    Call this when the user says goodbye or 'that's all'.
    """
    profile = ctx.userdata.lead_profile
   
    # Save to JSON file (Append mode)
    db_path = os.path.join(os.path.dirname(__file__), LEADS_FILE)
   
    entry = asdict(profile)
    entry["timestamp"] = datetime.now().isoformat()
   
    # Read existing, append, write back (Simple JSON DB)
    existing_data = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r") as f:
                existing_data = json.load(f)
        except: pass
   
    existing_data.append(entry)
   
    with open(db_path, "w") as f:
        json.dump(existing_data, f, indent=4)
       
    print(f"✅ LEAD SAVED TO {LEADS_FILE}")
    # Return a final summary string orientation to MegaFlow
    name = profile.name or "there"
    use_case = profile.use_case or "your requested use case"
    email = profile.email or "the email you provided"
    return f"Lead saved. Summarize the call for the user: 'Thanks {name}, I have your info regarding {use_case}. We will email you at {email}. Goodbye!'"

# ======================================================
# 🧠 4. AGENT DEFINITION
# ======================================================

class SDRAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=f"""
            You are 'Sarah', a friendly and professional Sales Development Rep (SDR) for 'MegaFlow'.
           
            📘 **YOUR KNOWLEDGE BASE (FAQ):**
            {MEGAFLOW_FAQ_TEXT}
           
            🎯 **YOUR GOAL:**
            1. Answer questions about MegaFlow (inventory, orders, billing) using the FAQ.
            2. **QUALIFY THE LEAD:** Naturally ask for the following details during the chat:
               - Name
               - Company / Role
               - Email
               - What are they trying to build or automate? (Use Case)
               - Timeline (When do they need it?)
           
            ⚙️ **BEHAVIOR:**
            - **Be Conversational:** Don't interrogate the user. Answer a question, THEN ask for a detail.
            - *Example:* "MegaFlow helps manage inventory and billing. By the way, how large is your team?"
            - **Capture Data:** Use `update_lead_profile` immediately when the user provides new info.
            - **Closing:** When the user is done, use `submit_lead_and_end`.
           
            🚫 **RESTRICTIONS:**
            - If you don't know an answer, say "I'll check with our team and email you." (Don't hallucinate pricing or capabilities not in the FAQ).
            """,
            tools=[update_lead_profile, submit_lead_and_end],
        )

# ======================================================
# 🎬 ENTRYPOINT (LiveKit worker)
# ======================================================

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    print("\n" + "💼" * 25)
    print("🚀 STARTING MegaFlow SDR SESSION")
   
    # 1. Initialize State
    userdata = Userdata(lead_profile=LeadProfile())

    # 2. Setup Agent session - use your configured plugins
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-natalie", # Professional, warm female voice
            style="Promo",        
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )
   
    # 3. Start
    await session.start(
        agent=SDRAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
