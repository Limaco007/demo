from website import create_app
from flask_mail import Mail, Message

app = create_app()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "sylvesterchima11@gmail.com"
app.config['MAIL_PASSWORD'] = "cgpfztdefimakjct"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route('/sendemail')
def sendemail():
    html = r'''
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Invite</title>
            </head>
            <body>
                <p> Hi [[0]]!</p>
                <p>You've been invited to join [[1]]. To verify your account, simply click on the button below or copy this link <a href="[[2]]">[[2]]</a></p>
                <a href="[[2]]" style="display:block; background-color:cornflowerblue; color: white; padding: 10px;">Click here</a>
                <p>Hope you will find [[1]] useful!</p>
                <p>
                    Best <br>
                    The [[1]] team
                </p>

            </body>
            </html>
        '''
    msg = Message('Trolog Invite', sender = 'sylvesterchima11@gmail.com')

    #if they are more than 1 recipient then loop through them and add the email like this
    msg.recipients.append('sylvesterchima11@outlook.com')

    #use msg.html instaed of msg.body then replace your placeholder in your template with value you want
    msg.html = html.replace('[[0]]','Chima').replace('[[1]]','Trolog').replace('[[2]]','http://127.0.0.1:5000/')
    mail.send(msg)
    return "sent"

if __name__=='__main__':
    app.run(debug=True)












