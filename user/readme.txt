该文件夹为用户管理应用程序。

views.py: 用户请求处理
urls.py: URL重写
models.py: 用户相关数据库模型
admin.py: 管理员配置


相关入口程序：
模块		api地址		入口函数名
验证码		/user/captcha	views.getCAPTCHA
登录		/user/login	views.login
登出		/user/logout	views.logout
注册		/user/register	views.register
修改密码		/user/password	views.modPwd
上传头像		/user/avatar	views.uploadAvatar
用户信息		/user/info		views.updateInfo
忘记密码		/user/reset	views.resetPwd

