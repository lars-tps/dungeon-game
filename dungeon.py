import os
import random


# this function generates the coordinates for the map, and contains values to be used in display_map function
def generate_map(width, height):
    """
    This function takes two integers as the 'width' and 'height' for the dungeon
    :param width: takes integer for x dimension
    :param height: takes integer for y dimension
    :return: a dictionary containing the generated coordinates, height, width, and their respective ranges
    """
    coordinates = [(x, y) for y in range(height) for x in range(width)]
    height_range = range(height)
    width_range = range(width)
    return ({"coordinates": coordinates,
             "height_range": height_range,
             "width_range": width_range,
             "height": height,
             "width": width})


# this function gets 3 random coordinates from map_dict
def random_coordinates(generated_dict):
    """Takes the 'coordinates' key in a dictionary and returns 3 random coordinates"""
    return random.sample(generated_dict["coordinates"], 3)


# this function displays the map to the user, x is map dictionary
def display_map(generated_dict):
    width = generated_dict["width"]
    coordinates = generated_dict["coordinates"]
    print(" _"*width)
    tile = "|{}"

    for cell in coordinates:
        x, y = cell
        if x < (width - 1):
            line_end = ""
            if cell == player:
                output = tile.format("X")
            else:
                output = tile.format("_")
        else:
            line_end = "\n"
            if cell == player:
                output = tile.format("X|")
            else:
                output = tile.format("_|")
        print(output, end=line_end)


# check movement prompt for invalid inputs
def check_input(x):
    x = x.upper()
    possibilities = {"UP", "DOWN", "LEFT", "RIGHT", "QUIT"}
    while True:
        if len({x} & possibilities) != 1:
            print("Invalid input! Please try again.")
            x = input(">  ").upper()
            continue
        if len({x} & possibilities) == 1:
            break
    return x


# move player, except invalid moves (past edges, etc)
def move_player(movement):
    global player
    global map_dict
    x, y = player
    previous_position = player
    coordinates = map_dict["coordinates"]
    possibilities = set()
    for point in coordinates:
        possibilities.add(point)

    if movement == "RIGHT":
        x += 1
        player = (x, y)
    elif movement == "LEFT":
        x -= 1
        player = (x, y)
    elif movement == "UP":
        y -= 1
        player = (x, y)
    elif movement == "DOWN":
        y += 1
        player = (x, y)
    while True:
        if len({player} & possibilities) != 1:
            player = previous_position
            continue
        elif len({player} & possibilities) == 1:
            break
    return player


# clear screen and redraw grid
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def game_loop():
    while True:
        print("You are currently in room {}".format(player))
        print("Enter 'QUIT' to quit")
        print("Enter 'LEFT', 'RIGHT', 'UP', 'DOWN' to move.")
        display_map(map_dict)
        move = check_input(input(">  "))
        if move == "QUIT":
            print("Player abandoned the dungeon")
            break
        move_player(move)
        clear_screen()
        display_map(map_dict)
        print("You are now in {}".format(player))
        while (player != door) and (player != monster):
            move = check_input(input(">  "))
            move_player(move)
            if move == "QUIT":
                print("Player abandoned the dungeon")
                break
            display_map(map_dict)
            print("You are now in {}".format(player))
        if player == door:
            print("You found the door!")
        if player == monster:
            print("You are slain by the monster!")
        break


def yes_or_no(prompt):
    """
    Prompts user for 'y' or 'n'
    if neither, prompts user again for 'y' or 'n'
    """
    user_input = str(input(prompt))
    while user_input.lower() != "y" and user_input.lower() != "n":
        print("**Error!**\nPlease only enter 'Y' or 'N'\n")
        user_input = str(input(prompt))
    return user_input


if __name__ == '__main__':
    n_column = int(input("Please enter a value for the Y dimension\nrecommendation: 3 to 5\n>  "))
    n_row = int(input("Please enter a value for the X dimension\nrecommendation: 3 to 5\n>  "))
    map_dict = generate_map(n_row, n_column)
    player, door, monster = random_coordinates(map_dict)
    print("Welcome to the dungeon!")
    input("press ENTER to start")
    clear_screen()
    while True:
        game_loop()
        again = yes_or_no("Do you want to play again?\n(Y/N)")
        if again.lower() == "y":
            player, door, monster = random_coordinates(map_dict)
            continue
        elif again.lower() == "n":
            print("Thanks for playing!")
            break
