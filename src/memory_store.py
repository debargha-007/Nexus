# ------- // Long-term memory for the User preferences // ------ #
import json
import os
from typing import List
from .state import UserProfile

MEM_FILE = "user_long_term_memory.json"


class MemoryStore:
    """
    A simple persistent storage for Long-Term User Memory.
    In production, replace JSON file with a Vector DB (Pinecone/Weaviate) or Postgres.
    """

    @staticmethod
    def load_profile() -> UserProfile:
        if not os.path.exists(MEM_FILE):
            return UserProfile()

        try:
            with open(MEM_FILE, "r") as f:
                data = json.load(f)
            return UserProfile(**data)
        except Exception:
            return UserProfile()

    @staticmethod
    def update_profile(new_preference: str):
        profile = MemoryStore.load_profile()
        if new_preference not in profile.preferences:
            profile.preferences.append(new_preference)
            MemoryStore.save_profile(profile)

    @staticmethod
    def save_profile(profile: UserProfile):
        with open(MEM_FILE, "w") as f:
            json.dump(profile.model_dump(), f, indent=2)

    @staticmethod
    def set_tone(tone: str):
        profile = MemoryStore.load_profile()
        profile.tone_preference = tone  # Set the tone preference
        MemoryStore.save_profile(profile)
