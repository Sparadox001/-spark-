import json
from flask import Blueprint, render_template, url_for

portal = Blueprint('portal', __name__)


@portal.route("/portal/initMenu")
def init_menu():
    rdata = dict()
    head = dict()
    head['title'] = "人物剧情分析"
    head['href'] = "/welcome"
    rdata['homeInfo'] = head
    logos = dict()
    logos['title'] = "FireandBlood"
    logos['image'] = url_for("static", filename="portal/images/logo.jpg")
    logos['href'] = ""
    rdata['logoInfo'] = logos
    rdata['menuInfo'] = [{
        "title":
        "展示界面",
        "icon":
        "fa fa-address-book",
        "href":
        '',
        "target":
        "_self",
        "child": [{
            "title": "人物剧情分析",
            "href": "/welcome",
            "icon": "fa fa-home",
            "target": "_self"
        },{
            "title": "播出季节分析",
            "href": "",
            "icon": "fa fa-delicious",
            "target": "_self",
             "child": [{
                "title": "观看人数",
                "href": "/season1",
                "icon": "fa fa-signal",
                "target": "_self"
            }, {
                "title": "参评人数",
                "href": "/season2",
                "icon": "fa fa-cloud",
                "target": "_self"
            }, {
                "title": "评分",
                "href": "/season3",
                "icon": "fa fa-pie-chart",
                "target": "_self"
            },]
        },{
            "title": "播出时间序列分析",
            "href": "",
            "icon": "fa fa-codepen",
            "target": "_self",
             "child": [{
                "title": "年份推移",
                "href": "/time1",
                "icon": "fa fa-signal",
                "target": "_self"
            }, {
                "title": "月份推移",
                "href": "/time2",
                "icon": "fa fa-cloud",
                "target": "_self"
            },]
        },{
            "title": "导演与作者分析",
            "href": "",
            "icon": "fa fa-medium",
            "target": "_self",
             "child": [{
                "title": "导演与剧集",
                "href": "/direct1",
                "icon": "fa fa-signal",
                "target": "_self"
            }, {
                "title": "作者与剧集",
                "href": "/direct2",
                "icon": "fa fa-cloud",
                "target": "_self"
            },] }
        ]
    }]
    return json.dumps(rdata, ensure_ascii=False)
