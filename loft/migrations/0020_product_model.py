# Generated by Django 5.1.1 on 2024-11-02 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0019_alter_order_product_ratingproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Модель'),
        ),
    ]
