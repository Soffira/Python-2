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
    'port' : 8000
}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file, Loader=json.loader)
        config.update(file_config)
        
host, port = config.get('host'), config.get('port')

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    
    print(f'Server started with { host }:{ port }')
    
    while True:
        client, address = sock.accept()
        print(f'Client was detected { address[0] }:{adress[1] }')
        
        b_request = client.recv(config.get('buffersize'))
        print(f'Client send message { b_request.decode() }')
        
        client.send(b_request)
        client.close()        
except KeyboardInterrupt:
    print('Server shutdown.')
