# Generated by Django 3.1.3 on 2020-11-19 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue_system', '0002_auto_20201118_2123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seatrank',
            old_name='seat_col',
            new_name='col',
        ),
        migrations.RenameField(
            model_name='seatrank',
            old_name='seat_row',
            new_name='row',
        ),
    ]
