import time
from datetime import datetime
import base64

from flask import Flask, request, jsonify, session, url_for, render_template, send_from_directory, Response

from . import admin
from ..models import Admin, db
from random import randrange

from pyecharts import options as opts
from pyecharts.charts import Bar
from .gen_graph import gender_pie, age_bar, city_bar, news_click_rate, news_collection, user_numAndIncrease

"""管理员接口"""


@admin.route("/", methods=['GET'])
def admin_index():
    return render_template("index.html")

@admin.route("/index.css", methods=['GET'])
def admin_css():
    return render_template("index.css")

@admin.route("/icon/icon.png", methods=['GET'])
def admin_icon():
    return Response(open("/root/my/cnsoft2022/server/code/app/admin/templates/ico/logo.png", 'rb').read(), mimetype="img/png")
    
@admin.route("/get_gender_pie")
def get_gender_pie():
    c = gender_pie().dump_options()
    return c


@admin.route("/get_age_bar")
def get_age_bar():
    c = age_bar().dump_options()
    return c


@admin.route("/get_city_bar")
def get_city_bar():
    c = city_bar().dump_options_with_quotes()
    return c


@admin.route("/get_news_click_rate")
def get_news_click_rate():
    c = news_click_rate().dump_options()
    return c


@admin.route("/get_news_collection")
def get_news_collection():
    c = news_collection().dump_options()
    return c


@admin.route("/get_user_numAndIncrease")
def get_user_numAndIncrease():
    c = user_numAndIncrease().dump_options()
    return c
