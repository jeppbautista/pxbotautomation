from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    expiration = models.DateField(null=False)
    member_id = models.CharField(max_length=10, null=False)
    deposit = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    payout = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    earnings = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    total_earned = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    px_expiration = models.CharField(max_length=50, default="Never")

    def __str__(self):
        return self.username

LOGS_CHOICES = (
    ("INFO", "INFO"),
    ("WARNING", "WARNING"),
    ("ERROR", "ERROR")
)


class TransactionLog(models.Model):
    log_date = models.DateTimeField(auto_now_add=True)
    log_message = models.TextField(null=False)
    type = models.CharField(choices=LOGS_CHOICES, max_length=30)

    def __str__(self):
        return self.log_message[:50]

class Config(models.Model):
    loading_time_in_min = models.IntegerField(default=60)


    def __str__(self):
        return "CONFIG"

# def encryption():
    # from cryptography.fernet import Fernet
    # key = Fernet.generate_key()
    # cipher_suite = Fernet(key)
    # cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
    # plain_text = cipher_suite.decrypt(cipher_text)