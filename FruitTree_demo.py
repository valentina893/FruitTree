import socket, pickle, time, random, copy
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('800x600')
root.title("FruitTree")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

exit_button = Button(root, text="exit", command=lambda: close_program(server))
exit_button.grid(row=4, column=4, sticky="e, s")

title = Label(root, text="FruitTree", font=('TkDefaultFont', 30),fg='yellow')
title.grid(row=0, column=2)

'''FRONT-END COMPONENTS BELOW'''

curr_widgets = []

# FRONT END FUNCTIONS BELOW

def next_screen(pos):
    '''
    Function: switches UI to next visual screen function in a sequence of 1 -> 2 -> 3. NOT to be confused with a future quit_fight function that goes from 3 -> 1.
    '''

    print('next_screen has been called')

    for i in curr_widgets:

        i.destroy()

    curr_widgets.clear()

    screen_seq[pos+1]()

def prev_screen(pos):
    '''
    Function: switches UI to next visual screen function in a sequence of 2 -> 1. NOT to be confused with quit_fight function.
    '''

    print('prev_screen has been called')

    for i in curr_widgets:

        i.destroy()
    
    curr_widgets.clear()

    screen_seq[pos-1]()

def screen1():
    '''
    Function: First Multiplayer Screen. Creates username, port, and chooses fruit.
    Appearance: Title, Username Label, Port Label, Fruit Container, Fruit Buttons, Username Input, Port Input, Host & Join Button, Errors for all input methods
    Host and Join buttons: tied to backend socket/game logic functions.
    Fruit Buttons: tied fruit_button function that assigns data to user_dict.
    '''

    print('screen1 has been called')

    usernameLabel = Label(root, text="username:")
    usernameInput = Entry(root)
    portLabel = Label(root, text="port:")
    portInput = Entry(root)
    hostButton = Button(root, text="host", command=lambda: host_server(usernameInput.get(), portInput.get()))
    joinButton = Button(root, text="join", command=lambda: join_server(usernameInput.get(), portInput.get()))
    usernameError = Label(root, font=('TkDefaultFont', 8), text="")
    portError = Label(root, font=('TkDefaultFont', 8), text="")
    fruitContainer = LabelFrame(root, text="fruits:")
    apple = Button(fruitContainer, text="apple",command=lambda: fruit_buttons(apple, "apple"))
    mango = Button(fruitContainer, text="mango", command=lambda: fruit_buttons(mango, "mango"))
    lemon = Button(fruitContainer, text="lemon", command=lambda: fruit_buttons(lemon, "lemon"))
    strawberry = Button(fruitContainer, text="strawberry", command=lambda: fruit_buttons(strawberry, "strawberry"))
    banana = Button(fruitContainer, text="banana", command=lambda: fruit_buttons(banana, "banana"))
    orange = Button(fruitContainer, text="orange", command=lambda: fruit_buttons(orange, "orange"))
    fruitError = Label(root, text=None, font=('TkDefaultFont', 8))
    connectionHostError = Label(root, text=None, font=('TkDefaultFont', 15))

    usernameLabel.grid(row=1, column=1, sticky="e")
    usernameInput.grid(row=1, column=2)
    portLabel.grid(row=2,column=1, sticky="e")
    portInput.grid(row=2,column=2)
    hostButton.grid(row=3, column=4, pady=4)
    joinButton.grid(row=3,column=4, sticky="s")
    usernameError.grid(row=1, column=3, columnspan=2, sticky="w")
    portError.grid(row=2, column=3, columnspan=2, sticky="w")
    fruitContainer.grid(row=3,column=1, columnspan=3)
    fruitError.grid(row=4,column=2, sticky="n")
    connectionHostError.grid(row=4,column=2,sticky="s")

    apple.grid(row=0,column=0, padx=5, pady=5)
    mango.grid(row=0,column=1, padx=5, pady=5)
    lemon.grid(row=0,column=2, padx=5, pady=5)
    strawberry.grid(row=1,column=0, padx=5, pady=5)
    banana.grid(row=1,column=1, padx=5, pady=5)
    orange.grid(row=1,column=2, padx=5, pady=5)

    root.update_idletasks()

    curr_widgets.append(usernameLabel)
    curr_widgets.append(usernameInput)
    curr_widgets.append(portLabel)
    curr_widgets.append(portInput)
    curr_widgets.append(hostButton)
    curr_widgets.append(joinButton)
    curr_widgets.append(usernameError)
    curr_widgets.append(portError)
    curr_widgets.append(fruitContainer)
    curr_widgets.append(fruitError)
    curr_widgets.append(connectionHostError)

