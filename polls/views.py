from django.shortcuts import render
from django.http import JsonResponse
import json
from django.http import HttpResponse
from polls.models import Choice
from polls.models import Group
from polls.models import Pool
from polls.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.files.base import ContentFile
import platform
from django.contrib.auth.decorators import login_required
from polls.models import Dictionary
from time import sleep
#from django.utils import simplejson

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        checkUser = User.objects.filter(username__exact=username, password__exact=password)
        if checkUser:
            user = User.objects.filter(username=username, password=password).values()
            userID = user[0]['id']
            operator = user[0]['operator']
            print(f'userID:{userID},operator:{operator}')
            if operator == 0:
                template_var = {}
                index = Pool.objects.order_by('?')[:2].values()
                randomIndex = Dictionary.objects.filter(id=3).values()[0]['data_value']
                template_var['pic1'] = Pool.objects.get(id=index[0]['id'])
                print(template_var['pic1'].title)
                if randomIndex == '2':
                    template_var['pic2'] = Pool.objects.get(id=index[1]['id'])
                else:
                    index2= Pool.objects.filter(group_id=template_var['pic1'].group_id).order_by('?').values()[0]['id']
                    template_var['pic2'] = Pool.objects.get(id=index2)
                    print(template_var['pic2'])
                template_var['userID'] = userID
                template_var['useCount'] = Choice.objects.filter(user_id=userID).count()
                if template_var['useCount']>0:
                    temp_last = Choice.objects.filter(user_id=userID).order_by('-choose_time').values()[0]
                    template_var['last1']=Pool.objects.get(id=temp_last['left_pic_id'])
                    template_var['last2'] = Pool.objects.get(id=temp_last['right_pic_id'])
                    template_var['lastIndex'] = temp_last['id']
                else:
                    template_var['last1'] = {'id': 0}
                    template_var['last2'] = {'id': 0}
                    template_var['lastIndex'] = 0
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
                else:
                    ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
                User.objects.filter(id=userID).update(last_login_ip=ip, last_login_time=timezone.now())
                template_var['max_time'] = Dictionary.objects.filter(id=1).values()[0]['data_value']
                return render(request, "home.html", template_var)
            # elif operator == 1:
            # return render(request,"check.html",{'userID': json.dumps(userID)})
            else:
                return HttpResponse('你还未通过审核，请联系管理员后再登录')
        else:
            return HttpResponse('用户名或密码错误，请刷新页面后再次登录')
    return render(request, 'login.html')


def insert_record(request):
    left = request.POST['left']
    right = request.POST['right']
    choice = request.POST['choice']
    usetime = request.POST['usetime']
    userID = request.POST['userID']
    newChoice = Choice(use_time=usetime, left_pic_id=left, right_pic_id=right, choice_num=choice, user_id=userID)
    print("newChoice")
    print(newChoice)
    newChoice.save()
    return JsonResponse({'inserted': True})


def update_record(request):
    id = request.POST['id']
    choice = request.POST['choice']
    usetime = request.POST['usetime']
    Choice.objects.filter(id=id).update(choice_num=choice,use_time=usetime)
    return JsonResponse({'updated': True})


def get_info(request):
    print(platform.platform())
    temp_str = {}
    temp_str[0] = platform.platform()
    temp_str[1] = platform.version()
    temp_str[2] = timezone.now()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    temp_str[3] = ip
    temp_str[4] = platform.processor()
    temp_str[5] = 'zh-Hans'
    temp_str[6] = '8000'
    return JsonResponse(temp_str)


def timeCount(request):
    max_time = {}
    max_time["changeResult"] = 0
    if request.method == "POST":
        Dictionary.objects.filter(id=1).update(data_value= request.POST['out_time'])
        max_time['changeResult'] = 1
    max_time["maxTime"] = Dictionary.objects.filter(id=1).values()[0]['data_value']
    return render(request, 'admin/timeCount.html', max_time)


def recordAccount(request):
    acount_attr = {}
    acount_attr["changeResult"] = 0
    if request.method == "POST":
        Dictionary.objects.filter(id=2).update(data_value=request.POST['global_account'])
        acount_attr['changeResult'] = 1
    acount_attr["global_account"] = Dictionary.objects.filter(id=2).values()[0]['data_value']
    return render(request, 'admin/recordAccount.html', acount_attr)


def randomManage(request):
    random_attr={}
    random_attr["changeResult"] = 0
    if request.method == 'POST':
        myAttr = request.POST['myattr']
        if myAttr:
            Dictionary.objects.filter(id=3).update(data_value=myAttr)
            random_attr["changeResult"] = 1
            random_attr["random_status"] = Dictionary.objects.filter(id=3).values()[0]['data_value']
            return render(request, 'admin/randomManage.html', {"random_status": random_attr["random_status"],
                                                               "changeResult": random_attr["changeResult"]})
    random_attr["random_status"] = Dictionary.objects.filter(id=3).values()[0]['data_value']
    print(random_attr['changeResult'])
    return render(request, 'admin/randomManage.html', {"random_status": random_attr["random_status"],
                                                       "changeResult": random_attr["changeResult"]})

# def getRandomRadio(request):
#     return JsonResponse(Dictionary.objects.filter(id=3).values()[0]['data_value'])
