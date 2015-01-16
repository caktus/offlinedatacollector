# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hygiene', '0002_cleaning_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cleaning',
            unique_together=set([('user', 'date')]),
        ),
    ]
