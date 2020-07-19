# 汤泉苗木信息网公众号
## 项目背景：
家乡汤泉苗木资源的整合，打通货主、二手贩、户主信息传递的延迟

## 资源准备：
- 公众号（服务号）
- 云主机
- 域名备案

## 运行准备：
- 开发环境：Python 3.6.8
- 开发框架：webpy
- 中间件：MariaDB 5.5.65

## 运行：
```shell
数据表创建：
MariaDB [(none)]> create table infos(id int(10) AUTO_INCREMENT,name varchar(10),iphone varchar(15),address varchar(20),info varchar(255),createtime timestamp,primary key('id'));

执行启动脚本：
[root@VM-0-14-centos vxoffcount]# ./start.sh
```
