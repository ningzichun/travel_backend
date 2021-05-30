该文件夹为长图应用文件夹。

 .
├─photo
│  │  admin.py	管理员配置
│  │  models.py	长图数据库模型
│  │  tasks.py	Celery异步任务程序
│  │  urls.py	URL重写
│  │  views.py	用户请求处理
│  │
│  └─modules	长图生成模块
│      │  begin_plog.py	长图部分合成
│      │  cost_calculate.py	代价函数计算
│      │  genetic_for_longpic.py	遗传模块
│      │  get_template.py	元素合成
│      │  long_pic.py	长图接口
│      │  pl_lunzi.py	长图部分合成
│      │
│      ├─imgs
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

urls.py: 路由映射模块
views.py: 路由映射函数模块，逻辑处理路由映射的需求
models.py: 模型模块，工作序列类
admin.py: 管理接口



相关入口程序：
模块		api地址			入口函数名
新建长图		/photo/new		views.newPhoto
上传文件		/photo/$work_id/upload	views.uploadImage
开始生成长图	/photo/$work_id/start	views.startPhoto
获取作业状态	/photo/$work_id/status	views.getStatus
删除长图		/photo/$work_id/delete	views.deletePhoto
用户生成长图列表	/photo/list		views.myPhotoList
用户所有长图列表	/photo/myall		views.myPhotoListAll
分享的长图列表	/photo/all			views.photoListAll
点赞长图		/photo/<int:wid>/like	views.likePhoto
获取长图评论	/photo/<int:wid>/comment	views.getComment
评论长图		/photo/<int:wid>/comment/new	views.newComment
给评论点赞	/photo/comment/<int:cid>/like	views.likeComment
删评		/photo/comment/<int:cid>/delete	views.deleteComment


