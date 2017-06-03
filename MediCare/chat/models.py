from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, related_name='+')
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+')

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('date',)
        db_table = 'messages_message'

    def __unicode__(self):
        return self.message

    @staticmethod
    def receive_message(from_user,message):
        message=message[:1000]
        user_message=Message(message=message,
                             user=from_user,
                             conversation=from_user)
        user_message.save()
        return user_message

    @staticmethod
    def send_message(to_user, message):
        message = message[:1000]
        current_user_message = Message(message=message,
                                       user=to_user,
                                       conversation=to_user)
        current_user_message.save()

        return current_user_message

    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(
            user=user).values('conversation').annotate(
                last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                })

        return users