def screen2(): # UNUSED
    '''
    Function: Loading screen while waiting for host or joining player. Will greet user in way dependent on if they are the host or joining player. Allows host to give permission to whoever joins.
    Appearance: Title, Loading_Label, Success_Label, Accept_button, kick_button
    '''

    print('screen2 has been called')

    loading = Label(root, text=f"hello, {user_dict['name']}. please wait for {user_dict['loading']}")
    status = Label(root)
    # accept = Button(root, text="accept", command=None) # host exclusive
    # kick = Button(root, text="kick", command=None) # host exclusive
    back_button = Button(root, text="back", command=lambda: None)

    loading.grid(row=1, column=2)
    status.grid(row=2,column=2)
    back_button.grid(row=4, column=0, sticky="w,s")

    root.update_idletasks()

    curr_widgets.append(loading)
    curr_widgets.append(status)
    curr_widgets.append(back_button)

def screen3():
    '''
    Function: displays full battle screen with moves for user and enemy user, fruit, and hp
    inclues: 
        - User: surrounding frame, character_name, hp, attack, charge, quit_fight
        - Enemy: surrounding frame, username, character_name, hp
        - misc: status_message
    '''

    title.grid_forget()

    user_frame = LabelFrame(root, text=f"{user_dict['fruit_name']}:") # user based widgets
    user_hp = ttk.Progressbar(user_frame, orient='horizontal', mode='determinate', length=150, value=100)
    attack = Button(user_frame, text="attack", fg="blue", command=None)
    charge = Button(user_frame, text="charge", fg="red", command=None)
    quit_fight = Button(root, text="quit fight", command=None)
    message = Label(root, text=f"{enemy_dict['name']} has connected!", font = ("TkDefaultFont", 20))

    enemy_title = Label(root, text=f"{enemy_dict['name']}'s {enemy_dict['fruit_name']}:", font=("TkDefaultFont", 15)) # enemy based widgets
    enemy_hp = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=300, value=100)

    user_frame.grid(row=3, rowspan=2, column=0, columnspan=2)
    user_hp.grid(row=0,column=0,columnspan=2)
    attack.grid(row=1, column=0, padx=10, pady=10)
    charge.grid(row=1, column=1, padx=10, pady=10)
    quit_fight.grid(row=4, column=0, sticky="w, s")
    message.grid(row=2, column=1, columnspan=3)
    enemy_title.grid(row=0, column=3)
    enemy_hp.grid(row=1,column=3, sticky="n")

    root.update_idletasks()

    curr_widgets.append(user_frame)
    curr_widgets.append(user_hp)
    curr_widgets.append(attack)
    curr_widgets.append(charge)
    curr_widgets.append(quit_fight)
    curr_widgets.append(message)
    curr_widgets.append(enemy_title)
    curr_widgets.append(enemy_hp)

    battle_sequence()

screen_seq = [screen1, screen2, screen3]

'''BACK-END COMPONENTS BELOW'''

server = None

generic_moves = {

    "attack":10,
    "charge":10,
    "crit":(1, 5),
    "miss":(1, 8)

}

user_dict = {

    "name":None,
    "fruit_name":None,
    "fruit_dict":None,
    "button":None,
    "loading":None,
    "health":100

}

