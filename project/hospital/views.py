from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64

# Create your views here.

def gen_content():
    content = {
        'title': 'Hospital Admin System',
        'path': '/hospital',
        # 有哪些表
        'models': [
            {
                'name': 'test_model1',
            },
            {
                'name': 'test_model2',
            }
        ],
        'has_add_permission': True,
        # 选中的表中有哪些行
        'results': []
    }
    return content

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
