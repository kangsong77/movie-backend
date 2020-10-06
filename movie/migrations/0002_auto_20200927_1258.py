# Generated by Django 3.1 on 2020-09-27 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviecast',
            name='tmdb_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast', to='movie.moviedetail'),
        ),
    ]
