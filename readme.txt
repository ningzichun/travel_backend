该文件夹为django后端程序，同时包含安装运行脚本、数据模型、视频模板等。
各文件夹的功能如下，每个文件夹中各有详细说明文档。
 .
├─api	供前端调用的接口
│  └─views.py	对来自用户的请求的解析及处理
│  └─modules	接口所用模块
│      └─get_color.py	主题色提取模块
│      └─FSRCNN	超分辨率
├─forum	社区
├─media	媒体文件
│  ├─avatars	用户头像
│  ├─movies	影集生成结果
│  └─photos	长图生成结果
├─movie	影集
│  └─modules	影集模块代码
│      └─cost_calculate.py	距离计算
│      └─filelist.py	文件清单
│      └─generate.py	影集生成模块
│      └─genetic.py	遗传模块
│      └─info.py	图片数据（天气、主题色）分析接口
│      └─resources.py	影集程序资源
│      └─templates.py	影集模板数据
│      └─assets	影集数据集
├─photo	长图
│  └─modules	长图生成模块
│      ├─cost_calculate.py	距离计算模块
│      ├─genetic_for_longpic.py	遗传模块
│      ├─long_pic.py	图片生成模块
│      ├─resources	资源文件夹
│      └─templates	模板文件夹
├─scripts	管理脚本
├─static	静态文件
│  └─images	图片资源
├─templates	网页模板
├─tmp	临时文件夹
├─travel	项目主配置目录
│  ├─modules	项目公用模块
│  │  └─get_color.py	主题色提取代码
│  │  └─location.py	地理位置逆编码
│  │  └─Poem	诗词生成代码及数据集
│  └─resources	公用资源模块及数据集
│  │  └─fsrcnn_x2.pth	超分辨率模型
│  │  └─weather.pkl	天气识别模型
│      └─mapdata	行政区划数据
└─user	用户管理模块


接口文档为本文件夹中的 django后端接口.md 。