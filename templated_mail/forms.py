from django import forms
from django.contrib.auth import get_user_model

from .send import send_templated_mail


class MailForm(forms.Form):
    template_name = forms.CharField()
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().all(),
        widget=forms.CheckboxSelectMultiple
    )

    def save(self):
        template_name = self.cleaned_data['template_name']
        users = self.cleaned_data['users']

        for user in users:
            send_templated_mail(
                template_name,
                [user.email],
                context = dict(
                    user = user
                ),
            )
