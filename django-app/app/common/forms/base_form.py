from django import forms
from stringcase import snakecase


def snake_case_and_rename_id(key):
    """
    snake cases key and renames to 'pk' if 'id', because 'id' shadows built in
    """
    new_key = snakecase(key)
    if new_key == 'id':
        new_key = 'pk'
    return new_key


class BaseForm(forms.Form):
    def __init__(self, data):
        """
        Snake cases all form keys.
        Ex: `createdBy` -> `created_by`
        """
        transformed_data = {
            snake_case_and_rename_id(key): val for key, val in data.items()
        }
        super().__init__(transformed_data)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()

        # NOTE - Django forms will set non required fields to None or to an empty string if
        #        the form field is not passed into the form.

        # Filter for fields that are passed through the form and remove fields that where
        # not passed into the form.
        cleaned_data = {
            form_field: cleaned_data[form_field]
            for form_field in self.data if form_field in cleaned_data
        }

        return cleaned_data
