from dotenv import load_dotenv
import os

# load .env.local explicitly
load_dotenv('.env.local')

print("FROM .env.local LIVEKIT_URL =", os.getenv("LIVEKIT_URL"))
print("FROM .env.local LIVEKIT_API_KEY =", os.getenv("LIVEKIT_API_KEY"))
print("FROM .env.local LIVEKIT_API_SECRET =", os.getenv("LIVEKIT_API_SECRET"))
