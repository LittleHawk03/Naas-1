# Generated by Django 4.2.4 on 2023-09-05 05:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_field', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
            ],
        ),
        migrations.CreateModel(
            name='NotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('email', 'Mail'), ('webhook', 'Webhook'), ('sms', 'SMS'), ('slack', 'Slack')], default='email', max_length=30)),
                ('isSubscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SlackNotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incoming_webhook', models.URLField(validators=[django.core.validators.URLValidator])),
                ('slack_channel', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SMSNotificatonChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_field', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookNotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webhook_url', models.URLField(validators=[django.core.validators.URLValidator])),
            ],
        ),
    ]
