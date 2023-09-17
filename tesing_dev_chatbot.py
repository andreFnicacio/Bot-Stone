import os
from twilio.rest import Client


client = Client()

from_whatsapp_number='whatsapp:+5516997506091'
to_whatsapp_number='whatsapp:+5527996653686'

client.messages.create(body='/link',from_=from_whatsapp_number,to=to_whatsapp_number)
