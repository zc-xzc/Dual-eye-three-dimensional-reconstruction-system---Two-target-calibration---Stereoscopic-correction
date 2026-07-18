import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances

# 提供的数据
categories = ['bottle', 'battery', 'medicine', 'ointment', 'brick', 'potato', 'carrot', 'turnip', 'cobblestone']
precision = [0.926, 0.926, 0.952, 0.972, 0.99, 0.928, 0.984, 0.996, 0.355]
recall = [0.939, 0.901, 0.954, 0.982, 1, 0.955, 0.989, 1, 0.41]
f1_score = [0.977, 0.971, 0.976, 0.989, 0.995, 0.98, 0.981, 0.995, 0.223]
auc_roc = [0.637, 0.727, 0.785, 0.703, 0.845, 0.643, 0.651, 0.648, 0.0968]

# 将数据转换为矩阵形式
data_matrix = np.array([precision, recall, f1_score, auc_roc])

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(data_matrix, annot=True, fmt=".3f", cmap="YlGnBu",
            xticklabels=categories,
            yticklabels=["Precision", "Recall", "F1 Score", "AUC-ROC"])
plt.title("Heatmap of Model Metrics")
plt.show()

# 计算类别之间的欧氏距离
distance_matrix = pairwise_distances(data_matrix.T, metric="euclidean")

# 绘制距离图
plt.figure(figsize=(10, 8))
sns.heatmap(distance_matrix, annot=True, fmt=".2f", cmap="viridis",
            xticklabels=categories,
            yticklabels=categories)
plt.title("Distance Matrix of Categories")
plt.show()