# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cleaning',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False, help_text='Did you clean?')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='cleanings')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
