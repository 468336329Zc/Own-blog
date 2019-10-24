# Own-blog

个人博客采用python+flask编写

我的网站展示：<https://zhangchuanjun.cn/



#### 项目部署

采用ubuntu16.04+nginx+gunicorn       

gunicorn简介：支持wsgi的一个web服务器，能够与各种支持wsgi协议的web框架协作运行，flask就是一个支持wsgi协议的应用服务器。

##### 1.配置MySQL

（1）修改下config.py里连接MySQL的代码，修改下账号和密码以及需要连接的数据库

然后本地运行，进入navicat，转储SQL文件。



（2）然后到服务器上下载MySQL，需要设置权限，允许远程连接到服务器上的MySQL。

具体步骤：<https://blog.csdn.net/xiangwanpeng/article/details/54562362>

我们使用本地电脑连接上服务器上的MySQL后，我们创建一个数据库，也就是之前在config.py里修改的数据库，

进入数据库，运行我们之前转储的SQL文件。

MySQL就算配置好了

##### 2.部署项目到服务器

部署详情：<https://zhangchuan.blog.csdn.net/article/details/101038987



#### 评论模块：

采用了第三方评论管理系统valine +网站管理工具leadcloud配合使用

valine配置手册：<https://deserts.io/valine-admin-document/>

#### 人脸识别登录

采用了face-recognition库，face-recognition详情：<https://github.com/ageitgey/face_recognition>

##### face-recognition环境配置：

##### face-recognition环境配置

因为face-recognition是基于dlib c++深度学习的，所以需要先编译dlib，才能pip install face-recognition

ubuntu或者windows上编译dlib方法：

[https://zhangchuanjun.cn/articles/detail/ubunutu+Windows%E4%B8%8B%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AE%E4%BD%BF%E7%94%A8%E5%BC%80%E6%BA%90%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB%E5%BA%93face_recognition/](https://zhangchuanjun.cn/articles/detail/ubunutu+Windows下安装配置使用开源人脸识别库face_recognition/)

或者：<https://zhangchuan.blog.csdn.net/article/details/100696800>



### Markdown：

采用的是[editor.md](https://pandao.github.io/editor.md/)

editor.md的使用：<https://zhangchuan.blog.csdn.net/article/details/97554425>

### 注意点：

如果将项目部署到服务器上的话，由于是用js打开网络摄像头的，新的一些浏览器会拒绝提供打开摄像头的权限，是需要有ssl证书。

网上免费证书申请：<https://zhangchuan.blog.csdn.net/article/details/102570783>





