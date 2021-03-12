from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self.db)
    def features(self):
        return self.get_queryset().filter(featured=True)


GROUPS_CHOICES = (
    ('women', 'Women'), ('men', "Men"), ("kids", "Kids"), ("sport", "Sports")
)

TAGS_CHOICES = (
    ('t-shirt', 'T-Shirt'), ('shirt', "Shirt"), ("jeans", "Jeans"), ("shoes", "Shoes"), ('accessories', "Accessories"),
    ('bike', 'Bike'), ('weights', "Weights")
)


class Tags(models.Model):
    name = models.CharField(max_length = 255, choices=TAGS_CHOICES, unique=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length = 255, choices=GROUPS_CHOICES, unique=True)
    tags = models.ManyToManyField(Tags,related_name="tags")
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default = 0)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    tags = models.ForeignKey(Tags, blank=True, null=True,on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("product:details", kwargs={'slug':self.slug})

    def __str__(self):
        return self.title




def product_pre_save_receiver(sender, instance, *args, **kwargs):
    i = 1
    while not instance.slug:
        instance.slug = instance.name + '-' + str(i)
        i +=0

#2.12
pre_save.connect(product_pre_save_receiver, sender = Product)
