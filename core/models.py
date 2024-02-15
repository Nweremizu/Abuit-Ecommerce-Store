from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from abuit_user.models import User

AVAliABLITY_CHOICES = (
    ("In Stock", "In Stock"),
    ("Out of Stock", "Out of Stock"),
    ("Pre-Order", "Pre-Order"),
    ("Coming Soon", "Coming Soon"),
)

RATING_CHOICES = (
    ("1", "★☆☆☆☆"),
    ("2", "★★☆☆☆"),
    ("3", "★★★☆☆"),
    ("4", "★★★★☆"),
    ("5", "★★★★★"),
)


# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet='abcdefghijk1234567890')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Book(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="bk")

    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=100, null=False, blank=False, default="Abuit")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="books")
    description = models.TextField(null=True, blank=True, default=f"A Wonderfull Book called {title}")
    price = models.DecimalField(max_digits=99999, decimal_places=2)
    old_price = models.DecimalField(max_digits=99999, decimal_places=2, default="2000")

    publication_year = models.IntegerField(default=2023)
    availablity = models.CharField(max_length=40, choices=AVAliABLITY_CHOICES, default="Pre-Order")
    in_stock = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "books"

    def book_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percent_discount(self):
        return (self.price / self.old_price) * 100

    def is_new(self):
        return self.date_added.year == timezone.now().year


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=99999, decimal_places=2, default="0.00")
    paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    image = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=99999, decimal_places=2, default="0.00")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_item_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50" />' % (self.image))

    def __str__(self):
        return self.invoice_number



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
