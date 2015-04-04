#!/usr/bin/python3

'''
Russell Stanley
CSE 3320
Lab 4
'''

from fs import *
import os
import pickle

def main():
    #import pdb; pdb.set_trace()
    commands = [
        'createfs', 'formatfs', 'savefs', 'openfs', 'quit', 
        'list', 'remove', 'put', 'get', 'link', 'unlink', 'help',
    ]

    print('Welcome! Please type a command. Type "help" for a list of commands')

    while True:
        cmd_args = input('>>> ').lower().split()
        
        if cmd_args[0] == 'quit':
            return

        elif cmd_args[0] == 'createfs':
            try:
                file_sys = FileSystem(int(cmd_args[1]))
            except TypeError:
                print('Error: argument must be an integer.')
            except IndexError:
                print('Error: createfs takes an argument.')
                
        elif cmd_args[0] == 'formatfs':
            try:
                file_sys.fmt(cmd_args[1], cmd_args[2])
            except IndexError:
                print('Error: formatfs takes two arguments.')
            except TypeError:
                print('Error: arguments must be integers.')

        elif cmd_args[0] == 'savefs':
            try:
                file_sys.savefs(cmd_args[1])
            except IndexError:
                print('Please provide name argument.')

        elif cmd_args[0] == 'openfs':
            if os.path.isfile(cmd_args[1]):
                try:
                    f = open(cmd_args[1], 'rb')
                    file_sys = pickle.load(f)
                    f.close
                    print('Now working in disk: %s' % file_sys.disk_name())
                except TypeError:
                    print('Not a valid disk file')
            else:
                print('No disk file named %s.' % cmd_args[1])

        elif cmd_args[0] == 'list':
            file_sys.ls()

        elif cmd_args[0] == 'remove':
            try:
                file_sys.remove(cmd_args[1])
            except IndexError:
                print('Error: must provide filename argument.')

        elif cmd_args[0] == 'put':
            try:
                if os.path.isfile(cmd_args[1]):
                    file_sys.put(cmd_args[1])
                else:
                    print('No file named %s.' % cmd_args[1]) 
            except IndexError:
                print('Error: must provide filename argument.')

        elif cmd_args[0] == 'get':
            try:
                file_sys.get(cmd_args[1])
            except IndexError:
                print('Error: must provide filename argument.')

        elif cmd_args[0] == 'link':
            try:
                file_sys.link(cmd_args[1], cmd_args[2])
            except IndexError:
                print('Error: link takes two arguments.')

        elif cmd_args[0] == 'unlink':
            try:
                file_sys.unlink(cmd_args[1])
            except IndexError:
                print('Error: unlink takes an argument.')

        elif cmd_args[0] == 'help':
            for c in commands:
                print(c)

        else:
            print('Command unrecognized. Type "help" for a list of commands.')

if __name__ == '__main__':
    main()
