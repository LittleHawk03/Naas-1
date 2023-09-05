# Generated by Django 4.2.4 on 2023-09-05 03:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
                ('notification_type', models.CharField(choices=[('email', 'Mail'), ('webhook', 'Webhook'), ('sms', 'SMS'), ('slack', 'Slack')], default='email', max_length=30)),
                ('isSubscribed', models.BooleanField(default=False)),
                ('nc_object_id', models.PositiveIntegerField()),
                ('nc_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nc_content_type', to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='EmailNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('email_field', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='SlackNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('incoming_webhook', models.URLField(validators=[django.core.validators.URLValidator])),
                ('slack_channel', models.CharField(max_length=100)),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='SMSNotificatonChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('sms_field', models.CharField(blank=True, max_length=30)),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
        migrations.CreateModel(
            name='WebhookNotificationChannel',
            fields=[
                ('notificationchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notification_channel.notificationchannel')),
                ('webhook_url', models.URLField(validators=[django.core.validators.URLValidator])),
            ],
            bases=('notification_channel.notificationchannel',),
        ),
    ]
