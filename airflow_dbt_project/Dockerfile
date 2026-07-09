FROM apache/airflow:3.3.0

USER root 
# 切换容器用户为 root（默认airflow镜像普通用户无apt安装权限）

RUN apt-get update && apt-get install -y gcc && apt-get clean
# 更新apt软件源，安装gcc编译工具，然后清理缓存减小镜像体积

USER airflow 
# 切回airflow普通用户（生产不建议长期用root运行程序）

COPY requirements.txt .
# 把宿主机当前目录的requirements.txt复制到容器airflow用户工作目录

RUN pip install --no-cache-dir -r requirements.txt
# 读取依赖文件安装Python包，--no-cache-dir 不缓存pip安装包，瘦身镜像