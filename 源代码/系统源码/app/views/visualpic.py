from flask import Blueprint, render_template
import pymongo
import pandas as pd

from io import BytesIO
import base64
import imageio

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import re

from pyecharts.charts import Scatter, Pie, Bar
from pyecharts.charts import Line,Bar3D,Gauge, Timeline,Grid
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import seaborn as sns


plt.rcParams['font.family'] = ['SimHei']

visualpic = Blueprint('visualpic', __name__)


season_avgdata = pd.read_csv('app\static\data\season_avgdata.csv')
top_words = pd.read_csv('app\static\data\\top_words.csv')
years_data = pd.read_csv('app\static\data\years_data.csv')
months_data = pd.read_csv('app\static\data\months_data.csv')
director_avgdata = pd.read_csv('app\static\data\director_avgdata.csv')
director_countdata = pd.read_csv('app\static\data\director_countdata.csv')
writer_avgdata = pd.read_csv('app\static\data\writer_avgdata.csv')
writer_countdata = pd.read_csv('app\static\data\writer_countdata.csv')

@visualpic.route("/welcome")
def cloud():
   with open("app\static\data\desc.txt", encoding="utf-8") as f:
    s = f.read()

    # 读取自定义图片
    custom_mask = np.array(Image.open('app\static\img\dargon1.jpeg'))

    # 创建词云对象，设置自定义图片作为底图
    wc = WordCloud(
        width=1920,
        height=1080,
        background_color='white',
        max_words=100,
        mask=custom_mask  # 设置自定义图片作为底图
    )
    # 加载词云文本
    wc.generate(s)
    wordcloud_img1 = BytesIO()
    wc.to_image().save(wordcloud_img1, format='PNG')
    wordcloud1 = base64.b64encode(
        wordcloud_img1.getvalue()).decode('utf-8')
    

    # 读取数据
    
    # 清洗数据，去除value列中的各种杂乱符号
    top_words['value'] = top_words['value'].astype(str)  # 确保所有值都是字符串
    top_words['value'] = top_words['value'].apply(lambda x: re.sub(r'[^A-Za-z\s]', '', x))
    # 分组并计算总频次
    cleaned_top_words = top_words.groupby('value')['count'].sum().reset_index()
    # 将清洗后的数据转换为词云需要的字符串
    word_frequencies = {row['value']: row['count'] for _, row in cleaned_top_words.iterrows()}
    # 读取自定义图片
    # custom_mask = np.array(Image.open(r'./3.jpg'))
    # 生成词云
    wc2 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies)
    wordcloud_img = BytesIO()
    wc2.to_image().save(wordcloud_img, format='PNG')
    wordcloud2 = base64.b64encode(
        wordcloud_img.getvalue()).decode('utf-8')
    
    return render_template('pages/welcome.html', plt1=wordcloud1, plt2=wordcloud2)
    
    # return render_template('pages/welcome.html', plt_base64=wordcloud, ghvh=hjj)


@visualpic.route("/direct2")
def direct2():
   
    x_data = writer_avgdata['written_by'].tolist()[::-1]
    y_data = writer_avgdata['avg(imdb_rating)'].round(1).tolist()[::-1]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(x_data)
        .add_yaxis(
            '',
            y_data,
            category_gap='50%',
            itemstyle_opts={
            "normal": {
            "color": JsCode(
            """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(0, 244, 255, 1)'
                        }, {
                            offset: 1,
                            color: 'rgba(100, 160, 167, 1)'
                        }], false)"""
                            ),
            "barBorderRadius": [30, 30, 30, 30],
            "shadowColor": "rgb(0, 160, 221)",
                        }
                    },  # 设置柱形图颜色为渐变色
        )
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))    
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name='评分'),
            title_opts=opts.TitleOpts(title='不同作者编写剧集的平均得分',pos_left='33%',pos_top="3%"),
            legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
        )
    )

    # 设置整体布局
    grid = (
        Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_right='10%',  # 将柱形图的中心位置偏向右侧
                pos_top='10%',  # 调整图表位置
                width='70%',  # 调整整体图表宽度
                height='80%',  # 调整整体图表高度
            )
        )
    )
    line_html1 = grid.render_embed()

    x_data = writer_countdata['written_by'].tolist()
    y_data = writer_countdata['count'].tolist()

    pie = (
        Pie(init_opts=opts.InitOpts(
           
                theme=ThemeType.DARK)
            )
        .add(
            '',
            [list(z) for z in zip(x_data, y_data)],
            radius=['0%', '60%'],
            center=['50%', '50%'],
            label_opts=opts.LabelOpts(is_show=True),
        )    
        .set_global_opts(
            title_opts=opts.TitleOpts(title='各作者所编写的剧集的占比',pos_left='38%',pos_top="5%"),
            legend_opts=opts.LegendOpts(
                type_="scroll", 
                pos_left="left",  # 调整图例位置
                pos_bottom="10%",
                orient="vertical"
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter='作者：{b} \n 编写的剧集数：{c} \n 总占比：({d}%)'),
            position="outside"
        )
    )


    line_html2 = pie.render_embed()
    # 显示图表
    return render_template('pages/direct2.html',
                        script=grid.js_dependencies,
                        direct21=line_html1,
                        direct22=line_html2,
                        )

