# Generated by Django 5.1.4 on 2024-12-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_remove_book_category_book_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='library.category'),
        ),
    ]
