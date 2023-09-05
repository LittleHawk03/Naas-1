# Generated by Django 4.2.4 on 2023-09-05 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=30, null=True, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=15)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField()),
                ('account_create_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
