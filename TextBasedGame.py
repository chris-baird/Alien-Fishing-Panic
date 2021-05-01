# Chris Baird

# OS module for setting up console clear
import os


# Detecting what OS user is on
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# State reducer for the game, takes the games state and an action to perform on the state. returns a new copy of the stat if called without arguments
def game_reducer(action=None, game_state=None):
    # Sets up game state if argument is not passed in
    if action is None:
        action = {'type': None}
    if game_state is None:
        # Game state
        game_state = {'game_started': False,
                      'game_over': False,
                      'player_win': False,
                      'player': {'location': {'room_name': 'None', 'x': None, 'y': None}, 'inventory': [],
                                 'selected_command': ''},
                      'items': [{'name': 'Strange Flashing Armor', 'flavor_text': ''},
                                {'name': 'Boots of Cosmic Protection', 'flavor_text': ''},
                                {'name': 'Ring of Metallurgic Power', 'flavor_text': ''},
                                {'name': 'Technological Stick of Beating', 'flavor_text': ''},
                                {'name': 'Improvised Head Protection', 'flavor_text': ''},
                                {'name': 'Cloak of Ultimate Greatness', 'flavor_text': ''},
                                {'name': 'Strange Potion of Alien Rapid Dialect', 'flavor_text': ''}],
                      'valid_moves': ['north', 'south', 'east', 'west'],
                      'boss': {'location': {'x': None, 'y': None}},
                      'output': '',
                      'error': {'type': {'move': False, 'item': False, 'command': False}},
                      # Using a XY coordinate system for the rooms
                      'rooms': [
                          [{'room_name': "Science Lab",
                            'item': {'item_name': 'Boots of Cosmic Protection', 'in_room': True, 'collected': False,
                                     }, 'board_position': (0, 0)},
                           {'room_name': "Engine Room",
                            'item': {'item_name': 'Strange Flashing Armor', 'in_room': True, 'collected': False,
                                     }, 'board_position': (0, 1)},
                           {'room_name': "Supply Closet",
                            'item': {'item_name': 'Ring of Metallurgic Power', 'in_room': True, 'collected': False,
                                     }, 'board_position': (0, 2)}],
                          [{'room_name': "Kitchen",
                            'item': {'item_name': 'Technological Stick of Beating', 'in_room': True, 'collected': False,
                                     }, 'board_position': (1, 0)},
                           {'room_name': "Control Room",
                            'item': {'item_name': 'Improvised Head Protection', 'in_room': True, 'collected': False,
                                     }, 'board_position': (1, 1)},
                           {'room_name': "Weapons Armory",
                            'item': {'item_name': 'Strange Potion of Alien Rapid Dialect', 'in_room': True,
                                     'collected': False,
                                     }, 'board_position': (1, 2)}],
                          [{'room_name': "Captains Quarters",
                            'item': {'item_name': None, 'in_room': False, 'collected': False,
                                     }, 'board_position': (2, 0)},
                           {'room_name': "Landing Bay",
                            'item': {'item_name': 'Cloak of Ultimate Greatness', 'in_room': True, 'collected': False,
                                     }, 'board_position': (2, 1)},
                           {'room_name': "Cargo Hold",
                            'item': {'item_name': None, 'in_room': False, 'collected': False,
                                     }, 'board_position': (2, 2)}]]}
    # Starts the game
    if action['type'] == 'START_GAME':
        state_copy = game_state.copy()
        # Start the game

        state_copy['game_started'] = True

        return state_copy
    # Check if the game should continue or end with a win/lose
    if action['type'] == 'WIN_LOSE_CONTINUE':
        # Player location
        player_location = game_state['player']['location']
        # Boss location
        boss_location = game_state['boss']['location']
        # Creating a copy of the game state to mutate
        state_copy = game_state.copy()
        # If the player moves into the room the boss is located in the game ends with a lose
        if (player_location['x'] == boss_location['x']) and (player_location['y'] == boss_location['y']):
            state_copy['game_over'] = True
            return state_copy
        # If the player collects all 7 items the game ends with a win
        if len(state_copy['player']['inventory']) == 7:
            print(
                'As you collect the last item the boss rushes through the door and shoots at you but your armor protects you! "WHATS THIS? YOU COLLECTED ALL OF MY ITEMS? GAH YOU HAVE BEATEN ME, PLEASE SPARE MY LIFE!" You decide to let the alien live if he promises to stop adubucting fisherman. The day is saved and you are the hero. GAME OVER ')
            return exit()
        # Returning state copy if neither above happens
        return state_copy
    # Moves the player into a new room
    if action['type'] == 'MOVE':

        state_copy = game_state.copy()

        # Players current coordinates
        player_x = state_copy['player']['location']['x']
        player_y = state_copy['player']['location']['y']

        # Up and Down
        x_min = 0
        x_max = 2

        # Left and Right
        y_min = 0
        y_max = 2

        # Getting move direction from player
        move_direction = input('Type North, East, South or West to move to a different room ')

        # Checking if input was a valid move & setting error if true
        if move_direction not in game_state['valid_moves']:
            # state_copy['error']['type']['command'] = True
            print('Invalid Command!')
            return game_reducer({'type': 'MOVE'}, state_copy)
        # Case for North
        if move_direction == 'north':
            # Out of bounds to the north
            if player_x <= x_min:
                print('You can not go that way!')
                return game_reducer({'type': 'MOVE'}, state_copy)
            # Moves the player
            else:
                state_copy['player']['location']['x'] = player_x - 1
                state_copy['player']['location']['room_name'] = state_copy['rooms'][player_x - 1][player_y]['room_name']
        # Case for South
        if move_direction == 'south':
            # Out of bounds to the south
            if player_x >= x_max:
                print('You can not go that way!')
                return game_reducer({'type': 'MOVE'}, state_copy)
            # Moves the player
            else:
                state_copy['player']['location']['x'] = player_x + 1
                state_copy['player']['location']['room_name'] = state_copy['rooms'][player_x + 1][player_y]['room_name']
        # Case for East
        if move_direction == 'east':
            # Out of bounds to the east
            if player_y >= y_max:
                print('You can not go that way!')
                state_copy['error']['command'] = True
                return game_reducer({'type': 'MOVE'}, state_copy)
            # Moves the player
            else:
                state_copy['player']['location']['y'] = player_y + 1
                state_copy['player']['location']['room_name'] = state_copy['rooms'][player_x][player_y + 1]['room_name']
        # Case for West
        if move_direction == 'west':
            # Out of bounds to the west
            if player_y <= y_min:
                print('You can not go that way!')
                state_copy['error']['command'] = True
                return game_reducer({'type': 'MOVE'}, state_copy)
            # Moves the player
            else:
                state_copy['player']['location']['y'] = player_y - 1
                state_copy['player']['location']['room_name'] = state_copy['rooms'][player_x][player_y - 1]['room_name']

        return state_copy
    # Gets the item in the room if one exists
    if action['type'] == 'GET_ITEM':
        state_copy = game_state.copy()
        player_x = state_copy['player']['location']['x']
        player_y = state_copy['player']['location']['y']
        # Checks if item is in room
        if state_copy['rooms'][player_x][player_y]['item']['in_room']:
            # Appends item to players inventory
            state_copy['player']['inventory'].append(state_copy['rooms'][player_x][player_y]['item']['item_name'])
            # Sets the item state to false for the room
            state_copy['rooms'][player_x][player_y]['item']['in_room'] = False
            return state_copy
        # Clears console
        cls()
        print('There are no items in this room')
        return state_copy

    # Gets the player command
    if action['type'] == 'GET_PLAYER_COMMAND':
        player_command = input('TYPE "MOVE" to change rooms or "GET" to pick up an item ')
        # Using recursion to check if the player typed a valid command
        if (player_command != 'move') and (player_command != 'get'):
            return game_reducer({'type': 'GET_PLAYER_COMMAND'}, game_state)

        state_copy = game_state.copy()
        # Sets the game state for player command
        state_copy['player']['selected_command'] = player_command
        return state_copy

    # Runs the players selected command
    if action['type'] == 'RUN_PLAYER_COMMAND':
        state_copy = game_state.copy()
        # Move selected
        if state_copy['player']['selected_command'] == 'move':
            return game_reducer({'type': 'MOVE'}, state_copy)
        # Get selected
        if state_copy['player']['selected_command'] == 'get':
            return game_reducer({'type': 'GET_ITEM'}, state_copy)
        return

    # Spawns the player
    if action['type'] == 'SPAWN_PLAYER':
        # Creating a copy of the game state
        state_copy = game_state.copy()

        # Updates players location in state copy
        state_copy['player']['location']['x'] = 2
        state_copy['player']['location']['y'] = 2

        # Searches for the room by coordinates and assigned the player location named from that from name
        for row in state_copy['rooms']:
            for room in row:
                if room['board_position'][0] == 2 and room['board_position'][1] == 2:
                    state_copy['player']['location']['room_name'] = room['room_name']

                    break

        print('You Awake in the {}'.format(state_copy['player']['location']['room_name']))
        # Returns updated state
        return state_copy
    # Spawns boss
    if action['type'] == 'SPAWN_BOSS':
        state_copy = game_state.copy()
        # Boss spawn coords DEV NOTE this is hard coded for now but will be random one a new bugs are figured out.
        state_copy['boss']['location'] = {
            'x': 2,
            'y': 0
        }

        # Checks if the new boss location is the same as the player and rerolls if they are in the same room
        if (state_copy['player']['location']['x'] == state_copy['boss']['location']['x']) and (
                state_copy['player']['location']['y'] ==
                state_copy['boss']['location']['y']):
            # Using recursing to ensure boss does not spawn in the player room
            return game_reducer({'type': 'SPAWN_BOSS'}, state_copy)
        return state_copy

    if action['type'] == 'RENDER_DISPLAY':
        cls()
        print('You are in the {}'.format(game_state['player']['location']['room_name']))
        print(('inventory {}'.format(game_state['player']['inventory'])))
        return game_state


