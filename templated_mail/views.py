from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import MailForm


@staff_member_required
def send_mail(request, template="templated_mail/send_mail.html"):

    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Messages sent successfully!')
            return redirect('send_mandrill_message')
    else:
        form = MailForm()

    return render(
        request,
        template,
        dict(
            form = form,
        )
    )
