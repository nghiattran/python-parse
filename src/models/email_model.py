import sendgrid
from src.utils import get_config


def sendgrid_init(email_to, subject, subs, email_from):
    sendgrid_info = get_config(key="SENDGRID_INFO")
    sg = sendgrid.SendGridClient(sendgrid_info['SENDGRID_API_KEY'])
    message = sendgrid.Mail()
    message.add_to(email_to)
    message.set_subject(subject)
    if email_from is None:
        email_from = '{}<{}>'.format(
            sendgrid_info['SENDGRID_NAME'],
            sendgrid_info['SENDGRID_EMAIL']
        )
    message.set_from(email_from)
    for key in subs:
        message.add_substitution(key, subs[key])

    return sg, message


def send_email_template(email_to, subject, template_id, subs, email_from):
    sg, message = sendgrid_init(email_to, subject, subs, email_from)
    message.set_html(' ')
    message.add_filter('templates', 'enable', '1')
    message.add_filter('templates', 'template_id', template_id)

    return sg.send(message)


def send_email(email_to, subject, content, subs, email_from=None):
    if get_config(key='SENDGRID_INFO') == {}:
        return 200, 'Not send email'

    sg, message = sendgrid_init(email_to, subject, subs, email_from)
    message.set_html(content)

    return sg.send(message)


def send_activation_email(email, objectId, username=None):
    if username is None:
        username = '{}<{}>'.format(email.split("@", 1)[0], email)

    app_info = get_config(key='APP_INFO')

    email_to = '{}<{}>'.format(username, email)
    subject = 'Activation'
    content = "<html><head><title></title><link href='https://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'><style type='text/css'></style></head><body style='background-color: #fDfDfD;'><div style='font-family: Ubuntu, sans-serif;background-color: white;width: 80%;margin: auto;padding: 20px;border: 1px solid #E5E5E5;'> <h4 style='font-size:24px'>Hi {{name}} ,</h4><p style='font-size:18px'>Congrats! Your {{app}} account has been created successfully.</p><p style='font-size:18px'>Click on the button below to activate your account.</p><div style='padding-top: 15px;padding-bottom: 15px;width: 100%;margin: auto;text-align:center'><a href='{{link}}' style='margin: auto;background: #3BCA96;background-image: -webkit-linear-gradient(top, #3BCA96, #3BCA90);background-image: -moz-linear-gradient(top, #3BCA96, #3BCA90);background-image: -ms-linear-gradient(top, #3BCA96, #3BCA90);background-image: -o-linear-gradient(top, #3BCA96, #3BCA90);background-image: linear-gradient(to bottom, #3BCA96, #3BCA90);-webkit-border-radius: 3;-moz-border-radius: 3;border-radius: 3px;text-shadow: 1px 1px 3px #666666;font-family: Arial;color: #ffffff;font-size: 23px;padding: 10px 20px 10px 20px;text-decoration: none;'>Activate Your Account</a></div><p style='font-size:18px'>Best regards,</p><p style='font-size:18px'>The {{app}} team</p></div></body></html>"
    subs = {
        '{{name}}': username,
        '{{app}}': app_info['APP_NAME'],
        '{{link}}': '{}activate/{}>'.format(get_config(key='API_LINK'), objectId)
    }

    return send_email(
        email_to=email_to,
        email_from=None,
        subject=subject,
        subs=subs,
        content=content)


def send_reset_password_email(email, password, username=None):
    if username is None:
        username = '{}<{}>'.format(email.split("@", 1)[0], email)

    email_to = '{}<{}>'.format(username, email)
    subject = 'Reset for password for {}'.format(get_config(key='APP_NAME'))
    content = "<html><head><title></title><link href='https://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'><style type='text/css'></style></head><body style='background-color: #fDfDfD;'><div style='font-family: Ubuntu, sans-serif;background-color: white;width: 80%;margin: auto;padding: 20px;border: 1px solid #E5E5E5;'> <h4 style='font-size:24px'>Hi {{name}},</h4><p style='font-size:18px'>We have received a request to set a new password for your {{app}} account. </p><p style='font-size:18px'>Your new password is shown in the bow below.</p><div style='padding-top: 15px;padding-bottom: 15px;width: 100%;margin: auto;text-align:center'><div style='margin: auto;background: #3BCA96;background-image: -webkit-linear-gradient(top, #3BCA96, #3BCA90);background-image: -moz-linear-gradient(top, #3BCA96, #3BCA90);background-image: -ms-linear-gradient(top, #3BCA96, #3BCA90);background-image: -o-linear-gradient(top, #3BCA96, #3BCA90);background-image: linear-gradient(to bottom, #3BCA96, #3BCA90);-webkit-border-radius: 3;-moz-border-radius: 3;border-radius: 3px;text-shadow: 1px 1px 3px #666666;font-family: Arial;width: 400px;color: #ffffff;font-size: 23px;padding: 10px 20px 10px 20px;text-decoration: none;'>{{password}}</div></div><p style='font-size:18px'>Please login to <a href='{{link}}'>{{app}}</a> and change your password</p><p style='font-size:18px'>Best regards,</p><p style='font-size:18px'>The {{app}} team</p></div></body></html>"
    subs = {
        '{{name}}': username,
        '{{app}}': get_config(key='APP_NAME'),
        '{{link}}': get_config(key='APP_LINK'),
        '{{password}}': password
    }
    return send_email(
        email_to=email_to,
        email_from=None,
        subject=subject,
        subs=subs,
        content=content)