enemy_dict = {

    "name":None,
    "fruit_name":None,
    "fruit_dict":None,
    "health":100

}

# HOST Functions

def host_server(username, port): # FIXME: way to avoid blocking network search?
    '''
    Function: Creates a server for the host after receiving the username, port, and fruit.
    Activated by: screen1's host button widget.
    Followed by: Input check, server creation, pickled data, screen2 function to wait for joining player and for host to accept.
    Parameters: username and port (obtained by respective inputfields)
    '''

    print('host_server has been called')

    global user_dict, server

    if server != None:

        server = None

    if input_check(username, port, user_dict, curr_widgets[6], curr_widgets[7], curr_widgets[9]) == False:

        curr_widgets[5].configure(command=None)

        user_dict["loading"] = "joining player."

        user_dict["name"] = username 
        sent_username = pickle.dumps(username) # gets ready to send username
    
        sent_fruitname = pickle.dumps(user_dict["fruit_name"]) # gets ready to send fruitname and transplants fruit stats
        user_dict["fruit_dict"] = copy.copy(generic_moves)

        #next_screen(0)

        print('UI blocked by socket')

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((socket.gethostname(), int(port)))
        server.listen(1)
        #server.setblocking(False)

        try:

                clientsocket, address = server.accept()
                print("connection established")
                #server.setblocking(False)
                recv_pickle_user = clientsocket.recv(1024)
                recv_username = pickle.loads(recv_pickle_user)
                clientsocket.sendall(sent_username)
                recv_pickle_fruit = clientsocket.recv(1024)
                recv_fruit = pickle.loads(recv_pickle_fruit)
                clientsocket.sendall(sent_fruitname)
                print(f"{recv_username} has connected!")

        except:
                
                curr_widgets[-1].configure(text="connection error")
                print('server has stopped operating')
                

        #curr_widgets[1].configure(text="waiting for joining player")

        else:


                enemy_dict["name"] = recv_username
                enemy_dict["fruit_name"] = recv_fruit
                enemy_dict["fruit_dict"] = generic_moves

                
                #curr_widgets[1].configure(text=f"{recv_username} has connected")

                next_screen(1)

        '''else:



            curr_widgets[1].configure(text=f"user {recv_username} wants to join! do you accept?")'''       

# JOIN Functions

def join_server(username, port): # FIXME: way to avoid blocking network search?
    '''
    Function: Searches for and joins server after collecting username, port, and fruit.
    Activated by: screen1's join button widget.
    Followed by: Input check, server creation, pickled data, screen2 function to wait for host.
    Parameters: username and port (obtained by respective inputfields)
    '''

    print('join_server has been called')

    global user_dict

    if input_check(username, port, user_dict, curr_widgets[6], curr_widgets[7], curr_widgets[9]) == False:

        user_dict["name"] = username 
        sent_username = pickle.dumps(username) # gets ready to send username

        sent_fruitname = pickle.dumps(user_dict["fruit_name"]) # gets ready to send fruitname and transplants fruit stats
        user_dict["fruit_dict"] = copy.copy(generic_moves)

        user_dict["loading"] = "host."

        #next_screen(0)


        #server.setblocking(False)

        #searching = True

        #while searching:
            
        try:
                
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                server.connect((socket.gethostname(), int(port)))
                print("connected to host")
                #server.setblocking(False)
                server.sendall(sent_username)
                recv_pickle_user = server.recv(1024)
                recv_username = pickle.loads(recv_pickle_user)
                server.sendall(sent_fruitname)
                recv_pickle_fruit = server.recv(1024)
                
                recv_fruit = pickle.loads(recv_pickle_fruit)

        except:

                curr_widgets[-1].configure(text="connection error")
                searching = False

        else:

                enemy_dict["name"] = recv_username
                enemy_dict["fruit_name"] = recv_fruit
                enemy_dict["fruit_dict"] = generic_moves
        
                print(f'host is {recv_username}')
                #curr_widgets[1].configure(text=f"you have connected to {recv_username}")
                next_screen(1)
        #except ConnectionRefusedError:

                #searching = False             

