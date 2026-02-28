const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, '../database/liji.db');

// 读取测试数据
const accounts = JSON.parse(fs.readFileSync(path.join(__dirname, 'test_accounts.json'), 'utf8'));
const posts = JSON.parse(fs.readFileSync(path.join(__dirname, 'test_posts.json'), 'utf8'));

const db = new sqlite3.Database(dbPath);

console.log('开始导入测试数据...');

// 清空现有测试数据
db.run('DELETE FROM users WHERE id >= 10001');
db.run('DELETE FROM posts WHERE id >= 1');

// 导入用户数据
let userCount = 0;
const insertUser = db.prepare(`
    INSERT INTO users (id, username, phone, password_hash, real_name, avatar, bio, province, city, is_vip, service_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

accounts.forEach(acc => {
    insertUser.run(
        acc.id,
        acc.username,
        acc.phone,
        acc.password,
        acc.name,
        acc.avatar,
        acc.bio,
        acc.province,
        acc.city,
        acc.is_vip ? 1 : 0,
        acc.service_count
    );
    userCount++;
});

insertUser.finalize();

// 导入帖子数据
let postCount = 0;
const insertPost = db.prepare(`
    INSERT INTO posts (id, user_id, content, images, location, view_count, like_count, comment_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

posts.forEach(post => {
    insertPost.run(
        post.id,
        post.user_id,
        post.content,
        JSON.stringify(post.images),
        post.location,
        post.view_count,
        post.like_count,
        post.comment_count,
        post.created_at
    );
    postCount++;
});

insertPost.finalize();

db.close();

console.log(`✅ 已导入 ${userCount} 个虚拟用户`);
console.log(`✅ 已导入 ${postCount} 条虚拟帖子`);
console.log('测试数据准备完成！');
