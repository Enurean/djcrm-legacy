from django.db import models



class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"