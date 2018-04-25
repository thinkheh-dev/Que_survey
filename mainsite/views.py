from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .forms import InfoPersonForm, CompanyBasicInfoForm, QuestionsForm, OptionForm
from .models import Questionnaire, Questions, Option

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
        if info_form.is_valid():
            new_info_form = info_form.save(commit=False)
            new_info_form.questionnaire_id = nearly_que.id
            new_info_form.save()

            cic_id = new_info_form.pk
            print(cic_id)
            return HttpResponseRedirect(reverse('company_basic_info_action', args=[cic_id]))

@csrf_protect
def company_basic_info_action(request, cic_id):
    context = {}
    if request.method == "GET":
        company_basic_info = CompanyBasicInfoForm()
        cic_id = cic_id
        context['cic_id'] = cic_id
        context['company_basic_info'] = company_basic_info
    return render(request, 'questions_sme_info.html', context)

@csrf_protect
def company_basic_info_commit(request):
    if request.method == "POST":
        basic_info_form = CompanyBasicInfoForm(request.POST)
        if basic_info_form.is_valid():
            new_basic_info_form = basic_info_form.save(commit=False)
            new_basic_info_form.info_of_company_id = request.POST.get('cic_id')
            new_basic_info_form.save()

            bif_id = new_basic_info_form.pk

            return HttpResponseRedirect(reverse('enterprise_need_action', args=[bif_id]))

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
        que_list = Questions.objects.filter(questionnaire_id=nearly_que.id).values_list()
        for option_name in que_list:
            op_name = "op_name"+str(option_name[0])
            answer = request.POST.getlist(op_name)
            answer_list.append(answer)
        print(answer_list)

    return render(request, 'questions_sme_need.html', context)
    
              
