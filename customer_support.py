import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(first_name, recepient, email_subject, email_body):
    message = Mail(
        from_email='femiosinkolu@gmail.com',
        to_emails='victorolufemi@ieee.org',
        subject="From The Agrobot Project: "+email_subject,
        html_content= f"{email_body} <p> </p> <strong> Sender's email: {recepient}</strong> <p> </p><strong> Sender's first name: {first_name}</strong>")
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        send_to_user(first_name, recepient, email_subject)
    except Exception as e:
        print(str(e))

def send_to_user(first_name, recepient, email_subject):
    message = Mail(
        from_email='femiosinkolu@gmail.com',
        to_emails= recepient,
        subject="From Agrobot Support: "+email_subject,
        html_content= f"Hi {first_name}, This is to confirm to you that we got your email, the support team will reach out to you soon")
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))