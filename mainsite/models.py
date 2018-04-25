from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Questionnaire(models.Model):
    '''问卷表'''
    title = models.CharField(max_length=50, verbose_name="问卷名")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    questionnaire_explain = RichTextUploadingField(verbose_name="问卷说明")
    #questions = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="问题外键")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改的时间")

    def __str__(self):
        return "<%s : Questionnaire >" % self.title

    class Meta:
        ordering = ['-create_time',]
        verbose_name_plural = "问卷管理"

class Questions(models.Model):
    '''选择题问卷问题表'''
    question_name = models.CharField(max_length=50, verbose_name="问题题目")
    question_visible = models.BooleanField(default=True, verbose_name="题目是否可见")
    multi_select_boolean = models.BooleanField(default=True, verbose_name="题目是否多选")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="对应的问卷")

    def __str__(self):
        return "<%s : Questions>" % self.question_name

    class Meta:
        verbose_name_plural = "选择题问题管理"
        ordering = ['id']

class Option(models.Model):
    '''问卷问题选项表'''
    option_content = models.CharField(max_length=50, verbose_name="选项内容")
    option_visible = models.BooleanField(default=True, verbose_name="选项是否可见")
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="对应的问题")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="对应的问卷", default=1)

    def __str__(self):
        return "<%s : Option>" % self.option_content

    class Meta:
        verbose_name_plural = "选项管理"
        ordering = ['id']

class Questions_Char(models.Model):
    '''填写类问卷问题表'''
    question_char_name = models.CharField(max_length=20,verbose_name="填写类问题标题")
    question_char_content = models.CharField(max_length=500, verbose_name="填写类问题内容")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="对应的问卷")

    def __str__(self):
        return "<%s : Questions_Char>" % self.question_char_name

    class Meta:
        verbose_name_plural = "填写类问题管理"

class Answer(models.Model):
    '''问卷回答表'''
    #user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="对应的问卷", default=1)
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="所属问题")
    option = models.ManyToManyField(Option, related_name="answer_option")
    # val = models.IntegerField(null=True, blank=True, verbose_name="数字答案")
    # content = models.CharField(max_length=255, null=True, blank=True, verbose_name="文本答案")

    def __str__(self):
        return self.questions

    class Meta:
        verbose_name_plural = "问卷回答表"

class InformationOfPerson(models.Model):
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
    
    company_name = models.CharField(max_length=200, blank=False, verbose_name="企业名称")
    social_credit_code = models.CharField(max_length=18, blank=False, verbose_name="社会统一信用代码")
    #signature = models.CharField(max_length=30, blank=False, verbose_name="填表人姓名")
    job_title = models.CharField(max_length=30, blank=False, verbose_name="职务或职称")
    phone = models.CharField(max_length=11, blank=False, verbose_name="联系电话（手机）")
    responsible_person = models.CharField(max_length=30, blank=False, verbose_name="企业负责人姓名")
    sex = models.IntegerField(choices=SEX_CHOICES, verbose_name="性别")
    political_status = models.CharField(max_length=30, blank=False, verbose_name="政治面貌")
    age = models.IntegerField(choices=AGE_CHOICES, verbose_name="年龄")
    degree_of_education = models.IntegerField(choices=EDUCATION_CHOICES, verbose_name="文化程度")
    company_registered_address = models.CharField(max_length=200, blank=False, verbose_name="公司注册地址")
    established_time = models.DateField(verbose_name="成立时间")
    website_url = models.URLField(blank=True, verbose_name="公司网址")
    email_adress = models.EmailField(blank=False, verbose_name="电子邮件地址")
    #QQ_num = models.CharField(max_length=20, blank=False, verbose_name="QQ号码")
    company_profiles = models.TextField(blank=True, verbose_name="公司介绍")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="所属问卷")



    def __str__(self):
        return "<%s>的基本信息" % self.company_name

    class Meta:
        verbose_name_plural = "企业基本信息管理"

class CompanyBasicInfo(models.Model):
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

    organization_category = models.IntegerField(choices=ORG_KIND, verbose_name="组织类别")
    industry_classification = models.IntegerField(choices=IND_CLASS, verbose_name="产业分类")
    registered_fund = models.CharField(max_length=10, verbose_name="注册资金")
    annual_revenue = models.CharField(max_length=10, verbose_name="企业年营业收入")
    current_number_of_employees = models.CharField(max_length=5, verbose_name="现从业人数")
    college_degree_or_above = models.CharField(max_length=5, verbose_name="大专及以上学历人数")
    intermediate_and_above_titles = models.CharField(max_length=5, verbose_name="中级及以上职称人数")
    info_of_company = models.OneToOneField(InformationOfPerson, on_delete=models.CASCADE, verbose_name="归属于哪个企业")

    def __str__(self):
        return "ID为%s的企业的基本情况" % self.id

    class Meta:
        verbose_name_plural = "企业基本情况管理"