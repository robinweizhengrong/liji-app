// 礼纪APP - API服务
const API_BASE_URL = window.location.origin;

// ==================== 档期管理 ====================
const BookingAPI = {
    // 获取所有档期
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/api/bookings`);
        return response.json();
    },

    // 创建档期
    async create(data) {
        const response = await fetch(`${API_BASE_URL}/api/bookings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    // 更新档期
    async update(id, data) {
        const response = await fetch(`${API_BASE_URL}/api/bookings/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    // 删除档期
    async delete(id) {
        const response = await fetch(`${API_BASE_URL}/api/bookings/${id}`, {
            method: 'DELETE'
        });
        return response.json();
    }
};

// ==================== 客户管理 ====================
const CustomerAPI = {
    // 获取所有客户
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/api/customers`);
        return response.json();
    },

    // 创建客户
    async create(data) {
        const response = await fetch(`${API_BASE_URL}/api/customers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};

// ==================== 文件上传 ====================
const UploadAPI = {
    // 上传文件
    async upload(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });
        return response.json();
    },

    // 获取上传的文件列表
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/api/uploads`);
        return response.json();
    }
};

// ==================== 统计数据 ====================
const StatsAPI = {
    // 获取统计数据
    async get() {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        return response.json();
    }
};

// ==================== 工具函数 ====================
const Utils = {
    // 格式化日期
    formatDate(dateStr) {
        const date = new Date(dateStr);
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    },

    // 格式化时间
    formatTime(dateStr) {
        const date = new Date(dateStr);
        return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },

    // 显示Toast
    showToast(message) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 10000;
            font-size: 14px;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2000);
    },

    // 显示加载中
    showLoading() {
        const loading = document.createElement('div');
        loading.id = 'global-loading';
        loading.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        loading.innerHTML = '<div style="font-size: 18px;">加载中...</div>';
        document.body.appendChild(loading);
    },

    // 隐藏加载中
    hideLoading() {
        const loading = document.getElementById('global-loading');
        if (loading) loading.remove();
    }
};

// ==================== 全局状态管理 ====================
const AppState = {
    currentUser: null,
    bookings: [],
    customers: [],
    stats: {},

    // 初始化
    async init() {
        await this.loadStats();
        await this.loadBookings();
        await this.loadCustomers();
    },

    // 加载统计数据
    async loadStats() {
        this.stats = await StatsAPI.get();
    },

    // 加载档期数据
    async loadBookings() {
        this.bookings = await BookingAPI.getAll();
    },

    // 加载客户数据
    async loadCustomers() {
        this.customers = await CustomerAPI.getAll();
    }
};

// 导出API
window.LijiAPI = {
    Booking: BookingAPI,
    Customer: CustomerAPI,
    Upload: UploadAPI,
    Stats: StatsAPI,
    Utils: Utils,
    State: AppState
};
