from django.db import models


class Pic(models.Model):
    img = models.TextField()


class Size(models.Model):
    name = models.TextField()
    picture = models.ForeignKey(Pic, models.DO_NOTHING, null=True)


class Product(models.Model):
    name = models.TextField()
    sizes = models.ManyToManyField(Size)
    picture = models.ForeignKey(Pic, models.DO_NOTHING)


class Description(models.Model):
    text = models.TextField()
    product = models.OneToOneField(Product, models.CASCADE)
