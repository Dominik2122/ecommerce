from django.db import models
from django.db.models.signals import pre_save
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self.db)
    def features(self):
        return self.get_queryset().filter(featured=True)


class Product(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default = 0)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = ProductManager()

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    i = 1
    while not instance.slug:
        instance.slug = instance.name + '-' + str(i)
        i +=0

#2.12
pre_save.connect(product_pre_save_receiver, sender = Product)
