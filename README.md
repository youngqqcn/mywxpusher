# mywxpusher

机子掉线，通过微信推送通知，需要部署在外网。

### 安装docker

```
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```


## 安装docker-compose

```
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

docker-compose version
```


## 启动

```
git clone https://github.com/youngqqcn/mywxpusher.git

cd mywxpusher

make start
```

启动：直接使用 `make start` 启动即可
停止：使用`make stop` 停止即可



--------------------------------
docker-compose  常用操作

```
# 前台启动
docker-compose up

# 后台启动
docker-compose up -d

# 停止
docker-compose stop

# 查看当前正在运行的服务
docker-compose ps


# 查看日志
# docker logs -f 容器名
docker logs -f mywxpusher-docker-monitor-1
```