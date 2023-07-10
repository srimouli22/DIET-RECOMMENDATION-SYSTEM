import numpy as np
from flask import Flask, request, jsonify, render_template
from model import Weight_Gain, Weight_Loss, Healthy
from calend import add_event
from flask_mail import Mail, Message
from email.mime.text import MIMEText
import smtplib, ssl
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict():
    age=int(request.args.get('age'))
    weight=float(request.args.get('weight'))
    height=float(request.args.get('height'))
    fun=int(request.args.get('fun'))
    k=int(request.args.get('k'))

    if(k==1):
        status = Weight_Loss(age, weight, height, fun)
    elif(k==2):
        status = Weight_Gain(age, weight, height, fun)
    else:
        status = Healthy(age, weight, height, fun)
        
    return render_template('result.html', bmi=str(round(status['bmi'], 2)), status=status['status'], diet=", ".join(status['food_items']))

@app.route('/calendar',methods=['POST'])
def calendar():
    mailrec=request.form.get('gmailid')
    diet = str(request.form.get('diet'))
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "nandamsrimowli@gmail.com"  
    receiver_email = mailrec
    password = "jgjzbhggcwwnmjlt"
    message = 'Hi ' + str(mailrec) + ', Thanks for visiting our Diet Recommender System. Based on the data we collected, the diet that we recommend you to follow is as follows.\nFood items - ' + diet + '\nThank You and have great health ahead! \nTEAM PERSONAL DIET RECOMMENDER.'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return render_template('sent.html')

if __name__ == "__main__":
    app.run(debug=True)