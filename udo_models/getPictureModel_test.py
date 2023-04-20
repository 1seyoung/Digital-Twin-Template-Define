import requests
import shutil
import time
import sys
import cv2
import numpy as np
import datetime

import asyncio
import aiohttp

BASEURL = 'http://192.168.43.1/osc/'

async def get_picture():
    async with aiohttp.ClientSession() as session:
        # Start camera session
        data = {"name": "camera.getImage", "parameters": {}}
        resp = await session.post(BASEURL + 'commands/execute', json=data)
        if resp.status != 200:
            raise Exception('camera.getImage: {}'.format(resp.status))
        response_json = await resp.json()
        session_id = response_json["results"]["sessionId"]
        print('SessionId: {}'.format(session_id))

        data = {"name": "camera.takePicture", "parameters": {"sessionId": session_id}}
        resp = await session.post(BASEURL + 'commands/execute', json=data)
        if resp.status != 200:
            raise Exception('camera.takePicture: {}'.format(resp.status))
        response_json = await resp.json()
        picture_url = response_json["results"]["fileUrl"]
        async with session.get(picture_url) as response:
            picture_data = await response.content.read()
        nparr = np.frombuffer(picture_data, np.uint8)
        img = cv2.imdecode(np.frombuffer(nparr, np.uint8), cv2.IMREAD_COLOR)

        return img


async def main():

    # Start camera session


    # Get image from camera
    frame = await get_picture()

    # Add text with current time
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_size, _ = cv2.getTextSize(text, font, 1, 2)
    text_x = int((frame.shape[1]) / 2) - 5
    text_y = frame.shape[0] - 30
    position = (text_x, text_y)
    fontScale = 7
    thickness = 5
    color = (255, 255, 255)
    cv2.putText(frame, text, position, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow('frame', frame)