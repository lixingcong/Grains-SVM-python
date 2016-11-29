## 简易五谷分类器

> Tested on Python 2.7.12

一个模式识别课程小设计，使用电脑端训练识别谷物样本

使用SVM分类器，提取谷物的几个特征进行简单分类

### 依赖

主要是图像库
- opencv 2.4.13
- numpy

### 使用方法

主要是csv文件与谷物文件的对应关系
- 将相应的谷物放进data/grains文件夹内
- 编写对应的data/grain_list.csv，文件格式参考python/class_csv.py
- 修改python/main.py中选择是否重新计算特征还是载入csv特征
- 运行cd python && python main.py

![](/preview.png)

日期：2016-11-29