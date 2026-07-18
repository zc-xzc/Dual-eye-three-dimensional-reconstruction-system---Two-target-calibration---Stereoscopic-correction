import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
import scipy.cluster.hierarchy as sch
from sklearn.decomposition import PCA
from pandas.plotting import parallel_coordinates

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 数据整理（包含推测的中文类别）
data = {
    "Class": ["所有类别", "矿泉水瓶", "电池", "过期药品", "药膏", "砖块", "土豆", "胡萝卜", "白萝卜", "鹅卵石", "易拉罐", "瓷片"],
    "Group1_P": [0.904, 0.946, 0.955, 0.938, 0.978, 0.995, 0.931, 0.973, 0.997, 0.426, 0.946, 0.426],
    "Group1_R": [0.903, 0.926, 0.877, 0.954, 0.983, 0.999, 0.949, 0.978, 1.0, 0.462, 0.926, 0.462],
    "Group1_mAP50": [0.912, 0.976, 0.974, 0.978, 0.993, 0.995, 0.983, 0.982, 0.995, 0.335, 0.976, 0.335],
    "Group1_mAP50-95": [0.653, 0.643, 0.737, 0.794, 0.714, 0.858, 0.664, 0.678, 0.655, 0.136, 0.643, 0.136],
    "Group2_P": [0.893, 0.93, 0.931, 0.952, 0.973, 0.99, 0.928, 0.984, 0.996, 0.352, 0.93, 0.352],
    "Group2_R": [0.901, 0.939, 0.896, 0.951, 0.982, 1.0, 0.947, 0.989, 1.0, 0.404, 0.939, 0.404],
    "Group2_mAP50": [0.9, 0.977, 0.971, 0.977, 0.988, 0.995, 0.98, 0.981, 0.995, 0.24, 0.977, 0.24],
    "Group2_mAP50-95": [0.638, 0.637, 0.726, 0.787, 0.705, 0.844, 0.645, 0.651, 0.648, 0.103, 0.637, 0.103],
    "Group3_P": [0.905, 0.943, 0.959, 0.96, 0.968, 0.994, 0.953, 0.978, 0.998, 0.391, 0.943, 0.391],
    "Group3_R": [0.898, 0.925, 0.876, 0.952, 0.991, 0.999, 0.924, 0.981, 1.0, 0.436, 0.925, 0.436],
    "Group3_mAP50": [0.904, 0.971, 0.973, 0.98, 0.994, 0.995, 0.975, 0.983, 0.995, 0.274, 0.971, 0.274],
    "Group3_mAP50-95": [0.649, 0.643, 0.739, 0.798, 0.723, 0.864, 0.647, 0.664, 0.642, 0.119, 0.643, 0.119],
    "Group4_P": [0.893, 0.914, 0.96, 0.93, 0.969, 0.992, 0.917, 0.983, 0.994, 0.381, 0.914, 0.381],
    "Group4_R": [0.871, 0.901, 0.861, 0.948, 0.977, 0.998, 0.88, 0.989, 1.0, 0.282, 0.901, 0.282],
    "Group4_mAP50": [0.907, 0.973, 0.966, 0.978, 0.987, 0.995, 0.959, 0.987, 0.995, 0.323, 0.973, 0.323],
    "Group4_mAP50-95": [0.62, 0.608, 0.687, 0.765, 0.676, 0.809, 0.595, 0.666, 0.644, 0.132, 0.608, 0.132]
}

df = pd.DataFrame(data)
df.set_index("Class", inplace=True)

# 数据预测（推测缺失数据）
def predict_missing_data(df, method='linear'):
    for col in df.columns:
        x = np.arange(len(df.index))
        y = df[col].values
        if np.isnan(y).any():
            x_known = x[~np.isnan(y)]
            y_known = y[~np.isnan(y)]
            if len(x_known) > 0:
                spline = interp1d(x_known, y_known, kind=method, fill_value="extrapolate")
                y_pred = spline(x)
                df[col] = y_pred
    return df

df = predict_missing_data(df)

# 1. 绘制热力图（优化后）
plt.figure(figsize=(14, 8))
sns.heatmap(df, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, linecolor="lightgray")
plt.title("不同类别和组别的指标热力图", fontsize=16, fontweight='bold')
plt.xlabel("指标", fontsize=12)
plt.ylabel("类别", fontsize=12)
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300)
plt.show()

