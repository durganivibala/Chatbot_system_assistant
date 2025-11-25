from collections import deque
from sentence_transformers import SentenceTransformer, util
import os
import json
from embedder import get_embedder


class ChatMemory:
    def __init__(self, max_turns=50, persist_dir="memory_sessions"):
        self.max_turns = max_turns
        self.history = deque(maxlen=max_turns)  # each item: {"user":..., "bot":..., "embedding":...}
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.embedder = get_embedder()   # reuse same BGE-large model

    def add(self, user_text: str, bot_text: str):
        """Add a new conversation turn and cache its embedding (based on combined turn)."""
        combined = f"User: {user_text}\nAssistant: {bot_text}"
        emb = self.embedder.encode(combined)
        self.history.append({"user": user_text, "bot": bot_text, "embedding": emb.tolist()})

    def clear(self):
        self.history.clear()

    def list_all(self):
        return list(self.history)

    def save_session(self, session_id: str):
        path = os.path.join(self.persist_dir, f"{session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.list_all(), f, ensure_ascii=False, indent=2)

    def load_session(self, session_id: str):
        path = os.path.join(self.persist_dir, f"{session_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
                self.history = deque(items, maxlen=self.max_turns)

    def get_relevant(self, query: str, top_k: int = 3, threshold: float = 0.55):
        """Return up to top_k relevant turns (most recent first) where similarity > threshold."""
        if not self.history:
            return []

        q_emb = self.embedder.encode(query)
        sims = []
        for idx, turn in enumerate(self.history):
            # turn['embedding'] is a list if persisted; convert
            emb = turn["embedding"]
            score = util.cos_sim(q_emb, emb)[0][0].item()
            sims.append((score, idx, turn))

        # sort by score desc, tie-breaker by recency (higher idx)
        sims_sorted = sorted(sims, key=lambda x: (x[0], x[1]), reverse=True)
        filtered = [t for s, i, t in sims_sorted if s >= threshold]
        return filtered[:top_k]

    def format_for_prompt(self, turns):
        """Format a list of turns into a string to include in the LLM prompt."""
        if not turns:
            return ""
        lines = []
        # keep order: oldest -> newest for context coherence
        for t in turns[::-1]:
            lines.append(f"User: {t['user']}\nAssistant: {t['bot']}")
        return "\n\n".join(lines)
