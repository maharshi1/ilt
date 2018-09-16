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
        form = AddMap(request.POST)
        if form.is_valid():
            res, msg = form.save()
            template_values['msg'] = msg
            if res:
                template_values['form'] = AddMap()

    return render(request, 'addmap.html', template_values)

def add_word(request):
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
