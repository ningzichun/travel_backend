该文件夹为django配置文件夹，包括项目配置文件。同时，该文件夹也存储公用的代码、模型文件及资源文件。

├─travel
│  ├─modules
│  │  └─get_color.py	主题色提取代码
│  │  └─location.py	地理位置逆编码
│  │  └─Poem
│  │  │  └─checkpoint	检查点
│  │  │  └─corpus	模型文件
│  │  │  └─data	诗词数据
│  │  │  └─codes	诗词生成代码
│  ├─resources	模型与资源文件
│  │  └─fsrcnn_x2.pth	超分辨率模型
│  │  └─weather.pkl	天气识别模型
│  │  └─mapdata	行政区划数据

codes.py: 公用程序代码，如返回数据递交程序，发信代码
load_files.py: 模型预加载程序，在程序首次载入时加载模型
models.py: 模型定义，如天气识别网络模型
settings.py: 项目配置文件
urls.py: URL重写规则
views.py: 用户请求处理视图
