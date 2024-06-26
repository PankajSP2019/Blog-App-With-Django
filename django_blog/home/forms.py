# Created By - Pankaj Kumar Das
# For Using Custom Form

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.forms import PasswordInput


# For Re-Captcha Field
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'old_password':
                field.widget.attrs.update({'placeholder': 'Enter Old Password'})
            elif field_name == 'new_password1':
                field.widget.attrs.update({'placeholder': 'Enter New Password'})
            elif field_name == 'new_password2':
                field.widget.attrs.update({'placeholder': 'Confirm New Password'})


# Another Approach Change Password Form
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control'}


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # field.widget.attrs.update({'autocomplete': 'off'})


class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'new_password1':
                field.widget.attrs.update({'placeholder': 'Enter New Password'})
            elif field_name == 'new_password2':
                field.widget.attrs.update({'placeholder': 'Confirm New Password'})
