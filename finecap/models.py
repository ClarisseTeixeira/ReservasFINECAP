from django.db import models

# Create your models here.

from django.db import models

# Create your models here.



class Stand(models.Model):
    localizacao = models.CharField(max_length=250)
    valor = models.DecimalField(max_digits=10, decimal_places=2) 
    def __str__(self):
        return self.localizacao

class Reserva(models.Model):
    cnpj = models.CharField(max_length=250)
    nome_empresa = models.CharField(max_length=250)
    categoria_empresa = models.CharField(max_length=250)
    quitato = models.BooleanField(default=False)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)