@visualpic.route("/direct1")
def direct1():
    x_data = director_avgdata['directed_by'].tolist()[::-1]
    y_data = director_avgdata['avg(imdb_rating)'].round(1).tolist()[::-1]
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(x_data)
        .add_yaxis(
            'y轴',
            y_data,
            category_gap='50%',
            itemstyle_opts={
            "normal": {
            "color": JsCode(
            """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(0, 244, 255, 1)'
                        }, {
                            offset: 1,
                            color: 'rgba(100, 160, 167, 1)'
                        }], false)"""
                            ),
            "barBorderRadius": [30, 30, 30, 30],
            "shadowColor": "rgb(0, 160, 221)",
                        }
                    },  # 设置柱形图颜色为渐变色
        )
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))    
        .set_global_opts(
            
            xaxis_opts=opts.AxisOpts(name='评分'),
            title_opts=opts.TitleOpts(title='不同导演拍摄的剧集的平均得分',pos_left='33%',pos_top="3%"),
            legend_opts = opts.LegendOpts(is_show = False),
        )
    )
   
    # 设置整体布局
    grid = (
        Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_right='10%',  # 将柱形图的中心位置偏向右侧
                pos_top='10%',  # 调整图表位置
                width='70%',  # 调整整体图表宽度
                height='80%',  # 调整整体图表高度
            )
        )
    )
    
    line_html1 = grid.render_embed()


    director_countdata = pd.read_csv('app\static\data\director_countdata.csv')
    
    # 提取 x 和 y 数据
    x_data = director_countdata['directed_by'].tolist()
    y_data = director_countdata['count'].tolist()

    pie = (
        Pie(init_opts=opts.InitOpts(
                theme=ThemeType.DARK)
            )
        .add(
            '',
            [list(z) for z in zip(x_data, y_data)],
            radius=['20%', '60%'],
            center=['40%', '50%'],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=True),
        )    
        .set_global_opts(
            title_opts=opts.TitleOpts(title='各导演所导演的剧集的占比',pos_left='33%',pos_top="5%"),
            legend_opts=opts.LegendOpts(
                type_="scroll", 
                pos_left="right",  # 调整图例位置
                pos_top="2%",
                orient="vertical"
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter='{b}:{c} \n ({d}%)'),
            position="outside"
        )
    )

    line_html2 = pie.render_embed()
    # 显示图表
    return render_template('pages/direct1.html',
                        script=grid.js_dependencies,
                        direct1=line_html1,
                        direct2=line_html2,
                        )


