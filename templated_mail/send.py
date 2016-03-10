from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context


def get_default_from_email():
        default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

        if default_from_email is None:
            raise ImproperlyConfigured(
                'DEFAULT_FROM_EMAIL setting required to send mail without explicit from_email'
            )

        return default_from_email


def send_templated_mail(template_name, to, context=None, subject=None, from_email=None, cc=None, bcc=None, connection=None, fail_silently=False):  # noqa
    if context is None:
        context = {}

    EmailTemplate = apps.get_model(app_label='templated_mail', model_name='EmailTemplate')

    email_template = EmailTemplate.objects.get(template_name=template_name)

    html_template = Template(email_template.html)
    html_body = html_template.render(Context(context))

    plain_text = email_template.get_plain_text()

    if from_email is None:
        from_email = email_template.default_from

    if from_email == '':
        from_email = get_default_from_email()

    if not isinstance(to, list):
        to = [to]

    if subject is None:
        subject = email_template.subject

    if bcc is None:
        bcc = []
        if hasattr(settings, 'TEMPLATED_EMAIL_BCC'):
            bcc.append(settings.TEMPLATED_EMAIL_BCC)

    msg = EmailMultiAlternatives(subject, plain_text, from_email, to, bcc=bcc, connection=connection, cc=cc)
    msg.attach_alternative(html_body, "text/html")
    return msg.send(fail_silently=fail_silently)
