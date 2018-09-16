# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mapping.models import LanguagesMapping

class LanguagesMappingAdmin(admin.ModelAdmin):


    class Meta:
        model = LanguagesMapping

admin.site.register(LanguagesMapping, LanguagesMappingAdmin)