@visualpic.route("/time2")
def time2():
    def transMonthStr(x):
        return str(x)+'月'

    x_data = months_data['month'].apply(transMonthStr).tolist()
    views = months_data['us_viewers'].round(0).tolist()
    imdb = months_data['imdb_rating'].round(2).tolist()
    total_votes = months_data['total_votes'].round(0).tolist()

    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "本月份参与评价人数",
            total_votes,
            yaxis_index=0,
            color="#d14a61",
            itemstyle_opts={"barBorderRadius": [30, 30, 20, 20]}
        )
        .add_yaxis(
            "本月份总观看人数",
            views,
            yaxis_index=1,
            color="#5793f3",
            itemstyle_opts={"barBorderRadius": [30, 30, 20, 20]}
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="观看人数",
                type_="value",
                min_=0,
                max_=12000000,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}人次"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="评分",
                min_=0,
                max_=10,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}分"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="参与评价人数",
                min_=0,
                max_=80000,
                position="right",
                offset=100,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}人次"),
            ),
            title_opts=opts.TitleOpts(title="播放月份综合分析"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            
        )
    )
    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "本月份剧集评价",
            imdb,
            linestyle_opts=opts.LineStyleOpts(color='green', width=3, type_='dashed'),  # 配置折线样式
            itemstyle_opts=opts.ItemStyleOpts(color='red', border_color='yellow', border_width=2),  # 配置图元样式
            symbol='pin',  # 设置图元形状
            symbol_size=20,  # 设置图元大小
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=True),
        )
    )

    bar.overlap(line)
    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    grid.add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)

    line_html = grid.render_embed()
    # 显示图表
    return render_template('pages/time2.html',
                        script=grid.js_dependencies,
                        time2=line_html,)

@visualpic.route("/time1")
def time1():
    # 统一列名
    season_columns_name = season_avgdata.columns.tolist()
    new_colums_name = ['year']
    for colum in season_columns_name[1:]:
        new_colums_name.append((colum))
    years_data.columns = new_colums_name
    years_season_data = pd.merge(season_avgdata[['season','avg(total_votes)']],years_data,on='avg(total_votes)',how='left')
    def transYearStr(x):
        return str(x)+'年'
    def tranSeasonStr(x):
        return '第'+str(x)+'季'

    x_axis = years_season_data['year'].apply(transYearStr).tolist()
    y_axis = years_season_data['season'].apply(tranSeasonStr).tolist()
    views_data = years_season_data['avg(us_viewers)'].round(0).tolist()

    x_len = len(x_axis)
    y_len = len(y_axis)
    data = []
    for i in range(x_len):
        for j in range(y_len):
            if(i == j):
                tmp = [i,j,views_data[i]]
            else:
                tmp = [i,j,0]
            data.append(tmp)

    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'
    ]

    # 创建 Bar3D 图表
    bar3d = Bar3D(init_opts=opts.InitOpts(
       theme=ThemeType.DARK))

    # 添加数据到 Bar3D 图表
    bar3d.add(
        "",
        [[d[1], d[0], d[2]] for d in data],
        xaxis3d_opts=opts.Axis3DOpts(
            type_='category',
            data=x_axis,
            axislabel_opts=opts.LabelOpts(color="white"),  # 设置轴标签颜色为白色
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            type_='category',
            data=y_axis,
            axislabel_opts=opts.LabelOpts(color="white"),  # 设置轴标签颜色为白色
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            type_='value',
            axislabel_opts=opts.LabelOpts(color="white"),  # 设置轴标签颜色为白色
        ),
        grid3d_opts=opts.Grid3DOpts(is_rotate=True,rotate_speed=15,width=200,depth=80),
        shading="lambert",
    )

    # 设置全局配置
    bar3d.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=12000000,
            range_color=range_color,
           
        ),
        legend_opts = opts.LegendOpts(is_show = False),
    )

    line_html = bar3d.render_embed()
    # 显示图表
    return render_template('pages/time1.html',
                        script=bar3d.js_dependencies,
                        time1=line_html,)


