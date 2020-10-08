# Generated by Django 2.1.5 on 2019-02-12 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_supertrait_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supertrait',
            name='group',
        ),
        migrations.AlterField(
            model_name='supertrait',
            name='opposite',
            field=models.CharField(default='x', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]