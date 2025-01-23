from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator




class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(90)],
                                                                            null=True, blank=True,)
    phone_number = PhoneNumberField()
    ROLE_CHOICES = (
        ('клиент', 'клиент',),
        ('курьер', 'курьер'),
        ('владелец магазина', 'владелец магазина')

    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=32, default='клиент')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name

class Store(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner_store')
    store_image = models.ImageField(upload_to='store_image/')
    store_name = models.CharField(max_length=65)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_str')
    address = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.store_name}'


class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contact')
    title = models.CharField(max_length=16, null=True, blank=True)
    phone_number = PhoneNumberField()
    website = models.URLField(unique=True, verbose_name="Веб-сайт", null=True, blank=True)

    def __str__(self):
        return f'{self.store}'



class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    product_image = models.ImageField(upload_to='product_image/')
    product_name = models.CharField(max_length=32)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product_name}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart}'

    def get_total_price(self):
        return self.product.price * self.quantity



class ProductCombo(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_combo')
    combo_name = models.CharField(max_length=32)
    combo_image = models.ImageField()
    combo_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.combo_name}'


class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_orders')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
    STATUS_CHOICES = (
        ('в обработке', 'в обработке'),
        ('Отправлен', ' Отправлен'),
        ('Доставлен', 'Доставлен'),
        ('отменён', ' отменён')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='в обработке')
    delivery_address = models.CharField(max_length=65)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.products}, {self.status}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_name')
    status = models.BooleanField(verbose_name='статус курьера')
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_set')

    def __str__(self):
        return f'{self.current_orders}'


class RatingCourier(models.Model):
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.courier}, {self.stars}'


    def get_avg_rating(self):
       ratings = self.ratings.all()
       if ratings.exists():
          return round(sum([i.stars for i in ratings]) / ratings.count(), 1)
       return 0


    def get_count_people(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.count()
        return 0


class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_review')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.store}, {self.rating}'

