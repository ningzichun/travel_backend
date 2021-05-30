该文件夹为影集应用目录，含影集生成接口代码、影集生成模块及所需资源文件。
 .
├─movie
│  │  admin.py	管理员配置
│  │  models.py	影集数据库模型
│  │  tasks.py	Celery异步任务程序
│  │  urls.py	URL重写
│  │  views.py	用户请求处理
│  │
│  └─modules	影集模块代码
│      │  cost_calculate.py	代价函数计算
│      │  filelist.py	资源文件清单
│      │  generate.py	影集生成模块
│      │  genetic.py	遗传模块
│      │  get_tempalte.py
│      │  info.py	图片数据（天气、主题色）分析接口
│      │  resources.py	影集程序资源
│      │  templates.py	影集元素数据
│      │
│      └─assets	影集数据集
│          ├─clips	片段
│          ├─fonts	字体
│          ├─gifs	贴图
│          ├─images	图像
│          └─music	音乐


相关入口程序：
模块		api地址			入口函数名
新建影集		/movie/new		views.newWork
上传文件		/movie/$work_id/upload	views.uploadImage
开始生成影集	/movie/$work_id/start	views.startWork
获取作业状态	/movie/$work_id/status	views.getStatus
删除影集		/movie/$work_id/delete	views.deleteMovie
用户影集列表	/movie/list		views.myMovieList
用户所有影集列表	/movie/myall		views.myMovieListAll
分享的影集列表	/movie/all			views.movieListAll
分享的影集分类	/movie/tag/<int:tag>	views.movieListTag
点赞影集		/movie/<int:wid>/like	views.likeComment
获取影集评论	/movie/<int:wid>/comment	views.getComment
评论影集		/movie/<int:wid>/comment/new	views.newComment
给评论点赞	/movie/comment/<int:cid>/like	views.likeComment
删评		/movie/comment/<int:cid>/delete	views.deleteComment

