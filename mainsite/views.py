from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse
from .forms import InfoPersonForm, CompanyBasicInfoForm
from .models import Questionnaire, Questions, Option, Answer, InformationOfPerson, CompanyBasicInfo

def company_info_action(request):
    context = {}
    if request.method == "GET":
        company_info = InfoPersonForm()
        context['company_info'] = company_info
        return render(request, 'questions_sme_baseinfo.html', context)

@csrf_protect
def company_info_commit(request):
    today = timezone.now()
    nearly_que = Questionnaire.objects.filter(create_time__lt = today).first()
    if request.method == "POST":
        info_form = InfoPersonForm(request.POST)
        print(info_form.is_valid())
        if info_form.is_valid():
            new_info_form = info_form.save(commit=False)
            new_info_form.company_name = info_form.cleaned_data['company_name']
            new_info_form.social_credit_code = info_form.cleaned_data['social_credit_code']
            new_info_form.phone = info_form.cleaned_data['phone']
            new_info_form.save()
            cic_id = new_info_form.pk
            return HttpResponseRedirect(reverse('company_basic_info_action', args=[cic_id]))
        else:
            context = {}
            context['company_info'] = info_form
            return render(request, 'questions_sme_baseinfo.html', context)

@csrf_protect
def company_basic_info_action(request, cic_id):
    context = {}
    if request.method == "GET":
        company_basic_info = CompanyBasicInfoForm()
        cic_id = cic_id
        context['cic_id'] = cic_id
        context['company_basic_info'] = company_basic_info
        return render(request, 'questions_sme_info.html', context)
    if request.method == "POST":
        basic_info_form = CompanyBasicInfoForm(request.POST)
        if basic_info_form.is_valid():
            new_basic_info_form = basic_info_form.save(commit=False)
            new_basic_info_form.info_of_company_id = cic_id
            new_basic_info_form.registered_fund = basic_info_form.cleaned_data['registered_fund']
            new_basic_info_form.annual_revenue = basic_info_form.cleaned_data['annual_revenue']
            new_basic_info_form.current_number_of_employees = basic_info_form.cleaned_data['current_number_of_employees']
            new_basic_info_form.college_degree_or_above = basic_info_form.cleaned_data['college_degree_or_above']
            new_basic_info_form.intermediate_and_above_titles = basic_info_form.cleaned_data['intermediate_and_above_titles']
            new_basic_info_form.save()

            bif_id = new_basic_info_form.pk

            return HttpResponseRedirect(reverse('enterprise_need_action', args=[bif_id]))
        else:
            context = {}
            context['cic_id'] = cic_id
            context['company_basic_info'] = basic_info_form
            return render(request, 'questions_sme_info.html', context)

@csrf_protect
def enterprise_need_action(request, bif_id):
    today = timezone.now()
    nearly_que = Questionnaire.objects.filter(create_time__lt=today).first()
    
    if request.method == "GET":
        questions = Questions.objects.filter(questionnaire_id=nearly_que.id)
        options = Option.objects.filter(questionnaire_id=nearly_que.id)
        context = {}
        context['questions'] = questions
        context['options'] = options

    if request.method == "POST":
        answer_list = []
        answer = []
        #取得问题列表
        que_list = Questions.objects.filter(questionnaire_id=nearly_que.id).values_list()
        #取得问题所属人的id
        que_owner_id = InformationOfPerson.objects.filter(id=CompanyBasicInfo.objects.filter(id=bif_id).values()[0].get('id')).values()[0].get('id')
        #利用循环获得用户填写的问卷答案列表
        for option_name in que_list:
            op_name = "op_name"+str(option_name[0])
            answer = request.POST.getlist(op_name)
            #组装列表，包含答案和问题ID
            answer.append(option_name[0])
            answer_list.append(answer)
        print(answer_list)

        #遍历包含答案ID和问题ID的列表
        for answer_id_all in answer_list:
            #第一层循环，取得上一列表中的列表元素（又一个列表），并取得列表内元素（列表）的长度
            answer_len=len(answer_id_all)
            #第二层循环，将每一个问题的答案，分别存入对应的字段
            for i in range(0, answer_len-1):
                #取得单个的列表元素
                option_id = answer_id_all[i]
                #实例化Answer模型
                answer_store = Answer()
                #先赋值存入Answer表中的ForeignKey
                answer_store.questionnaire_id = nearly_que.id
                answer_store.questions_id = answer_id_all[-1]
                answer_store.save()
                
                #写入Answer表中的ManyToMany字段，需要使用add方法
                answer_store.option.add(option_id)
                answer_store.answer_owner.add(que_owner_id)
                answer_store.save()

        return HttpResponse('成功了！')

    return render(request, 'questions_sme_need.html', context)


def display_data(request):

    context = {}
    option_all_statistics = Option.objects.annotate(option_count=Count('answer_option')).exclude(option_count=0)
    # Option.objects.annotate(option_count=Count('answer_option')).values('option_content','option_count')

    que_list = Questions.objects.all()
    que_id_list=list(que_list.values_list('id'))
    que_name_list = list(que_list.values_list('question_name'))

    option_statistics_all_list = []

    for_count = 0

    for id_list in que_id_list:
        
        #这个临时列表定义的语句很重要，用于重置子列表，不可以定义在循环外，否则列表会包含所有内容
        option_statistics_list = []

        ''' 开始拼装子列表 '''
        title_name_list = []
        #迭代取出集合中的问题标题
        for title_name in que_name_list:
            #保存到临时的列表中
            title_name_list.append(title_name[0])
        #将整个结果保存在一个临时列表中
        option_statistics_list.append(title_name_list[for_count])

        #获取非0统计的选项内容
        que_by_title = list(option_all_statistics.filter(questions_id=id_list[0]).values_list('option_content'))

        x_name_list = []
        #迭代取出集合中的内容文字
        for x_name in que_by_title:
            #保存到临时的列表中
            x_name_list.append(x_name[0])
        #将整个结果保存在一个临时列表中
        option_statistics_list.append(x_name_list)

        #获取非0统计的选项内容
        que_by_count = list(option_all_statistics.filter(questions_id=id_list[0]).values_list('option_count'))
        option_count_data = []
        #迭代取出集合中的选项统计数
        for option_data in que_by_count:
            #保存到临时的列表中
            option_count_data.append(option_data[0])
        #将整个结果保存在一个临时列表中
        option_statistics_list.append(option_count_data)

        #将最终结果，保存到最终列表中，最终列表的形式 ： [ [[1],[2],[3]], [[1],[2],[3]], ... ]
        option_statistics_all_list.append(option_statistics_list)
        #用于获取名称的计数
        for_count += 1

    print(option_statistics_all_list)


    #传递最终结果到数据显示页面
    context['option_statistics_all_list'] = option_statistics_all_list
    
    return render(request, 'display_data.html', context)


    
              
