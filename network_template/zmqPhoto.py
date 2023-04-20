#pub
import zmq
import base64

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

message = {"type": "image", "data": encoded_string}

socket.send_json(message)


'''
import zmq

def publish_image(filename):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    with open(filename, 'rb') as f:
        image_bytes = f.read()

    socket.send(image_bytes)

'''

#sub
'''
import zmq
import base64

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

while True:
    message = socket.recv_json()
    if message["type"] == "image":
        encoded_data = message["data"]
        image_data = base64.b64decode(encoded_data)
        # process the image_data as needed

'''