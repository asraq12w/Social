# Generated by Django 5.0.4 on 2024-04-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0004_ticket_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='message',
            field=models.TextField(),
        ),
    ]