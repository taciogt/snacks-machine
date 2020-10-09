from django.db import models


class SnackModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'Snack: {self.name} (R$ {self.price:.2f})'

    def as_dict(self):
        return {
            'name': self.name,
            'price': self.price
        }
