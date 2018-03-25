import cv2
import json
import requests
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
from tkinter import messagebox as tkMessageBox
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACc18858412b40734752bf440bddae0388"
auth_token = "a14bcb60232b4339e2d20ea556e49c1f"
client = Client(account_sid, auth_token)
text_sent = False

def analyze_frame(image_path, threshold):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Prediction-key': 'da332d2afd7446509f189200f7b85126',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'iterationId': '',
        'application': '',
    })
    
    image = open(image_path, "rb").read()

    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/customvision/v1.1/Prediction/4e402c59-95bf-4deb-a937-3b8e9bac2676/image?%s" % params, image, headers)
        response = conn.getresponse()
        analysis = json.loads(response.read())
        #print(analysis)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    result = 0
    dict_list = analysis['Predictions']
    for dictionary in dict_list:
        if dictionary['Tag'] == 'not_gun':
            if dictionary['Probability'] >= threshold:
                return 0
        elif dictionary['Probability'] > result:
                result = dictionary['Probability']
    return result

camera = cv2.VideoCapture(0)

#analysis every frame
threshold = 0.75

i = 0
while(True):
    ret, frame = camera.read()
    cv2.imshow('PaxVision', frame)
    i += 1
    
    if i == 150:
        cv2.imwrite('capture.jpg', frame)
        alarm = analyze_frame('capture.jpg', threshold)
        if alarm > threshold:
            print("ALARM: " + str(alarm))
            if not text_sent:
            	'''
            	client.api.account.messages.create(
    				to = "+12065039531",
    				from_ = "+16085300923",
    				body = "Firearm detected! Probability: " + str(alarm))
    			'''

            	tkMessageBox.showinfo(title = "Alert", message = "Firearm detected! Probability: " + str(alarm))

            	text_sent = True
        else:
            print("NO GUN DETECTED: " + str(alarm))
        i = 0
    
    key = cv2.waitKey(3)
    #ESC key press
    if key%256 == 27:
        break
        
camera.release()
cv2.destroyAllWindows()