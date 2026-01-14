import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 数据处理
groups = ["一", "二", "三", "四"]
classes = ["all", "bottle", "battery", "medicine", "ointment", "brick", "potato", "carrot", "turnip", "cobblestone"]

# 每组数据的 P, R, mAP50, mAP50-95
data = {
    "Group": [],
    "Class": [],
    "P": [],
    "R": [],
    "mAP50": [],
    "mAP50-95": []
}

# 填充数据
group_data = [
    {
        "P": [0.893, 0.943, 0.959, 0.96, 0.968, 0.994, 0.953, 0.978, 0.998, 0.391],
        "R": [0.871, 0.925, 0.876, 0.952, 0.991, 0.999, 0.924, 0.981, 1.0, 0.436],
        "mAP50": [0.907, 0.971, 0.973, 0.98, 0.994, 0.995, 0.975, 0.983, 0.995, 0.274],
        "mAP50-95": [0.62, 0.643, 0.739, 0.798, 0.723, 0.864, 0.647, 0.664, 0.642, 0.119]
    },
    {
        "P": [0.893, 0.93, 0.931, 0.952, 0.973, 0.99, 0.928, 0.984, 0.996, 0.352],
        "R": [0.871, 0.939, 0.896, 0.951, 0.982, 1.0, 0.947, 0.989, 1.0, 0.404],
        "mAP50": [0.9, 0.977, 0.971, 0.977, 0.988, 0.995, 0.98, 0.981, 0.995, 0.24],
        "mAP50-95": [0.638, 0.637, 0.726, 0.787, 0.705, 0.844, 0.645, 0.651, 0.648, 0.103]
    },
    {
        "P": [0.905, 0.943, 0.959, 0.96, 0.968, 0.994, 0.953, 0.978, 0.998, 0.391],
        "R": [0.898, 0.925, 0.876, 0.952, 0.991, 0.999, 0.924, 0.981, 1.0, 0.436],
        "mAP50": [0.904, 0.971, 0.973, 0.98, 0.994, 0.995, 0.975, 0.983, 0.995, 0.274],
        "mAP50-95": [0.649, 0.643, 0.739, 0.798, 0.723, 0.864, 0.647, 0.664, 0.642, 0.119]
    },
    {
        "P": [0.893, 0.914, 0.96, 0.93, 0.969, 0.992, 0.917, 0.983, 0.994, 0.381],
        "R": [0.871, 0.901, 0.861, 0.948, 0.977, 0.998, 0.88, 0.989, 1.0, 0.282],
        "mAP50": [0.907, 0.973, 0.966, 0.978, 0.987, 0.995, 0.959, 0.987, 0.995, 0.323],
        "mAP50-95": [0.62, 0.608, 0.687, 0.765, 0.676, 0.809, 0.595, 0.666, 0.644, 0.132]
    }
]

for i, group in enumerate(groups):
    for j, cls in enumerate(classes):
        data["Group"].append(group)
        data["Class"].append(cls)
        data["P"].append(group_data[i]["P"][j])
        data["R"].append(group_data[i]["R"][j])
        data["mAP50"].append(group_data[i]["mAP50"][j])
        data["mAP50-95"].append(group_data[i]["mAP50-95"][j])
#转换为 DataFrame
df = pd.DataFrame(data)
#创建一个复杂的多图布局
fig = plt.figure(figsize=(20, 15))
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], width_ratios=[1, 1], hspace=0.4, wspace=0.3)
#配色方案
colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold']
cmap = LinearSegmentedColormap.from_list('custom', colors, N=4)
#图表1：分组柱状图（P和R对比）
ax1 = fig.add_subplot(gs[0, 0])
sns.barplot(x="Class", y="P", hue="Group", data=df, palette=colors, ax=ax1, alpha=0.7)
sns.barplot(x="Class", y="R", hue="Group", data=df, palette=colors, ax=ax1, alpha=0.3)
ax1.set_title('精确率(P)与召回率(R)对比', fontsize=14, fontweight='bold')
ax1.set_xticks(range(len(classes)))  # 设置 x 轴刻度位置
ax1.set_xticklabels(classes, rotation=45, ha='right')  # 设置 x 轴标签
ax1.set_ylabel('值')
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
# 图表2：雷达图（综合性能）
ax2 = fig.add_subplot(gs[0, 1], polar=True)
theta = np.linspace(0, 2 * np.pi, len(classes) + 1, endpoint=True)  # 添加闭合点，长度为 len(classes) + 1
for i, group in enumerate(groups):
    values = df[df["Group"] == group]["mAP50"].values[:len(classes)]
    values = np.concatenate((values, [values[0]]))  # 添加起点值以闭合雷达图
    ax2.fill(theta, values, color=colors[i], alpha=0.25, label=f'Group {group}')
    ax2.plot(theta, values, color=colors[i], linewidth=2)
ax2.set_title('mAP50雷达图', fontsize=14, fontweight='bold')
ax2.set_yticklabels([])  # 隐藏 y 轴刻度
ax2.set_xticks(theta[:-1])  # 设置 x 轴刻度位置
ax2.set_xticklabels(classes, fontsize=8)  # 设置 x 轴标签
ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2))
#图表3：热图（mAP50-95对比）
ax3 = fig.add_subplot(gs[1, :])
pivot_df = df.pivot(index="Class", columns="Group", values="mAP50-95")
sns.heatmap(pivot_df, annot=True, cmap=cmap, cbar_kws={'label': 'mAP50-95值'}, ax=ax3)
ax3.set_title('mAP50-95热图对比', fontsize=14, fontweight='bold')
ax3.set_xlabel('组别')
ax3.set_ylabel('类别')
# 图表4：3D散点图（综合分析）
ax4 = fig.add_subplot(gs[2, 0], projection='3d')
for i, group in enumerate(groups):
    group_df = df[df["Group"] == group]  # 这里需要缩进
    ax4.scatter(group_df["P"], group_df["R"], group_df["mAP50"],
                label=f'Group {group}', color=colors[i], marker='o')
ax4.set_title('3D综合性能分析', fontsize=14, fontweight='bold')
ax4.set_xlabel('精确率(P)')
ax4.set_ylabel('召回率(R)')
ax4.set_zlabel('mAP50')# 图表5：误差条图（mAP50-95对比）
ax5 = fig.add_subplot(gs[2, 1])
for i, group in enumerate(groups):
    group_df = df[df["Group"] == group]  # 这里需要缩进
    ax5.errorbar(classes, group_df["mAP50-95"], yerr=0.05, label=f'Group {group}',
                 color=colors[i], fmt='o-', capsize=5)
ax5.set_title('mAP50-95误差条图', fontsize=14, fontweight='bold')
ax5.set_ylabel('mAP50-95值')
ax5.legend(loc='upper right')
ax5.grid(axis='y', linestyle='--', alpha=0.7)#添加标题
fig.suptitle('四组数据性能对比分析', fontsize=18, fontweight='bold', y=0.95)
#保存图表
plt.tight_layout()
plt.savefig('科研论文图表.png', dpi=300, bbox_inches='tight')
plt.show()
