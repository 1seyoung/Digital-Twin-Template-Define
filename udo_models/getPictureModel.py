import requests
import shutil
import time
import sys
import cv2
import numpy as np
import datetime

BASEURL = 'http://192.168.43.1/osc/'
cap_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Get camera information
resp = requests.get(BASEURL + 'info')
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception('GET /osc/info/ {}'.format(resp.status_code))
print('Manufacturer: {}'.format(resp.json()["manufacturer"]))
print('Model: {}'.format(resp.json()["model"]))
print('Firmware: {}'.format(resp.json()["firmwareVersion"]))
print('Serial: {}'.format(resp.json()["serialNumber"]))

# Get camera state
resp = requests.post(BASEURL + 'state')
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception('GET /osc/state/ {}'.format(resp.status_code))
print('batteryLevel: {}'.format(resp.json()["state"]["batteryLevel"]*100))

# Start camera session
data = {"name": "camera.startSession", "parameters": {} }
resp = requests.post(BASEURL + 'commands/execute', json=data)
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception('camera.startSession: {}'.format(resp.status_code))
sessionId = (resp.json()["results"]["sessionId"])
print ('SessionId: {}'.format(sessionId))

# Define function to get image from camera
def getPicture():
    # Take new image
    data = {"name": "camera.takePicture", "parameters": { "sessionId": sessionId} }
    resp = requests.post(BASEURL + 'commands/execute', json=data)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('camera.takePicture: {}'.format(resp.status_code))
    pictureId = (resp.json()["id"])

    # Wait for image processing
    sys.stdout.write('Waiting for image processing')
    sys.stdout.flush()
    for x in range(1, 30):
        sys.stdout.write('.')
        sys.stdout.flush()
        data = {"id": pictureId } 
        resp = requests.post(BASEURL + 'commands/status', json=data)
        if format(resp.json()["state"])=='done': 
            break
        time.sleep(3)
    print ('')

    # Get new image
    data = {"name": "camera.getImage", "parameters": { "fileUri": resp.json()["results"]["fileUri"] } }
    resp = requests.post(BASEURL + 'commands/execute', json=data)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('camera.getImage: {}'.format(resp))
    img_arr = resp.content
    img = cv2.imdecode(np.frombuffer(img_arr, np.uint8), cv2.IMREAD_COLOR)

    # Return image
    return img

# Open camera and stream video
# Open camera and stream video
cap = cv2.VideoCapture(0)

while True:
    # Get image from camera
    frame = getPicture()

    # Add text with current time
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
    text_size, _ = cv2.getTextSize(text, font, 1, 2)
    text_x = int((frame.shape[1]) / 3)
    text_y = int((frame.shape[0]/5))*4
    position = (text_x, text_y)
    fontScale = 5
    color = (255, 255, 255)
    thickness = 30
    cv2.putText(frame, text, position, font, fontScale, color, thickness, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Check if 'q' key was pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done
cap.release()
cv2.destroyAllWindows()






##