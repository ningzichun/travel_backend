该文件夹为长图所需模块文件夹。

 .
│  └─modules	长图生成模块
│      │  begin_plog.py	长图部分合成
│      │  cost_calculate.py	代价函数计算
│      │  genetic_for_longpic.py	遗传模块
│      │  get_template.py	元素合成
│      │  long_pic.py	长图接口
│      │  pl_lunzi.py	长图部分合成
│      │
│      ├─imgs	封面封底数据
│      ├─PoolNet	显著性检测模块
│      │  │  caijian_main.py	裁剪模块
│      │  │  get_main_pic.py	主接口实现
│      │  │  lunzi.py	相关工具
│      │  │  solver.py	模型解析
│      │  ├─dataset	数据集
│      │  │      dataset.py	数据集工具
│      │  └─networks	网络
│      │          deeplab_resnet.py		resnet网络
│      │          poolnet.py	池化网络
│      ├─resources	长图资源文件夹
│      └─templates	长图数据文件夹

