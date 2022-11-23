from __future__ import annotations

import base64
import binascii
import datetime
from enum import Enum
from typing import Type
from functools import singledispatch

from django.apps import apps
from django.db import models, connection
from django.contrib import auth
from django.contrib.auth.models import User
from . import models as my_models


class ErrorMsg(Enum):
    no_permission_err = "用户没有访问权限"
    not_found = "找不到指定的项目"
    integrity_err = "主键重复: "
    data_err = "输入字段错误: "
    login_failed = "用户名或密码错误，登录失败"


class AdvancedSearchType(Enum):
    patient = "patient"     # search all patients of specified doctor
    mr = "medicalrecord"        # search all medical records


class ViewBackend:
    class Perm(Enum):
        """
        permission Enum struct, only two variants
        can edit in admin site (group permission)
        `view`: view permission
        `edit`: including add, change, delete, **must be granted at the same time**
        """
        view = "view"
        edit = "change"

    app: apps.AppConfig = apps.get_app_config("hospital")

    @staticmethod
    def extractIndexResults(model_results: models.query.RawQuerySet) -> list[dict]:
        """
        filter the request results, generate corresponding params for `render`
        :param model_results: raw query results
        :return: content result params
        """
        if model_results.model in {my_models.Doctor, my_models.Patient}:
            return [{"value": "{} {}".format(result.name, result.pk),
                     "link": result.pk} for result in model_results]
        else:
            return [{"value": result.pk,
                     "link": result.pk} for result in model_results]

    @staticmethod
    def fillModelProperties(content: dict, model_name: str) -> None:
        """
        fill properties for specific model
        :param content: respond content
        :param model_name: name of model
        :return: None
        """
        for m in content['models']:
            if m['name'] == model_name:
                for k, v in m.items():
                    # 将选中的表的name等信息放到content直接索引中
                    content[k] = v
                break

    @staticmethod
    def getUsername(request) -> str:
        """
        get username by request
        :param request:
        :return:
        """
        user = auth.get_user(request)
        return user.username

    @staticmethod
    def checkPermission(user: User, model: models.Model | Type[models.Model], perm: Perm) -> bool:
        """
        check if current user has specific permission
        :param user:
        :param model:
        :param perm: Enum Perm, only edit & view permission types
        :return: bool, whether user has the permission
        """
        permission = "{}.{}_{}".format(model._meta.app_label, perm.value, model._meta.model_name)
        return user.has_perm(permission)

    @staticmethod
    def getPostItemID(item: models.Model, form: dict) -> str:
        """
        get Item id from the form
        :param item: corresponding item model needed
        :param form:
        :return: item id in form
        """
        return form[item._meta.pk.verbose_name]

    @staticmethod
    def genButtonContent(model: models.Model) -> list[dict]:
        if model == my_models.Doctor:
            return [
                {
                    "value": "View all Patients",
                    "type": AdvancedSearchType.patient.value
                },
                {
                    "value": "View all MR",
                    "type": AdvancedSearchType.mr.value
                },
            ]
        return []

    @classmethod
    def updateItem(cls, user: User, item: models.Model, form: dict, insert: bool = True) -> None:
        """
        add item, fields from `form`
        :param cls:
        :param user:
        :param item: model which add item to
        :param form: param dict
        :param insert: whether insert item, or update it
        """
        if not cls.checkPermission(user, item, cls.Perm.edit):
            raise PermissionError
        key_list = []
        value_list = []
        for field in item._meta.fields:
            field: models.Field
            if field == item._meta.pk and not insert:
                continue
            key_list.append(field.column)
            if field.column in {"photo", "picture"}:
                if insert:
                    try:
                        value_list.append(base64.b64decode(form[field.verbose_name]))
                    except binascii.Error:
                        value_list.append(b'')
                else:
                    key_list.pop()
            else:
                value_list.append(form[field.verbose_name])
        if insert:
            query = "INSERT INTO {} ({}) VALUES ({})".format(
                item._meta.db_table,
                ", ".join(key_list),
                ", ".join(["%s" for _ in range(len(key_list))]))
        else:
            query = "UPDATE {} SET {} WHERE {}=%s".format(
                item._meta.db_table,
                ", ".join(["{} =%s".format(key) for key in key_list]),
                item._meta.pk.db_column)
            value_list.append(item.pk)      # primary key in `where` clause
        with connection.cursor() as cursor:
            cursor.execute(query, value_list)

    @classmethod
    def deleteItem(cls, user: User, item: models.Model) -> None:
        """
        delete the specific item
        :param user: user made the request
        :param item: item to delete
        """
        if not cls.checkPermission(user, item, cls.Perm.edit):
            raise PermissionError
        query = "DELETE FROM {} WHERE {}=%s".format(item._meta.db_table, item._meta.pk.db_column)
        with connection.cursor() as cursor:
            cursor.execute(query, [item.pk])
        pass

    @classmethod
    def genContent(cls, request) -> dict[str, str | list | list[dict]]:
        """
        generate general content
        :param request:
        :return: general content that will be filled with other backend functions
        """
        x: models.Model
        content = {'title': 'Hospital Admin System',
                   'app': '/hospital',
                   'path': '/data',
                   'has_add_permission': True,
                   'results': [],
                   'username': cls.getUsername(request),
                   'models': [{"name": x._meta.verbose_name,
                               "link": x._meta.model_name}
                              for x in cls.app.get_models()],
                   }
        return content

    @classmethod
    def getIndexResult(cls, user: User, model: models.Model,
                       search_value: str | None = None,
                       search_type: AdvancedSearchType | None = None) -> models.query.RawQuerySet | None:
        """
        get raw SQL results from database
        :param user: user launched this query, used by permission system
        :param model: model
        :param search_value: value to be searched
        :param search_type: search in which key (used in advanced search)
        :return: will return in the form of raw query result of corresponding model
        """
        if not cls.checkPermission(user, model, cls.Perm.view):
            raise PermissionError
        if search_value is None:
            # select all
            return model.objects.raw("select * from {}".format(model._meta.db_table))
        if search_type is None:  # default search method
            search_value = "%" + search_value + "%"
            if model._meta.model_name == "doctor" or model._meta.model_name == "patient":
                query = "SELECT * FROM {} where {} LIKE %s or name LIKE %s" \
                    .format(model._meta.db_table, model._meta.pk.db_column)
                return model.objects.raw(query, [search_value, search_value])
                # results = model.objects.raw("select * from doctor")
            else:
                query = "SELECT * FROM {} where {} LIKE %s".format(model._meta.db_table, model._meta.pk.db_column)
                return model.objects.raw(query, search_value)
        else:
            if search_type == AdvancedSearchType.patient:
                query = "SELECT * FROM patient WHERE patient.patientID IN " \
                        "(SELECT medical_records.patientID FROM medical_records " \
                        "WHERE medical_records.doctorID=%s)"
                return model.objects.raw(query, [search_value])
            elif search_type == AdvancedSearchType.mr:
                query = "SELECT * FROM medical_records WHERE doctorID=%s"
                return model.objects.raw(query, [search_value])

    @classmethod
    def getItem(cls, user: User, model: models.Model, pk: str) -> models.Model | None:
        """
        get specific item in table, which primary key = `pk`
        :param user: querying user
        :param model: target model
        :param pk: primary key value
        :return: corresponding record item
        """
        if not cls.checkPermission(user, model, cls.Perm.view):
            raise PermissionError
        query = "SELECT * FROM {} where {}=%s".format(model._meta.db_table, model._meta.pk.db_column)
        results = model.objects.raw(query, [pk])
        if len(results) == 0:
            return None
        assert len(results) == 1  # primary key should be unique
        return results[0]

    @classmethod
    def genFieldSet(cls, item: models.Model, create: bool = False) -> list[dict]:
        """
        generate (show) fields of a model in the form of `fieldset`
        :param item: query result item
        :param create: will generate blank form if `create` is True
        :return: `fieldset` dictionary generated
        """
        return_list = []
        for field in item._meta.fields:
            field: models.Field
            if not create:
                field_value = field.value_from_object(item)
                if type(field) == models.ForeignKey:
                    foreign_model: models.Model = field.related_model
                    item_content = genItemContent(field, field_value, model_name=foreign_model._meta.model_name)
                elif field.name in {"photo", "picture"}:
                    item_content = genItemContent(field, field_value, is_picture=True)
                else:  # default param
                    item_content = genItemContent(field, field_value)
                if field == item._meta.pk:
                    item_content["readonly"] = True
            else:
                if type(field) == models.ForeignKey:
                    # foreign_model: models.Model = field.related_model
                    item_content = genItemContent(models.CharField(verbose_name=field.name, blank=False), "")
                elif type(field) == models.DateTimeField:
                    item_content = genItemContent(field, datetime.datetime.now())
                else:
                    item_content = genItemContent(field, "")
            return_list.append(item_content)
        return return_list

    @classmethod
    def get_model(cls, model_name: str) -> models.Model | None:
        """
        get corresponding model
        :param model_name:
        :return: model, will return None if model does not exist
        """
        try:
            return cls.app.get_model(model_name)
        except LookupError:
            return None


