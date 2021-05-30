[toc]

# 后端安装配置手册

### 简介

这是 TravelLog 主后端程序的安装及配置手册。包含完整的接口、模型及元素，具备前端运行所需的全部程序代码及数据集。参考安装脚本为 /script/install.sh ，本文档为安装及配置过程的详细说明。



### 系统准备

程序在 Ubuntu Server LTS 20.04 及 Debian 10 下测试通过。安装依赖项时，工作目录为代码目录。

##### 安装依赖项

```bash
apt update
apt install nginx -y
apt install mariadb-server mariadb-client redis -y
apt install python3 python3-pip build-essential imagemagick npm ffmpeg -y
apt install libgl1-mesa-glx libvips-dev -y
```

##### 配置Python环境

```bash
python3 -m pip install --upgrade pip
pip3 install -r ./scripts/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install ./scripts/moviepy-2.0.0.dev2.tar.gz
```

##### 配置Node环境

```bash
nodejs -v 
npm -v 
npm config set strict-ssl false
npm config set registry https://registry.npm.taobao.org
npm install --registry https://registry.npm.taobao.org -g n  
n  stable    
PATH="$PATH"
npm -g config set user root
echo 'NODE_PATH="/usr/local/lib/node_modules/"' >> /etc/environment 
export NODE_PATH=/usr/local/lib/node_modules/
npm config set sharp_binary_host "https://npm.taobao.org/mirrors/sharp"
npm config set sharp_libvips_binary_host "https://npm.taobao.org/mirrors/sharp-libvips"
npm install sharp -g
npm install --registry https://registry.npm.taobao.org -g ffmpeg-concat || fallback

```



### 配置

##### 数据库配置

```bash
mysql_secure_installation
service mysql start
```

##### 修改uwsgi.ini文件中的路径

根据实际情况，修改启动目录。

```bash
sed -i "s#BASE_DIR#$target_dir#g" ./uwsgi.ini || fallback
```

##### ImageMagick配置

注释  \<policy domain="path" rights="none" pattern="@*"/>，加 \<policy domain="coder" rights="none" pattern="TEXT" />。

```bash
sed -i '/policy\ domain\=\"path\"\ rights\=\"none\"\ pattern\=\"\@\*/i\  <policy domain="coder" rights="none" pattern="TEXT" />' /etc/ImageMagick-6/policy.xml
sed -i -e '/policy\ domain\=\"path\"\ rights\=\"none\"\ pattern\=\"\@\*/d' /etc/ImageMagick-6/policy.xml
```

##### 初始化Django数据

```bash
source ./scripts/config.sh
```

##### 配置Django服务

修改服务文件的启动目录，并启用服务。

```bash
cp ./scripts/travel.service /lib/systemd/system	
sed -i "s#BASE_DIR#$target_dir#g" /lib/systemd/system/travel.service	#修改启动目录
sed -i "s#SERVICE_USER#www#g" /lib/systemd/system/travel.service	#修改启动用户
systemctl enable travel	#启用服务
```

##### nginx中uwsgi接口配置

```
    location / { 

        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
        uwsgi_read_timeout 2;
    }   
    location /media {
        alias BASE_DIR/media/;
    }  
    location /static {

        expires 30d;
        autoindex on; 
        add_header Cache-Control private;
        alias BASE_DIR/static/;
    }
```



### 优化

##### 临时目录读写性能改善

在程序运行过程中，会向临时文件夹中写入一定的文件，如在视频片段的合成中会生成临时帧。改善临时文件读写性能将会显著提升服务器运行效率。这里，我们将临时目录挂载为内存盘，将tmpfs挂载到/tmp。

```bash
vi /etc/fstab
```

在末尾加上下列语句，按需修改size的值。

```bash
tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=22G 0 0
```

保存后重启服务器即可。

##### mariadb集群

vi /etc/my.cnf 打开配置文件，增加以下配置信息。

```
wsrep-provider=/usr/lib64/galera-3/libgalera_smm.so   # wsrep提供者

wsrep_cluster_name='mysql_cluster'  #集群的名字，必须是统一的
wsrep_cluster_address=gcomm://192.168.119.128,192.168.119.129,192.168.119.130  #集群中的其他节点地址

wsrep_node_name = node1              #该节点的名称
wsrep_node_address='192.168.119.128' #该节点的地址

wsrep_sst_method=rsync    # 集群使用rsync同步方式
wsrep_sst_auth=USER_STR:PASS_STR # 集群同步的用户名密码
```

使用到的端口：（4个）

默认的galera端口为TCP 4567；另外还需要注意SST方式的端口，例如mysqldump的端口为TCP 3306，需保证各个节点的端口相互可达。

3306：数据库对外服务的端口
444：请求SST(State Snapshot Transfer,全量数据传送)的端口号
4567：组成员之间进行沟通的端口号
4568：用于传输IST（Incremental State Transfer,增量数据传送）的端口号

集群至少需要2个节点，但建议不少于3个节点。当集群只有2个节点时，若某一节点异常，而不是由systemd或init手动关闭，另一节点的状态会转变为nonoperational。