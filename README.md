# Avocado Templated Mail

We were using Mandrill to make it easier to preview and edit the content
in our transactional emails. This is our local solution, partially built
on https://github.com/oeegor/dj-templated-mail/

This isn't an email backend, you will have to use something like Amazon
SES to send the email.

It does provide models to store email templates in your database so they
can be updated, previewed and sent with out technical knowledge or
console access.

## Basics

Django 1.7 or higher, should work with Python 2.7 or 3.4 or higher.

Install from github for now

```
pip install git+git://github.com/AvocadoCoop/avocado-templated-mail.git
```

Add `templated_mail` to your `INSTALLED_APPS`

```
INSTALLED_APPS = (
    ...
    'templated_mail'
)
```

You will need to `migrate`

```
./manage.py migrate
```

You can then add some templates to your database through the django
admin and send them in code:

```
from templated_mail import send_templated_mail

# ...

send_templated_mail(
    'Your Template Name',
    context = dict(name='Guido'),
    from = 'info@example.com',
    to = ['to@example.com'],
)
```

This will throw an exception, `EmailTemplate.DoesNotExist`, if there
isn't a template named 'Your Template Name' in your database.

`send_templated_mail` supports the same interface as `EmailMessage`
[Doc](https://docs.djangoproject.com/en/1.7/topics/email/#django.core.mail.EmailMessage)
less the attachments part, PR welcome.

## The Templates

The templates support an HTML body and either an explicit plain text
version or the plain text will be generated automatically.

In addition the HTML body will be treated like a Django template and the
context which is passed in can be integrated into the message.

The plain text strategy is to first render the HTML body as a template
and then strip out all the tags.

## Views

For previews to work and to easily send an email to a subset of users
enable the included views:

```
# urls.py

urlpatterns = [
  # ...
  url('^mail/', include('templated_mail.urls')),
]
```

## Template

The use the mail sending view `mail/send/` for e.g. you will need to provide a template in `templated_mail/send_mail.html`. Here is an example:

```
{% extends "base.html" %}

{% block contents %}
<form class="" role="form" method="post">
    {% csrf_token %}
    <h2>Send Templated Message</h2>
    {{ form.as_p }}
    <input type="submit" value="Send">
</form>
{% endblock contents %}
```

## Other Settings

```
TEMPLATED_EMAIL_BCC = 'report@example.com'
```

With `TEMPLATED_EMAIL_BCC` set all message send with templated_email
send function will bcc this address, this is handy for tracking you
outbound email to make sure there are any quality issues over time.