@visualpic.route("/season3")
def season3():
    x_data = season_avgdata['season'].tolist()
    y_data = season_avgdata['avg(imdb_rating)'].round(2).tolist()

    # 创建 Timeline 对象
    timeline = Timeline(init_opts=opts.InitOpts(theme=ThemeType.DARK))

    # 为每个季数创建一个 Gauge 图表并添加到 Timeline
    for season, rating in zip(x_data, y_data):
        # 将评分转换为0-100的百分比
        # 现在是0.0作为底线，10.0作为满分，可修改让指针变化更明显
        percentage = round((rating-0 )/ 10 * 100, 1)

        gauge = (
            Gauge()
            .add(
                "",
                [("本季评分", percentage)],
                title_label_opts=opts.LabelOpts(
                font_size=28, color="white", font_family="Microsoft YaHei"
            ),
                min_=0,
                max_=100,
                split_number=5,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=[(0.2, "red"), (0.8, "yellow"), (1, "green")], width=30
                    )
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"第{season}季 - 本季平均评分",pos_left='center'),
                legend_opts = opts.LegendOpts(is_show = False),
            )
        )
        timeline.add(gauge, f"第{season}季")

    # 设置 Timeline 配置
    timeline.add_schema(
        play_interval=1000,
        is_auto_play=True,
        is_loop_play=True,
        pos_bottom="10px",
        pos_left="195px",
    )
    line_html = timeline.render_embed()
    # 显示图表
    return render_template('pages/season3.html',
                        script=timeline.js_dependencies,
                        chart3_html=line_html,)


@visualpic.route("/season2")
def season2():
    x_data = x_data = season_avgdata['season'].tolist()
    x_data.insert(0,0)
    y_data = y_data = season_avgdata['avg(total_votes)'].round(0).tolist()
    y_data.insert(0,0)

    # 创建 Line 图表对象
    line = Line(init_opts={"theme": ThemeType.DARK})

    line.add_xaxis(x_data)
    line.add_yaxis("平均观众数", y_data, is_smooth=False,
                linestyle_opts=opts.LineStyleOpts(color='green', width=2, type_='dashed'),  # 配置折线样式
                itemstyle_opts=opts.ItemStyleOpts(color='red', border_color='yellow', border_width=3),  # 配置图元样式
                symbol='pin',  # 设置图元形状
                symbol_size=20,  # 设置图元大小
                ) 

    # 设置全局图表选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="参与评价人数与播放季的关系",pos_top='1%',pos_left='40%'),
        xaxis_opts=opts.AxisOpts(name="播放季数",
                                splitline_opts=opts.SplitLineOpts(is_show=False)  # 隐藏 x 轴网格线
                                ),
        yaxis_opts=opts.AxisOpts(name= "参与评价人数",
                                splitline_opts=opts.SplitLineOpts(is_show=True),  # 显示 y 轴网格线
                                axisline_opts=opts.AxisLineOpts(  # 配置 y 轴轴线
                                linestyle_opts=opts.LineStyleOpts(color='white')
                            )
                                ),
        legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
    )

    line_html = line.render_embed()
    # 显示图表
    return render_template('pages/season2.html',
                        script=line.js_dependencies,
                        chart2_html=line_html,)


@visualpic.route("/season1")
def season1():
    x_data = x_data = season_avgdata['season'].tolist()
    x_data.insert(0,0)
    y_data = y_data = season_avgdata['avg(us_viewers)'].round(0).tolist()
    y_data.insert(0,0)

    # 创建 Line 图表对象
    line = Line(init_opts={"theme": ThemeType.DARK})

    line.add_xaxis(x_data)
    line.add_yaxis("平均观众数", y_data, is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(color='red', width=2, type_='dashed'),  # 配置折线样式
                itemstyle_opts=opts.ItemStyleOpts(color='blue', border_color='yellow', border_width=4),  # 配置图元样式
                symbol='diamond',  # 设置图元形状
                symbol_size=15,  # 设置图元大小
                )  # 设置 is_smooth=True 来显示平滑的曲线

    # 设置线条样式
    line.set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(color='rgba(80, 255, 140, 0.7)',opacity= 0.6),  # 设置面积图透明度
        label_opts={"is_show": False}  # 设置不显示标签
    )

    # 设置全局图表选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="观看人数与播放季的关系",pos_top='1%',pos_left='40%'),
        xaxis_opts=opts.AxisOpts(name="播放季数"),
        yaxis_opts=opts.AxisOpts(name= "平均观众数"),
        legend_opts=opts.LegendOpts(is_show=False)  # 隐藏图例
    )
    line_html = line.render_embed()
    # 显示图表
    return render_template('pages/season1.html',
                        script=line.js_dependencies,
                        chart1_html=line_html,)
