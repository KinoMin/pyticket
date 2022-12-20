

# 12306_reptile

---

# 运行所需依赖
```bash
pip3 install requests -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install datetime -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install selenium -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install opencv-python -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install chardet -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install schedule -i https://mirrors.cloud.tencent.com/pypi/simple
pip3 install ttkbootstrap -i https://pypi.tuna.tsinghua.edu.cn/simple 
```

# 介绍
该项目使用 Python3 抓取 12306 实现在线抢票功能。

web开发使用 [Django](https://docs.djangoproject.com/)开发, 可视化界面使用 [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/zh/styleguide/entry/)进行开发。

# 运行
```bash
python3 ticket.py
```