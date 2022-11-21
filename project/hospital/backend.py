from __future__ import annotations

from django.apps import apps
from django.db import models
from django.contrib import auth
from . import models as my_models


class ViewBackend:
    app: apps.AppConfig = apps.get_app_config("hospital")

    @staticmethod
    def extractResults(model_results: models.query.RawQuerySet) -> list[dict]:
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
    def getUser(request) -> str:
        user = auth.get_user(request)
        return user.username

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
                   'username': cls.getUser(request),
                   'models': [{"name": x._meta.verbose_name,
                               "link": x._meta.model_name}
                              for x in cls.app.get_models()],
                   }
        return content

    @classmethod
    def getResult(cls, user, model: models.Model, value: str | None = None, key: str | None = None) \
            -> models.query.RawQuerySet:
        """
        get raw SQL results from database
        :param user: user launched this query, used by permission system
        :param model: model
        :param value: value to be searched
        :param key: search in which key (used in advanced search)
        :return: will return in the form of raw query result of corresponding model
        """
        # TODO: add user authentication
        if value is None:
            # select all
            return model.objects.raw("select * from {}".format(model._meta.db_table))
        if key is None:  # default search method
            if model._meta.model_name == "doctor" or model._meta.model_name == "patient":
                value += "%"
                query = "SELECT * FROM {} where {} LIKE %s or name LIKE %s" \
                    .format(model._meta.db_table, model._meta.pk.db_column)
                results = model.objects.raw(query, (value, value))
                # results = model.objects.raw("select * from doctor")
            else:
                query = "SELECT * FROM {} where {} = %s".format(model._meta.db_table, model._meta.pk.db_column)
                results = model.objects.raw(query, value)
            return results
        # else:
        # TODO: advanced query

    @classmethod
    def genFieldSet(cls, model: models.Model, item: str, create: bool = False) -> list[dict]:
        """
        generate (show) fields of a model in the form of `fieldset`
        :param model:
        :param item: model item name, usually is pk
        :param create: will generate blank form if `create` is True
        :return: `fieldset` dictionary generated
        """
        for field in model._meta.fields:
            pass

    @classmethod
    def get_model(cls, model_name) -> models.Model | None:
        try:
            return cls.app.get_model(model_name)
        except LookupError:
            return None
