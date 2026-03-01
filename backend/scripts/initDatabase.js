const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../database/liji.db');

// 确保数据库目录存在
const dbDir = path.dirname(DB_PATH);
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

const db = new sqlite3.Database(DB_PATH);

// 初始化数据库表
const initTables = () => {
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            // 启用外键约束
            db.run('PRAGMA foreign_keys = ON');
            
            // 用户表
            db.run(`
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT,
                    avatar TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            `);
            
            // 服务者表
            db.run(`
                CREATE TABLE IF NOT EXISTS providers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    type TEXT,
                    city TEXT,
                    address TEXT,
                    description TEXT,
                    rating REAL DEFAULT 5.0,
                    image TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            `);
            
            // 服务项目表
            db.run(`
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL,
                    duration TEXT,
                    FOREIGN KEY (provider_id) REFERENCES providers(id)
                )
            `);
            
            // 订单表
            db.run(`
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_no TEXT UNIQUE NOT NULL,
                    provider_id INTEGER,
                    service_id INTEGER,
                    contact_name TEXT NOT NULL,
                    contact_phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    service_date TEXT NOT NULL,
                    notes TEXT,
                    total_amount REAL,
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (provider_id) REFERENCES providers(id),
                    FOREIGN KEY (service_id) REFERENCES services(id)
                )
            `, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });
    });
};

// 插入示例数据
const seedData = () => {
    return new Promise((resolve, reject) => {
        // 检查是否已有数据
        db.get('SELECT COUNT(*) as count FROM providers', (err, row) => {
            if (err) {
                reject(err);
                return;
            }
            
            if (row.count > 0) {
                console.log('✅ 数据库已有数据，跳过初始化');
                resolve();
                return;
            }
            
            // 插入示例服务者
            const providers = [
                { name: '福寿殡葬服务中心', phone: '13800138001', type: 'funeral', city: '北京', address: '北京市朝阳区建国路88号', description: '专业殡葬服务，24小时服务', rating: 4.8, image: '/images/provider1.jpg' },
                { name: '安宁殡仪服务公司', phone: '13800138002', type: 'funeral', city: '北京', address: '北京市海淀区中关村大街1号', description: '提供一站式殡仪服务', rating: 4.6, image: '/images/provider2.jpg' },
                { name: '永恒纪念礼仪公司', phone: '13800138003', type: 'ceremony', city: '上海', address: '上海市浦东新区陆家嘴环路1000号', description: '专业追思会策划', rating: 4.9, image: '/images/provider3.jpg' }
            ];
            
            const insertProvider = db.prepare(`
                INSERT INTO providers (name, phone, type, city, address, description, rating, image) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            `);
            
            providers.forEach(p => {
                insertProvider.run(p.name, p.phone, p.type, p.city, p.address, p.description, p.rating, p.image);
            });
            insertProvider.finalize();
            
            // 插入示例服务项目
            const services = [
                { provider_id: 1, name: '基础殡葬套餐', description: '包含遗体接运、冷藏、火化等基本服务', price: 5800, duration: '3天' },
                { provider_id: 1, name: '豪华殡葬套餐', description: '包含全套殡葬服务、灵堂布置、追思会等', price: 15800, duration: '5天' },
                { provider_id: 2, name: '标准殡仪服务', description: '专业殡仪服务，包含遗体美容、告别仪式', price: 8800, duration: '3天' },
                { provider_id: 3, name: '追思会策划', description: '专业追思会策划与执行', price: 5000, duration: '1天' }
            ];
            
            const insertService = db.prepare(`
                INSERT INTO services (provider_id, name, description, price, duration) 
                VALUES (?, ?, ?, ?, ?)
            `);
            
            services.forEach(s => {
                insertService.run(s.provider_id, s.name, s.description, s.price, s.duration);
            });
            insertService.finalize();
            
            console.log('✅ 示例数据插入成功');
            resolve();
        });
    });
};

// 执行初始化
const init = async () => {
    try {
        console.log('🔄 正在初始化数据库...');
        await initTables();
        console.log('✅ 数据库表创建成功');
        await seedData();
        console.log('✅ 数据库初始化完成');
    } catch (err) {
        console.error('❌ 数据库初始化失败:', err);
    } finally {
        db.close();
    }
};

init();
