-- 注音練習歷史記錄資料庫初始化腳本
-- Database: zhuyin_practice

-- 建立使用者資料表
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',  -- 預留給未來的後端認證
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 建立練習歷史記錄資料表
CREATE TABLE IF NOT EXISTS practice_history (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    word VARCHAR(10) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_ms INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (end_time - start_time)) * 1000
    ) STORED,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 建立索引以優化查詢效能
-- 1. 按使用者和時間查詢歷史記錄（最常用）
CREATE INDEX IF NOT EXISTS idx_user_time ON practice_history(user_id, start_time DESC);

-- 2. 按使用者名稱快速查找
CREATE INDEX IF NOT EXISTS idx_username ON users(username);

-- 3. 按使用者和正確性查詢（統計用）
CREATE INDEX IF NOT EXISTS idx_user_correct ON practice_history(user_id, is_correct);

-- 顯示建立的資料表
\dt

-- 顯示索引
\di
