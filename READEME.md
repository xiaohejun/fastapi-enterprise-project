集成测试后的使用说明
1. 本地开发环境测试
bash
# 创建虚拟环境并安装依赖
make venv
source venv/bin/activate
make install
make install-test

# 启动测试数据库
docker-compose up -d test-db

# 运行所有测试
make test

# 或者运行特定测试
make test-unit
make test-integration

# 生成覆盖率报告
make test-coverage
2. Docker环境测试
bash
# 构建测试镜像
make docker-build-test

# 启动测试数据库
docker-compose up -d test-db

# 运行测试
make docker-test

# 运行测试并生成覆盖率报告
make docker-test-coverage
3. 完整Docker环境运行
bash
# 构建并启动所有服务
make docker-build
make docker-up

# 应用数据库迁移
make docker-migrate

# 运行测试（针对开发环境）
make docker-test

查看测试覆盖率报告：

bash
# 在浏览器中打开覆盖率报告
open htmlcov/index.html