import json

class Location:
    def __init__(self, name):
        self.name = name
        self.neighbours = {}

    def __repr__(self):
        return f"location({self.name})"
    
    def describe(self):
        if not self.neighbours:
            return "You see nothing nearby."
        
        names = [f"the {name}" for name in self.neighbours.keys()]
        
        if len(names) == 1:
            return f"You see {names[0]}."
        else:
            return f"You see {', '.join(names[:-1])}, and {names[-1]}."

class World:
    def __init__(self, world_file):
        self.locations = {}
        self.entrypoint = self.generate(world_file)

    def generate(self, worldfile):
        with open(worldfile, 'r') as f:
            data = json.load(f)

        for loc_data in data["locations"]:
            name = loc_data["name"]
            self.locations[name] = Location(name)

        for loc_data in data["locations"]:
            loc = self.locations[loc_data["name"]]
            for n_name in loc_data["neighbours"]:
                loc.neighbours[n_name] = self.locations[n_name]

        for loc_data in data["locations"]:
            if loc_data.get("entrypoint", False):
                return self.locations[loc_data["name"]]

        return next(iter(self.locations.values()))

