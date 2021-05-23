from CarfuelBackEnd import settings


class SendSMS(object):
    def sendMessageBirdSMS(self, data,otp):
        smsBody = "<#Your OTP is " + otp
        body = {
            "originator": "CARFUEL",
            "recipients": request['phonenumber'],
            "body": smsBody
        }
        headers = {"content-type": "application/json; charset=UTF-8",
                   'Authorization': 'AccessKey ' + settings.MESSAGE_BIRD_ACCESS_KEY}
        try:
            response = requests.post(settings.MESSAGE_BIRD_URL, data=body, headers=headers)
            print("Status code", response.status_code)
            responseBody = response.text
            print("*****Response body********", responseBody)
            description = ""
            for item in responseBody['errors']:
                description = item['description']
                print("******description*********", description)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print("An exception occurred",e.args)
            return False