# Recursive function that check if player want's to play
def start_game():
    command = input('Type play to start or exit to quit ')
    if command == 'exit':
        return False
    if command == 'play':
        return True
    # If neither above commands re runs function to get valid command
    return start_game()


# Set up game function that uses recursion and passes the game state to each task and runs that task
def setup_game(state=game_reducer(), task_index=0, tasks=('START_GAME', 'SPAWN_PLAYER', 'SPAWN_BOSS')):
    # Check if all the tasks have been complete
    if task_index == len(tasks):
        return state
    # Running current task through the game reducer
    updated_state = game_reducer({'type': tasks[task_index]}, state)
    # Recursively calls the setup function with the new state, updated counter and tasks list
    return setup_game(updated_state, task_index + 1, tasks)


# Prints the game intro
def print_intro():
    print(
        'Welcome to Alien Fishing Panic. You were fishing on the great lake Michigan when suddenly a loud hum and bright light appear above. You have been abducted by an alien overlord. Upon waking up, you are in an empty room with multiple exits. The objective is to move from each room collecting each item before encountering the boss.')

    return


# Main loop using recursion, takes in the game state, task index and tasks
def game_loop(state, task_index=0,
              tasks=('GET_PLAYER_COMMAND', 'RUN_PLAYER_COMMAND', 'WIN_LOSE_CONTINUE', 'RENDER_DISPLAY')):
    # Checks if any of the requirements for game-over have been met
    if state['game_over']:
        print('Game Over, You ran into the boss and he blasted you')
        return

    # Checks if all the tasks have been complete and resets the task index
    if task_index == (len(tasks) - 1):
        task_index = -1
    # Using recursion to cycle through all the tasks one at a time passing the new state and tasks to each and incrementing a counter variable
    return game_loop(game_reducer({'type': tasks[task_index]}, state), task_index + 1, tasks)


# Main entry function
def main_menu():
    if start_game():
        print_intro()
        game_loop(setup_game())


# Entry Point
main_menu()
