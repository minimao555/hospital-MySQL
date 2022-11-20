from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse
from django.apps import apps
from django.db import models
import base64


# Create your views here.
def gen_content():
    content = {'title': 'Hospital Admin System',
               'path': '/hospital',
               'has_add_permission': True,
               'results': [],
               'models': [{"name": x._meta.verbose_name}
                          for x in apps.get_app_config("hospital").get_models()],
               }
    return content


@login_required(redirect_field_name='next', login_url='/login/')
def index(request):
    content = gen_content()
    path_list = request.path.split('/')
    model = path_list[-1] if path_list[-1] else path_list[-2] # 路径最后可能是/
    for m in content['models']:
        if m['name'] == model:
            content['results'] = [
                {'value': '123'},
                {'value': 'qwe'},
                {'value': 'asd'}
            ]
            for k, v in m.items():
                # 将选中的表的name等信息放到content直接索引中
                content[k] = v
            break
    # print(content)

    return render(request, r'change_list.html', context=content)


def login(request):
    context_general = {
        'site_title': "医院数字化管理系统",
        'site_header': "医院数字化管理系统",
    }
    if request.method == 'GET':
        return render(request, r'login.html', context=context_general)
    else:
        username = request.POST['username']
        passwd = request.POST['password']
        user = auth.authenticate(username=username, password=passwd)
        if user:
            auth.login(request, user)
            redirect_to = request.GET.get('next', '/')
            return redirect(redirect_to)
        else:
            messages.error(request, "用户名或密码错误，登录失败")
            return redirect(r'/login.html', context={"next": request.POST['next']})


def logout(request):
    auth.logout(request)
    return redirect(r'/index.html')


def form(request):
    if request.method == 'GET':
        content = gen_content()
        path_list = request.path.split('/')
        if len(path_list) < 2:
            raise "Path error: " + request.path
        item = path_list[-2] if path_list[-1] else path_list[-3]
        model = path_list[-3] if path_list[-1] else path_list[-4]
        for m in content['models']:
            if m['name'] == model:
                for k, v in m.items():
                    # 将选中的表的name等信息放到content直接索引中
                    content[k] = v
                break
        content['item'] = item
        content['fieldset'] = [
            {
                "required": True,
                "type": "text",
                "name": "hhh",
                "data": "qqqq"
            },
            {
                "required": True,
                "type": "textarea",
                "name": "www",
                "data": "eeee",
                "cols": 40,
                "rows": 30
            },
            {
                "required": True,
                "type": "select",
                "name": "test_model2",
                "opts": ["123", "qwe", "asd"],
                # "edit_url": "",
                "selected": "123"
            },
            {
                "required": True,
                "type": "picture",
                "name": "photo",
                "base64": base64.b64encode(open('hospital/templates/doctor_0.png', 'rb').read()).decode(),
                "cols": 40,
                "rows": 30
            },
        ]
        # print(content)
        return render(request, r'change_form.html', context=content)
    elif request.method == 'POST':
        print(request.body)
        return redirect(request.path)


def addform(request):
    content = gen_content()
    path_list = request.path.split('/')
    if len(path_list) < 2:
        raise "Path error: " + request.path
    item = path_list[-1] if path_list[-1] else path_list[-2]
    model = path_list[-2] if path_list[-1] else path_list[-3]
    for m in content['models']:
        if m['name'] == model:
            for k, v in m.items():
                # 将选中的表的name等信息放到content直接索引中
                content[k] = v
            break
    content['fieldset'] = [
        {
            "required": True,
            "type": "text",
            "name": "hhh",
            "data": ""
        },
        {
            "required": True,
            "type": "textarea",
            "name": "www",
            "data": "",
            "cols": 40,
            "rows": 30
        },
        {
            "required": True,
            "type": "select",
            "name": "test_model2",
            "opts": ["123", "qwe", "asd"],
            # "edit_url": "",
            "selected": ""
        },
        {
            "required": True,
            "type": "picture",
            "name": "photo",
            "base64": "",
            "cols": 40,
            "rows": 30
        },
    ]
    # print(content)
    return render(request, r'change_form.html', context=content)


def deleteform(request):
    print(request.path)
    path_list = request.path.split("/")
    # 重定向到二级目录
    return redirect("/".join(path_list[:-2] if path_list[-1] else path_list[:-3]))

def ico(request):
    return HttpResponse(open(r'hospital\templates\ico\logo.png', 'rb').read(), content_type='image/jpg')
