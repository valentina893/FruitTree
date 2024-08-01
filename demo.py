import time, socket, sys, pickle, copy

p1 = { # 184 bytes
        'h':[10, 'hit'],
        'stats':100
        }

p2 = { # 184 bytes
        'k':[10, 'kick'],
        'stats':100
        }

def t1():

    time.sleep(1)

def interact(server_and_name):

    print(server_and_name[-1])

    u_inp = input().lower()

    move = True

    while move:

        if u_inp == list(server_and_name[-1].keys())[0]:

            sent_move = pickle.dumps(server_and_name[-1][u_inp])
            server_and_name[0].sendall(sent_move)
            move = False
        
        else:

            print('not valid')
    
    receive(server_and_name)

def receive(server_and_name):

    listening = True

    while listening:

        move_recv = server_and_name[0].recv(200)
        listening = False
    
    enemy_move = pickle.loads(move_recv)

    print(server_and_name[1], 'used', enemy_move)

'''
P1 FUNCTIONS 
'''

def create_server():

    port = int(input('create port: '))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port)) # (ip, port)
    s.listen(1)

    print('waiting for connection...')
    try:
        clientsocket, address = s.accept()
        obj_recv = clientsocket.recv(200)
        join_user = pickle.loads(obj_recv)
        obj = pickle.dumps(user)
        clientsocket.sendall(obj)
        print(join_user, 'has joined the game.')    
    except:
        print('no joining users found.')
    
    player_dict = copy.deepcopy(p1)
    return [clientsocket, join_user, player_dict]

'''
P2 FUNCTIONS
'''

def join_server():

    global player_dict

    port = int(input('type port: '))

    searching = True

    while searching:

        print('searching for hosts...')

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostname(), port)) # (ip, port)
            joining_name = pickle.dumps(user)
            s.sendall(joining_name)
            obj_recv = s.recv(200)
            host_user = pickle.loads(obj_recv)
            print('connected to', host_user)
            searching = False
        except:
            t1()
            print('no available hosts found.\ntry again?')
            choice = input().lower()
            if choice == 'y':
                continue
            elif choice == 'new port':
                port = int(input('type port: '))
            elif choice == 'n':
                searching = False
            else:
                continue
        
        player_dict = copy.deepcopy(p2)
        return [s, host_user, player_dict]
    
    player_dict = p2

def send(server):

    t1()
    print('make move')

    u_inp = input().lower()

    turn = True

    while turn:

        if u_inp == 'y':
            
            turn = False
            obj = pickle.dumps([1,2,3,4])
            server.sendall(obj)
    
        else:

            print('not valid')
    
    recv_updt(server)

def recv_updt(s):

    listening = True

    while listening:

        obj_recv = s.recv(200)
        listening = False
    
    obj_recv = pickle.loads(obj_recv)

    print(obj_recv)

user = input('user: ')

print('host or join?')

u_inp = input().lower()

game = True

if u_inp == 'host':

    cs_u = create_server()

    while game:

        interact(cs_u)

elif u_inp == 'join':

    s_ho = join_server()

    while game:

        interact(s_ho)