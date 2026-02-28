const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../config/database');
const router = express.Router();

// 注册
router.post('/register', async (req, res) => {
    const { phone, password, name } = req.body;
    
    if (!phone || !password) {
        return res.status(400).json({ error: '手机号和密码不能为空' });
    }
    
    const hashedPassword = await bcrypt.hash(password, 10);
    
    db.run(
        'INSERT INTO users (phone, password, name) VALUES (?, ?, ?)',
        [phone, hashedPassword, name || phone],
        function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed')) {
                    return res.status(409).json({ error: '手机号已注册' });
                }
                return res.status(500).json({ error: '注册失败' });
            }
            
            const token = jwt.sign(
                { userId: this.lastID, phone },
                process.env.JWT_SECRET || 'default-secret',
                { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
            );
            
            res.json({
                message: '注册成功',
                token,
                user: { id: this.lastID, phone, name: name || phone }
            });
        }
    );
});

// 登录
router.post('/login', (req, res) => {
    const { phone, password } = req.body;
    
    if (!phone || !password) {
        return res.status(400).json({ error: '手机号和密码不能为空' });
    }
    
    db.get('SELECT * FROM users WHERE phone = ?', [phone], async (err, user) => {
        if (err) {
            return res.status(500).json({ error: '查询失败' });
        }
        
        if (!user) {
            return res.status(401).json({ error: '用户不存在' });
        }
        
        const isValid = await bcrypt.compare(password, user.password);
        
        if (!isValid) {
            return res.status(401).json({ error: '密码错误' });
        }
        
        const token = jwt.sign(
            { userId: user.id, phone: user.phone },
            process.env.JWT_SECRET || 'default-secret',
            { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
        );
        
        res.json({
            message: '登录成功',
            token,
            user: {
                id: user.id,
                phone: user.phone,
                name: user.name,
                avatar: user.avatar
            }
        });
    });
});

module.exports = router;
