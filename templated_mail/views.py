from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import MailForm
from .models import EmailTemplate


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


@staff_member_required
def preview(request, template_pk, template="templated_mail/preview.html"):
    email_template = get_object_or_404(EmailTemplate, pk=template_pk)

    text = request.GET.get('text', False)
    if text is not False:
        text = True

    return render(
        request,
        template,
        dict(
            email_template = email_template,
            text = text,
        )
    )
