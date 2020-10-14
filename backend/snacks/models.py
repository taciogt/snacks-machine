from django.db import models


class SnackModel(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=128, unique=True)
    price = models.FloatField(verbose_name='Preço')
    available_quantity = models.PositiveSmallIntegerField(verbose_name='Quantidade em estoque', default=0)

    class Meta:
        verbose_name = 'Snack'
        verbose_name_plural = 'Snacks'

    def __str__(self):
        return f'Snack: {self.name} (R$ {self.price:.2f})'

    def as_dict(self):
        return {field.name: getattr(self, field.name)
                for field in self._meta.get_fields()
                if field.name != 'id'}
