from parsing import Command
from build_world import World
from player import Player
from items import Item

def handle_go(c: Command):
    global scope
    if c.target in player.position.neighbours:
        player.move(player.position.neighbours[c.target])
        scope = update_scope()
    else:
        print(f"You can't go to the {c.target} from here.")

def handle_open(c: Command):
    global scope
    if c.subject == "inventory" or c.target == "inventory":
        player.open_inventory()
    elif (c.subject, "c") in scope:
        player.position.containers[c.subject].open()
        scope = update_scope(list(player.position.containers[c.subject].contents.keys()))
    else:
        print("You can't open that.")

def handle_take(c: Command):
    global scope
    if (c.subject, "i") in scope:
        item_tuple = world.global_items[c.subject]
        player.take(item_tuple[0])
        print(f"you took the {c.subject}.")

        if player.position.name == [item_tuple[1]]:
            player.position.items.pop(c.subject, None)
        elif item_tuple[1] in player.position.containers.keys():
            player.position.containers[item_tuple[1]].contents.pop(c.subject, None)

        scope = update_scope()
    else:
        print("You can't take that.")
            
command_handlers = {
    "go": handle_go,
    "open": handle_open,
    "take": handle_take
}

def handle_input():
    print("> ", end="")
    move = input()
    if move.lower() in ("quit", "exit"):
        print("Goodbye!")
        exit()

    c = Command(move)
    handler = command_handlers[c.action]
    handler(c)

def describe():
    print(f"You are in the {player.position.name}.")
    player.position.describe()

def update_scope(new_items = []):
    locations_in_scope = [(neighbour, "l") for neighbour in player.position.neighbours.keys()]
    items_in_scope = [(item, "i") for item in player.position.items.keys()] + [(item, "i") for item in new_items]
    containers_in_scope = [(container, "c") for container in player.position.containers.keys()]
    return locations_in_scope + items_in_scope + containers_in_scope

def game_loop():
    while True:
        global scope
        describe()
        #print(scope)

        print()
        try:
            handle_input()
        except(SystemExit): raise
        except:
            print("You can't do that.")
            raise
        print()

def main():
    global player, world, scope
    world = World("world.json")
    player = Player(world.entrypoint)
    scope = update_scope()

    actions = list(command_handlers.keys())
    print(f"Actions: {', '.join(actions[:-1])}, and {actions[-1]}. \n")

    game_loop()

if __name__ == "__main__":
    main()