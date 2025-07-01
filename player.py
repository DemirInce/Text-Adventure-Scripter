from collections import defaultdict
from build_world import Location
from build_world import Container
from build_world import Gateway
from items import Item

class Player:
    def __init__(self, position: Location):
        self.position = position
        self.inventory = Container("inventory")

    def move(self, new_position):
        for gate in self.position.gateways:
            if (new_position.name == gate.location_1 or new_position.name == gate.location_2) and gate.locked:
                if self.inventory.contents[f"{new_position.name} key"]:
                    gate.locked = False
                    self.position = new_position
                    print(f"You opened the door with the {new_position.name} key.")
                    self.inventory.contents.pop(f"{new_position.name} key", None)
                else:
                    print(f"The door to the {new_position.name} is locked.")

                return()
        else:            
            self.position = new_position 

    def take(self, item: Item):
        self.inventory.contents[item.name].append(item)

    def open_inventory(self):
        if not self.inventory.contents:
            print("Your inventory is empty.")
        else:
            item_count = defaultdict(int)
            for item in self.inventory.contents.keys():
                item_count[item] = len(self.inventory.contents[item])
            print("You are carrying:")
            for item, count in item_count.items():
                print(f"- {item}{f' x{count}' if count > 1 else ""}")