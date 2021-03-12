from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save, post_save
import random
import string
# Create your models here.
ORDER_STATUS_CHOICES = (
    ('created', 'Created'), ('paid', "Paid"), ("shipped", "Shipped"), ("refunded", "Refunded")
)


class Order(models.Model):
    order_id        = models.CharField(max_length=50, blank=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=50, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=5.99, max_digits = 100, decimal_places = 2)
    order_total     = models.DecimalField(default=0.00, max_digits = 100, decimal_places = 2)

    def __str__(self):
        return self.order_id

def random_str(size=7, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        order_id = random_str()
        obj_exist = Order.objects.filter(order_id=order_id)
        if obj_exist:
            return pre_save_create_order_id(sender, instance, *args, **kwargs)
        else:
            cart_obj = instance.cart
            instance.order_total = cart_obj.total
            instance.order_id = order_id
            instance.save()
            return instance

def post_save_cart_total(sender, instance, *args, **kwargs):
    cart_obj = instance
    cart_total = cart_obj.total
    cart_id = cart_obj.id
    qs = Order.objects.filter(cart__id =cart_id)
    if qs.count()==1:
        order_obj = qs.first()
        order_obj.order_total = cart_total
        order_obj.save()


post_save.connect(post_save_cart_total, sender=Cart)
pre_save.connect(pre_save_create_order_id, sender=Order)
