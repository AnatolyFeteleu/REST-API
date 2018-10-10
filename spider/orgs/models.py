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


class Merchandise(models.Model):
    name = models.CharField(max_length=25)
    category = models.ForeignKey(Category)
    price = models.IntegerField()
    enterprise = models.ForeignKey(Enterprise)
    sales_in = models.ManyToManyField(EnterpriseNetwork)

    def __str__(self):
        return '{} ({})'.format(self.name, self.category)
