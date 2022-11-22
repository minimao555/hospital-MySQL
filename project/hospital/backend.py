from __future__ import annotations

from enum import Enum
from typing import Type
from functools import singledispatch

from django.apps import apps
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from . import models as my_models


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
    def checkPermission(user: User, model: Type[models.Model], perm: Perm) -> bool:
        """
        check if current user has specific permission
        :param user:
        :param model:
        :param perm: Enum Perm, only edit & view permission types
        :return: bool, whether user has the permission
        """
        permission = "{}.{}_{}".format(model._meta.app_label, perm, model._meta.model_name)
        return user.has_perm(permission)

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
    def getIndexResult(cls, user: User, model: models.Model, value: str | None = None, key: str | None = None) \
            -> models.query.RawQuerySet | None:
        """
        get raw SQL results from database
        :param user: user launched this query, used by permission system
        :param model: model
        :param value: value to be searched
        :param key: search in which key (used in advanced search)
        :return: will return in the form of raw query result of corresponding model
        """
        if not cls.checkPermission(user, model, cls.Perm.view):
            return None
        if value is None:
            # select all
            return model.objects.raw("select * from {}".format(model._meta.db_table))
        if key is None:  # default search method
            value = "%" + value + "%"
            if model._meta.model_name == "doctor" or model._meta.model_name == "patient":
                query = "SELECT * FROM {} where {} LIKE %s or name LIKE %s" \
                    .format(model._meta.db_table, model._meta.pk.db_column)
                results = model.objects.raw(query, (value, value))
                # results = model.objects.raw("select * from doctor")
            else:
                query = "SELECT * FROM {} where {} LIKE %s".format(model._meta.db_table, model._meta.pk.db_column)
                return model.objects.raw(query, value)
            return results
        # else:
        # TODO: advanced query

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
            return None
        query = "SELECT * FROM {} where {}=%s".format(model._meta.db_table, model._meta.pk.db_column)
        results = model.objects.raw(query, [pk])
        if len(results) == 0:
            return None
        assert len(results) == 1      # primary key should be unique
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
            else:
                field_value = ""
            return_list.append(genItemContent(field, field_value))

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


# TODO: finish genItemContent
@singledispatch
def genItemContent(field: models.Field, value: str) -> dict:
    """
    generate Content subset for each item, single dispatched for generic type support
    :param field: target field
    :param value: field value
    :return: content dict generated
    """
    raise NotImplementedError("Unknown Field Type")


@genItemContent.register(models.CharField)
@genItemContent.register(models.IntegerField)
def _(field: models.CharField | models.IntegerField, value: str) -> dict:
    print("text block")
    pass


@genItemContent.register(models.TextField)
def _(field: models.TextField, value: str) -> dict:
    print("textarea block")
    pass


@genItemContent.register(models.ForeignKey)
def _(field: models.ForeignKey, value: str) -> dict:
    print("text block(can't edit)")
    pass


@genItemContent.register(models.DateTimeField)
def _(field: models.ForeignKey, value: str) -> dict:
    print("Datetime block")
    pass
