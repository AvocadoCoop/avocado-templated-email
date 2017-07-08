from django import forms
from django.contrib.auth import get_user_model

from .send import send_templated_mail
from . import models


class MailForm(forms.Form):
    template_name = forms.CharField()
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean_template_name(self):
        template_name = self.cleaned_data['template_name']

        try:
            models.EmailTemplate.objects.get(template_name=template_name)
        except models.EmailTemplate.DoesNotExist:
            raise forms.ValidationError("Template with the name {} not found".format(template_name))

        return template_name

    def save(self):
        template_name = self.cleaned_data['template_name']
        users = self.cleaned_data['users']

        count = 0
        for user in users:
            send_templated_mail(
                template_name,
                [user.email],
                context = dict(
                    user = user
                ),
            )
            count += 1

        return count
