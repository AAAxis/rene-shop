from django.db import models
from .misc import get_conversion_rate
from storages.backends.gcloud import GoogleCloudStorage


class GoogleCloudMediaStorage(GoogleCloudStorage):
    default_acl = 'publicRead'
    file_overwrite = False
    bucket_name = 'rene-shop'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ManyToManyField(Category)
    is_3d = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    
    def convert_price(self, to_currency):
        if to_currency == 'USD':
            return self.price  # No conversion needed
        rate = get_conversion_rate('USD', to_currency)
        return self.price * rate


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.size} - {self.product.name}"


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='product_images/', storage=GoogleCloudMediaStorage())

    def __str__(self):
        return f"Photo for {self.product.name}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"
