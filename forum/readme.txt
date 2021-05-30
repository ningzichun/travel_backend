该文件夹为社区模块代码。

views.py: 用户请求处理
urls.py: URL重写
models.py: 相关数据库模型
admin.py: 管理员配置


相关入口程序：
模块		api地址			入口函数名
获取帖子概要	/forum/			views.index
获取一页帖子	/forum/page/$page_num	views.getPage
获取某个帖子	/forum/post/$pid		views.getPost
发帖		/forum/post/new		views.newPost
修改帖子		/forum/post/$pid/edit	views.editPost
删帖		/forum/post/$pid/delete	views.deletePost
给帖子点赞 	/forum/post/$pid/like	views.likePost
评论文章		/forum/comment/new	views.newComment
删评		/forum/comment/$cid/delete	views.deleteComment
给评论点赞	/forum/comment/$cid/like	views.deleteComment
