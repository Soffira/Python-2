import yaml
import json
import socket
import logging
from argparse import ArgumentParser

from actions import resolve
from protocol import validate_request, make_response

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
        file_config = yaml.load(file, Loader=yaml.loader)
        config.update(file_config)
        
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('main.log'),
        logging.StreamHandler(),
    ]
)

host, port = config.get('host'), config.get('port')

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    
    logging.info(f'Server was started with { host }:{ port }')
    
    while True:
        client, address = sock.accept()
        logging.info(f'Client was detected { address[0] }:{address[1] }')
        
        b_request = client.recv(config.get('buffersize'))
        
        request = json.loads(b_request.decode())
        
        if validate_request(request):
            actions_name = request.get('action')
            controller = resolve(actions_name)
            if controller:
                try:
                    logging.info(f'Client send valid request {request}')
                    response = controller(request)
                except Exception as err:
                    logging.critical(f'Internet server error: {err}')
                    response = make_response(request, 500, data='Internet server error')
            else:
                logging.error(f'Controller with action name {actions_name} does not exists')
                response = make_response(request, 404, 'Action not found')
        else:
            logging.error(f'Client send invalid request { request }')
            response = make_response(request, 400, 'Wrong request')
            
        str_response = json.dumps(response)
        client.send(str_response.encode())
    
    
except KeyboardInterrupt:
    print('Server shutdown.')