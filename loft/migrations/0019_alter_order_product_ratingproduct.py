# Generated by Django 5.1.1 on 2024-11-02 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0018_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.product', verbose_name='Покупатель'),
        ),
        migrations.CreateModel(
            name='RatingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Оценка')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество оценок')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='loft.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
    ]
