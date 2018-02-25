from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render, HttpResponse

from tutor.models import Record_Visitor, Visitor, Counter

def send_email(subject, body):
    import smtplib


    # IN views.py you have to provice the credentials

    gmail_user = "monprof286@gmail.com" # email from which account you want to send emails
    gmail_pwd = "monprof286"  # password of above email
    FROM = "monprof286@gmail.com"
    # This is the list of users who will recieve the email
    # If I add your email address here you will start getting emails
    recipient = ["monprof286286@gmail.com", "286gilberto@gmail.com"] # list of email recievers
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
        return True
    except:
        print("failed to send mail")
        return False


def design_message(name, email, number, message):
    formatted_message = "Hello Mister Gilbert!\nA New Message from MonProf has been recieved\n"
    formatted_message += "Submitted by: " + name + "\n"
    formatted_message += "Contact Information: \n  Phone Number: " + number + "\n  Email: " + email + "\n"
    formatted_message += "Message :\n  " + message + "\n Thank You!"
    return formatted_message


def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')


    today = datetime.today()
    today = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    try:
        visitor = Visitor.objects.get(ip=ip)
        if visitor:
            try:
                Record_Visitor.objects.get(date=today, ip=visitor)
                record_visitor = Record_Visitor.objects.filter(date=today, ip=visitor) \
                    .update(total_today=F('total_today') + 1, total_overall=F('total_overall') + 1)
            except Record_Visitor.DoesNotExist:
                try:
                    latest_record = Record_Visitor.objects.filter(ip=visitor).order_by('-id')[:1].first()
                    if latest_record:
                        total_overall = latest_record.total_overall
                    else:
                        total_overall = 0
                except Record_Visitor.DoesNotExist:
                    total_overall = 0
                Record_Visitor.objects.create(ip=visitor, date=today, total_today=1, total_overall=total_overall+1)
            try:
                Counters = Counter.objects.get(date=today)
                if Counters:
                    Counter.objects.filter(date=today) \
                        .update(total_today=F('total_today') + 1, total_overall=F('total_today') + 1)
            except Counter.DoesNotExist:
                try:
                    yesterdays_record = Counter.objects.all().order_by('-id')[:1].first()
                    if yesterdays_record:
                        total_overall = yesterdays_record.total_overall
                    else:
                        total_overall = 0
                except Counter.DoesNotExist:
                    total_overall = 0
                Counter.objects.create(date=today, total_today=1, total_overall=total_overall+1)


    except Visitor.DoesNotExist:
        visitor = Visitor.objects.create(ip=ip)
        try:
            latest_record = Record_Visitor.objects.get(ip=visitor).order_by('-id')[:1].first()
            total_overall = latest_record.total_overall
        except Record_Visitor.DoesNotExist:
            total_overall = 1
        Record_Visitor.objects.create(ip=visitor, date=today, total_today=1, total_overall=total_overall)
        try:
            Counters = Counter.objects.get(date=today)
            if Counters:
                Counter.objects.filter(date=today) \
                .update(total_today=F('total_today') + 1, total_overall=F('total_today') + 1)
        except Counter.DoesNotExist:
            try:
                yesterdays_record = Counter.objects.all().order_by('-id')[:1].first()
                total_overall = yesterdays_record.total_overall
            except Counter.DoesNotExist:
                total_overall = 1
            Counter.objects.create(date=today, total_today=1, total_overall=total_overall)




    error = False
    email_sent = False
    if request.method == 'POST':
        name = request.POST.get('name') if "name" in request.POST else None
        sender = request.POST.get('sender') if "sender" in request.POST else None
        number = request.POST.get('number') if "number" in request.POST else None
        message = request.POST.get('message') if "message" in request.POST else None

        if name and sender and number and message:
            formatted_message = design_message(name, sender, number, message)
            print(formatted_message)
            email_sent = send_email("Email From MonProf", formatted_message)
            if not email_sent:
                error = True

    return render(request, 'home/index.html', {
        "error": error,
        "email_sent": email_sent
    })
