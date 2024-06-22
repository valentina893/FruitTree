import time, random, copy

def t1():
    time.sleep(1)

def p1_reg_move():

    t1()
    print(p1c_name, ':', p1c_move_list, p1c_dict['stats'][0], p1c_dict['stats'][1])

    u_inp = input().lower()

    if u_inp == p1c_move_list[0]: # regular move
        p1c_dict[p1c_move_list[0]][0] -= 1
        return (p1c_dict[p1c_move_list[0]], p1c_dict)
    else:
        return p1c_dict[p1c_move_list[1]]
    
def en_reg_move():
# should ai be smart enough to not choose useless attacks? --> ai will be stupid for now
    en_inp = random.choice(p2c_move_list)

    p2c_dict[en_inp][0] -= 1
    return (p2c_dict[en_inp], p2c_dict)

def p1_tag_move():

    u_inp = input()

    pass

def en_tag_move():

    pass

def p2_reg_move():

    u_inp = input()

    pass

def p2_tag_move():
    
    u_inp = input()

    pass

def damage(dam, dct):

    dct['stats'][0] -= dam

    return dct

def combat(): # takes player choices as values, flips coin to see who goes first using values, uses functions to manipulate health and stats

    p1 = p1_move()
    p2 = p2_move()

    print('player 1 used', p1[0][-1])
    print('player 2 used', p2[0][-1])

    p2c_dict = damage(p1[0][1], p2[1])

    print('p2 health is', p2c_dict['stats'][0])

mango = { # name : pp, damage, speed-weight, crit, miss, call
           'h':[5, 10, 0.5, (1,6), (1,8), 'regular', 'hit'],
           'm':[5, 0, 0.3, None, None, 'special', 'morph'],
           'stats':[100, 1] # health, power
          }

banana = {
           'k':[5, 10, 0.5, (1,6), (1,8), 'regular', 'kick'],
           's':[5, 20, 0.2, (3,6), (2,8), 'special', 'shoot'],
           'stats':[100, 1]
          }

strawberry = {
            'p':[5, 10, 0.5, (1,6), (1,8), 'regular', 'pound'],
            'x':[5, 0, 0.3, None, None, 'special', 'x'], #healing ability
            'stats':[100, 1]
        }

char_sel = {
            'm':['mango', mango],
            'b':['banana', banana],
            's':['strawberry', strawberry],
           }

g_mode_sel = {
              (1, 'r'):[1, 'regular', p1_reg_move, en_reg_move],
              (1, 't'):[1, 'tag', p1_tag_move, en_tag_move],
              (2, 'r'):[2, 'regular', p1_reg_move, p2_reg_move],
              (2, 't'):[2, 'tag', p1_tag_move, p2_tag_move]
             }

g_mode_choice = (None, None) # holds data of amt of players, game mode
char_choice1 = [] # holds character data for player 1
char_choice2 = [] # holds character data for player 2 (real or bot)

print('fruit tree') # start of game
t1()
print('1 player or 2 players?')

while g_mode_choice == (None, None): # chooses the amt of players and game mode
    p_amt = int(input())
    if p_amt == 1 or 2:
        g_mode_choice = (p_amt, None)
        print('regular or tag mode?')
        while g_mode_choice == (p_amt, None):
            m_choice = input().lower()
            if m_choice in ['r', 't']:
                g_mode_choice = (p_amt, m_choice) 
            else:
                print('not valid')
                t1()
                print('regular or tag mode?')
    else:
        print('not valid')
        t1()
        print('1 player or 2 players?')

t1()
print('game mode:', g_mode_sel[g_mode_choice][0], 'player,', g_mode_sel[g_mode_choice][1], 'mode') # states the selected amount of players and game mode

t1()
char_sel_display = [char_sel[list(char_sel.keys())[0]][0], char_sel[list(char_sel.keys())[1]][0], char_sel[list(char_sel.keys())[2]][0]]
print(char_sel_display)

if g_mode_choice[1] == 'r': # chooses characters if in regular mode
    while len(char_choice1) < 1:
        p1_char1 = input().lower()
        if p1_char1 in char_sel.keys():
            char_choice1.append(p1_char1)
            p1c_dict = copy.deepcopy(char_sel[char_choice1[0]][1])
            p1c_name = char_sel[char_choice1[0]][0]
        else:
            print('not valid')
        if g_mode_choice[0] == 2:
            while len(char_choice2) < 1:
                p2_char1 = input().lower()
                if p2_char1 in char_sel.keys():
                        char_choice2.append(p2_char1)
                else:
                    print('not valid')
        else:
            p2_char1 = random.choice(list(char_sel.keys()))
            char_choice2.append(p2_char1)
        p2c_dict = copy.deepcopy(char_sel[char_choice2[0]][1])
        p2c_name = char_sel[char_choice2[0]][0]
    t1()
    print(char_sel[p1_char1][0], 'vs.', char_sel[p2_char1][0]) # states the selected characters (reg mode)

else: # char_sel for tag mode
    while len(char_choice1) < 1:
        choice_lst1 = list(char_sel.keys())
        p1_char1 = input().lower()
        if p1_char1 in choice_lst1:
            char_choice1.append(p1_char1)
            choice_lst1.remove(p1_char1)
            p1c_dict = copy.deepcopy(char_sel[char_choice1[0]][1])
            p1c_name = char_sel[char_choice1[0]][0]
            while len(char_choice1) < 2:
                p1_char2 = input().lower()
                if p1_char2 in choice_lst1:
                    char_choice1.append(p1_char2)
                    p1c2_dict = copy.deepcopy(char_sel[char_choice1[1]][1])
                    p1c2_name = char_sel[char_choice1[1]][0]
                else:
                    print('not valid')
        else:
            print('not valid')
    if g_mode_choice[0] == 2: # char_sel for 2t
        while len(char_choice2) < 1:
            choice_lst2 = list(char_sel.keys())
            p2_char1 = input().lower()
            if p2_char1 in choice_lst2:
                char_choice2.append(p2_char1)
                choice_lst2.remove(p2_char1)
                while len(char_choice2) < 2:
                    p2_char2 = input().lower()
                    if p2_char2 in choice_lst2:
                        char_choice2.append(p2_char2)
                    else:
                        print('not valid')
            else:
                print('not valid')
    else: # char_sel for 1t
        choice_lst2 = list(char_sel.keys())
        p2_char1 = random.choice(choice_lst2)
        char_choice2.append(p2_char1)
        choice_lst2.remove(p2_char1)
        p2_char2 = random.choice(choice_lst2)
        char_choice2.append(p2_char2)
    p2c_dict = copy.deepcopy(char_sel[char_choice2[0]][1])
    p2c_name = char_sel[char_choice2[0]][0]
    p2c2_dict = copy.deepcopy(char_sel[char_choice2[1]][1])
    p2c2_name = char_sel[char_choice2[1]][0]
    t1()
    print(char_sel[p1_char1][0], '&', char_sel[p1_char2][0], 'vs.', char_sel[p2_char1][0], '&', char_sel[p2_char2][0]) # states the selected tag teams

p1c_move_list = list(p1c_dict.keys())[0:-1]
p2c_move_list = list(p2c_dict.keys())[0:-1]

p1_move = g_mode_sel[g_mode_choice][2]
p2_move = g_mode_sel[g_mode_choice][3]

t1()
print('Ready?')
t1()
print('GO!')

Game = True

while Game == True:
    combat()
    if p2c_dict['stats'][0] <= 0:
        Game = False