# Generated by Django 3.2.13 on 2022-05-09 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_room', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('house_rent', models.DecimalField(decimal_places=4, max_digits=10)),
                ('house_image', models.ImageField(blank=True, null=True, upload_to='House/images/')),
                ('status', models.BooleanField(default=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('house_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agent.type')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agent.room')),
            ],
        ),
        migrations.CreateModel(
            name='Agent_House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('house', models.ManyToManyField(to='Agent.House')),
            ],
        ),
    ]
