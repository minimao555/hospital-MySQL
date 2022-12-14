import django.db
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Line
import json
import datetime
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
    if "doctor" in request.GET:     # advanced search link
        search_type = "doctor"
        search_value = request.GET.get("doctor")
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
    return render(request, './change_list.html'.format(model_name), context=content)


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
        'patient_num_male_and_female',
        'registration_num_type',
        'total_payment_in_a_period_of_time',
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
    c = '{}'
    name = request.POST['name']
    if name == 'patient_num_male_and_female':
        data = ViewBackend().get_patient_num_male_and_female()
        c = (
            Pie()
            .add("", data)
            .set_colors(["yellow", "red"])
            .set_global_opts(title_opts=opts.TitleOpts(title="病人男女数量"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .dump_options_with_quotes()
        )
    elif name == 'registration_num_type':
        data = ViewBackend.get_registration_num_type()
        c = (
            Bar()
            .add_xaxis([x[0] for x in next(iter(data.values()))])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple", "black", "orange", "yellow"])
            .set_global_opts(
                title_opts=opts.TitleOpts(title="挂号单类型", subtitle=""),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
            )
        )
        for k, v in data.items():
            c.add_yaxis(k, v)
        c = c.dump_options_with_quotes()
    elif name == 'total_payment_in_a_period_of_time':
        year_begin = 1980
        year_end = 2022
        data = []
        for year in range(year_begin, year_end + 1):
            begin = datetime.date(year, 1, 1)
            end = datetime.date(year, 12, 31)
            d = ViewBackend.get_total_payment_in_a_period_of_time(str(begin), str(end))
            data.append(d)
        c = (
            Line()
            .add_xaxis([str(y) for y in range(year_begin, year_end + 1)])
            .add_yaxis("商家A", data, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="营业额"))
            .dump_options_with_quotes()
        )
    return json_response(json.loads(c))


def ico(request):
    return HttpResponse(open(r'hospital\templates\ico\logo.png', 'rb').read(), content_type='image/jpg')
