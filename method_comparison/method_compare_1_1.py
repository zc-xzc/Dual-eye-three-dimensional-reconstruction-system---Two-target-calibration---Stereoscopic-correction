from graphviz import Digraph

# 设置字体，确保支持中文
font_name = "Microsoft YaHei"  # Windows系统可用字体
# font_name = "PingFang"  # macOS系统可用字体
# font_name = "Noto Sans CJK"  # Linux系统可用字体

# 设置全局样式
node_style = {'shape': 'box', 'fontname': font_name, 'fontsize': '12', 'style': 'filled', 'fillcolor': 'lightgray'}
edge_style = {'fontname': font_name, 'fontsize': '10'}
graph_style = {'rankdir': 'LR', 'size': '10,5', 'bgcolor': 'white', 'fontname': font_name, 'fontsize': '14'}


# 方案一流程图
def draw_flowchart_1():
    dot = Digraph(comment='方案一流程图', node_attr=node_style, edge_attr=edge_style, graph_attr=graph_style)
    dot.attr(label="方案一流程图", labelloc="t")

    # 添加节点
    dot.node('开始', label='开始')
    dot.node('垃圾暂存', label='垃圾暂存')
    dot.node('图像采集', label='图像采集')
    dot.node('图像识别', label='图像识别')
    dot.node('控制信号发送', label='控制信号发送')
    dot.node('机械平台移动', label='机械平台移动')
    dot.node('垃圾抓取', label='垃圾抓取')
    dot.node('垃圾投放', label='垃圾投放')
    dot.node('垃圾压缩', label='垃圾压缩')
    dot.node('垃圾观察', label='垃圾观察')
    dot.node('垃圾清理', label='垃圾清理')
    dot.node('结束1', label='结束')

    # 添加边
    dot.edge('开始', '垃圾暂存')
    dot.edge('垃圾暂存', '图像采集')
    dot.edge('图像采集', '图像识别')
    dot.edge('图像识别', '控制信号发送')
    dot.edge('控制信号发送', '机械平台移动')
    dot.edge('机械平台移动', '垃圾抓取')
    dot.edge('垃圾抓取', '垃圾投放')
    dot.edge('垃圾投放', '垃圾压缩')
    dot.edge('垃圾压缩', '垃圾观察')
    dot.edge('垃圾观察', '垃圾清理')
    dot.edge('垃圾清理', '结束1')

    # 保存并渲染
    dot.render('flowchart_1', format='png', view=True)


# 方案二流程图
def draw_flowchart_2():
    dot = Digraph(comment='方案二流程图', node_attr=node_style, edge_attr=edge_style, graph_attr=graph_style)
    dot.attr(label="方案二流程图", labelloc="t")

    # 添加节点
    dot.node('开始2', label='开始')
    dot.node('图像采集2', label='图像采集')
    dot.node('图像上传', label='图像上传')
    dot.node('图像预处理', label='图像预处理')
    dot.node('垃圾识别', label='垃圾识别')
    dot.node('控制信号发送2', label='控制信号发送')
    dot.node('转板转动', label='转板转动')
    dot.node('垃圾存储', label='垃圾存储')
    dot.node('垃圾清理2', label='垃圾清理')
    dot.node('结束2', label='结束')

    # 添加边
    dot.edge('开始2', '图像采集2')
    dot.edge('图像采集2', '图像上传')
    dot.edge('图像上传', '图像预处理')
    dot.edge('图像预处理', '垃圾识别')
    dot.edge('垃圾识别', '控制信号发送2')
    dot.edge('控制信号发送2', '转板转动')
    dot.edge('转板转动', '垃圾存储')
    dot.edge('垃圾存储', '垃圾清理2')
    dot.edge('垃圾清理2', '结束2')

    # 保存并渲染
    dot.render('flowchart_2', format='png', view=True)


# 方案三流程图
def draw_flowchart_3():
    dot = Digraph(comment='方案三流程图', node_attr=node_style, edge_attr=edge_style, graph_attr=graph_style)
    dot.attr(label="方案三流程图", labelloc="t")

    # 添加节点
    dot.node('开始3', label='开始')
    dot.node('垃圾投放', label='垃圾投放')
    dot.node('垃圾引导', label='垃圾引导')
    dot.node('图像采集与识别', label='图像采集与识别')
    dot.node('抓取装置启动', label='抓取装置启动')
    dot.node('垃圾抓取', label='垃圾抓取')
    dot.node('垃圾投放3', label='垃圾投放')
    dot.node('垃圾储存', label='垃圾储存')
    dot.node('满载检测', label='满载检测')
    dot.node('垃圾清理3', label='垃圾清理')
    dot.node('结束3', label='结束')

    # 添加边
    dot.edge('开始3', '垃圾投放')
    dot.edge('垃圾投放', '垃圾引导')
    dot.edge('垃圾引导', '图像采集与识别')
    dot.edge('图像采集与识别', '抓取装置启动')
    dot.edge('抓取装置启动', '垃圾抓取')
    dot.edge('垃圾抓取', '垃圾投放3')
    dot.edge('垃圾投放3', '垃圾储存')
    dot.edge('垃圾储存', '满载检测')
    dot.edge('满载检测', '垃圾清理3')
    dot.edge('垃圾清理3', '结束3')

    # 保存并渲染
    dot.render('flowchart_3', format='png', view=True)


# 绘制所有流程图
draw_flowchart_1()
draw_flowchart_2()
draw_flowchart_3()