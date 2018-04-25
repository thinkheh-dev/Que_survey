#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-18 10:34:03
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django.utils import timezone
from django.shortcuts import render
from mainsite.models import Questionnaire

def index(request):
    today = timezone.now()
    nearly_que = Questionnaire.objects.filter(create_time__lt = today).first()
    context = {}
    context['nearly_que'] = nearly_que
    return render(request, 'questions_index.html', context)
