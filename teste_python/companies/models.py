from django.db import models
from accounts.models import User


class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies', null=True, blank=True)
    users = models.ManyToManyField(User, related_name='companies')
    cnpj = models.CharField(max_length=20, unique=True)
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_fantasia
