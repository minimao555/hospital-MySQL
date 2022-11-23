import django.db
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
import json
from .backend import ViewBackend, ErrorMsg, AdvancedSearchType


# Create your views here.
@login_required(redirect_field_name='next', login_url='/login/')
def index(request):
    content = ViewBackend.genContent(request)
    path_list = request.path.strip('/').split('/')
    model_name = path_list[-1]
    if (model := ViewBackend.get_model(model_name)) is None:
        messages.error(request, ErrorMsg.not_found.value)
        return redirect('/')
    search_value = request.GET.get("search")
    search_type = None
    for search_type_candidate in AdvancedSearchType:
        if search_type_candidate.value in request.GET:
            search_type = search_type_candidate
            search_value = request.GET.get(search_type_candidate.value)
            model = ViewBackend.get_model(search_type.value)
            break
    try:
        search_results = ViewBackend.getIndexResult(auth.get_user(request), model, search_value, search_type)
    except PermissionError:
        messages.error(request, ErrorMsg.no_permission_err.value)
        return redirect('/')
    content['results'] = ViewBackend.extractIndexResults(search_results)
    for m in content['models']:
        if m['name'].replace(' ', '') == model_name:
            for k, v in m.items():
                # 将选中的表的name等信息放到content直接索引中
                content[k] = v
            break
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
            messages.error(request, ErrorMsg.login_failed.value)
            return redirect(r'/hospital/login/', context={"next": request.POST['next']})


def logout(request):
    auth.logout(request)
    return redirect("/")


def form(request):
    content = ViewBackend.genContent(request)
    path_list = request.path.strip('/').split('/')
    item_pk = path_list[-2]
    model_name = path_list[-3]
    if ((model := ViewBackend.get_model(model_name)) is None) or \
            ((item := ViewBackend.getItem(auth.get_user(request), model, item_pk)) is None):
        messages.error(request, ErrorMsg.not_found.value)
        return redirect("/")
    if request.method == 'GET':
        ViewBackend.fillModelProperties(content, model_name)
        content['item'] = item_pk
        content['fieldset'] = ViewBackend.genFieldSet(item)
        content["buttons"] = ViewBackend.genButtonContent(model)
        return render(request, r'change_form.html', context=content)
    elif request.method == 'POST':
        try:
            ViewBackend.updateItem(auth.get_user(request), item, request.POST, insert=False)
            goto = request.POST['goto']
            if goto == "save":
                return redirect('../../')
            elif goto == "add another":
                return redirect('../../add')
            elif goto == "continue edit":
                return redirect(request.path)
            return redirect(request.path)
        except PermissionError:
            messages.error(request, ErrorMsg.no_permission_err.value)
        except django.db.IntegrityError as e:
            messages.error(request, ErrorMsg.integrity_err.value + str(e))
        except django.db.DataError as e:
            messages.error(request, ErrorMsg.data_err.value + str(e))
        return redirect(request.path)


def addForm(request):
    content = ViewBackend.genContent(request)
    path_list = request.path.strip('/').split('/')
    model_name = path_list[-2]
    if (model := ViewBackend.get_model(model_name)) is None:
        messages.error(request, ErrorMsg.not_found.value)
        return redirect("/")
    if request.method == 'GET':
        ViewBackend.fillModelProperties(content, model_name)
        content['fieldset'] = ViewBackend.genFieldSet(model, create=True)
        return render(request, r'change_form.html', context=content)
    elif request.method == 'POST':
        try:
            ViewBackend.updateItem(auth.get_user(request), model, request.POST, insert=True)
            goto = request.POST['goto']
            if goto == "save":
                return redirect('./')
            elif goto == "add another":
                return redirect(request.path)
            elif goto == "continue edit":
                item_id = ViewBackend.getPostItemID(model, request.POST)
                return redirect('./%s/change' % item_id)
            return redirect(request.path)
        except PermissionError:
            messages.error(request, ErrorMsg.no_permission_err.value)
        except django.db.IntegrityError as e:
            messages.error(request, ErrorMsg.integrity_err.value + str(e))
        except django.db.DataError as e:
            messages.error(request, ErrorMsg.data_err.value + str(e))
        return redirect(request.path)


def deleteForm(request):
    user = auth.get_user(request)
    path_list = request.path.strip("/").split("/")
    if ((model := ViewBackend.get_model(path_list[-3])) is None) or \
       ((item := ViewBackend.getItem(user, model, path_list[-2])) is None):
        messages.error(request, ErrorMsg.not_found.value)
        return redirect('/')
    try:
        ViewBackend.deleteItem(user, item)
    except PermissionError:
        messages.error(request, ErrorMsg.no_permission_err.value)

    # redirect to List view
    return redirect("../../")


def graph(request):
    content = ViewBackend.genContent(request)

    content['graph'] = [
        'Pie',
        'Pie1',
        'Pie2',
        'Pie3',
        'Bar'
    ]

    return render(request, r'change_list.html', context=content)


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def render_graph(request):
    c = (
        Pie()
        .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
        .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .dump_options_with_quotes()
    )
    return json_response(json.loads(c))


def ico(request):
    return HttpResponse(open(r'hospital\templates\ico\logo.png', 'rb').read(), content_type='image/jpg')
