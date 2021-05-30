该文件夹为模型测试接口程序。
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

views.py: 用户请求处理
urls.py: URL重写
models.py: 相关数据库模型
admin.py: 管理员配置

相关入口程序：
模块		api地址		入口函数名
色彩提取		/api/color		views.getColorFunc
超分辨率		/api/fsrcnn	views.FSRCNNFunc
天气识别		/api/weather	views.weatherFunc
坐标解析		/api/location	views.getLocation
诗词生成		/api/poem	views.getPoem
图片生成诗词	/api/img2poem	views.genPoemFromImg
风格迁移 		/api/style		views.stylizePhoto
