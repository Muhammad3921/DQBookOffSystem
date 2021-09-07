import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def sendmail(msg):
    #mongillo.celina@gmail.com
    #apnahasnain@gmail.com
    message = Mail(
        from_email='apnahasnain@gmail.com',
        to_emails='apnahasnain@gmail.com',
        subject='Employee Book-off Dates',
        html_content='<h2 style="text-align: center"><span style="font-family: helvetica, sans-serif">Hello Celina, This is Makhs Bot. If there are any problems you can reply to this email to let me know. Anyways heres the books offs.&nbsp;</span></h2><div style="font-family: inherit; text-align: center"><span style="font-family: times new roman,times,serif">'+msg+'</span></div>'
        )

    try:
        sg = SendGridAPIClient(os.getenv("APIKEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

