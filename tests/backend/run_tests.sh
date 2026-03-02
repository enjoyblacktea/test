#!/bin/bash
# Test Runner Script for Backend API Tests
# Automatically sets up test database and runs pytest

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== 後端 API 測試運行腳本 ===${NC}\n"

# Configuration
DB_USER="${DB_USER:-zhuyin_user}"
DB_NAME="zhuyin_practice_test"
BACKEND_DIR="../../backend"
MIGRATION_FILE="$BACKEND_DIR/migrations/init_db.sql"

# Step 1: Check PostgreSQL is running
echo -e "${YELLOW}[1/5]${NC} 檢查 PostgreSQL 狀態..."
if ! pg_isready -q; then
    echo -e "${RED}✗ PostgreSQL 未運行${NC}"
    echo "請啟動 PostgreSQL: sudo systemctl start postgresql"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL 運行中${NC}\n"

# Step 2: Check if test database exists
echo -e "${YELLOW}[2/5]${NC} 檢查測試資料庫..."
if psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo -e "${GREEN}✓ 測試資料庫已存在: $DB_NAME${NC}"
else
    echo -e "${YELLOW}! 測試資料庫不存在，正在創建...${NC}"
    createdb -U "$DB_USER" "$DB_NAME" || {
        echo -e "${RED}✗ 無法創建資料庫${NC}"
        echo "手動創建: createdb -U $DB_USER $DB_NAME"
        exit 1
    }
    echo -e "${GREEN}✓ 測試資料庫已創建${NC}"
fi
echo ""

# Step 3: Run migrations
echo -e "${YELLOW}[3/5]${NC} 執行資料庫遷移..."
if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}✗ 找不到遷移檔案: $MIGRATION_FILE${NC}"
    exit 1
fi

# Check if migrations already run
TABLE_COUNT=$(psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
if [ "$TABLE_COUNT" -lt 3 ]; then
    echo -e "${YELLOW}執行遷移腳本...${NC}"
    psql -U "$DB_USER" -d "$DB_NAME" -f "$MIGRATION_FILE" > /dev/null || {
        echo -e "${RED}✗ 遷移失敗${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ 遷移完成${NC}"
else
    echo -e "${GREEN}✓ 資料庫結構已初始化 ($TABLE_COUNT 個資料表)${NC}"
fi
echo ""

# Step 4: Check Python dependencies
echo -e "${YELLOW}[4/5]${NC} 檢查 Python 依賴..."
if ! python3 -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}! pytest 未安裝，正在安裝...${NC}"
    cd "$BACKEND_DIR" && uv pip install pytest pytest-cov
    echo -e "${GREEN}✓ pytest 已安裝${NC}"
else
    echo -e "${GREEN}✓ pytest 已安裝${NC}"
fi
echo ""

# Step 5: Run tests
echo -e "${YELLOW}[5/5]${NC} 執行測試..."
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Run pytest with options
pytest test_api.py -v --tb=short "$@"

TEST_RESULT=$?

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ 所有測試通過！${NC}"
else
    echo -e "${RED}✗ 部分測試失敗（退出碼: $TEST_RESULT）${NC}"
fi

exit $TEST_RESULT
