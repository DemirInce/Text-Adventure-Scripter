VERBS = {
    "go", "look", "take", "drop", "use", "open", "close", "talk", "give",
    "read", "push", "pull", "unlock", "lock", "examine"
}

DIRECTIONS = {
    "north", "south", "east", "west", "up", "down"
}

PREPOSITIONS = {
    "on", "with", "to", "in", "into", "at", "from", "under", "by"
}

FILLER_WORDS = {
    "the", "a", "an", "please", "then", "and"
}

class Command:
    def __init__(self, input: str):
        self.raw = input
        self.action, self.subject, self.preposition, self.target = self.parse(input)

    def tokenzie(self, input: str) -> list:
        words = input.strip().lower().split()
        return [w for w in words if w not in FILLER_WORDS]

    def parse(self, input: str) -> tuple:
        tokens = self.tokenzie(input)

        if not tokens:
            return None, None, None, None

        action = tokens[0] if tokens[0] in VERBS else None
        if not action:
            return None, None, None, None

        tokens = tokens[1:]

        prep_index = -1
        for i, token in enumerate(tokens):
            if token in PREPOSITIONS:
                prep_index = i
                break

        if prep_index != -1:
            subject = " ".join(tokens[:prep_index]) if prep_index > 0 else None
            preposition = tokens[prep_index]
            target = " ".join(tokens[prep_index + 1:]) if prep_index + 1 < len(tokens) else None
        else:
            subject = " ".join(tokens) if tokens else None
            preposition = None
            target = None

        return action, subject, preposition, target
    
    def print(self):
        print(f"Raw: {self.raw}\nAction: {self.action}\nSubject: {self.subject}\nPrep: {self.preposition}\nTarget: {self.target}")

if __name__=="__main__": 
    Command("go to the kitchen").print()

