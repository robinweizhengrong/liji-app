const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../database/liji.db');

const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
        console.error('数据库连接失败:', err);
    } else {
        console.log('✅ 数据库连接成功');
    }
});

// 启用外键约束
db.run('PRAGMA foreign_keys = ON');

module.exports = db;
