from parsing import Command
from build_world import World
from build_world import Location

class entity:
    def __init__(self, position: Location):
        self.position = position

    def move(self, new_position):
        self.position = new_position    

def handle_go(c):
    if c.target in player.position.neighbours:
        player.move(player.position.neighbours[c.target])
    else:
        print(f"You can't go to the {c.target} from here.")

command_handlers = {
    "go": handle_go,
}

def describe():
    print(f"You are in the {player.position.name}.")
    print(player.position.describe())

def handle_input():
    print("> ", end="")
    move = input()
    if move.lower() in ("quit", "exit"):
        print("Goodbye!")
        exit()

    c = Command(move)
    handler = command_handlers[c.action]
    handler(c)

def game_loop():
    while True:
        describe()

        try:
            handle_input()
        except:
            print("You can't do that.")

def main():
    global player, world
    world = World("world.json")
    player = entity(world.entrypoint)
    print(f"To Move: 'go to [location]")

    game_loop()

if __name__ == "__main__":
    main()