# 🏢 后端部署指南

本指南将引导您完成 WHartTest 后端服务的生产环境部署。系统已改为使用API方式调用嵌入模型，无需本地下载模型文件。



### 🛠️ 后端部署
部署后端服务前，需要部署以下服务：
xinference、playwright-mcp、qdrant、postgres、redis、drawio


#### 1. 系统准备
首先，安装 `uv`，一个先进的 Python 包管理器。
```bash
# 安装 uv (官方安装方式)
curl -LsSf https://astral.sh/uv/install.sh | sh

# python安装uv
pip install uv
```

#### 2. 克隆项目
```bash
git clone https://github.com/MGdaasLab/WHartTest.git
cd WHartTest_Django
```

#### 3. 创建并激活虚拟环境
使用 `uv` 创建并激活一个基于 Python 3.11 的虚拟环境。
```bash
# 使用 Python 3.11 创建虚拟环境
uv venv --python 3.11 

# 激活虚拟环境
source .venv/bin/activate #ubantu激活方式
.venv\Scripts\activate #Windows激活方式
```

#### 4. 安装依赖
使用 `uv` 高效地安装项目依赖。
```bash
uv pip install -r requirements.txt
```

#### 5. env配置
```
cp .env.example .env  # 创建env副本使其生效

注意：env中的向量库、数据库的具体配置以及后端地址需要手动修改和你实际部署的服务配置要对应
```


#### 6. 数据库迁移和初始化
```bash
# 执行数据库迁移
uv run python manage.py migrate
# 初始化数据库
uv run python manage.py init_admin
```

#### 7.. 启动服务
```bash
# 开发环境启动
uv run uvicorn wharttest_django.asgi:application --reload --host 127.0.0.1 --port 8000
```