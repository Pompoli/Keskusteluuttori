# Generated by Django 3.0.8 on 2020-10-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_line_answerto_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='answerTo_extra',
            field=models.ManyToManyField(blank=True, related_name='_line_answerTo_extra_+', to='chat.Line'),
        ),
    ]
