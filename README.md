# Title: IFB102-Mini Project
This image might not be the best representation for the project. It will be updated in the near future. | A unsuspecting stranger approaches! No stealing today :)
:-------------------------:|:-------------------------:
![Powerpoint slide showing the Pi4B and Logitech camera, with a program flow diagram. TBH not a great representation :(](https://api.llay.au/Detection/Ppt1.png) | ![Picture of Twilio sending WhatsApp messages](https://api.llay.au/Detection/Screenshot_20240521-051613.png)

## Contents:
1. Description
2. Detection
3. Messages
4. Future Implementations
5. Structure
6. Packages

## 1. Description
This project is made for an assignment within the Queensland University of Technology's IFB102 subject. It implements a Raspberry Pi 4B, and a Logitech HD Webcam C270, 720p, to act as a doorbell camera of sorts. It appears that I have forgotten what a doorbell is and is no plan or functionality for physically pressing a button. The program detects for movement, and if in that movement it finds a person, it sends an image and alert of the person via WhatsApp to the end user's number. In reality, the implementation of this project, in this state, has only considered sending notifications to a hard-coded primary user. Anything more is outside the scope of this project.
This project can be downloaded an run on a computer with a webcam. I believe the experience will be better than a Raspberry Pi 4B.

## 2. Detection
For movement and person detection, OpenCV was used. The person detection uses OpenCV's pre-trained haar cascades model, which feels like cheating.
Initially I had issues using this on the Pi4B, as I had imported it as "from cv2 import data". I was unable to resolve what appeared to be compatible import with 
Python 3.12 but incompatible with Python 3.9 (which was the version installed on the Pi4B), but it is possible to simply download the XML file and point to its file location. 
To keep my WhatsApp from being spammed, and to keep my Twilio credits in the free tier, in **sendmessage.py** there is a constant *LAST_SEEN_THRESHOLD*, and it controls the amount of seconds since seeing a person that are sufficient to consider any new movement/person detected part of a new interaction (requiring a new message alert).

## 3. Messages
To serve the messages, Twilio was used due to the free-tier credits (which should last the duration of this project).
To be able to serve images (.png) to the end user, Twilio required a URL. As such, Cloudflare's R2 file storage system was used.
OpenCV frames would be written to file locally, and the local file would be uploaded to a R2 bucket which has an accessible image URL endpoint for Twilio to use. 

![Picture of some code in VSCode of code relating to Cloudflare R2](https://api.llay.au/Detection/bucket.png)

> [!TIP]
> If you want to set up Twilio in Python you might find [this](https://www.twilio.com/docs/whatsapp/quickstart/python) helpful.
> Or, if you want to set up a Cloudflare R2 instance you might find [this](https://developers.cloudflare.com/r2/get-started/) helpful.
> Generally, Cloudflare is great because there is a lot you can get within the free-tier!

## 4. Future Implementations
Next I want to see if it is feasable to create a WebRTC stream. I think the Pi4B has 2GB of RAM so it may not be a good idea, but if when the WebRTC stream is established, everything else in the program does not run until the stream ends, it might be a possibility. I also want to add in external face classification as an extra addition.

## 5. Structure:
- main.py
  - movement.py
  - sendmessage.py
    - bucket.py

## 6. Packages:
- import cv2
- from cv2 import data 
- import numpy as np
- import time
- import twilio
- import boto3
- import sys
> [!CAUTION]
> The from cv2 import data package works well in Python versions such as 3.12, but may be incompatible with version 3.9.



