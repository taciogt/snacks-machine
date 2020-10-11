from django.db import models


class SnackModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.FloatField()
    available_quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Snack: {self.name} (R$ {self.price:.2f})'

    def as_dict(self):
        return {field.name: getattr(self, field.name)
                for field in self._meta.get_fields()
                if field.name != 'id'}
