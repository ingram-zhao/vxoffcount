# !/bin/bash

# 1.安装第三方模块：requirements.txt
pip3 install -r requirements.txt > /dev/null

# 2.启动定时任务：getAccessToken.py
nohup python3 getAccessToken.py > ./logs/getAccessToken.out &

# 3.生成自定义菜单：vxapi.py
python3 vxapi.py > /dev/null

# 4.启动服务：main.py 80
nohup python3 main.py 80 > ./logs/start.out &


