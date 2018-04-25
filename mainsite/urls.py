#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-18 10:31:06
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_info_action, name="company_info"),
    path('company-info-commit/', views.company_info_commit, name="company_info_commit" ),
    path('company-basic-info-action/<int:cic_id>', views.company_basic_info_action, name="company_basic_info_action"),
    path('company-basic-info-commit/', views.company_basic_info_commit, name="company_basic_info_commit"),
    path('que-form-action/<int:bif_id>', views.enterprise_need_action, name="enterprise_need_action"),
]
