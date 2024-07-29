from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Performance(models.Model):
    date = models.DateField(null=True, blank=True)
    Tonnage_dosage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Humidite_entree = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Production_totale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    HM = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Cs_Gas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Cs_gazoline = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Cs_Fuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Performance: {self.Tonnage_dosage}, {self.Humidite_entree}, {self.Production_totale}, {self.HM}, {self.Cs_Gas}, {self.Cs_gazoline}, {self.Cs_Fuel}"



