# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import music
import ast #convert list into string and vice versa

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
        
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_code, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
                            
                elif my_msg[0] == 'c':
                    peer = my_msg[1:].strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                        
#                elif my_msg[0] == 'p':
#                   poem_idx = my_msg[1:].strip()
#                    mysend(self.s, M_POEM + poem_idx)
#                    poem = myrecv(self.s)[1:].strip()
#                    if (len(poem) > 0):
#                        self.out_msg += poem + '\n\n'
#                    else:
#                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                        
                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer 
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # My stuff, going out
                if my_msg == '!music':
                    mysend(self.s, M_MUSIC + self.me)
                    self.state = S_MUSIC
                    self.out_msg += music_menu
                else:
                    mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                    if my_msg == 'bye':
                        self.disconnect()
                        self.state = S_LOGGEDIN
                        self.peer = ''
                    
            if len(peer_msg) > 0:   # Peer's stuff, coming in
                # New peer joins
                if peer_code == M_CONNECT:
                    self.out_msg += "(" + peer_msg + " joined)\n"
                elif peer_code == M_MUSIC:
                    self.out_msg += peer_msg + " has invited you to play music!\n"
                    self.state = S_MUSIC
                    self.out_msg += music_menu
                else:
                    self.out_msg += peer_msg

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
                
                
                
#==============================================================================
# When in Music Mode
#==============================================================================
        elif self.state == S_MUSIC:
            if len(my_msg) > 0:
                if my_msg[:4] == 'done':
                    mysend(self.s, M_MUSIC_OUT + self.me)
                    self.state = S_CHATTING
                    self.out_msg += 'You have exited Music Mode\n'
                    self.out_msg += 'Welcome back to Chat Mode.'
                    self.out_msg += 'Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                        
                else: # just sending a normal chat message
                    mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
        
        
        
        
        
#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg
