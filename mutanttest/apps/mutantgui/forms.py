# -*- coding: utf-8 -*-
from django import forms

from mutant.forms import FieldDefinitionTypeField

from utils import FIELD_TYPES, get_mutant_type


class AddFieldForm(forms.Form):
    field_type = forms.ChoiceField(choices=FIELD_TYPES)

    def clean_field_type(self):
        return int(self.cleaned_data['field_type'])


def get_field_def_form(field_type_pk, model_def_queryset):

    class Meta:
        model = get_mutant_type(field_type_pk)

    form_attrs = {
        'Meta': Meta,
        'content_type': FieldDefinitionTypeField(widget=forms.HiddenInput),
        'model_def': forms.ModelChoiceField(queryset=model_def_queryset,
                                            widget=forms.HiddenInput)
    }

    return type('FieldDefinitionForm', (forms.ModelForm,), form_attrs)
