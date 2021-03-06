# coding: utf-8

"""
 Created by liuying on 2018/9/2.
"""

MONGO_HOST = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product'
KEYWORDS = '美食'

l1 = """
女鞋 红人同款 夏上新 帆布鞋 小皮鞋 一脚蹬 松糕厚底 平底鞋 低跟 中跟 高跟 穆勒鞋 复古方头 尖头 小粗跟 细跟 男鞋 休闲鞋 板鞋 帆布鞋 运动风 豆豆鞋 乐福鞋 雕花布洛克 船鞋 增高鞋 正装商务 户外休闲 爸爸鞋 德比鞋 孟克鞋 布鞋 女包 骚包 双肩包 男包 旅行箱 钱包 真皮包 大牌 宽肩带 小方包 水桶包 迷你包 链条包 贝壳包 波士顿包 手拿包 单肩包 手提包 斜挎包 零钱包 妈妈包 欧美潮搭 日韩流行 青春学院 男士商务 雅痞休闲 拉杆箱 腰包 胸包 手工皮具 红人优品 帽子 贝雷帽 渔夫帽 鸭舌帽 礼帽 草帽 爵士帽 盆帽 八角帽 丝巾 披肩 真丝围巾 棉麻围巾 方巾 手套 真皮手套 触屏手套 半指手套 全指手套 真皮腰带 腰带 手工皮带
"""
l2 = """
连衣裙 保暖连体 裤子 羽绒 居家睡衣 针织 帽子 亲子装 童鞋 学步鞋 女童运动鞋 男童运动鞋 毛毛虫童鞋 雪地靴 马丁靴 长靴 玩具 积木 毛绒玩具 早教 儿童自行车 电动童车 遥控模型 户外玩具 亲子玩具 学习用品 描红本 美妈大衣 孕妇裤 月子服 哺乳文胸 吸奶器 防辐射 孕妇内裤 连衣裙 待产包 孕妇牛仔裤 孕妇营养品 防溢乳垫 美德乐 十月妈咪 三洋 Bravado 新生儿 婴儿床 婴儿推车 睡袋 抱被 隔尿垫 学步车 安抚奶嘴 体温计 纸尿裤 花王 洗衣液 湿巾 爱他美 羊奶粉 特殊配方奶粉 喜宝 惠氏 启赋 牛栏 美素佳儿 贝因美 雅培 美赞臣 可瑞康 a2 嘉宝 美林 米粉 泡芙 溶溶豆 肉肠 果肉条 奶片 益生菌 维生素 钙铁锌 DHA 宝宝食用油 核桃油 葡萄糖 宝宝调料 奶瓶 餐具 餐椅 暖奶器
"""
l3 = """
淘宝速达 实体商场服务 淘火炬品牌 生活电器 厨房电器 个人护理 空气净化器 扫地机器人 吸尘器 取暖器 烤箱 豆浆机 榨汁料理 电饭煲 吹风机 足浴盆 剃须刀 卷发器 按摩器材 冬季火锅 蓝牙耳机 电暖桌 蓝牙音箱 电热毯 加湿器 暖风机 淘宝速达 淘宝火炬品牌 实体商场服务 2小时送货服务 surface平板电脑 苹果/Apple iPad Pro 电脑主机 数码相机 电玩动漫 单反相机 华为 MateBook IPAD mini4 游戏主机 鼠标键盘 无人机 二手数码 二手手机 二手笔记本 二手平板电脑 
"""
l4 = """
面膜 洁面 防晒 爽肤水 眼霜 乳液 面霜 精华 卸妆 男士护肤 眼线 粉底液 BB霜 隔离 睫毛膏 彩妆盘 唇膏 腮红 香水 精油 身体护理 丰胸 纤体 脱毛 海外直邮 洗发水 护发素 发膜 头发造型 染发膏 烫发水 假发 沐浴露 私处护理 身体乳液 牙膏 牙刷 漱口水 足浴 足贴 洗手液 卫生巾 成人纸尿裤 抽纸 卷纸 洗衣液 清洁剂 厨房清洁 家私/皮具护理 香薰 B族维生素 葡萄籽 辅酶Q10 消化酶 软骨素 维生素C 钙 大豆异黄酮 益生菌 鱼油 氨基葡萄糖 葡萄籽 生物素 玛咖（玛卡） 酵素 螺旋藻 胶原蛋白 月见草油 DHA 蔓越莓 左旋肉碱 褪黑素 锯棕榈
"""
l5 = """鸡尾酒 精酿啤酒 洋酒 红酒 荔枝 水果 百香果 芒果 小龙虾 樱桃 榴莲 杨梅 牛排 柠檬 海参 水蜜桃 咸鸭蛋 李子 桃子 龙虾 苹果 黄桃 火龙果 波罗蜜 山竹 蓝莓 鸡胸肉 猕猴桃 三文鱼 红薯 车厘子 海鲜 冰皮月饼 零食大礼包 牛肉干 面包 辣条 红枣 核桃 饼干 巧克力 葡萄干 芒果干 绿豆糕 薯片 锅巴 海苔 月饼 蛋黄酥 猪肉脯 花生 长沙臭豆腐 瓜子 山渣 全麦面包 早餐 腰果 压缩饼干"""