# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mapping.forms import AddMap, AddWord
from mapping.models import LanguagesMapping


def add_map(request):
    form = AddMap(request.POST or None)
    template_values = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            res, msg = form.save()
            template_values['msg'] = msg
            if res:
                template_values['form'] = AddMap()

    return render(request, 'addmap.html', template_values)

def add_word(request, rw=None):
    form = AddWord(request.POST or None)
    template_values = {'form': form}

    if request.method == 'POST':
        form = AddWord(request.POST)
        if form.is_valid():
            res, msg = form.save()
            template_values['msg'] = msg
            if res:
                template_values['form'] = AddWord()

    return render(request, 'add.html', template_values)

def list_outlier(request):
    outliers = LanguagesMapping.objects.filter(mapping=None)
    return render(request, 'list_outlier.html', {'outliers': outliers})

def view_actions(request):
    tv = {'languages': LanguagesMapping.REV_LANGUAGE_TYPE.keys()}
    return render(request, 'view_actions.html', tv)

def map_lang(request, language):
    langcode = LanguagesMapping.REV_LANGUAGE_TYPE.get(language)
    if langcode:
        nmw = LanguagesMapping.objects.exclude(
            lang_type=langcode
        ).exclude(mapping__lang_type=langcode)
    return render(request, 'list_outlier.html', {'outliers': nmw})
