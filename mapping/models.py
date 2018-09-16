# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class LanguagesMapping(models.Model):

    LT_HINDI = 10
    LT_MARATHI = 20
    LT_TELUGU = 40
    LT_KANNADA = 60
    LT_MALYALAM = 80
    LT_KONKANI = 100

    LANGUAGE_TYPE = (
        (LT_HINDI, 'Hindi'),
        (LT_MARATHI, 'Marathi'),
        (LT_TELUGU, 'Telugu'),
        (LT_MALYALAM, 'Malyalam'),
        (LT_KONKANI, 'Konkani'),
    )

    REV_LANGUAGE_TYPE = {
        'hindi': LT_HINDI,
        'marathi': LT_MARATHI,
        'telugu': LT_TELUGU,
        'malyalam': LT_MALYALAM,
        'konkani': LT_KONKANI
    }

    lang_type = models.PositiveSmallIntegerField(
        choices=LANGUAGE_TYPE, blank=False, null=False, db_index=True
    )
    root_w = models.CharField(
        max_length=255, blank=False, null=False
    )
    mapping = models.ManyToManyField('self', related_name='mapping')


    class Meta:
        unique_together = (('root_w', 'lang_type' ),)

    def __str__(self):
        return '<{}:{}>'.format(self.pk, unicode(self.root_w))
