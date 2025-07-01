from items import Item
from collections import defaultdict
import json

class Container:
    def __init__(self, name):
        self.name = name
        self.contents = defaultdict(list)

    def open(self):
        if not self.contents:
            print(f"This {self.name} is empty.")
        else:
            item_count = defaultdict(int)
            for item in self.contents.keys():
                item_count[item] = len(self.contents[item])
            print(f"This {self.name} contains:")
            for item, count in item_count.items():
                print(f"- {item}{f' x{count}' if count > 1 else ""}")

class Gateway:
    def __init__(self, type, location_1, location_2, locked):
        self.type = type
        self.location_1 = location_1
        self.location_2 = location_2
        self.locked = locked

class Location:
    def __init__(self, name):
        self.name = name
        self.neighbours = defaultdict(Location)
        self.items = defaultdict(Item)
        self.containers = defaultdict(Container)
        self.gateways = []

    def __repr__(self):
        return f"location({self.name})"
    
    def describe(self):
        names = [f"the {name}" for name in self.neighbours.keys()]
        
        if len(names) == 1:
            print(f"You see {names[0]}.")
        else:
            print(f"You see {', '.join(names[:-1])}, and {names[-1]}.")
        
        objects = list(self.items.keys()) + list(self.containers.keys())
        if not objects:
            return
        elif len(objects) == 1:
            print(f"There is a {objects[0]}.")
        else:
            print(f"There is a {', a '.join(objects[:-1])}, and a {objects[-1]}.")

class World:
    def __init__(self, world_file):
        self.locations = defaultdict(Location)
        self.global_items = {}
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
            if loc_data.get("items", False):
                name = loc_data["name"]
                for item in loc_data["items"]:
                    i = Item(item)
                    self.locations[name].items[item] = i
                    self.global_items[item] = (i, name)

        for loc_data in data["locations"]:
            if "containers" in loc_data:
                name = loc_data["name"]
                for container_dict in loc_data["containers"]:
                    for container_name, items in container_dict.items():
                        self.locations[name].containers[container_name] = Container(container_name)
                        for item in items:
                            i = Item(item)
                            self.locations[name].containers[container_name].contents[item].append(i)
                            self.global_items[item] = (i, container_name)

        for loc_data in data["gateways"]:
            type = loc_data["type"]
            loc1 = loc_data["location_1"]
            loc2 = loc_data["location_2"]
            locked = False
            if loc_data.get("locked", False):
                locked = loc_data["locked"]

            gate = Gateway(type, loc1, loc2, locked)
            self.locations[loc1].gateways.append(gate)
            self.locations[loc2].gateways.append(gate)

        for loc_data in data["locations"]:
            if loc_data.get("entrypoint", False):
                return self.locations[loc_data["name"]]

        return next(iter(self.locations.values()))

