from src.utils import get_config
import twilio
import twilio.rest

def init():
    client = twilio.rest.TwilioRestClient(
        get_config(key='TWILLIO_ACCOUNT'),
        get_config(key='TWILLIO_AUTH_TOKEN')
    )
    return client

def send_sms(to_number, body, media_url=None):
    try:
        client = init()

        message = client.messages.create(
            to=to_number,
            from_=get_config(key='TWILLIO_NUMBER'),
            body=body,
            media_url=media_url
        )
        return message.error_code
    except twilio.TwilioRestException as e:
        return e