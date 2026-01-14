import matplotlib.pyplot as plt
import networkx as nx

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 定义流程图的节点和边
nodes = [
    "系统初始化",
    "垃圾投放",
    "图像采集",
    "图像数据存储",
    "图像预处理",
    "目标轮廓特征提取",
    "垃圾类别与深度信息识别",
    "目标定位识别分类",
    "抓取位姿计算",
    "分类信息传递",
    "机械平台移动",
    "垃圾抓取与分类",
    "状态监测与维护",
    "系统循环",
    "结束"
]

edges = [
    ("系统初始化", "垃圾投放"),
    ("垃圾投放", "图像采集"),
    ("图像采集", "图像数据存储"),
    ("图像数据存储", "图像预处理"),
    ("图像预处理", "目标轮廓特征提取"),
    ("目标轮廓特征提取", "垃圾类别与深度信息识别"),
    ("垃圾类别与深度信息识别", "目标定位识别分类"),
    ("目标定位识别分类", "抓取位姿计算"),
    ("抓取位姿计算", "分类信息传递"),
    ("分类信息传递", "机械平台移动"),
    ("机械平台移动", "垃圾抓取与分类"),
    ("垃圾抓取与分类", "状态监测与维护"),
    ("状态监测与维护", "系统循环"),
    ("系统循环", "图像采集"),
    ("系统循环", "结束")
]

# 创建有向图
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# 绘制流程图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=5000, node_color='lightblue')

# 绘制边
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# 添加标题
plt.title("垃圾自动分拣系统流程图", fontsize=16)

# 调整边的箭头
for edge in G.edges():
    nx.draw_networkx_edges(G, pos, edgelist=[edge],
                           connectionstyle='arc3,rad=0.1',
                           arrowsize=20, arrowstyle='-|>')

plt.tight_layout()
plt.axis('off')
plt.show()