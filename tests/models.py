from django.db import models


class Pic(models.Model):
    img = models.TextField()


class Size(models.Model):
    name = models.TextField()
    picture = models.ForeignKey(Pic, models.CASCADE, null=True)


class Product(models.Model):
    name = models.TextField()
    sizes = models.ManyToManyField(Size)
