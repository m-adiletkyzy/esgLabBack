from django import forms
from .models import Subscriber
from captcha.fields import CaptchaField

class SubscriberForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Subscriber
        fields = ['email', 'captcha']