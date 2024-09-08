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

def screen2():
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

screen_seq = [screen1, screen2]

'''BACK-END COMPONENTS BELOW'''

server = None

generic_moves = {

    "attack":10,
    "charge":10,
    "crit":None

}

user_dict = {

    "name":None,
    "fruit_name":None,
    "fruit_dict":None,
    "button":None,
    "loading":None

}

# HOST Functions

def host_server(username, port): # FIXME: unknown causes loading ball and screen glitch
    '''
    Function: Creates a server for the host after receiving the username, port, and fruit.
    Activated by: screen1's host button widget.
    Followed by: Input check, server creation, pickled data, screen2 function to wait for joining player and for host to accept.
    Parameters: username and port (obtained by respective inputfields)
    '''

    print('host_server has been called')

    global user_dict, server

    if input_check(username, port, user_dict, curr_widgets[6], curr_widgets[7], curr_widgets[9]) == False:

        user_dict["loading"] = "joining player."

        user_dict["name"] = username 
        sent_username = pickle.dumps(username) # gets ready to send username
    
        sent_fruitname = pickle.dumps(user_dict["fruit_name"]) # gets ready to send fruitname and transplants fruit stats
        user_dict["fruit_dict"] = copy.copy(generic_moves)

        next_screen(0)

        print('UI blocked by socket')

        curr_widgets[1].configure(text="waiting for joining player")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((socket.gethostname(), int(port)))
        server.listen(1)
        #server.setblocking(False)
        


        #try:

        clientsocket, address = server.accept()

        #except BlockingIOError:

        curr_widgets[1].configure(text="connected to joining player")

        '''else:

            recv_pickle_user = clientsocket.recv(200)
            recv_pickle_fruit = clientsocket.recv(200)
            recv_username = pickle.loads(recv_pickle_user)
            recv_fruit = pickle.loads(recv_pickle_fruit)
            clientsocket.sendall(sent_username)
            clientsocket.sendall(sent_fruitname)

            curr_widgets[1].configure(text=f"user {recv_username} wants to join! do you accept?")'''       

def close_program(server):

    print('close_program has been called')

    if server == None:

        root.destroy()

    else:

        server.close()
        root.destroy

# JOIN Functions

def join_server(username, port): # FIXME: try statement causes loading ball and screen glitch.
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

        next_screen(0)

        searching = True

        #while searching:
            
        #try: # somehow fucks up everything
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((socket.gethostname(), int(port)))
        #except ConnectionRefusedError:

        searching = False               

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

'''TESTING CODE'''

screen_seq[0]()

root.mainloop()