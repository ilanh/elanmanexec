from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PublicContrib


class PublicContribCreateForm(forms.ModelForm):
    class Meta:
        model = PublicContrib
        fields = [
            'shortname',
            'desc',
            'exid',
        ]
        labels = {
            'shortname': _('Short Name'),
            'desc': _('description'),
            'exid': _('External ID'),
        }
        help_texts = {
            'shortname': _('Directory name for that role'),
            'exid': _('Key to link yaml vars'),
        }
        error_messages = {
            'shortname': {
                'max_length': _("Name is too long."),
            },
            'exid': {
                'max_length': _("ID is too long."),
            },
        }

    def __init__(self, owner=None, *args, **kwargs):
        super(PublicContribCreateForm, self).__init__(*args, **kwargs)