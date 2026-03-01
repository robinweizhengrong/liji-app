const express = require('express');
const db = require('../config/database');
const router = express.Router();

// 创建订单
router.post('/', (req, res) => {
    const { provider_id, service_id, contact_name, contact_phone, address, service_date, notes, total_amount } = req.body;
    
    if (!provider_id || !service_id || !contact_name || !contact_phone || !address || !service_date) {
        return res.status(400).json({ error: '请填写完整的订单信息' });
    }
    
    const orderNo = 'ORD' + Date.now() + Math.floor(Math.random() * 1000);
    const status = 'pending';
    const created_at = new Date().toISOString();
    
    db.run(
        `INSERT INTO orders (order_no, provider_id, service_id, contact_name, contact_phone, address, service_date, notes, total_amount, status, created_at) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [orderNo, provider_id, service_id, contact_name, contact_phone, address, service_date, notes || '', total_amount || 0, status, created_at],
        function(err) {
            if (err) {
                console.error('创建订单失败:', err);
                return res.status(500).json({ error: '创建订单失败' });
            }
            
            res.json({
                message: '订单创建成功',
                order: {
                    id: this.lastID,
                    order_no: orderNo,
                    provider_id,
                    service_id,
                    contact_name,
                    contact_phone,
                    address,
                    service_date,
                    notes,
                    total_amount,
                    status,
                    created_at
                }
            });
        }
    );
});

// 获取订单详情
router.get('/:id', (req, res) => {
    const { id } = req.params;
    
    db.get(`
        SELECT o.*, p.name as provider_name, p.phone as provider_phone, s.name as service_name 
        FROM orders o
        LEFT JOIN providers p ON o.provider_id = p.id
        LEFT JOIN services s ON o.service_id = s.id
        WHERE o.id = ?
    `, [id], (err, order) => {
        if (err) {
            console.error('查询订单失败:', err);
            return res.status(500).json({ error: '查询订单失败' });
        }
        
        if (!order) {
            return res.status(404).json({ error: '订单不存在' });
        }
        
        res.json(order);
    });
});

module.exports = router;
