# Generated by Django 4.2.2 on 2023-07-12 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('-created_at',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]