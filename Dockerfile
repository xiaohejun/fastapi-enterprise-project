# FROM python:3.11-slim

# WORKDIR /app

# # 安装系统依赖
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     && rm -rf /var/lib/apt/lists/*

# # 安装Python依赖
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 复制项目文件
# COPY . .

# # 暴露端口
# EXPOSE 8000

# # 设置环境变量
# ENV PYTHONPATH=/app

# # 启动命令
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# 第一阶段：构建阶段
FROM python:3.13 AS builder

# 设置工作目录
WORKDIR /code

# 复制项目依赖文件
COPY requirements.txt .

RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/ 
RUN pip config set install.trusted-host mirrors.aliyun.com

# 创建虚拟环境并安装依赖
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段：运行阶段
FROM python:3.13-slim

# 创建非 root 用户
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

# 设置工作目录
WORKDIR /code

# 复制虚拟环境
COPY --from=builder /venv /venv

# 复制项目代码
COPY . .

# 设置环境变量，让系统使用虚拟环境
ENV PATH="/venv/bin:$PATH"

# 更改文件所有权为 appuser
RUN chown -R appuser:appgroup /code

# 切换到 appuser
USER appuser

# 暴露应用端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

