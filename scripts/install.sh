#!/bin/bash

function fallback(){
    echo "未能成功安装"
    exit 1
}

if [ `whoami` = "root" ];then  
    echo "TravelLog部署脚本"
else  
    echo "需要root权限运行"
    exit 0
fi
target_dir=$(pwd)/travel

# echo "下载程序"
# apt update || fallback
# apt install wget unzip -y || fallback

# wget $url -O travel.zip || fallback
# unzip travel.zip -d $target_dir || fallback
#rm travel.zip || fallback

cd $target_dir || fallback

echo "安装依赖项"
apt update || fallback
apt install nginx -y || fallback
apt install mariadb-server mariadb-client redis -y || fallback
apt install python3 python3-pip build-essential imagemagick npm ffmpeg -y || fallback
apt install libgl1-mesa-glx libvips-dev -y || fallback
python3 -m pip install --upgrade pip
pip3 install -r ./scripts/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple || fallback
pip3 install ./scripts/moviepy-2.0.0.dev2.tar.gz
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

echo "数据库配置"
mysql_secure_installation || fallback
service mysql start || fallback

echo "修改配置文件"
cp ./scripts/uwsgi.ini . -f || fallback
sed -i "s#BASE_DIR#$target_dir#g" ./uwsgi.ini || fallback
cat /etc/ImageMagick-6/policy.xml | grep policy\ domain\=\"path\"\ rights\=\"none\"\ pattern\=\"\@\*
#sed -i -e '/string/d' fine
sed -i '/policy\ domain\=\"path\"\ rights\=\"none\"\ pattern\=\"\@\*/i\  <policy domain="coder" rights="none" pattern="TEXT" />' /etc/ImageMagick-6/policy.xml
sed -i -e '/policy\ domain\=\"path\"\ rights\=\"none\"\ pattern\=\"\@\*/d' /etc/ImageMagick-6/policy.xml
source ./scripts/config.sh || fallback

echo "安装服务"
cp ./scripts/travel.service /lib/systemd/system
sed -i "s#BASE_DIR#$target_dir#g" /lib/systemd/system/travel.service || fallback
sed -i "s#SERVICE_USER#www#g" /lib/systemd/system/travel.service || fallback
systemctl enable travel

echo "安装完成，请进一步配置nginx服务"
exit 0
