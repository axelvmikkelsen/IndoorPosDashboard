from django import forms
from django.forms.models import modelform_factory
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets, Textarea
from django.utils.translation import ugettext_lazy as _
