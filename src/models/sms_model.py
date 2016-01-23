# @name <%= app_name %>
# @description
# Utility functions for sending emails

from src.utils import get_config
import twilio
import twilio.rest

def init():
    twillio_info = get_config(key='TWILLIO_INFO')

    client = twilio.rest.TwilioRestClient(
        twillio_info['TWILLIO_ACCOUNT'],
        twillio_info['TWILLIO_AUTH_TOKEN']
    )
    return client

def send_sms(to_number, body, media_url=None):
    try:
        twillio_info = get_config(key='TWILLIO_INFO')
        client = init()
        message = client.messages.create(
            to=to_number,
            from_=twillio_info['TWILLIO_NUMBER'],
            body=body,
            media_url=media_url
        )
        return message.error_code
    except twilio.TwilioRestException as e:
        return e