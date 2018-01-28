class Player:
    def __init__(self, full_name: str = "Unknown"):
        self.name = full_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Player: \"%s\">" % self.name
