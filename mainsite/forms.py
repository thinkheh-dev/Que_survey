#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-19 15:20:15
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$
from django import forms
from django.forms import widgets
from django.forms import fields
from .models import InformationOfPerson, CompanyBasicInfo, Questionnaire, Questions, Questions_Char, Option

class InfoPersonForm(forms.ModelForm):

    SEX_CHOICES = (
        (1,"男"),
        (2,"女"),
    )

    AGE_CHOICES = (
        (1,"30岁以下"),
        (2,"31-40岁"),
        (3,"41-50岁"),
        (4,"51岁以上"), 
    )

    EDUCATION_CHOICES = (
        (1,"初中"),
        (2,"高中(中专)"),
        (3,"大专"),
        (4,"本科"),
        (5,"本科以上"),
    )

    company_name = forms.CharField(error_messages={'required':'企业名称不能为空'},
                                    widget = widgets.TextInput(attrs={'placeholder':"请输入企业全称",'class':"form-control"}))

    social_credit_code = forms.CharField(max_length=18, error_messages={'required':'社会统一信用代码不能为空'}, 
                                          widget =widgets.TextInput(attrs={'class':"form-control"}))

    established_time = forms.DateField(error_messages={'required':'成立时间不能为空'}, widget=widgets.DateInput(attrs={'class':"form-control",'type':"date"}))
    responsible_person = forms.CharField(error_messages={'required':'负责人不能为空'}, widget=widgets.TextInput(attrs={'class':"form-control"}))
    #job_title = forms.CharField(error_messages={'required':'职务或职称不能为空'}, widget=widgets.TextInput(attrs={'class':"form-control"}))
    sex = forms.ChoiceField(error_messages={'required':'性别不能为空'}, choices=SEX_CHOICES,widget=widgets.RadioSelect())
    age = forms.ChoiceField(error_messages={'required':'年龄不能为空'}, choices=AGE_CHOICES,widget=widgets.RadioSelect())
    degree_of_education = forms.ChoiceField(error_messages={'required':'文化程度不能为空'}, choices=EDUCATION_CHOICES,widget=widgets.RadioSelect())
    phone = forms.CharField(max_length=11, error_messages={'required':'手机号不能为空'}, widget=widgets.TextInput(attrs={'placeholder':"为方便联系，请您填写手机号。", 'class':"form-control"}))
    political_status = forms.CharField(error_messages={'required':'政治面貌不能为空'}, widget=widgets.TextInput(attrs={'class':"form-control"}))
    company_registered_address = forms.CharField(error_messages={'required':'企业注册地址不能为空'}, widget=widgets.TextInput(attrs={'class':"form-control"}))
    website_url = forms.URLField(error_messages={'required':'企业网址不能为空'}, widget=widgets.URLInput(attrs={'placeholder':"网址、微信公众号全称、博客网址", 'class':"form-control"}))
    email_adress = forms.EmailField(error_messages={'required':'email地址不能为空'}, widget=widgets.EmailInput(attrs={'class':"form-control"}))
    company_profiles = forms.CharField(widget=widgets.Textarea(attrs={'class':"form-control",'rows':"3"}))

    # 使用ModelForm时的内部类
    class Meta:
        model = InformationOfPerson
        exclude = ['questionnaire']

class CompanyBasicInfoForm(forms.ModelForm):
    ORG_KIND = (
        (1,"股份有限公司"),
        (2,"有限责任公司"),
        (3,"非公司制企业"),
        (4,"私营独资企业"),
        (5,"私营合伙企业"),
        (6,"其他")
    )

    IND_CLASS = (
        (1,"农业"),
        (2,"林业"),
        (3,"水利"),
        (4,"电力"),
        (5,"热力"),
        (6,"批发"),
        (7,"住宿"),
        (8,"采矿业"),
        (9,"制造业"),
        (10,"建筑业"),
        (11,"零售业"),
        (12,"餐饮业"),
        (13,"物业管理"),
        (14,"房地产业"),
        (15,"信息传输业"),
        (16,"交通运输业"),
        (17,"畜牧业和渔业"),
        (18,"仓诸和邮电业"),
        (19,"租赁和商务服务业"),
        (20,"文化、体育和娱乐业"),
        (21,"科学研究和技术服务业"),
        (22,"软件和信息技术服务业"),
        (23,"燃气及水生产和供应业"),
        (24,"环境和公共设施管理业"),
        (25,"居民服务、修理和其他服务业"),
        (26,"其他未列明行业")
    )

    organization_category = forms.ChoiceField(choices=ORG_KIND,widget=widgets.Select(attrs={'class':"form-control"}))
    industry_classification = forms.ChoiceField(choices=IND_CLASS, widget=widgets.Select(attrs={'class':"form-control"}))

    registered_fund = forms.CharField(max_length=10, error_messages={'required':'注册资金不能为空'}, 
                                      widget=widgets.TextInput(attrs={'class':"form-control"}))

    annual_revenue = forms.CharField(max_length=10, error_messages={'required':'企业年营业收入不能为空'}, 
                                     widget=widgets.TextInput(attrs={'class':"form-control"}))

    current_number_of_employees = forms.CharField(max_length=5, error_messages={'required':'现从业人数不能为空'}, 
                                                  widget=widgets.TextInput(attrs={'class':"form-control"}))

    college_degree_or_above = forms.CharField(max_length=5, error_messages={'required':'大专及以上学历人数不能为空'}, 
                                              widget=widgets.TextInput(attrs={'class':"form-control"}))

    intermediate_and_above_titles = forms.CharField(max_length=5, error_messages={'required':'中级及以上职称人数不能为空'}, 
                                                    widget=widgets.TextInput(attrs={'class':"form-control"}))

     # 使用ModelForm时的内部类
    class Meta:
        model = CompanyBasicInfo
        exclude = ['info_of_company']

