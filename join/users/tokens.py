from django.contrib.auth.tokens import PasswordResetTokenGenerator
#from django.utils import six
import six
import logging

logger = logging.getLogger(__name__)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value = (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
        logger.debug(f'Generated hash value for user {user.pk}: {hash_value}')
        return hash_value

account_activation_token = AccountActivationTokenGenerator()
