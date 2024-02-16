from django import forms

from common.forms.base_form import BaseForm
from core.repositories import UserRepository, AccountRepository


class CreatedByFormMixin(BaseForm):
    created_by = forms.ModelChoiceField(queryset=UserRepository.get_queryset())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # created_by is not required when updating
        form_name = type(self).__name__
        if form_name.startswith('Update'):
            self.fields['created_by'].required = False
