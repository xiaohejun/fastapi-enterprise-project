# Makefile for AI Simulation Platform

ENV ?= dev

include $(ENV).env

# Variables
PROJECT_NAME := ai-sim-platform-$(ENV)
DOCKER_COMPOSE := COMPOSE_BAKE=true docker-compose --env-file $(ENV).env -p $(PROJECT_NAME)
PYTHON := python3
PIP := pip3
ALEMBIC := alembic
PYTEST := pytest

# Environment
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate

# Default target
all: help

##@ 初始化

.PHONY: venv
venv: ## 创建Python虚拟环境
	@echo "Creating Python virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created. Activate with: source $(VENV)/bin/activate"

.PHONY: install
install: ## 安装项目依赖
	@echo "Installing dependencies..."
	@$(PIP) install -U pip
	@$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

.PHONY: install-test
install-test: ## 安装测试依赖
	@echo "Installing test dependencies..."
	@$(PIP) install -r requirements-test.txt
	@echo "Test dependencies installed."

##@ 数据库迁移
.PHONY: migrate
migrate: ## 创建数据库迁移
	@echo "Creating database migration..."
	$(ALEMBIC) revision --autogenerate -m "auto migration"
	@echo "Migration created. Apply with: make upgrade"

.PHONY: upgrade
upgrade: ## 应用数据库迁移
	@echo "Applying database migrations..."
	$(ALEMBIC) upgrade head
	@echo "Migrations applied."

##@ 开发

.PHONY: run
run: ## 运行开发服务器
	@echo "Starting development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

##@ Docker

re-up: ## 删除之前容器的卷，重新构建镜像，然后前台运行
	@echo "Removing previous containers and volumes, rebuilding images, and starting containers in foreground..."
	$(DOCKER_COMPOSE) down -v --remove-orphans
	$(DOCKER_COMPOSE) up --build

.PHONY: build
build: ## 构建Docker镜像
	@echo "Building Docker images..."
	$(DOCKER_COMPOSE) build

.PHONY: upd
upd: ## 后台启动Docker容器
	@echo "Starting containers..."
	@$(DOCKER_COMPOSE) up -d

config:
	@$(DOCKER_COMPOSE) config

.PHONY: up
up: ## 前台启动Docker容器
	@echo "Starting containers in foreground..."
	$(DOCKER_COMPOSE) up

upb: ## 先构建镜像，然后前台启动Docker容器
	@echo "Starting containers in background..."
	$(DOCKER_COMPOSE) up --build

up-b-d: ## 先构建镜像，然后后台启动Docker容器
	@echo "Starting containers in background with build..."
	$(DOCKER_COMPOSE) up -d --build

.PHONY: down
down: ## 停止Docker容器
	@echo "Stopping containers..."
	$(DOCKER_COMPOSE) down

down-v:
	@echo "Stopping containers and removing volumes..."
	$(DOCKER_COMPOSE) down -v

.PHONY: docker-logs
logs: ## 查看容器日志
	$(DOCKER_COMPOSE) logs -f

# 运行单个测试文件
test-file:
	$(PYTEST) -vx $(file)

# 运行单个测试用例
test-case:
	@make up-b-d
	@sleep 2 # 等待容器启动，TODO: 优化等待时间
	@echo "Running test case: $(file)::$(case)"
	$(PYTEST) -vx --showlocals $(file)::$(case)
	@make down-v

.PHONY: test
test: ## 运行所有测试
	@echo "Running all tests..."
	$(PYTEST) -v --cov=app --cov-report=term-missing --cov-report=html

test-async-db: start-test-db
	PYTHONPATH=$(SOURCE_DIR) $(PYTEST) -v $(CORE_TEST_DIR)/test_async_database.py
	$(MAKE) stop-test-db

.PHONY: test-unit
test-unit: ## 运行单元测试
	@echo "Running unit tests..."
	$(PYTEST) -vx --showlocals  # 立即失败并显示详细输出：

.PHONY: test-unit-pdb
test-unit-pdb: ## 运行单元测试并进入调试模式
	$(PYTEST) tests/unit --pdb  # 立即失败并进入调试模式

.PHONY: test-integration
test-integration: ## 运行集成测试
	@echo "Running integration tests..."
	$(PYTEST) tests/integration -v


.PHONY: test-coverage
test-coverage: ## 生成测试覆盖率报告
	@echo "Generating test coverage report..."
	$(PYTEST) --cov=app --cov-report=html
	@echo "Coverage report generated at htmlcov/index.html"

.PHONY: lint
lint: ## 运行代码检查
	@echo "Running linters..."
	flake8 app/
	black --check app/
	mypy app/

.PHONY: format
format: ## 格式化代码
	@echo "Formatting code..."
	black app/
	isort app/



# .PHONY: docker-migrate
# migrate: ## 在Docker环境中运行数据库迁移
# 	@echo "Running database migrations in Docker..."
# 	$(DOCKER_COMPOSE) exec web alembic upgrade head

# .PHONY: docker-test
# test: docker-build-test ## 在Docker中运行测试
# 	@echo "Running tests in Docker..."
# 	docker run --rm --network=host -v $(PWD)/tests:/app/tests ai-sim-test

# .PHONY: docker-test-coverage
# test-coverage: docker-build-test ## 在Docker中运行测试并生成覆盖率报告
# 	@echo "Running tests with coverage in Docker..."
# 	docker run --rm --network=host -v $(PWD)/tests:/app/tests -v $(PWD)/coverage:/app/coverage ai-sim-test pytest --cov=app --cov-report=html:coverage/html

##@ 工具

.PHONY: shell
shell: ## 打开数据库交互式shell
	psql "postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@localhost:$(POSTGRES_LOCAL_PORT)/$(POSTGRES_DB)"

.PHONY: clean
clean: ## 清理临时文件
	@echo "Cleaning temporary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf coverage
	rm -f .coverage

.PHONY: help
help: ## 显示帮助信息
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)