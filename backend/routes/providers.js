const express = require('express');
const db = require('../config/database');
const router = express.Router();

// 获取服务者列表
router.get('/', (req, res) => {
    const { type, city, page = 1, limit = 20 } = req.query;
    
    let sql = 'SELECT * FROM providers WHERE 1=1';
    const params = [];
    
    if (type) {
        sql += ' AND type = ?';
        params.push(type);
    }
    
    if (city) {
        sql += ' AND city = ?';
        params.push(city);
    }
    
    sql += ' ORDER BY rating DESC LIMIT ? OFFSET ?';
    params.push(parseInt(limit), (parseInt(page) - 1) * parseInt(limit));
    
    db.all(sql, params, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: '查询失败' });
        }
        res.json({ providers: rows, page: parseInt(page), limit: parseInt(limit) });
    });
});

// 获取服务者详情
router.get('/:id', (req, res) => {
    const { id } = req.params;
    
    db.get('SELECT * FROM providers WHERE id = ?', [id], (err, provider) => {
        if (err) {
            return res.status(500).json({ error: '查询失败' });
        }
        
        if (!provider) {
            return res.status(404).json({ error: '服务者不存在' });
        }
        
        // 获取服务项目
        db.all('SELECT * FROM services WHERE provider_id = ?', [id], (err, services) => {
            if (err) {
                return res.status(500).json({ error: '查询服务项目失败' });
            }
            
            res.json({ ...provider, services });
        });
    });
});

module.exports = router;