@singledispatch
def genItemContent(field: models.Field, value, **kwargs) -> dict:
    """
    generate Content subset for each item, single dispatched for generic type support
    :param field: target field
    :param value: field value
    :return: content dict generated
    """
    raise NotImplementedError("Unknown Field Type")


@genItemContent.register(models.CharField)
@genItemContent.register(models.IntegerField)
@genItemContent.register(models.FloatField)
def _(field: models.Field, value: str) -> dict:
    ret: dict = {
        "required": not field.blank,
        "type": "text",
        "data": value,
        "name": field.verbose_name,
        # "check": "age",
        # "check": "phone",
    }
    return ret


@genItemContent.register(models.TextField)
def _(field: models.TextField, value: str | bytes, is_picture: bool = False) -> dict:
    if not is_picture:
        ret: dict = {
            "required": not field.blank,
            "type": "textarea",
            "data": value,
            "name": field.verbose_name,
            "cols": 40,
            "rows": 30,
        }
    else:
        ret: dict = {
            "required": not field.blank,
            "type": "picture",
            "name": field.verbose_name,
            "base64": base64.b64encode(value).decode(),
        }
    return ret


@genItemContent.register(models.ForeignKey)
def _(field: models.ForeignKey, value: str, model_name: str) -> dict:
    ret: dict = {
        "required": not field.blank,
        "type": "link",
        "data": value,
        "name": field.verbose_name,
        "link": "{}/{}".format(model_name, value),
    }
    return ret


@genItemContent.register(models.DateTimeField)
def _(field: models.DateTimeField, value: datetime.datetime) -> dict:
    ret: dict = {
        "required": not field.blank,
        "type": "time",
        "name": field.verbose_name,
    }
    if value is not None:
        ret["data"] = {
            "date": value.date(),
            "time": value.time(),
        }
    return ret
