# Created By Pankaj Kumar Das
# Generate Token, For Email Verification

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp)
        )


generate_token = TokenGenerator()


# Another Approach
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
