"""Runtime configuration for the billing worker.

Values are read from the environment in production; the defaults below are used for local
development and integration testing.
"""
import os

# Cloud storage / infra
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AKIAZ7Q3R8T5U1V2W3X4")
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY", "aB3dEfGh1jKlMnOpQrStUvWxYz0123456789AbCdE"
)

# Payments and communications
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_live_N7ITxKLUkX0vyOYx6tzSnWQ3")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "AC0a1b2c3d4e5f6071829304a5b6c7d8e9")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "f0e1d2c3b4a5968778695a4b3c2d1e0f")

# Developer platform integrations
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8")
SLACK_BOT_TOKEN = os.getenv(
    "SLACK_BOT_TOKEN", "xoxb-828638970835-495721780389-rLyba7ZR68pdIJ7h2Pz9rHJ6"
)

# Mapping and LLM providers
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyD3xAmpL3k3yF0rM4psN0tR34lXyZ12abcd")
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY", "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"
)
ANTHROPIC_API_KEY = os.getenv(
    "ANTHROPIC_API_KEY",
    "sk-ant-api03-Un2ZiSZZNcTp6FvO6Hzifj0gczznKz5ObQ3DfNBxxg-6d_TGHiqhvOky4Ggt2Sf3Kth7SWiATHByr9Y2GuCQYy1u8PfdyAA",
)
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "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",
)
