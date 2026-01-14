import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
from scipy.cluster.hierarchy import linkage, dendrogram
from mpl_toolkits.mplot3d import Axes3D

# 提供的数据
categories = ['bottle', 'battery', 'medicine', 'ointment', 'brick', 'potato', 'carrot', 'turnip', 'cobblestone']
precision = [0.926, 0.926, 0.952, 0.972, 0.99, 0.928, 0.984, 0.996, 0.355]
recall = [0.939, 0.901, 0.954, 0.982, 1, 0.955, 0.989, 1, 0.41]
f1_score = [0.977, 0.971, 0.976, 0.989, 0.995, 0.98, 0.981, 0.995, 0.223]
auc_roc = [0.637, 0.727, 0.785, 0.703, 0.845, 0.643, 0.651, 0.648, 0.0968]

# 绘制小提琴图
# 小提琴图结合了箱线图和密度图，能够展示数据的分布情况
plt.figure(figsize=(12, 8))
data = [precision, recall, f1_score, auc_roc]
sns.violinplot(data=data, palette="Set2")
plt.xticks(ticks=[0, 1, 2, 3], labels=["Precision", "Recall", "F1 Score", "AUC-ROC"])
plt.title("Violin Plot of Model Metrics")
plt.xlabel("Metrics")
plt.ylabel("Values")
plt.tight_layout()
plt.savefig("violin_plot.png")
plt.show()

# 绘制层次聚类树图
# 层次聚类树图可以展示类别之间的相似性或差异性
plt.figure(figsize=(12, 8))
distance_matrix = np.array([precision, recall, f1_score, auc_roc]).T
linkage_matrix = linkage(distance_matrix, method="ward")
dendrogram(linkage_matrix, labels=categories)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Categories")
plt.ylabel("Distance")
plt.tight_layout()
plt.savefig("dendrogram.png")
plt.show()

# 绘制3D散点图
# 3D散点图可以展示多个指标之间的关系
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(precision, recall, auc_roc, c=f1_score, cmap="viridis", s=100)
ax.set_xlabel("Precision")
ax.set_ylabel("Recall")
ax.set_zlabel("AUC-ROC")
ax.set_title("3D Scatter Plot of Model Metrics")
plt.tight_layout()
plt.savefig("3d_scatter_plot.png")
plt.show()

# 绘制复杂热力图
# 热力图展示多个指标之间的关系，距离图展示类别之间的距离
plt.figure(figsize=(12, 10))
data_matrix = np.array([precision, recall, f1_score, auc_roc])
sns.heatmap(data_matrix, annot=True, fmt=".3f", cmap="YlGnBu",
            xticklabels=categories,
            yticklabels=["Precision", "Recall", "F1 Score", "AUC-ROC"])
plt.title("Heatmap of Model Metrics")
plt.tight_layout()
plt.savefig("heatmap.png")
plt.show()

# 计算类别之间的欧氏距离
distance_matrix = pairwise_distances(data_matrix.T, metric="euclidean")
plt.figure(figsize=(12, 10))
sns.heatmap(distance_matrix, annot=True, fmt=".2f", cmap="viridis",
            xticklabels=categories,
            yticklabels=categories)
plt.title("Distance Matrix of Categories")
plt.tight_layout()
plt.savefig("distance_matrix.png")
plt.show()