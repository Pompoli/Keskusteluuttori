# Generated by Django 3.0.8 on 2020-10-07 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20201007_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='answerTo_extra',
            field=models.ManyToManyField(blank=True, null=True, related_name='_line_answerTo_extra_+', to='chat.Line'),
        ),
    ]
