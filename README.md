## 简易五谷分类器

> Tested on Python 2.7.12

一个模式识别课程小设计，使用电脑端训练识别谷物样本

使用SVM分类器，提取谷物的几个特征进行简单分类

### 依赖

主要是图像库
- numpy
- opencv 2.4.13

### 使用方法

主要是csv文件与谷物文件的对应关系
- 重命名data_文件夹为data
- 将相应的谷物放进data/grains文件夹内
- 编写对应的data/grain_list.csv，csv文件格式参考python/class_csv.py注释
- 修改python/main.py中选择是否重新计算特征还是载入csv特征（见下文）
- 运行cd python && python main.py

### 是否载入csv特征

main.py中有个函数对My_Features类的方法， 用于决定重新载入itemlist计算新的特征还是从磁盘载入样本特征。

load_itemlist方法和load_saved_features不能同时使用。要么重新计算特征，要么从磁盘中载入已经计算好的样本特征。

	features_train.load_itemlist()
	features_train.save_features()
	features_train.load_saved_features()
	
方法|说明|备注
----|----|----
load_itemlist()|从磁盘中载入谷物的文件列表，重新计算特征|必选
save_features()|将计算好的特征值存入csv文件，以便下次不必重新计算|可选
load_saved_features()|从磁盘中载入已经计算好的样本特征，避免重复计算特征|必选

### C和gamma值的调优

对不同的训练采用不同的交叉验证，以获取最佳的C和gamma。在RBF核下这两个值决定了SVM分类器的性能。

使用[libsvm](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)进行调优。

### 运行截图

![](/preview.png)

日期：2016-11-29
