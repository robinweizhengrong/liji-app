# 礼纪APP - 虚拟测试账号数据
# 生成时间: 2026-02-27
# 总账号数: 120个 (12职业 × 10人)

import json
import random
import hashlib
from datetime import datetime, timedelta

# 职业列表
PROFESSIONS = [
    "策划师", "主持人", "礼仪师", "入殓师", "花艺师", 
    "摄像师", "摄影师", "歌手", "舞蹈", "乐队", "法事", "殡仪馆"
]

# 姓氏列表
SURNAMES = ['张', '王', '李', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗']

# 名字列表
NAMES = ['明', '华', '强', '伟', '磊', '静', '敏', '丽', '婷', '娜', '涛', '杰', '浩', '鹏', '宇', '欣', '雨', '晨', '辉', '霞', '龙', '凤', '刚', '勇', '军', '文', '武', '斌', '波', '超']

# 城市列表
CITIES = [
    ("四川省", "达州市"),
    ("四川省", "成都市"),
    ("四川省", "绵阳市"),
    ("北京市", "北京市"),
    ("上海市", "上海市"),
    ("广东省", "广州市"),
    ("广东省", "深圳市"),
    ("浙江省", "杭州市"),
    ("江苏省", "南京市"),
    ("湖北省", "武汉市"),
]

# 头像表情列表
AVATARS = ['👤', '👨', '👩', '🧑', '👴', '👵', '👦', '👧', '🧔', '👱']

# 生成随机手机号
def generate_phone():
    prefixes = ['138', '139', '135', '136', '137', '150', '151', '152', '157', '158', '159', '182', '183', '187', '188']
    return random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(8)])

# 生成随机姓名
def generate_name():
    return random.choice(SURNAMES) + random.choice(NAMES) + random.choice(['', random.choice(NAMES)])

# 生成测试账号
def generate_test_accounts():
    accounts = []
    account_id = 10001
    
    for profession in PROFESSIONS:
        for i in range(1, 11):  # 每个职业10个账号
            province, city = random.choice(CITIES)
            name = generate_name()
            phone = generate_phone()
            username = f"{profession}{i:02d}"
            password = "Test123456"
            
            account = {
                "id": account_id,
                "username": username,
                "password": password,
                "name": name,
                "phone": phone,
                "profession": profession,
                "province": province,
                "city": city,
                "avatar": random.choice(AVATARS),
                "bio": f"专业{profession}，从业{random.randint(3, 20)}年，服务{random.randint(100, 1000)}+场",
                "service_count": random.randint(50, 500),
                "fans": random.randint(10, 500),
                "following": random.randint(5, 100),
                "is_vip": random.choice([True, False]),
                "created_at": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
            }
            accounts.append(account)
            account_id += 1
    
    return accounts

# 生成帖子内容
POST_CONTENTS = [
    "今天刚完成一场告别仪式，家属非常满意，感谢团队的配合。🙏",
    "分享一个感人的故事，这位老先生一生奉献给了教育事业...",
    "守灵服务中，看到家属们对逝者的深情，让我更加理解这份工作的意义。",
    "新的花艺布置方案，大家觉得怎么样？💐",
    "今天学习了新的主持技巧，分享给大家。",
    "又一场圆满的仪式，记录一下工作日常。📸",
    "感谢客户的信任，我们会继续努力做好每一次服务。",
    "分享一下今天的场地布置，简约而庄重。",
    "从业第X年，见证了无数感人的告别时刻。",
    "每一次服务都是一次生命的教育，珍惜当下。",
    "刚完成一场传统法事，记录一下流程。",
    "团队协作真的很重要，感谢每一位伙伴。👥",
    "分享一段主持词，希望对大家有帮助。",
    "今天的仪式很特别，是一段跨越半个世纪的告别。",
    "用音乐送别，让告别更有温度。🎵"
]

POST_IMAGES = ['🕯️', '⚰️', '🌸', '🙏', '💐', '🎵', '📸', '🕊️', '🌹', '🎤', '🎬', '🎨']

# 生成虚拟帖子
def generate_posts(accounts):
    posts = []
    post_id = 1
    
    for account in accounts:
        # 每个账号发3-8条帖子
        post_count = random.randint(3, 8)
        
        for i in range(post_count):
            content = random.choice(POST_CONTENTS).replace('X', str(account['service_count'] // 100 + 1))
            has_images = random.choice([True, True, False])  # 70%概率有图片
            
            post = {
                "id": post_id,
                "user_id": account['id'],
                "username": account['name'],
                "profession": account['profession'],
                "avatar": account['avatar'],
                "content": content,
                "images": [random.choice(POST_IMAGES) for _ in range(random.randint(1, 3))] if has_images else [],
                "location": f"{account['province']} {account['city']}",
                "view_count": random.randint(50, 5000),
                "like_count": random.randint(5, 500),
                "comment_count": random.randint(0, 50),
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d %H:%M")
            }
            posts.append(post)
            post_id += 1
    
    return posts

# 生成数据
accounts = generate_test_accounts()
posts = generate_posts(accounts)

# 保存账号数据
with open('test_accounts.json', 'w', encoding='utf-8') as f:
    json.dump(accounts, f, ensure_ascii=False, indent=2)

# 保存帖子数据
with open('test_posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

# 生成Excel/CSV格式的账号表格
with open('test_accounts_table.txt', 'w', encoding='utf-8') as f:
    f.write("账号ID,用户名,密码,姓名,手机号,职业,省份,城市,简介,服务场次,粉丝数\n")
    for acc in accounts:
        f.write(f"{acc['id']},{acc['username']},{acc['password']},{acc['name']},{acc['phone']},{acc['profession']},{acc['province']},{acc['city']},{acc['bio']},{acc['service_count']},{acc['fans']}\n")

print(f"✅ 已生成 {len(accounts)} 个测试账号")
print(f"✅ 已生成 {len(posts)} 条测试帖子")
print(f"✅ 账号表格已保存至 test_accounts_table.txt")
print(f"✅ 详细数据已保存至 test_accounts.json 和 test_posts.json")
print()
print("=" * 60)
print("测试账号示例（前5个）：")
print("=" * 60)
for acc in accounts[:5]:
    print(f"用户名: {acc['username']:<12} 密码: {acc['password']:<12} 职业: {acc['profession']:<8} 姓名: {acc['name']}")
