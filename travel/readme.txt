该文件夹为django配置文件夹，包括项目配置文件。同时，该文件夹也存储公用的代码、模型文件及资源文件。

 .
├─travel
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



