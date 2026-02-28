#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
礼纪APP - 全国殡仪馆数据收集脚本
用于收集全国各省市的殡仪馆信息
"""

import json
import sqlite3
import os
import time
from datetime import datetime

# 数据文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), '../database/liji.db')
DATA_FILE = os.path.join(os.path.dirname(__file__), 'funeral_homes_data.json')

# 全国省市数据
PROVINCES_CITIES = {
    "北京市": ["北京市"],
    "天津市": ["天津市"],
    "河北省": ["石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市", "衡水市"],
    "山西省": ["太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市", "吕梁市"],
    "内蒙古自治区": ["呼和浩特市", "包头市", "乌海市", "赤峰市", "通辽市", "鄂尔多斯市", "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市", "兴安盟", "锡林郭勒盟", "阿拉善盟"],
    "辽宁省": ["沈阳市", "大连市", "鞍山市", "抚顺市", "本溪市", "丹东市", "锦州市", "营口市", "阜新市", "辽阳市", "盘锦市", "铁岭市", "朝阳市", "葫芦岛市"],
    "吉林省": ["长春市", "吉林市", "四平市", "辽源市", "通化市", "白山市", "松原市", "白城市", "延边朝鲜族自治州"],
    "黑龙江省": ["哈尔滨市", "齐齐哈尔市", "鸡西市", "鹤岗市", "双鸭山市", "大庆市", "伊春市", "佳木斯市", "七台河市", "牡丹江市", "黑河市", "绥化市", "大兴安岭地区"],
    "上海市": ["上海市"],
    "江苏省": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市", "宿迁市"],
    "浙江省": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"],
    "安徽省": ["合肥市", "芜湖市", "蚌埠市", "淮南市", "马鞍山市", "淮北市", "铜陵市", "安庆市", "黄山市", "滁州市", "阜阳市", "宿州市", "六安市", "亳州市", "池州市", "宣城市"],
    "福建省": ["福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市", "南平市", "龙岩市", "宁德市"],
    "江西省": ["南昌市", "景德镇市", "萍乡市", "九江市", "新余市", "鹰潭市", "赣州市", "吉安市", "宜春市", "抚州市", "上饶市"],
    "山东省": ["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "莱芜市", "临沂市", "德州市", "聊城市", "滨州市", "菏泽市"],
    "河南省": ["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"],
    "湖北省": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市", "恩施土家族苗族自治州", "仙桃市", "潜江市", "天门市", "神农架林区"],
    "湖南省": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市", "娄底市", "湘西土家族苗族自治州"],
    "广东省": ["广州市", "韶关市", "深圳市", "珠海市", "汕头市", "佛山市", "江门市", "湛江市", "茂名市", "肇庆市", "惠州市", "梅州市", "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市", "潮州市", "揭阳市", "云浮市"],
    "广西壮族自治区": ["南宁市", "柳州市", "桂林市", "梧州市", "北海市", "防城港市", "钦州市", "贵港市", "玉林市", "百色市", "贺州市", "河池市", "来宾市", "崇左市"],
    "海南省": ["海口市", "三亚市", "三沙市", "儋州市", "五指山市", "琼海市", "文昌市", "万宁市", "东方市", "定安县", "屯昌县", "澄迈县", "临高县", "白沙黎族自治县", "昌江黎族自治县", "乐东黎族自治县", "陵水黎族自治县", "保亭黎族苗族自治县", "琼中黎族苗族自治县"],
    "重庆市": ["重庆市"],
    "四川省": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市", "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市", "阿坝藏族羌族自治州", "甘孜藏族自治州", "凉山彝族自治州"],
    "贵州省": ["贵阳市", "六盘水市", "遵义市", "安顺市", "毕节市", "铜仁市", "黔西南布依族苗族自治州", "黔东南苗族侗族自治州", "黔南布依族苗族自治州"],
    "云南省": ["昆明市", "曲靖市", "玉溪市", "保山市", "昭通市", "丽江市", "普洱市", "临沧市", "楚雄彝族自治州", "红河哈尼族彝族自治州", "文山壮族苗族自治州", "西双版纳傣族自治州", "大理白族自治州", "德宏傣族景颇族自治州", "怒江傈僳族自治州", "迪庆藏族自治州"],
    "西藏自治区": ["拉萨市", "日喀则市", "昌都市", "林芝市", "山南市", "那曲市", "阿里地区"],
    "陕西省": ["西安市", "铜川市", "宝鸡市", "咸阳市", "渭南市", "延安市", "汉中市", "榆林市", "安康市", "商洛市"],
    "甘肃省": ["兰州市", "嘉峪关市", "金昌市", "白银市", "天水市", "武威市", "张掖市", "平凉市", "酒泉市", "庆阳市", "定西市", "陇南市", "临夏回族自治州", "甘南藏族自治州"],
    "青海省": ["西宁市", "海东市", "海北藏族自治州", "黄南藏族自治州", "海南藏族自治州", "果洛藏族自治州", "玉树藏族自治州", "海西蒙古族藏族自治州"],
    "宁夏回族自治区": ["银川市", "石嘴山市", "吴忠市", "固原市", "中卫市"],
    "新疆维吾尔自治区": ["乌鲁木齐市", "克拉玛依市", "吐鲁番市", "哈密市", "昌吉回族自治州", "博尔塔拉蒙古自治州", "巴音郭楞蒙古自治州", "阿克苏地区", "克孜勒苏柯尔克孜自治州", "喀什地区", "和田地区", "伊犁哈萨克自治州", "塔城地区", "阿勒泰地区", "石河子市", "阿拉尔市", "图木舒克市", "五家渠市", "北屯市", "铁门关市", "双河市", "可克达拉市", "昆玉市", "胡杨河市", "新星市"]
}

# 示例殡仪馆数据（按城市）
SAMPLE_DATA = {
    "四川省": {
        "达州市": [
            {
                "name": "达州市殡仪馆",
                "district": "通川区",
                "address": "达州市通川区金龙大道南段",
                "phone": "0818-2123456",
                "mobile": "13882821234",
                "contact_person": "李主任",
                "business_hours": "24小时",
                "services": ["遗体接运", "冷藏", "火化", "告别仪式", "骨灰存放"],
                "price_range": "2000-15000元",
                "price_details": '{"遗体接运": "300-800元", "冷藏": "100元/天", "火化": "500-1200元", "告别厅": "500-3000元", "骨灰盒": "200-5000元"}',
                "facilities": "大型告别厅3个，中型5个，小型10个，火化炉4台",
                "transport_info": "可乘公交12路、18路到达，或自驾从市区出发约15分钟"
            },
            {
                "name": "达州市仙鹤陵园",
                "district": "达川区",
                "address": "达州市达川区仙鹤路888号",
                "phone": "0818-2345678",
                "mobile": "13900139002",
                "contact_person": "王经理",
                "business_hours": "08:00-18:00",
                "services": ["墓地销售", "安葬服务", "祭祀服务", "骨灰安放"],
                "price_range": "8000-50000元",
                "price_details": '{"墓地": "8000元起", "安葬费": "2000元", "祭祀用品": "50-500元"}',
                "facilities": "墓区面积500亩，可容纳10万墓位",
                "transport_info": "位于达川区仙鹤山，环境优美，交通便利"
            },
            {
                "name": "达州市福寿园殡仪馆",
                "district": "通川区",
                "address": "达州市通川区凤凰大道西段168号",
                "phone": "0818-3456789",
                "mobile": "13700137003",
                "contact_person": "张主任",
                "business_hours": "24小时",
                "services": ["遗体接运", "整容", "火化", "告别仪式"],
                "price_range": "1500-10000元",
                "price_details": '{"遗体接运": "200-600元", "整容": "300-1000元", "火化": "400-1000元"}',
                "facilities": "设施现代化，服务周到",
                "transport_info": "市区中心位置，交通便利"
            }
        ],
        "成都市": [
            {
                "name": "成都市殡仪馆",
                "district": "金牛区",
                "address": "成都市金牛区天回镇",
                "phone": "028-83501234",
                "mobile": "13800138000",
                "contact_person": "王主任",
                "business_hours": "24小时",
                "services": ["遗体接运", "冷藏", "火化", "告别仪式", "骨灰存放"],
                "price_range": "3000-20000元",
                "price_details": '{"遗体接运": "500-1000元", "冷藏": "150元/天", "火化": "800-1500元", "告别厅": "1000-5000元", "骨灰盒": "300-8000元"}',
                "facilities": "大型综合性殡仪馆，设施齐全",
                "transport_info": "地铁3号线天回镇站，公交有9路、25路"
            }
        ]
    },
    "北京市": {
        "北京市": [
            {
                "name": "北京市八宝山殡仪馆",
                "district": "石景山区",
                "address": "北京市石景山区石景山路9号",
                "phone": "010-88255666",
                "mobile": "13800138001",
                "contact_person": "值班室",
                "business_hours": "24小时",
                "services": ["遗体接运", "冷藏", "火化", "告别仪式", "骨灰存放"],
                "price_range": "5000-30000元",
                "price_details": '{"遗体接运": "800-1500元", "冷藏": "200元/天", "火化": "1000-2000元", "告别厅": "2000-10000元"}',
                "facilities": "国家一级殡仪馆，设施一流",
                "transport_info": "地铁1号线八宝山站，公交337路、389路"
            }
        ]
    },
    "上海市": {
        "上海市": [
            {
                "name": "上海市龙华殡仪馆",
                "district": "徐汇区",
                "address": "上海市徐汇区漕溪路210号",
                "phone": "021-64381234",
                "mobile": "13800138002",
                "contact_person": "业务部",
                "business_hours": "24小时",
                "services": ["遗体接运", "冷藏", "火化", "告别仪式", "骨灰存放"],
                "price_range": "5000-25000元",
                "price_details": '{"遗体接运": "600-1200元", "冷藏": "180元/天", "火化": "900-1800元", "告别厅": "1500-8000元"}',
                "facilities": "大型现代化殡仪馆",
                "transport_info": "地铁3号线漕溪路站，公交120路、157路"
            }
        ]
    }
}

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建殡仪馆表
    cursor.execute('''
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
            services TEXT,
            price_range TEXT,
            price_details TEXT,
            facilities TEXT,
            transport_info TEXT,
            images TEXT,
            is_verified BOOLEAN DEFAULT 0,
            rating REAL DEFAULT 5.0,
            view_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建省市区表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            parent_code TEXT,
            level INTEGER NOT NULL,
            full_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ 数据库初始化完成")

def import_sample_data():
    """导入示例数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for province, cities in SAMPLE_DATA.items():
        for city, homes in cities.items():
            for home in homes:
                cursor.execute('''
                    INSERT OR REPLACE INTO funeral_homes 
                    (name, province, city, district, address, phone, mobile, contact_person, 
                     business_hours, services, price_range, price_details, facilities, transport_info)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    home['name'], province, city, home.get('district', ''),
                    home['address'], home['phone'], home['mobile'], home['contact_person'],
                    home['business_hours'], json.dumps(home['services'], ensure_ascii=False),
                    home['price_range'], home['price_details'], home['facilities'], home['transport_info']
                ))
                count += 1
    
    conn.commit()
    conn.close()
    print(f"✓ 已导入 {count} 条殡仪馆数据")

def export_to_json():
    """导出数据为JSON文件"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM funeral_homes WHERE status = "active"')
    columns = [description[0] for description in cursor.description]
    
    data = []
    for row in cursor.fetchall():
        item = dict(zip(columns, row))
        # 解析JSON字段
        if item.get('services'):
            try:
                item['services'] = json.loads(item['services'])
            except:
                pass
        if item.get('price_details'):
            try:
                item['price_details'] = json.loads(item['price_details'])
            except:
                pass
        if item.get('images'):
            try:
                item['images'] = json.loads(item['images'])
            except:
                pass
        data.append(item)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    conn.close()
    print(f"✓ 已导出 {len(data)} 条数据到 {DATA_FILE}")

def generate_insert_sql():
    """生成SQL插入语句"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM funeral_homes LIMIT 10')
    columns = [description[0] for description in cursor.description]
    
    sql_lines = []
    for row in cursor.fetchall():
        values = []
        for val in row:
            if val is None:
                values.append('NULL')
            elif isinstance(val, str):
                values.append(f"'{val.replace(chr(39), chr(39)+chr(39))}'")
            elif isinstance(val, (int, float)):
                values.append(str(val))
            else:
                values.append(f"'{str(val)}'")
        
        sql = f"INSERT INTO funeral_homes ({', '.join(columns)}) VALUES ({', '.join(values)});"
        sql_lines.append(sql)
    
    conn.close()
    
    with open('funeral_homes_insert.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))
    
    print(f"✓ 已生成SQL文件 funeral_homes_insert.sql")

if __name__ == '__main__':
    print("=" * 60)
    print("礼纪APP - 殡仪馆数据管理工具")
    print("=" * 60)
    print()
    
    # 初始化数据库
    init_database()
    
    # 导入示例数据
    import_sample_data()
    
    # 导出JSON
    export_to_json()
    
    # 生成SQL
    generate_insert_sql()
    
    print()
    print("=" * 60)
    print("数据管理完成！")
    print("=" * 60)
