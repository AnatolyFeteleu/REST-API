from django.db import models


# Models
class District(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class EnterpriseNetwork(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Enterprise(models.Model):
    district = models.ManyToManyField(District)
    name = models.CharField(max_length=25)
    description = models.TextField()
    affiliation = models.ManyToManyField(EnterpriseNetwork)

    def __str__(self):
        return '{}'.format(self.name)


class Merch(models.Model):
    name = models.CharField(max_length=25)
    merch = models.ManyToManyField(
        Enterprise,
        through='Merchandise',
    )


# Промежуточная модель
class Merchandise(models.Model):
    category = models.ForeignKey(Category)
    price = models.IntegerField()
    enterprise = models.ForeignKey(Enterprise)
    merch = models.ForeignKey(Merch)
