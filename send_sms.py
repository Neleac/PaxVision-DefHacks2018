# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACc18858412b40734752bf440bddae0388"
auth_token = "a14bcb60232b4339e2d20ea556e49c1f"

client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+12065039531",
    from_="+16085300923",
    body="this works bitch!")
