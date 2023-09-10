import json
import random

import requests

from CarfuelBackEnd import settings


class SendSMS(object):
    def sendMessageBirdSMS(data):
        otp = str(random.randint(1000, 9999))
        smsBody = "<#Your OTP is " + otp
        print(otp, data['phonenumber'])
        body = {
            'originator': 'CARFUEL',
            'recipients': data['phonenumber'],
            'body': smsBody
        }

        headers = {'content-type': 'application/json',
                   'Authorization': 'AccessKey ' + str(settings.MESSAGE_BIRD_ACCESS_KEY)}
        # print("Body*****",body,"\n","Headers******",headers)
        try:
            response = requests.post(str(settings.MESSAGE_BIRD_URL), data=body, headers=headers)
            print("Status code", response.status_code)
            responseBody = response.text
            print("*****Response body********", responseBody)
            description = ""
            for item in responseBody["errors"]:
                description = item[2]
                print("******description*********", description)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print("An exception occurred", e)
            return False
