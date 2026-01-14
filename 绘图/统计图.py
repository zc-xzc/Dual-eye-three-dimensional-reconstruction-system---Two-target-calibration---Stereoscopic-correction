import matplotlib.pyplot as plt
import numpy as np

# 类别
categories = ['bottle', 'battery', 'medicine', 'ointment', 'brick', 'potato', 'carrot', 'turnip', 'cobblestone']

# 每个类别的精确率、召回率和F1分数
precision = [0.926, 0.926, 0.952, 0.972, 0.99, 0.928, 0.984, 0.996, 0.355]
recall = [0.939, 0.901, 0.954, 0.982, 1, 0.955, 0.989, 1, 0.41]
f1_score = [0.977, 0.971, 0.976, 0.989, 0.995, 0.98, 0.981, 0.995, 0.223]

# 每个类别的AUC-ROC
auc_roc = [0.637, 0.727, 0.785, 0.703, 0.845, 0.643, 0.651, 0.648, 0.0968]

# 绘制精确率、召回率和F1分数的条形图
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.25
index = np.arange(len(categories))

bar1 = ax.bar(index, precision, bar_width, label='Precision')
bar2 = ax.bar(index + bar_width, recall, bar_width, label='Recall')
bar3 = ax.bar(index + 2 * bar_width, f1_score, bar_width, label='F1 Score')

ax.set_xlabel('Categories')
ax.set_ylabel('Scores')
ax.set_title('Precision, Recall, and F1 Score for Each Category')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(categories)
ax.legend()

plt.show()

# 绘制AUC-ROC的条形图
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = np.arange(len(categories))

bar = ax.bar(index, auc_roc, bar_width, label='AUC-ROC')

ax.set_xlabel('Categories')
ax.set_ylabel('AUC-ROC')
ax.set_title('AUC-ROC for Each Category')
ax.set_xticks(index)
ax.set_xticklabels(categories)
ax.legend()

plt.show()
