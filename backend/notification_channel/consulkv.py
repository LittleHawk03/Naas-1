import consul
from rest_framework.response import Response
from rest_framework import status

def put_consul_kv(notification_channel): 
    consul_host = "116.103.226.93"
    consul_port = 8500
    c = consul.Consul(host=consul_host,port=consul_port)
    user_id = notification_channel.user.id
    notification_type = notification_channel.notification_type
    channel_id = notification_channel.id
    if notification_type == 'email':
        email_field = notification_channel.email_field
        c.kv.put(f"users/{ user_id }/alarms/email/{ channel_id }/receiver", email_field)
    elif notification_type == 'webhook':
        webhook_url = notification_channel.webhook_url
        c.kv.put(f"users/{ user_id }/alarms/webhook/{ channel_id }/url", webhook_url)
    elif notification_type == 'sms':
        sms_field = notification_channel.sms_field
        c.kv.put(f"users/{ user_id }/alarms/sms/{ channel_id }/sms_field", sms_field[1:])
    elif notification_type == 'slack':
        incoming_webhook = notification_channel.incoming_webhook
        slack_channel = notification_channel.slack_channel
        slack_username = notification_channel.slack_username
        c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/username", slack_username)
        c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/channel", slack_channel)
        c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url", incoming_webhook)
    elif notification_type == 'telegram':
        tele_webhook = notification_channel.tele_webhook
        c.kv.put(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook", tele_webhook)
    else:
        return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
    

def delete_consul_kv(notification_channel):
    consul_host = "116.103.226.93"
    consul_port = 8500
    c = consul.Consul(host=consul_host,port=consul_port)
    user_id = notification_channel.user.id
    channel_id = notification_channel.id
    if notification_channel.notification_type == 'email':
        c.kv.delete(f"users/{ user_id }/alarms/email/{ channel_id }/receiver")
    elif notification_channel.notification_type == 'webhook':
        c.kv.delete(f"users/{ user_id }/alarms/webhook/{ channel_id }/url")
    elif notification_channel.notification_type == 'sms':
        c.kv.delete(f"users/{ user_id }/alarms/sms/{ channel_id }/url")
    elif notification_channel.notification_type == 'slack':
        c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/username")
        c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/channel")
        c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url")
    elif notification_channel.notification_type == 'telegram':
        c.kv.delete(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook")
    else:
        return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
    
    
def update_consul_kv(notification_channel, object_request):
        consul_host = "116.103.226.93"
        consul_port = 8500
        c = consul.Consul(host=consul_host,port=consul_port)
        user_id = notification_channel.user.id
        channel_id = notification_channel.id
        if notification_channel.notification_type == 'email':
            email_field = object_request['email_field']
            c.kv.put(f"users/{ user_id }/alarms/email/{ channel_id }/receiver", email_field)
        elif notification_channel.notification_type == 'webhook':
            webhook_url = object_request['webhook_url']
            c.kv.put(f"users/{ user_id }/alarms/webhook/{ channel_id }/url", webhook_url)
        elif notification_channel.notification_type == 'sms':
            sms_field = object_request['sms_field']
            c.kv.put(f"users/{ user_id }/alarms/sms/{ channel_id }/url", sms_field)
        elif notification_channel.notification_type == 'slack':
            incoming_webhook = object_request['incoming_webhook']
            slack_channel = object_request['slack_channel']
            slack_username = object_request['slack_username']
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/username", slack_username)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/channel", incoming_webhook)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url", slack_channel)
        elif notification_channel.notification_type == 'telegram':
            tele_webhook = notification_channel.tele_webhook
            c.kv.put(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook", tele_webhook)
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)