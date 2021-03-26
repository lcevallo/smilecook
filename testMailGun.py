import requests
from mailgun import MailgunApi

mailgun = MailgunApi(domain='sandbox813acc3bb61d406ea694a4e875b598f0.mailgun.org', api_key='08cf32cde9bd234e870989e190f50272-1553bd45-7c86ad62')

mailgun.send_email(to='lcevallo@gmail.com', subject='Pyhton enviando mails', text='Testing some Mailgun awesomeness!')


# requests.post(
#     "https://api.mailgun.net/v3/sandbox813acc3bb61d406ea694a4e875b598f0.mailgun.org/messages",
#     auth=("api", "08cf32cde9bd234e870989e190f50272-1553bd45-7c86ad62"),
#     data={"from": "Mailgun Sandbox <postmaster@sandbox813acc3bb61d406ea694a4e875b598f0.mailgun.org>",
#           "to": "lcevallo@gmail.com",
# "subject": "Python envia mail",
# "text": "Testing some Mailgun awesomness!"})
