from collections import deque

class ChatMemory:
    def __init__(self, max_turns=10):
        self.history = deque(maxlen=max_turns)
    
    def add(self, user, bot):
        self.history.append((user, bot))
    
    def get_formatted(self):
        return "\n".join([f"User: {u}\nAssistant: {b}" for u, b in self.history])
    
    def clear(self):
        self.history.clear()
