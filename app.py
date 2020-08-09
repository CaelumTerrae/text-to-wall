from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

currentURL = None

@app.route("/sms", methods=['GET', 'POST'])
def mms_reply():
    """Respond to incoming image texts"""
    imageURL = request.values.get('MediaUrl0', None)
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    if imageURL is None:
        resp.message("Please attach an image you want to see on Daran and Gavin's wall!")
    else:
        resp.message("Thank you for sending this image! It will promptly be displayed on Daran and Gavin's living room wall.")
        currentURL = imageURL
    return str(resp)

@app.route("/wall", methods=['GET'])
def wall():
    return str(currentURL)

if __name__ == "__main__":
    app.run(debug=True)
