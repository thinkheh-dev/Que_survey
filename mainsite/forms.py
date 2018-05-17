#/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-19 15:20:15
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$
from django import forms
import re
from django.forms import widgets
from django.forms import fields
from .models import InformationOfPerson, CompanyBasicInfo, Questionnaire, Questions, Option, AnswerText

class InfoPersonForm(forms.ModelForm):

    COUNTY_CHOICES = (
        (1,"个旧市"),
        (2,"开远市"),
        (3,"蒙自市"),
        (4,"建水县"),
        (5,"石屏县"),
        (6,"弥勒市"),
        (7,"泸西县"),
        (8,"红河县"),
        (9,"元阳县"),
        (10,"绿春县"),
        (11,"屏边县"),
        (12,"金平县"),
        (13,"河口县"),
    )

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


    county_name = forms.ChoiceField(label="您的公司所在县份", choices=COUNTY_CHOICES, widget=forms.Select(attrs={'class':"form-control"}))
    company_name = forms.CharField(label="企业名称", error_messages={'required':'企业名称不能为空'}, widget = forms.TextInput(attrs={'placeholder':"请输入企业全称",'class':"form-control"}))
    social_credit_code = forms.CharField(label="社会统一信用代码", max_length=18, error_messages={'required':'社会统一信用代码不能为空'}, widget =forms.TextInput(attrs={'class':"form-control"}))
    established_time = forms.DateField(label="成立时间", error_messages={'required':'成立时间不能为空'}, widget=forms.DateInput(attrs={'class':"form-control",'type':"date"}))
    responsible_person = forms.CharField(label="负责人", error_messages={'required':'负责人不能为空'}, widget=forms.TextInput(attrs={'class':"form-control"}))
    #job_title = forms.CharField(error_messages={'required':'职务或职称不能为空'}, widget=forms.TextInput(attrs={'class':"form-control"}))
    sex = forms.ChoiceField(label="性别", error_messages={'required':'性别不能为空'}, choices=SEX_CHOICES,widget=forms.RadioSelect(attrs={'class':"radio-inline"}))
    age = forms.ChoiceField(label="年龄", error_messages={'required':'年龄不能为空'}, choices=AGE_CHOICES,widget=forms.RadioSelect(attrs={'class':"radio-inline"}))
    degree_of_education = forms.ChoiceField(label="文化程度", error_messages={'required':'文化程度不能为空'}, choices=EDUCATION_CHOICES,widget=forms.RadioSelect(attrs={'class':"radio-inline "}))
    phone = forms.CharField(label="联系电话", max_length=11, error_messages={'required':'手机号不能为空'}, widget=forms.TextInput(attrs={'placeholder':"为方便联系，请您填写手机号。", 'class':"form-control"}))
    political_status = forms.CharField(required=False, label="政治面貌", error_messages={'required':'政治面貌不能为空'}, widget=forms.TextInput(attrs={'class':"form-control"}))
    company_registered_address = forms.CharField(required=False, label="企业注册地址", error_messages={'required':'企业注册地址不能为空'}, widget=forms.TextInput(attrs={'class':"form-control"}))
    website_url = forms.URLField(required=False, label="企业网址", error_messages={'required':'企业网址不能为空'}, widget=forms.URLInput(attrs={'placeholder':"请输入网址全称：例如 http://www.thinkheh.cn", 'class':"form-control"}))
    email_adress = forms.EmailField(required=False, label="Email地址", error_messages={'required':'email地址不能为空'}, widget=forms.EmailInput(attrs={'class':"form-control"}))
    company_profiles = forms.CharField(required=False, label="企业简介", widget=forms.Textarea(attrs={'class':"form-control",'rows':"3"}))

    # 使用ModelForm时的内部类
    class Meta:
        model = InformationOfPerson
        exclude = ['questionnaire']

    #效验公司名称是否存在
    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        if InformationOfPerson.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError('您的公司已经做过调查，无需再次填写')
        else:
            self.cleaned_data['company_name'] = company_name
        return company_name
        
    #效验社会统一信用代码是否存在并且无误
    def clean_social_credit_code(self):
        social_credit_code = self.cleaned_data['social_credit_code']
        pattern = re.compile(r'[^_IOZSVa-z\W]{2}\d{6}[^_IOZSVa-z\W]{10}')
        if pattern.match(social_credit_code) != None:
            if InformationOfPerson.objects.filter(social_credit_code=social_credit_code).exists():
                raise forms.ValidationError('您输入的社会统一信用代码已经存在')
            else:
                self.cleaned_data['social_credit_code'] = social_credit_code
        else:
            raise forms.ValidationError('您输入的社会统一信用代码有误')
        return social_credit_code

    #效验手机号是否存在并且无误
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = re.compile(r'((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})')
        if pattern.match(phone) != None:
            if InformationOfPerson.objects.filter(phone=phone).exists():
                raise forms.ValidationError('您输入的手机号码已经存在')
            else:
                self.cleaned_data['phone'] = phone
        else:
            raise forms.ValidationError('请输入正确的手机号码')
        return phone



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

    organization_category = forms.ChoiceField(choices=ORG_KIND,widget=forms.Select(attrs={'class':"form-control"}))
    industry_classification = forms.ChoiceField(choices=IND_CLASS, widget=forms.Select(attrs={'class':"form-control"}))

    registered_fund = forms.CharField(max_length=10, error_messages={'required':'注册资金不能为空'}, 
                                      widget=forms.TextInput(attrs={'class':"form-control"}))

    annual_revenue = forms.CharField(required=False, max_length=10, error_messages={'required':'企业年营业收入不能为空'}, 
                                     widget=forms.TextInput(attrs={'class':"form-control"}))

    current_number_of_employees = forms.CharField(max_length=5, error_messages={'required':'现从业人数不能为空'}, 
                                                  widget=forms.TextInput(attrs={'class':"form-control"}))

    college_degree_or_above = forms.CharField(required=False, max_length=5, error_messages={'required':'大专及以上学历人数不能为空'}, 
                                              widget=forms.TextInput(attrs={'class':"form-control"}))

    intermediate_and_above_titles = forms.CharField(required=False, max_length=5, error_messages={'required':'中级及以上职称人数不能为空'}, 
                                                    widget=forms.TextInput(attrs={'class':"form-control"}))

     # 使用ModelForm时的内部类
    class Meta:
        model = CompanyBasicInfo
        exclude = ['info_of_company']

    #效验是否为数字类型
    def clean_registered_fund(self):
        registered_fund = self.cleaned_data['registered_fund']

        try:
            registered_fund_zh = int(registered_fund)
        except ValueError as e:
            raise forms.ValidationError('注册资金只能为正整数')
        else:
            self.cleaned_data['registered_fund'] = registered_fund_zh

        return registered_fund

    #效验是否为数字类型
    def clean_annual_revenue(self):
        annual_revenue = self.cleaned_data['annual_revenue']

        try:
            annual_revenue_zh = int(annual_revenue)
        except ValueError as e:
            raise forms.ValidationError('企业年收入只能为正整数')
        else:
            self.cleaned_data['annual_revenue'] = annual_revenue_zh

        return annual_revenue

    #效验是否为数字类型
    def clean_current_number_of_employees(self):
        current_number_of_employees = self.cleaned_data['current_number_of_employees']

        try:
            current_number_of_employees_zh = int(current_number_of_employees)
        except ValueError as e:
            raise forms.ValidationError('现从业人数只能为正整数')
        else:
            self.cleaned_data['current_number_of_employees'] = current_number_of_employees_zh

        return current_number_of_employees

    #效验是否为数字类型
    def clean_college_degree_or_above(self):
        college_degree_or_above = self.cleaned_data['college_degree_or_above']

        try:
            college_degree_or_above_zh = int(college_degree_or_above)
        except ValueError as e:
            raise forms.ValidationError('大专及以上学历人数只能为正整数')
        else:
            self.cleaned_data['college_degree_or_above'] = college_degree_or_above_zh

        return college_degree_or_above

    #效验是否为数字类型
    def clean_intermediate_and_above_titles(self):
        intermediate_and_above_titles = self.cleaned_data['intermediate_and_above_titles']

        try:
            intermediate_and_above_titles_zh = int(intermediate_and_above_titles)
        except ValueError as e:
            raise forms.ValidationError('中级及以上职称人数只能为正整数')
        else:
            self.cleaned_data['intermediate_and_above_titles'] = intermediate_and_above_titles_zh

        return intermediate_and_above_titles

class QuestionsCharForm(forms.ModelForm):
    # 使用ModelForm时的内部类

    question_char_content = forms.CharField(label="您的企业还有哪些好的建议和补充", widget=forms.Textarea(attrs={'class':"form-control",'rows':"3"}))
    class Meta:
        model = AnswerText
        exclude = ['questionnaire', 'answer_owner']
