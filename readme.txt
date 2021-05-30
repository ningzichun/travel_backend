该文件夹为django后端程序，包含完整的接口、模型及元素，具备前端运行所需的全部程序代码及数据集。
参考安装脚本为 ./script/install.sh 。
每个文件夹中有更为详细说明文档 readme。
接口文档为本文件夹中的 django后端接口.md 。
安装配置文档为本文件夹中的 django后端安装手册.md

代码文件结构：
 .
├─api	供前端调用的接口
│  └─views.py	对来自用户的请求的解析及处理
│  └─modules	接口所用模块
│      └─get_color.py	主题色提取模块
│      ├─FSRCNN	超分辨率
│      │      fsrcnn.py	超分辨率处理接口
│      │      models.py		模型类
│      │      utils.py	相关工具
│      └─style	风格迁移模块
│              neural_style.py	风格迁移接口
│              transformer_net.py	风格迁移网络
│              utils.py	模块相关工具
├─forum	社区
├─media	媒体文件
│  ├─avatars	用户头像
│  ├─movies	影集生成结果
│  └─photos	长图生成结果
├─movie	影集模块
│  │  admin.py	管理员配置
│  │  models.py	影集数据库模型
│  │  tasks.py	Celery异步任务程序
│  │  urls.py	URL重写
│  │  views.py	用户请求处理
│  └─modules	影集模块代码
│      │  cost_calculate.py	代价函数计算
│      │  filelist.py	资源文件清单
│      │  generate.py	影集生成模块
│      │  genetic.py	遗传模块
│      │  get_tempalte.py
│      │  info.py	图片数据（天气、主题色）分析接口
│      │  resources.py	影集程序资源
│      │  templates.py	影集元素数据
│      └─assets	影集数据集
│          ├─clips	片段
│          ├─fonts	字体
│          ├─gifs	贴图
│          ├─images	图像
│          └─music	音乐
├─photo	长图模块
│  │  admin.py	管理员配置
│  │  models.py	长图数据库模型
│  │  tasks.py	Celery异步任务程序
│  │  urls.py	URL重写
│  │  views.py	用户请求处理
│  └─modules	长图生成模块
│      │  begin_plog.py	长图部分合成
│      │  cost_calculate.py	代价函数计算
│      │  genetic_for_longpic.py	遗传模块
│      │  get_template.py	元素合成
│      │  long_pic.py	长图接口
│      │  pl_lunzi.py	长图部分合成
│      ├─imgs	图像数据
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
├─scripts	管理脚本
│      clean.sh	缓存清理脚本
│      comands.txt	常用命令
│      config.sh	Django初始化配置脚本
│      Dockerfile	Docker脚本
│      install.sh	系统环境安装及配置脚本
│      moviepy-2.0.0.dev2.tar.gz	Moviepy程序包
│      reload.bat	重载脚本
│      reload.sh	重载脚本
│      requirements.txt	Python依赖包
│      start.bat	启动脚本
│      start.sh	启动脚本
│      travel.service	Linux服务配置文件
│      uwsgi.ini	uwsgi接口配置文件
├─static	静态文件
│  │  banner.json	首页轮播图信息
│  │  server.json	外链服务器信息
│  │
│  ├─city	城市印象图
│  └─images	轮播图等静态图像
├─templates	网页模板
├─tmp	临时文件夹
├─travel	项目主配置目录
│  │  celery.py	Celery接口程序
│  │  codes.py	公用程序代码，如返回数据递交程序，发信代码
│  │  load_files.py	模型预加载，使其仅在首次使用时加载模型
│  │  models.py	模型定义，如天气识别网络模型
│  │  settings.py	项目配置文件
│  │  urls.py	URL重写规则
│  │  views.py	用户请求处理视图
│  │  wsgi.py	WSGI接口程序
│  │
│  ├─modules
│  │  │  get_color.py	主题色提取代码
│  │  │  imgcheck.py	图像审核
│  │  │  location.py	地理位置逆编码
│  │  │
│  │  └─Poem
│  │      ├─checkpoint	检查点
│  │      ├─codes	诗词生成代码
│  │      ├─corpus	模型文件
│  │      └─data	诗词数据
│  │
│  └─resources	模型与资源文件
│      │  weather.pkl	天气识别模型
│      │  fsrcnn_x2.pth	超分辨率模型
│      │  fsrcnn_x3.pth	超分辨率模型
│      │  fsrcnn_x4.pth	超分辨率模型
│      │  mosaic.pth	风格迁移模型
│      │  candy.pth	风格迁移模型
│      │  starry-night.pth	风格迁移模型
│      │  udnie.pth	风格迁移模型
│      │  final.pth	显著性检测模型
│      │  resnet50_caffe.pth	显著性检测模型
│      │  cn_dict.py	物体检测标签翻译数据
│      │  postcode.py	地理信息与城市印象图对照信息
│      │  kumo.ttf	验证码字体
│      │
│      └─mapdata	逆地理编码所需行政区划数据
└─user	用户管理模块


