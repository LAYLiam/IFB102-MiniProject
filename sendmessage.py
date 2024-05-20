# [Send Message]
"""
    Main purpose:
        When prompted, using 3rd party Twilio to send a WhatsApp mesage to
        a target phone number/user. 

        A generated WhatsApp message currently follows this structure:
        f"{PERSON} detected at the {LOCATION}
        <Insert image of person's face (256 x 256 res)>
 
    [1] <Source was used to implement WhatsApp outbound comms. from the program without having
    to register as an official business. The method implemented here keeps the usage
    within Twilio's WhatsApp Sandbox permissions.> 
    Twilio. (n.d.). Programmable Messaging for WhatsApp and Python Quickstart.
            Retrieved 20 May, 2024 from https://www.twilio.com/docs/whatsapp/quickstart/python
    [2] <Source was used to learn how to send media via URL.>
    Phan, D., & Grinberg, M. (2014). How to Send a Picture on WhatsApp Using Twilio and Python.
            Retrieved 20 May, 2024 from https://www.twilio.com/en-us/blog/how-to-send-picture-whatsapp-twilio-python
"""

import cv2
import time
import requests
from pathlib import Path 
from twilio.rest import Client
import env
import bucket

"""Constants

:const LAST_SEEN_THRESHOLD: Duration if expires before refresh means movement detected is a new interaction.
:const LOCATION: Where the camera is located.
:const NO_IMAGE_ENDPOINT: URL if there is no image.
"""
LAST_SEEN_THRESHOLD = 15
LOCATION = "door"

"""Handle message processing if a face is detected, and a new message request made. 
"""
class ProcessMessage:   
    @staticmethod
    def upload_image(detection):
        """Takes face image photo, saves it locally
        and then uploads it to Cloudflare R2 bucket.

        :param detection: Cropped image of the face if face exists, else None.
        :return: null
        """
        image_path = str(Path.cwd()) + r"\storage\detection.png"
        cv2.imwrite(image_path, detection)
        bucket.s3.upload_image(image_path)
        return

    @staticmethod
    def get_image():
        """Checks if there is an existing image to send of the person.
        Makes a HTTP request to the endpoint, and if it is not found <404>
        then return the URL for no image.

        :return: Image of face URL if exists, else URL of no image picture.    
        """
        response = str(requests.get(env.S3_BUCKET_IMAGE_ENDPOINT))
        if (response == '<Response [404]>'):
            return env.S3_BUCKET_NO_IMAGE_ENDPOINT
        else: return env.S3_BUCKET_IMAGE_ENDPOINT

    @staticmethod
    def new_alert(last_seen):
        """Triggered when movement is made, and checks 
        if the previous time a person was seen exceeds the LAST_SEEN_THRESHOLD.
        If so, then the program will assume that any new/current movements are not 
        part of the previous interaction but make up a new interaction.

        :param last_seen: Last time a person was seen.
        :return: True if a new alert needs to be raised, else False.
        """
        return (time.time() - last_seen) > LAST_SEEN_THRESHOLD

    @staticmethod
    def new_message(detection):
        """Processes a new Twilio WhatsApp message on request according to source [1] and [2].
        Takes the image of the face of a person (detection), uploads it to a Cloudflare R2 bucket
        and sends message with picture via WhatsApp with a message alerting that a person has been detected.  
        
        :param detection: Cropped image of the face if face exists, else None.
        :return: null 
        """
        object = 'Person'
        ProcessMessage.upload_image(detection)
        image_url = ProcessMessage.get_image()

        # Send message via Twilio
        client = Client(env.TWILIO_ACCOUNT_SID, env.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'{object} detected at the {LOCATION}.',
            media_url=image_url,
            from_=env.TWILIO_OUTBOUND,
            to=env.TWILIO_RECEIVER,
        )
        print(f"Message sent to {env.TWILIO_RECEIVER}:{message.sid}")
        return

