# Generated by Django 3.0.8 on 2020-10-07 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20201007_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationfunction',
            name='trait',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='functions', to='chat.SuperTrait'),
        ),
    ]
