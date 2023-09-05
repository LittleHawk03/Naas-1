# Generated by Django 4.2.4 on 2023-09-05 08:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('notification_type', models.CharField(choices=[('email', 'Mail'), ('webhook', 'Webhook'), ('sms', 'SMS'), ('slack', 'Slack'), ('telegram', 'Telegram')], default='email', max_length=30)),
                ('isSubscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('webhook_url', models.URLField(validators=[django.core.validators.URLValidator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhook_notification_channels', to='users.users')),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='TelegramNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('tele_webhook', models.URLField(validators=[django.core.validators.URLValidator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tele_notification_channels', to='users.users')),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='SMSNotificatonChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('sms_field', models.CharField(blank=True, max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sms_notification_channels', to='users.users')),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='SlackNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('slack_username', models.CharField(default='Prometheus', max_length=100)),
                ('incoming_webhook', models.URLField(validators=[django.core.validators.URLValidator])),
                ('slack_channel', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_notification_channels', to='users.users')),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='EmailNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('email_field', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_notification_channels', to='users.users')),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
    ]
