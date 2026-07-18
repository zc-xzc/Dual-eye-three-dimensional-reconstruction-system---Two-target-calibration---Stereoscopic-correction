from graphviz import Digraph

# 设置字体，确保支持中文
font_name = "Microsoft YaHei"  # Windows系统可用字体


# font_name = "PingFang"  # macOS系统可用字体
# font_name = "Noto Sans CJK"  # Linux系统可用字体

# 方案一流程图
def draw_flowchart_1():
    dot = Digraph(comment='方案一流程图', node_attr={'shape': 'box', 'fontname': font_name})
    dot.attr(rankdir='LR', size='10,5', label="方案一流程图", labelloc="t", fontname=font_name)

    # 添加节点
    dot.node('开始', label='开始：用户将垃圾投入垃圾桶顶部的投放口')
    dot.node('垃圾暂存', label='垃圾暂存：垃圾落在垃圾暂存板上')
    dot.node('图像采集', label='图像采集：双目摄像头对暂存板上的垃圾进行图像采集')
    dot.node('图像识别', label='图像识别：采集到的图像信号发送至Jetson Nano上位机进行垃圾类型识别')
    dot.node('控制信号发送', label='控制信号发送：上位机根据识别结果向控制下位机发送控制信号')
    dot.node('机械平台移动', label='机械平台移动：下位机驱动两轴机械平台移动到指定位置')
    dot.node('垃圾抓取', label='垃圾抓取：步进电机控制机械爪的开合，抓取暂存板上的垃圾')
    dot.node('垃圾投放', label='垃圾投放：机械爪将抓取的垃圾投放到对应的垃圾桶中')
    dot.node('垃圾压缩', label='垃圾压缩：可回收垃圾经压缩装置压缩后滑落至垃圾桶')
    dot.node('垃圾观察', label='垃圾观察：通过透明箱体观察垃圾桶内垃圾是否装满')
    dot.node('垃圾清理', label='垃圾清理：垃圾桶装满后，抽取垃圾桶倒出垃圾')
    dot.node('结束1', label='结束：完成垃圾处理流程')

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
    dot = Digraph(comment='方案二流程图', node_attr={'shape': 'box', 'fontname': font_name})
    dot.attr(rankdir='LR', size='10,5', label="方案二流程图", labelloc="t", fontname=font_name)

    # 添加节点
    dot.node('开始2', label='开始：用户将垃圾投入垃圾箱')
    dot.node('图像采集2', label='图像采集：箱内的相机捕捉垃圾图像')
    dot.node('图像上传', label='图像上传：将图像上传至树莓派4B主控模块')
    dot.node('图像预处理', label='图像预处理：主控模块对图像进行预处理，去除背景噪声')
    dot.node('垃圾识别', label='垃圾识别：使用训练好的模型对垃圾进行分类识别')
    dot.node('控制信号发送2', label='控制信号发送：根据识别结果，主控模块发送信号控制电机')
    dot.node('转板转动', label='转板转动：电机驱动转板转动，将垃圾投入对应的垃圾桶')
    dot.node('垃圾存储', label='垃圾存储：垃圾落入垃圾存储箱中')
    dot.node('垃圾清理2', label='垃圾清理：垃圾存储箱底部的滑轨和插板方便垃圾清理和运输')
    dot.node('结束2', label='结束：完成垃圾处理流程')

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
    dot = Digraph(comment='方案三流程图', node_attr={'shape': 'box', 'fontname': font_name})
    dot.attr(rankdir='LR', size='10,5', label="方案三流程图", labelloc="t", fontname=font_name)

    # 添加节点
    dot.node('开始3', label='开始：用户按下按键启动装置')
    dot.node('垃圾投放', label='垃圾投放：将垃圾投入机架顶部的投放口')
    dot.node('垃圾引导', label='垃圾引导：翻板装置将垃圾引导至载物装置')
    dot.node('图像采集与识别', label='图像采集与识别：摄像头对垃圾进行图像采集和识别，确定垃圾类型和位置')
    dot.node('抓取装置启动', label='抓取装置启动：根据识别结果，抓取装置启动')
    dot.node('垃圾抓取', label='垃圾抓取：抓取装置利用多功能抓手抓取垃圾')
    dot.node('垃圾投放3', label='垃圾投放：抓取装置将垃圾投放至对应的垃圾箱')
    dot.node('垃圾储存', label='垃圾储存：垃圾进入储存装置中的不同箱筒')
    dot.node('满载检测', label='满载检测：满载检测设备实时监测垃圾储存情况')
    dot.node('垃圾清理3', label='垃圾清理：当垃圾箱满载时，进行垃圾清理')
    dot.node('结束3', label='结束：完成垃圾处理流程')

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