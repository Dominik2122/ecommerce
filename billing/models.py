from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from phone_field import PhoneField
User = settings.AUTH_USER_MODEL
# Create your models here.
import stripe
stripe.api_key = 'sk_test_51IXW3aCkhkhAd2s3znmhkXSYIzCuKI4eB46wGwcfFO5yjkx7eXCmfgfXq8sUiAltXuyZJti88K59JHvC2r9HavWG00dgpPm050'


class Address(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='address')
    city        = models.CharField(max_length=50)
    street      = models.CharField(max_length=50)
    phone       = PhoneField(help_text='Contact phone')


class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='billing_profile')
    email       = models.EmailField()
    address     = models.ForeignKey(Address, null=True, blank=True, on_delete = models.CASCADE)
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank = True)


    def __str__(self):
        return self.email

def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id:
        customer = stripe.Customer.create(
            email = instance.email
        )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender = BillingProfile)

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)
