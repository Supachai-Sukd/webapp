# Generated by Django 2.2.5 on 2019-09-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_auto_20190917_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('FA', 'Fashion'), ('EL', 'Electronics'), ('IT', 'IT & Gadget')], max_length=2),
        ),
    ]
