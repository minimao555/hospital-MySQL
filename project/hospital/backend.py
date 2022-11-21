from __future__ import annotations

from django.apps import apps
from django.db import models
from . import models as my_models


class ViewBackend:
    app: apps.AppConfig = apps.get_app_config("hospital")

    @staticmethod
    def display_results(model_results: models.query.RawQuerySet) -> list:
        if model_results.model in {my_models.Doctor, my_models.Patient}:
            return ["{} {}".format(result.name, result.pk) for result in model_results]
        else:
            return [result.pk for result in model_results]

    @classmethod
    def gen_content(cls) -> dict[str, str | list | list[dict]]:
        content = {'title': 'Hospital Admin System',
                   'path': '/hospital/data',
                   'has_add_permission': True,
                   'results': [],
                   'models': [{"name": x._meta.verbose_name,
                               "link": x._meta.model_name}
                              for x in cls.app.get_models()],
                   }
        return content

    @classmethod
    def get_result(cls, user, content: dict[str, str], model_name: str, value: str | None = None, key: str | None = None):
        # TODO: add user authentication
        model: models.Model = cls.app.get_model(model_name)
        if value is None:
            # select all
            return model.objects.raw("select * from {}".format(model._meta.db_table))
        if key is None:   # default search method
            if model_name == "doctor" or model_name == "patient":
                value += "%"
                query = "SELECT * FROM {} where {} LIKE %s or name LIKE %s"\
                    .format(model._meta.db_table, model._meta.pk.db_column)
                results = model.objects.raw(query, (value, value))
                # results = model.objects.raw("select * from doctor")
            else:
                query = "SELECT * FROM {} where {} = %s".format(model._meta.db_table, model._meta.pk.db_column)
                results = model.objects.raw(query, value)
            return results
        # else:
        # TODO: advanced query
