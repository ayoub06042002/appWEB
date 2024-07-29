# Generated by Django 5.0.7 on 2024-07-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('Tonnage_dosage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Humidite_entree', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Production_totale', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('HM', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Cs_Gas', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Cs_gazoline', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Cs_Fuel', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
        ),
    ]