# 2. 绘制聚类热力图（优化后）
dist_matrix = sch.distance.pdist(df.T, metric='euclidean')
linkage_matrix = sch.linkage(dist_matrix, method='ward')

plt.figure(figsize=(14, 8))
cluster_grid = sns.clustermap(df.T, row_linkage=linkage_matrix, col_cluster=True, cmap="YlGnBu", annot=True, fmt=".2f",
                              linewidths=0.5, linecolor="lightgray")
plt.title("不同类别和组别的聚类热力图", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("clustered_heatmap.png", dpi=300)
plt.show()

# 3. 绘制动态趋势图（优化后）
plt.figure(figsize=(14, 10))
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

for idx, group in enumerate(["Group1", "Group2", "Group3", "Group4"]):
    plt.plot(df.index, df[f"{group}_P"], marker='o', linestyle='-', color=colors[idx], label=f"{group} - P")
    plt.plot(df.index, df[f"{group}_R"], marker='s', linestyle='--', color=colors[idx], label=f"{group} - R")

plt.title("不同组别和类别的 P 和 R 指标趋势", fontsize=16, fontweight='bold')
plt.xlabel("类别", fontsize=12)
plt.ylabel("指标值", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("trend_line_chart.png", dpi=300)
plt.show()

# 4. 绘制雷达图（优化后）
categories = ['P', 'R', 'mAP50', 'mAP50-95']
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # 雷达图需要闭合

plt.figure(figsize=(14, 10))
ax = plt.subplot(111, polar=True)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, fontsize=10)

# 绘制每个类别的雷达图
for class_name in df.index:
    values = [
        df[f"Group1_P"].loc[class_name],
        df[f"Group1_R"].loc[class_name],
        df[f"Group1_mAP50"].loc[class_name],
        df[f"Group1_mAP50-95"].loc[class_name]
    ]
    values += values[:1]  # 雷达图需要闭合
    ax.plot(angles, values, label=class_name, linewidth=2, linestyle='-')
    ax.fill(angles, values, alpha=0.25)

plt.title("不同类别的指标雷达图", fontsize=16, fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.0), fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("radar_chart.png", dpi=300)
plt.show()

# 5. 绘制相关性矩阵（优化后）
corr_matrix = df.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, linecolor="lightgray")
plt.title("指标之间的相关性矩阵", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("correlation_matrix.png", dpi=300)
plt.show()

# 6. 绘制主成分分析（PCA）（优化后）
pca = PCA(n_components=2)
pca_result = pca.fit_transform(df.T)  # 使用 df.T 作为输入，样本是类别，特征是组的指标

plt.figure(figsize=(14, 10))

# 绘制所有数据点
for i, class_name in enumerate(df.index):
    plt.scatter(pca_result[i, 0], pca_result[i, 1], s=100, label=class_name)
    plt.text(pca_result[i, 0], pca_result[i, 1], class_name, fontsize=9, ha='right')

# 添加组别的中心点
group_centers = {}
for group in ["Group1", "Group2", "Group3", "Group4"]:
    group_indices = [i for i, col in enumerate(df.columns) if col.startswith(group)]
    group_pca = pca_result[group_indices]
    center = np.mean(group_pca, axis=0)
    group_centers[group] = center
    plt.scatter(center[0], center[1], marker='X', s=200, c='black', label=f"{group} 中心点")
    plt.text(center[0], center[1], group, fontsize=10, ha='left')

plt.title("主成分分析（PCA）", fontsize=16, fontweight='bold')
plt.xlabel("主成分 1", fontsize=12)
plt.ylabel("主成分 2", fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("pca_plot.png", dpi=300)
plt.show()

# 7. 绘制平行坐标图（优化后）
df_pivot = df.T
df_pivot.columns = df.index  # 设置列名为 df 的索引（Class 列）
df_pivot.reset_index(inplace=True)  # 将索引（原 df 的列名）变成一列
df_pivot.rename(columns={'index': 'Class'}, inplace=True)  # 将索引列重命名为 'Class'
df_pivot.set_index('Class', inplace=True)  # 将 'Class' 列设置为索引

plt.figure(figsize=(14, 8))
parallel_coordinates(df_pivot.reset_index(), 'Class', colormap=plt.cm.tab20b)
plt.title("不同类别和组别的平行坐标图", fontsize=16, fontweight='bold')
plt.xlabel("指标", fontsize=12)
plt.ylabel("值", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("parallel_coordinates.png", dpi=300)
plt.show()