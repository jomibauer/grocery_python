# Generated by Django 3.1.1 on 2020-12-09 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_shopuser_recipes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='recipes',
            field=models.CharField(default='"lololol"', max_length=200),
        ),
    ]
