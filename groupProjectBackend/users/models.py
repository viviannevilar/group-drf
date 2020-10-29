from django.contrib.auth.models import AbstractUser
from django.db import models
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.urls import reverse
from django.dispatch import receiver



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Comparalist Account"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@Comparalist",
        # to:
        [reset_password_token.user.email]
    )



class CustomUser(AbstractUser):
    preferred_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.username