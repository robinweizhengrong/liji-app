-- 礼纪APP 数据库完整结构
-- 创建时间: 2026-02-26

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE,
    email TEXT,
    password_hash TEXT NOT NULL,
    avatar TEXT,
    real_name TEXT,
    role TEXT DEFAULT 'user', -- user, admin
    province TEXT,
    city TEXT,
    district TEXT,
    bio TEXT,
    is_vip BOOLEAN DEFAULT 0,
    vip_expire_date DATE,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 殡仪馆表
CREATE TABLE IF NOT EXISTS funeral_homes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    province TEXT NOT NULL,
    city TEXT NOT NULL,
    district TEXT,
    address TEXT NOT NULL,
    phone TEXT,
    mobile TEXT,
    contact_person TEXT,
    email TEXT,
    website TEXT,
    business_hours TEXT,
    services TEXT, -- JSON格式存储服务项目
    price_range TEXT, -- 价格区间说明
    price_details TEXT, -- JSON格式详细价格
    facilities TEXT, -- 设施介绍
    transport_info TEXT, -- 交通信息
    images TEXT, -- JSON格式图片URL数组
    is_verified BOOLEAN DEFAULT 0,
    rating REAL DEFAULT 5.0,
    view_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 档期表
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- vigil, farewell, funeral, burial, memorial, consult, training, other
    title TEXT,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    customer_name TEXT,
    customer_phone TEXT,
    location TEXT,
    amount REAL,
    note TEXT,
    status TEXT DEFAULT 'confirmed', -- confirmed, reserved, cancelled
    reminder_sent BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. 客户表
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    source TEXT, -- 客户来源
    note TEXT,
    last_service_date DATE,
    service_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 5. 教学资料表
CREATE TABLE IF NOT EXISTS teaching_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL, -- script, eulogy, process, music, course
    subcategory TEXT, -- 细分类型
    content TEXT,
    video_url TEXT,
    audio_url TEXT,
    file_url TEXT,
    images TEXT, -- JSON格式
    author TEXT,
    is_vip BOOLEAN DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. 课程表
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL, -- host, planner, funeral_director, counselor, florist
    instructor TEXT,
    cover_image TEXT,
    video_url TEXT,
    duration INTEGER, -- 分钟
    price REAL DEFAULT 0,
    is_free BOOLEAN DEFAULT 0,
    is_vip BOOLEAN DEFAULT 0,
    chapters TEXT, -- JSON格式章节
    view_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. 动态/帖子表
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT,
    images TEXT, -- JSON格式
    video_url TEXT,
    location TEXT,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 8. 关注表
CREATE TABLE IF NOT EXISTS follows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follower_id INTEGER NOT NULL,
    following_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (following_id) REFERENCES users(id),
    UNIQUE(follower_id, following_id)
);

-- 9. 点赞表
CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    UNIQUE(user_id, post_id)
);

-- 10. 团队表
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    logo TEXT,
    description TEXT,
    province TEXT,
    city TEXT,
    leader_id INTEGER NOT NULL,
    member_count INTEGER DEFAULT 1,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leader_id) REFERENCES users(id)
);

-- 11. 团队成员表
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT DEFAULT 'member', -- leader, admin, member
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(team_id, user_id)
);

-- 12. 订单/预订表
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    customer_name TEXT,
    customer_phone TEXT,
    service_type TEXT,
    service_date DATE,
    location TEXT,
    amount REAL,
    status TEXT DEFAULT 'pending', -- pending, confirmed, completed, cancelled
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 13. 省市区数据表
CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    parent_code TEXT,
    level INTEGER NOT NULL, -- 1:省 2:市 3:区
    full_name TEXT
);

-- 插入示例殡仪馆数据（达州市）
INSERT INTO funeral_homes (name, province, city, district, address, phone, mobile, contact_person, business_hours, services, price_range, price_details, facilities, transport_info) VALUES
('达州市殡仪馆', '四川省', '达州市', '通川区', '达州市通川区金龙大道南段', '0818-1234567', '13800138001', '李主任', '24小时', '["遗体接运", "冷藏", "火化", "告别仪式", "骨灰存放"]', '2000-15000元', '{"遗体接运": "300-800元", "冷藏": "100元/天", "火化": "500-1200元", "告别厅": "500-3000元", "骨灰盒": "200-5000元"}', '大型告别厅3个，中型5个，小型10个，火化炉4台', '可乘公交12路、18路到达，或自驾从市区出发约15分钟'),
('达州市仙鹤陵园', '四川省', '达州市', '达川区', '达州市达川区仙鹤路', '0818-2345678', '13900139002', '王经理', '08:00-18:00', '["墓地销售", "安葬服务", "祭祀服务", "骨灰安放"]', '8000-50000元', '{"墓地": "8000元起", "安葬费": "2000元", "祭祀用品": "50-500元"}', '墓区面积500亩，可容纳10万墓位', '位于达川区仙鹤山，环境优美，交通便利'),
('达州市福寿园殡仪馆', '四川省', '达州市', '通川区', '达州市通川区凤凰大道', '0818-3456789', '13700137003', '张主任', '24小时', '["遗体接运", "整容", "火化", "告别仪式"]', '1500-10000元', '{"遗体接运": "200-600元", "整容": "300-1000元", "火化": "400-1000元"}', '设施现代化，服务周到', '市区中心位置，交通便利');

-- 插入示例教学资料
INSERT INTO teaching_materials (title, category, subcategory, content, author, is_vip) VALUES
('告别仪式主持词模板', 'script', 'farewell', '各位来宾，各位亲友：今天，我们怀着无比沉痛的心情，在这里举行XXX先生的告别仪式...', '礼纪官方', 0),
('守灵仪式全流程', 'process', 'vigil', '一、布置灵堂；二、遗体入灵；三、上香祭拜；四、守夜安排...', '礼纪官方', 0),
('传统丧葬礼仪规范', 'course', 'etiquette', '中国传统丧葬礼仪源远流长，主要包括：初终、小殓、大殓、成服、做七、百日、周年等...', '张礼仪师', 1),
('哀伤辅导沟通技巧', 'course', 'counseling', '面对失去亲人的家属，我们应该：1.倾听为主；2.避免说教；3.适当陪伴...', '李心理咨询师', 1);

-- 插入示例课程
INSERT INTO courses (title, description, category, instructor, duration, price, is_free) VALUES
('生命礼仪主持基础', '从零开始学习生命礼仪主持，包括发声训练、台词创作、流程把控等', 'host', '张明德', 120, 0, 1),
('传统丧葬礼仪规范详解', '深入学习中国传统丧葬礼仪的每个环节', 'host', '王德贵', 180, 99, 0),
('入殓师专业技能培训', '遗体处理、防腐、整容等专业技能培训', 'funeral_director', '陈师傅', 240, 199, 0),
('花艺布置在生命礼仪中的应用', '学习如何使用鲜花布置灵堂、告别厅', 'florist', '赵花艺师', 90, 49, 0);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_funeral_homes_province ON funeral_homes(province);
CREATE INDEX IF NOT EXISTS idx_funeral_homes_city ON funeral_homes(city);
CREATE INDEX IF NOT EXISTS idx_schedules_user ON schedules(user_id);
CREATE INDEX IF NOT EXISTS idx_schedules_date ON schedules(date);
CREATE INDEX IF NOT EXISTS idx_customers_user ON customers(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_user ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_regions_parent ON regions(parent_code);
