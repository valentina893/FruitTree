from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('800x600')

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

exit_button = Button(root, text="exit", command=root.quit)
exit_button.grid(row=4, column=4, sticky="e, s")

def next(pos):
    '''
    Function: goes to the correct next screen in sequence.
    '''

    screen_seq[pos+1]()

def back(pos):
    '''
    Function: goes to previous screen in sequence.
    '''

    screen_seq[pos-1]()

def exit_fight():

    screen_seq[0]()

def color(new):

    for i in curr_widgets[9:15]:

        i.configure(fg="black")
        root.update_idletasks
    
    new.configure(fg="green")

def screen0(): # TEMPORARILY UNUSED
    '''
    Function: Chooses amount of players.
    Includes: Label, singleButton, multiButton
    '''

    if len(curr_widgets) > 0:

        for i in curr_widgets:

            i.grid_forget()
        
        curr_widgets.clear()

    title = Label(root, text="FruitTree", font=('TkDefaultFont', 30),fg='yellow')
    text = Label(root, text="single or multiplayer?")
    button1 = Button(root, text="single", command=None)
    button2 = Button(root, text="multi", command=lambda: next(0))

    curr_widgets.append(text)
    curr_widgets.append(button1)
    curr_widgets.append(button2)

    title.grid(row=0, column=2)
    text.grid(row=1,column=2)
    button1.grid(row=2,column=1)
    button2.grid(row=2,column=3)

def screen1():
    '''
    Function: First Multiplayer Screen. Creates username, port, and chooses fruit. Host and Join buttons appear to respectively host or join server.
    Includes: Title, username:(Label) & port:(Label), InputField1 & InputField2, Host & Join, emptyError1 & emptyError2, apple, mango, lemon, strawberry, banana, orange, fruit_container, fruit_error
    '''

    if len(curr_widgets) > 0:

        for i in curr_widgets:

            i.destroy()

        curr_widgets.clear()

    title = Label(root, text="FruitTree", font=('TkDefaultFont', 30),fg='yellow')
    label1 = Label(root, text="username:")
    inputfield1 = Entry(root)
    label2 = Label(root, text="port:")
    inputfield2 = Entry(root)
    host = Button(root, text="host", command=lambda: next(0))
    join = Button(root, text="join", command=lambda: next(0))
    empty1 = Label(root, font=('TkDefaultFont', 8), text="*max 10 chars*\nfor username")
    empty2 = Label(root, font=('TkDefaultFont', 8), text="*use 4-digit*\nnumber")
    char_container = LabelFrame(root, text="fruits:")
    apple = Button(char_container, text="apple",command=lambda: color(apple)) # needs to revert back to white if another button is also pressed afterward,
    mango = Button(char_container, text="mango", command=lambda: color(mango))
    lemon = Button(char_container, text="lemon", command=lambda: color(lemon))
    strawberry = Button(char_container, text="strawberry", command=lambda: color(strawberry))
    banana = Button(char_container, text="banana", command=lambda: color(banana))
    orange = Button(char_container, text="orange", command=lambda: color(orange))
    empty3 = Label(root, text="*please choose fruit*", font=('TkDefaultFont', 8))
    #fruit_label = Label(root, text="fruit:")

    title.grid(row=0, column=2)
    label1.grid(row=1, column=1, sticky="e")
    inputfield1.grid(row=1, column=2)
    label2.grid(row=2,column=1, sticky="e")
    inputfield2.grid(row=2,column=2)
    host.grid(row=3, column=4, pady=4)
    join.grid(row=3,column=4, sticky="s")
    empty1.grid(row=1, column=3, sticky="w")
    empty2.grid(row=2, column=3, sticky="w")
    empty3.grid(row=4,column=2, sticky="n")
    #apple.grid(row=3,column=1, sticky="e, s")
    #mango.grid(row=3,column=2, sticky="s")
    #lemon.grid(row=3,column=3, sticky="w, s")
    #strawberry.grid(row=4,column=1, sticky="e, n")
    #banana.grid(row=4,column=2, sticky="n")
    #orange.grid(row=4,column=3, sticky="w, n")
    #fruit_label.grid(row=3,column=0, sticky="e, s")

    char_container.grid(row=3,column=1, columnspan=3)
    apple.grid(row=0,column=0, padx=5, pady=5)
    mango.grid(row=0,column=1, padx=5, pady=5)
    lemon.grid(row=0,column=2, padx=5, pady=5)
    strawberry.grid(row=1,column=0, padx=5, pady=5)
    banana.grid(row=1,column=1, padx=5, pady=5)
    orange.grid(row=1,column=2, padx=5, pady=5)

    root.update_idletasks()

    curr_widgets.append(title)
    curr_widgets.append(label1)
    curr_widgets.append(inputfield1)
    curr_widgets.append(label2)
    curr_widgets.append(inputfield2)
    curr_widgets.append(host)
    curr_widgets.append(join)
    curr_widgets.append(empty1)
    curr_widgets.append(empty2)
    curr_widgets.append(apple)
    curr_widgets.append(mango)
    curr_widgets.append(lemon)
    curr_widgets.append(strawberry)
    curr_widgets.append(banana)
    curr_widgets.append(orange)
    curr_widgets.append(char_container)
    curr_widgets.append(empty3)
    #curr_widgets.append(fruit_label)

def screen2():
    '''
    Function: Loading screen. Greets player and asks to wait for either the host or joining player.
    Includes: Label, dependent label, green light, dummy_next
    '''
    for i in curr_widgets[1:]:

        i.destroy()
        curr_widgets.remove(i)
    
    greet = Label(root, text="hello, user\nplease wait for host/joining player")
    green_light = Label(root, text="connected to other user")
    back_button = Button(root, text="back", command=lambda: back(1))
    dummy = Button(root, text="next", command=lambda: next(1))

    greet.grid(row=1,column=2)
    green_light.grid(row=2,column=2)
    back_button.grid(row=4, column=0, sticky="w,s")
    dummy.grid(row=3,column=2)

    root.update_idletasks()

    curr_widgets.append(greet)
    curr_widgets.append(green_light)
    curr_widgets.append(back_button)
    curr_widgets.append(dummy)

def screen3():
    '''
    Function: displays full battle screen with moves for user and enemy user, fruit, and hp
    inclues: 
        - User: surrounding frame, character_name, hp, attack, charge, quit_fight
        - Enemy: surrounding frame, username, character_name, hp
        - misc: status_message
    '''

    for i in curr_widgets:

        i.destroy()

    curr_widgets.clear()

    user_frame = LabelFrame(root, text="your character:") # user based widgets
    user_hp = ttk.Progressbar(user_frame, orient='horizontal', mode='determinate', length=150, value=100)
    attack = Button(user_frame, text="attack", fg="blue", command=None)
    charge = Button(user_frame, text="charge", fg="red", command=None)
    quit_fight = Button(root, text="quit fight", command=lambda: exit_fight())
    message = Label(root, text="this will display status messages during game.", font = ("TkDefaultFont", 20))

    enemy_title = Label(root, text="enemy's fruit:", font=("TkDefaultFont", 15)) # enemy based widgets
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

curr_widgets = []

screen_seq = [screen1, screen2, screen3]

selected_character = None

screen_seq[0]()

root.mainloop()