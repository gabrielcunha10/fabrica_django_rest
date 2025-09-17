from django.db import models

class Usuario(models.Model):
    nome = models.CharField()
    email = models.EmailField(unique=True)
    senha = models.CharField() 