# GENERIC FUNCTIONS

def input_check(username, port, user_dct, error1, error2, error3):
    '''
    Function: Checks if user has entered a valid username, port, and fruit
    Activated by: host/join server functions
    Followed by: rest of host join server functions that will continue if input_check returns True.
    '''

    print('input_check has been called')

    errors = False

    if len(username) <= 10 and len(username) > 0:

        try:

            error1.configure(text="")
        
        except:

            pass

    else:

        try:

            error1.configure(text="*use 1 - 10 chars*\nfor username")

        except:

            pass

        else:

            errors = True

    if len(port) == 4:

        try:

            int(port)
        
        except ValueError:

            error2.configure(text="*use 4-digit*\nnumber")

        else:

            try:

                error2.configure(text="")

            except:

                pass

    else:

        try:

            error2.configure(text="*use 4-digit*\nnumber")
        
        except:

            pass

        else:

            errors = True

    if user_dct[list(user_dct.keys())[2]] != None:

        try:

            error3.configure(text="")
        
        except:

            pass

    else:

        try:

            error3.configure(text="*please choose fruit*")
        
        except:

            pass

        else:

            errors = True
    
    return errors
            
def fruit_buttons(button, fruitname):
    '''
    Function: Sets user-dict to have fruit name and changes UI fruit button colors.
    Activated by: screen1's fruit buttons (each)
    Followed by: host_server function's prep for game
    Parameters: button is the button pressed for activating fruit_buttons, fruit_name is a manual parameter.
    '''

    print('fruit_button has been called')

    if user_dict['fruit_name'] == None:

        button.configure(fg="green")

    else:
        
        try:
            user_dict["button"].configure(fg="black")
        except:
            button.configure(fg="green")
        else:
            button.configure(fg="green")

    user_dict["fruit_name"] = fruitname
    user_dict["fruit_dict"] = copy.copy(generic_moves)
    user_dict["button"] = button

def t1():

    time.sleep(1)

def close_program(server):

    print('close_program has been called')

    if server == None:

        root.destroy()

    else:

        server.close()
        root.destroy()

# BATTLE Functions

def damage_move(move_set):
    '''
    Function: calculates stats of chosen move and formulates into dictionary to send out to client.
    '''

    global generic_moves

    print('damage_move was called')

    final = {

        "miss":None,
        "crit":None,
        "total":0

    }

    miss_chance = random.choice(range(move_set["miss"][0], move_set["miss"][-1]+1))
    if miss_chance != 1:
        final["miss"] = False
        crit_chance = random.choice(range(move_set["crit"][0], move_set["crit"][-1]+1))
        if crit_chance != 1:
            final["crit"] = False
            final["total"] = move_set["attack"]
            print(final)
            return final
        else:
            final["crit"] = True
            final["total"] += move_set["attack"] + 10
            print(final)
            return final
    else:
        final["miss"] = True
        final["total"] = move_set["attack"]
        print(final)
        return final

def user_move():
    '''
    Function: gives functionality to User's UI buttons to make move.
    Activated by the calling of screen3 which calls battle_sequence that has while loop.
    Followed by: recv_move() which listens for what enemy uses and the stats of the move. game stats are then affected.
    '''

    global user_dict, enemy_dict

    print('user_move has been called')

    curr_widgets[5].configure(text="what's your move?")
    curr_widgets[2].configure(command=lambda: damage_move(user_dict["fruit_dict"]))

    pass

def battle_sequence():
    '''
    Function: While loop that continues the battle until either fruit's health is 0 or below.
    '''

    print('battle sequnece has been called')

    battling = True

    while battling:

        user_move()
        battling = False

    pass

'''TESTING CODE'''

screen_seq[0]()

root.mainloop()