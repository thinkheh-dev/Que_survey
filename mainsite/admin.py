from django.contrib import admin
from mainsite.models import Questionnaire, Questions, Option, Answer, InformationOfPerson, Questions_Char, CompanyBasicInfo

class ChoiceQuestionInline(admin.TabularInline):
    model = Questions
    extra = 5

class ChoiceInline(admin.TabularInline):
    model = Option
    extra = 5

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_time', 'last_updated_time']
    ordering = ['id', ]

    #自定义管理界面--可以管理问卷对应的问题
    inlines = [ChoiceQuestionInline]

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['question_name', 'question_visible', 'multi_select_boolean', 'questionnaire']
    ordering = ['id', ]

    #自定义管理界面--可以管理问题对应的选项
    inlines = [ChoiceInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option_content', 'option_visible', 'questions']
    
@admin.register(Questions_Char)
class Questions_CharAdmin(admin.ModelAdmin):
    list_display = ['question_char_name', 'question_char_content', 'questionnaire']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['questionnaire', 'questions']

@admin.register(InformationOfPerson)
class InformationOfPersonAdmin(admin.ModelAdmin):
    list_display = ['county_name', 'company_name', 'social_credit_code', 'phone', 'responsible_person', 'sex', 
                    'political_status', 'age', 'degree_of_education', 'company_registered_address', 'established_time', 
                    'website_url', 'email_adress', 'company_profiles']

@admin.register(CompanyBasicInfo)
class CompanyBasicInfoAdmin(admin.ModelAdmin):
    list_display = ['organization_category', 'industry_classification', 'registered_fund', 'annual_revenue', 'current_number_of_employees', 'college_degree_or_above', 
                  'intermediate_and_above_titles', 'info_of_company']