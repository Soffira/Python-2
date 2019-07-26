import json
import socket
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)

args = parser.parse_args()

config = {
    'host' : 'localhost',
    'port' : 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file, Loader=json.loader)
        config.update(file_config)
        
host, port = config.get('host'), config.get('port')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client was started')
    
    presence_message = 'Hello'
    
    sock.send(presence_message.encode())
    print(f'Client send presence_message {presence_message}')
    
    b_response = sock.recv(config.get('buffersize'))
    print(f'Server send presence_message {b_response.decode()}')
except KeyboardInterrupt:
    print('Client shutdown.')
