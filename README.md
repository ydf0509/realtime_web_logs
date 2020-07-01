# realtime_web_logs
文件日志实时显示到web页面。附带全系统硬盘的文件浏览下载功能。

## 两种运行方式
```
1)拉取项目代码 
gunicorn -w 9 -k gevent --bind 0.0.0.0:8888 log_to_web:app

2) 使用命令行启动
先 pip  install realtime_web_logs
然后在命令行敲击   rwl  三个字母。运行原理类似与django celery scrapy这种命令行。

在浏览器打开 127.0.0.1(ip):9999端口，账号密码为 admin pass123，就嫩看到磁盘文件夹了。
除了包括python -m http.server的功能以外，最主要是嫩渲染彩色日志并自动实时刷新。

```

### 主要功能
~~~
看日志希望带有彩色，希望从浏览器上看到，不用连到机器上看。

 浏览系统的文件夹，scan + 系统文件夹的层级名字当做url路由，可以深层次看到机器上任何层级的文件夹，
 实现系统文件夹浏览下载。

如果是点击文件夹进入子目录。

如果是点击文件，尝试以文本格式读取文件，并以实时更新的方式显示到浏览器日志控制台并加彩。 
主要是要做到不遗漏推送日志和不重复推送日志，采用的是python 操作文件的seek和tell。

 ~~~ 

#### 浏览系统目录和下载文件的页面

##### windows

![Image text](https://i.niupic.com/images/2019/08/11/_118.png)

##### linux

![Image text](https://i.niupic.com/images/2020/07/01/8lFj.png)

#### 查看实时日志更新的页面，提供了暂停功能和自动下拉功能。把日志根据级别加了彩色，
#### 更容易观察哪些是严重的，哪些是debug的。
![Image text](https://i.niupic.com/images/2019/08/11/_119.png)

