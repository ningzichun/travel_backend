FROM ubuntu
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt update
RUN apt install mariadb-server mariadb-client redis -y && apt install python3 python3-pip build-essential imagemagick npm ffmpeg -y && apt install libgl1-mesa-glx libvips-dev -y 
EXPOSE 8000
