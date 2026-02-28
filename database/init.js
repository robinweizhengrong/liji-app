// 初始化数据库
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, 'liji.db');

// 如果数据库文件已存在，先删除（用于重新初始化）
if (fs.existsSync(dbPath)) {
    console.log('数据库已存在，跳过初始化');
    process.exit(0);
}

const db = new sqlite3.Database(dbPath);

console.log('🔄 正在初始化数据库...');

db.serialize(() => {
    // 档期表
    db.run(`CREATE TABLE IF NOT EXISTS bookings (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        customer_name TEXT,
        customer_phone TEXT,
        location TEXT,
        amount REAL,
        notes TEXT,
        status TEXT DEFAULT 'booked',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )`, (err) => {
        if (err) console.error('创建档期表失败:', err);
        else console.log('✅ 档期表创建成功');
    });

    // 客户表
    db.run(`CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        notes TEXT,
        source TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )`, (err) => {
        if (err) console.error('创建客户表失败:', err);
        else console.log('✅ 客户表创建成功');
    });

    // 服务记录表
    db.run(`CREATE TABLE IF NOT EXISTS services (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        booking_id TEXT,
        type TEXT,
        date TEXT,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (booking_id) REFERENCES bookings(id)
    )`, (err) => {
        if (err) console.error('创建服务记录表失败:', err);
        else console.log('✅ 服务记录表创建成功');
    });

    // 文件上传表
    db.run(`CREATE TABLE IF NOT EXISTS uploads (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        original_name TEXT,
        path TEXT NOT NULL,
        type TEXT,
        size INTEGER,
        uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
    )`, (err) => {
        if (err) console.error('创建文件上传表失败:', err);
        else console.log('✅ 文件上传表创建成功');
    });

    // 插入示例数据
    const { v4: uuidv4 } = require('uuid');
    
    // 示例客户
    const customerId1 = uuidv4();
    const customerId2 = uuidv4();
    
    db.run(`INSERT INTO customers (id, name, phone, notes, source) VALUES 
        (?, '王家属', '13800138001', '老客户推荐', '转介绍'),
        (?, '李家属', '13900139001', '第一次合作', '网络')`,
        [customerId1, customerId2],
        (err) => {
            if (err) console.error('插入示例客户失败:', err);
            else console.log('✅ 示例客户数据插入成功');
        }
    );

    // 示例档期
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    db.run(`INSERT INTO bookings (id, type, start_time, end_time, customer_name, customer_phone, location, amount, status) VALUES 
        (?, '守灵', ?, ?, '王家属', '13800138001', '龙华殡仪馆', 2800, 'booked'),
        (?, '告别仪式', ?, ?, '李家属', '13900139001', '西郊殡仪馆', 3500, 'booked')`,
        [
            uuidv4(), 
            now.toISOString(), 
            new Date(now.getTime() + 2 * 60 * 60 * 1000).toISOString(),
            uuidv4(),
            tomorrow.toISOString(),
            new Date(tomorrow.getTime() + 3 * 60 * 60 * 1000).toISOString()
        ],
        (err) => {
            if (err) console.error('插入示例档期失败:', err);
            else console.log('✅ 示例档期数据插入成功');
        }
    );
});

db.close(() => {
    console.log('🎉 数据库初始化完成！');
    console.log('📁 数据库文件:', dbPath);
});
