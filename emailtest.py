import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sendmail(msg):
    #mongillo.celina@gmail.com
    print(msg)
    message = Mail(
        from_email='apnahasnain@gmail.com',
        to_emails='apnahasnain@gmail.com',
        subject='Employee Book-off Dates',
        html_content='<h2 style="text-align: center"><span style="font-family: helvetica, sans-serif">Hello Celina, This is Makhs Bot. If there are any problems you can reply to this email to let me know. Anyways heres the books offs.&nbsp;</span></h2><div style="font-family: inherit; text-align: center"><span style="font-family: times new roman,times,serif">'+msg+'</span></div>'
        )

    try:
        sg = SendGridAPIClient(
            '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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def generateString(a_dict):
    months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']
    messagetosend = ""
    listToStr = ''
    for keys in a_dict:
        for elem in a_dict[keys]:
            str2 = elem.split("-")
            listToStr += ''.join(str2[1]+" of "+months[int(str2[0])-1]+", ")
        messagetosend += ("<Strong>"+keys + "</Strong>: " + listToStr+"<br>")
        listToStr = ''
    return messagetosend
