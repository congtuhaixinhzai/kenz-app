import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Comprehensive Vietnamese to Chinese mapping
ZH_MAP = {
    # 1. Navigation & Headers
    "Giới thiệu": "关于我们",
    "KTV HÀ NỘI": "河内KTV",
    "Hình ảnh": "图片环境",
    "Ưu đãi": "优惠活动",
    "Liên hệ": "联系我们",
    "Đánh giá": "顾客评价",
    "Tin tức": "新闻资讯",
    "Tin tức & kinh nghiệm hát karaoke": "新闻与欢唱攻略",
    "Đặt phòng ngay": "立即预订",
    "Đặt phòng": "预订包厢",
    "Đặt bàn": "预订留座",
    "Đặt bàn giữ chỗ": "预订留座",
    "Gọi điện": "致电热线",
    "Gọi ngay": "立即拨打",
    "Gọi": "拨打",
    "Zalo": "Zalo 客服",
    "WeChat": "微信客服",
    "Tiếng Việt": "Tiếng Việt",
    "中文": "中文",
    "HOT": "热门",
    "Trang chủ": "首页",
    "Hệ thống KTV Hà Nội": "河内KTV连锁系统",
    "Hệ Thống": "连锁系统",
    "Hệ Thống 36+ Quán Karaoke KTV Hà Nội": "河内 36+ KTV 豪华连锁系统",
    "Hệ Thống Karaoke KTV Hà Nội VIP": "河内顶级豪华KTV连锁系统",
    "Hệ Thống 36+ Quán Karaoke KTV Hà Nội VIP – Đặt Phòng Nhanh 24/7": "河内36+顶级豪华KTV连锁系统 – 24小时极速预订",
    "KARAOKE": "KARAOKE 豪华KTV",
    "KENZ": "KENZ 顶级连锁",
    "KTV VIP": "顶级豪华KTV",
    "VIP": "VIP 顶级包厢",
    "Website": "网站",
    "và": "及",
    "Quản trị test": "后台管理测试",
    "wxid_0oxdncgq75g312": "wxid_0oxdncgq75g312",
    "© 2026": "© 2026 版权所有",
    "© Karaoke Kenz Club 202 Trung Kính": "© Karaoke Kenz Club 202 Trung Kính 旗舰店",
    ". All rights reserved.": "。版权所有。",
    "Breadcrumb": "面包屑导航",
    "Hỗ trợ nhanh": "快捷客服",
    "Đóng": "关闭",
    "5 sao": "5 星好评",
    "★★★★★": "★★★★★ 五星好评",
    "⭐ 5.0 VIP": "⭐ 5.0 VIP 顶级认证",
    "· Cam kết dịch vụ phòng hát chất lượng cao.": "· 品质包厢保证，高标准服务体验。",
    "· Cam kết phục vụ chu đáo, chất lượng âm thanh đỉnh cao.": "· 承诺周到服务，震撼巅峰音质。",
    "Hotline đặt phòng VIP 24/7:": "24/7 VIP 预订专线：",
    "Hotline điều phối & đặt phòng VIP 24/7:": "24/7 VIP 预订及调度专线：",
    "Cam kết dịch vụ phòng hát chất lượng cao.": "品质包厢保证，高标准服务体验。",
    "Cam kết phục vụ chu đáo, chất lượng âm thanh đỉnh cao.": "承诺周到服务，震撼巅峰音质。",
    "Karaoke KTV Hà Nội": "河内顶级KTV连锁",

    # 2. Mega Dropdown Navigation & Stats
    "👑 HỆ THỐNG 36+ QUÁN KARAOKE KTV VIP": "👑 36+ 顶级豪华KTV连锁系统",
    "👑 HỆ THỐNG QUÁN KARAOKE KTV VIP (CẦU GIẤY & ĐỐNG ĐA)": "👑 豪华KTV连锁系统（纸桥 & 栋多郡）",
    "👑 HỆ THỐNG 21+ QUÁN KARAOKE KTV VIP": "👑 21+ 顶级豪华KTV连锁系统",
    "Xem tất cả 36 cơ sở →": "查看全部36家分店 →",
    "Xem tất cả 21 cơ sở →": "查看全部21家分店 →",
    "Xem toàn bộ 21 quán Cầu Giấy & Đống Đa →": "查看纸桥与栋多全部21家分店 →",
    "📍 Cầu Giấy (12 quán)": "📍 纸桥郡 Cầu Giấy (12家)",
    "📍 Cầu Giấy (Ưu tiên hàng đầu)": "📍 纸桥郡（顶级优先推荐）",
    "📍 Cầu Giấy (Cơ sở mở rộng)": "📍 纸桥郡（优质热门推荐）",
    "📍 Đống Đa (Trung tâm giải trí)": "📍 栋多郡（娱乐休闲中心）",
    "📍 Đống Đa & Hà Đông": "📍 栋多 & 河东郡 (15家)",
    "📍 Nam Từ Liêm & Khu Vực Khác": "📍 南慈廉 & 其他区域 (9家)",
    "📞 Hotline điều phối 24/7:": "📞 24小时调度热线：",
    "Xem bản đồ & toàn bộ 36 quán →": "查看地图及全部36家分店 →",
    "Xem bản đồ & toàn bộ 21 quán →": "查看地图及全部21家分店 →",
    "Xem tất cả 36 quán KTV": "查看全部36家KTV",
    "Xem tất cả 21 quán KTV": "查看全部21家KTV",
    "Xem tất cả 36 quán →": "查看全部36家分店 →",
    "Xem tất cả 21 quán →": "查看全部21家分店 →",
    "Xem đầy đủ 36 quán KTV Hà Nội & Sài Gòn": "查看河内及胡志明市全部36家KTV",
    "⭐ Kenz Club 202 Trung Kính": "⭐ Kenz Club 202 Trung Kính 旗舰店",
    "👑 Kenz Club 202 Trung Kính (Chính Chủ)": "👑 Kenz Club 202 Trung Kính (旗舰总店)",
    "Karaoke Kenz 202 Trung Kính": "Karaoke Kenz 202 Trung Kính 旗舰店",
    "⭐ Royal Club 97 Cầu Giấy": "⭐ Royal Club 97 Cầu Giấy (皇家旗舰店)",
    "⭐ Thượng Hải KTV 229 Tây Sơn": "⭐ Thượng Hải KTV 229 Tây Sơn (上海风情旗舰店)",
    "⭐ Tip Top 85G Nguyễn Khang": "⭐ Tip Top 85G Nguyễn Khang (顶尖品质店)",
    "⭐ LONDON 28 Thành Thái": "⭐ LONDON 28 Thành Thái (伦敦英伦店)",
    "⭐ Karaoke S 69 Trần Thái": "⭐ Karaoke S 69 Trần Thái (S 时尚名店)",
    "Summit 64 Trần Thái Tông": "Summit 64 Trần Thái Tông (巅峰皇家店)",
    "Zozo 12 Trần Kim Xuyến": "Zozo 12 Trần Kim Xuyến (佐佐时尚店)",
    "Flamenco 16-18 Vũ Phạm Hàm": "Flamenco 16-18 Vũ Phạm Hàm (弗拉门戈豪华店)",
    "36 quán": "36家分店",
    "21 quán": "21家分店",
    "36 quán KTV VIP": "36家顶级KTV",
    "21 quán KTV VIP": "21家顶级KTV",
    "1000+": "1000+ 间豪华包厢",
    "50.000+": "50,000+ 宾客好评",
    "1000+ Phòng hát đẳng cấp": "1000+ 间豪华包厢",
    "24/24h Đặt bàn giữ chỗ": "24小时预订留房",
    "Âm thanh Martin Audio UK": "英国原装 Martin Audio 音响",
    "Tòa nhà 6 tầng tráng lệ": "6层宏伟欧式独栋大楼",
    "Nội thất hoàng gia dát vàng": "奢华欧式宫廷镀金内饰",
    "Âm thanh BMB chuẩn Nhật": "日本原装 BMB 专业震撼音响",
    "PCCC chuẩn kiểm duyệt 100%": "100% 通过消防安全严格验收",
    "Mặt tiền rộng, bãi ô tô lớn": "宽阔门面与大型专属停车场",
    "Ánh sáng Laser Matrix 3D": "3D Matrix 矩阵激光舞美",
    "Thang máy tốc độ cao": "高速豪华静音观光电梯",
    "Âm thanh chuẩn quốc tế": "国际专业标准震撼音效",
    "Hệ thống PCCC thế hệ mới": "新一代专业标准消防系统",
    "Không gian hoàng gia sang trọng": "奢华欧式皇室艺术空间",

    # 3. Districts
    "Cầu Giấy": "纸桥郡 Cầu Giấy",
    "Đống Đa": "栋多郡 Đống Đa",
    "Hà Đông": "河东郡 Hà Đông",
    "Nam Từ Liêm": "南慈廉郡 Nam Từ Liêm",
    "Hai Bà Trưng": "二征夫人郡 Hai Bà Trưng",
    "Tây Hồ": "西湖郡 Tây Hồ",
    "Quận 1": "第一郡 Quận 1 (胡志明市)",
    "Quận 1 (TP.HCM)": "胡志明市第一郡",
    "Thanh Trì": "青池县 Thanh Trì",
    "Dương Nội": "杨内 Dương Nội",
    "Phú Lương": "富良 Phú Lương",
    "Quan Hoa": "关花 Quan Hoa",
    "📍 Cầu Giấy": "📍 纸桥郡 Cầu Giấy",
    "📍 Đống Đa": "📍 栋多郡 Đống Đa",
    "📍 Hà Đông": "📍 河东郡 Hà Đông",
    "📍 Nam Từ Liêm": "📍 南慈廉郡 Nam Từ Liêm",
    "📍 Hai Bà Trưng": "📍 二征夫人郡 Hai Bà Trưng",
    "📍 Tây Hồ": "📍 西湖郡 Tây Hồ",
    "📍 Quận 1 (TP.HCM)": "📍 第一郡 (胡志明市)",
    "📍 TP. Hồ Chí Minh": "📍 胡志明市",
    "TP. Hồ Chí Minh": "胡志明市",
    "📍 Thanh Trì": "📍 青池县 Thanh Trì",
    "🌟 Tất cả": "🌟 全部",
    "📍 QUẬN CẦU GIẤY": "📍 纸桥郡 CẦU GIẤY",
    "📍 QUẬN ĐỐNG ĐA": "📍 栋多郡 ĐỐNG ĐA",
    "📍 QUẬN HÀ ĐÔNG": "📍 河东郡 HÀ ĐÔNG",
    "📍 QUẬN NAM TỪ LIÊM": "📍 南慈廉郡 NAM TỪ LIÊM",
    "📍 QUẬN HAI BÀ TRƯNG": "📍 二征夫人郡 HAI BÀ TRƯNG",
    "📍 QUẬN TÂY HỒ": "📍 西湖郡 TÂY HỒ",
    "📍 QUẬN 1": "📍 胡志明市第一郡",
    "📍 QUẬN TP. HỒ CHÍ MINH": "📍 胡志明市第一郡",
    "📍 QUẬN THANH TRÌ": "📍 青池县 THANH TRÌ",

    # 4. Hero & Main Page
    "Karaoke Kenz · 202 Trung Kính, Yên Hoà, Cầu Giấy, Hà Nội": "Karaoke Kenz · 河内纸桥郡 Yên Hoà 坊 Trung Kính 街 202 号",
    "202 TRUNG KÍNH": "202 TRUNG KÍNH 旗舰总店",
    "202 Trung Kính": "202 Trung Kính 街",
    "202 Trung Kính, Yên Hoà, Cầu Giấy, Hà Nội": "河内纸桥郡 Trung Kính 街 202 号",
    "Karaoke Kenz 202 Trung Kính – 30 Phòng Hát Siêu VIP Cầu Giấy": "Karaoke Kenz 202 Trung Kính – 纸桥郡30间超级VIP豪华KTV包厢",
    "Hát hết mình,": "尽情欢唱，",
    "quẩy nhiệt tình": "嗨翻全场",
    "Hát hết mình, quẩy nhiệt tình.": "尽情欢唱，嗨翻全场。",
    "30 phòng hát Siêu VIP, âm thanh cực chất, nội thất sang trọng và hiện đại.": "30间超级VIP包厢，顶级震撼音响，豪华现代装修。",
    "Xem không gian": "查看包厢环境",
    "Đặt phòng hát nhanh nhất": "最快预订包厢",
    "Hotline:": "热线：",
    "24/24h": "24小时",
    "30 Phòng Siêu VIP": "30间超级VIP包厢",
    "Dàn loa JBL cực đã": "顶级JBL震撼音响",
    "5.0 Google Rating": "5.0 谷歌好评",
    "120+ Đánh giá 5 sao": "120+ 条五星好评",
    "Giữ Chỗ Trong 30s": "30秒快速留房",
    "Miễn phí không cần cọc": "完全免费 无需押金",
    "Menu VIP & Rượu Ngoại": "VIP酒水与进口名酒",
    "Trang trí sinh nhật theo yêu cầu": "按需免费布置生日派对",
    "ĐANG MỞ CỬA 24/24H": "24小时营业中",
    "Karaoke Kenz Club – điểm hẹn ca hát giữa phố Trung Kính": "Karaoke Kenz Club – Trung Kính 街上的欢唱地标",
    "Nằm tại": "Karaoke Kenz Club 坐落于",
    "202 Trung Kính, phường Yên Hoà, Cầu Giấy": "河内纸桥郡 Yên Hoà 坊 Trung Kính 街 202 号",
    ", Karaoke Kenz Club là điểm hẹn ca hát với": "，是一家配备",
    "hệ thống phòng VIP cách âm": "顶级专业隔音VIP包厢",
    ", phục vụ từ nhóm bạn nhỏ, gia đình đến những buổi tiệc đông người.": "的豪华KTV，接待小型朋友聚会、家庭乃至大型派对。",
    "Mỗi phòng là một không gian riêng: phong cách": "每间包厢都是独立私密空间：",
    "hiện đại": "现代风格",
    "rực rỡ đèn LED, màn hình lớn và âm nhạc sôi động cho các bạn trẻ; hoặc phong cách": "配备绚丽律动LED、大屏幕与动感音乐；或",
    "cổ điển": "古典风格",
    "sang trọng với đèn chùm lấp lánh cho những ai yêu sự thanh lịch.": "，以璀璨的水晶吊灯营造奢华典雅氛围。",
    "Dù là sinh nhật, liên hoan công ty hay một buổi tối thư giãn sau giờ làm, Karaoke Kenz Club luôn sẵn sàng để bạn hát hết mình.": "无论是生日派对、公司团建聚餐，还是下班后的惬意欢唱，Karaoke Kenz Club 随时为您呈现极致体验。",
    "Phòng VIP cách âm": "专业隔音VIP包厢",
    "Phòng gia đình, phòng Party và phòng Siêu VIP – phù hợp từ nhóm nhỏ đến tiệc đông người.": "家庭包厢、派对包厢及超级VIP包厢，适合小型聚会到大型宴会。",
    "Hai phong cách": "两大装修风格",
    "Hiện đại với LED nhiều màu, hoặc cổ điển với đèn chùm sang trọng.": "多彩LED现代律动风，或奢华水晶吊灯古典风。",
    "Đồ uống & đồ ăn nhẹ": "丰富酒水与精致小食",
    "Bia, nước ngọt, đĩa trái cây tươi, khô bò và nhiều món nhắm khác.": "进口啤酒、软饮、新鲜水果拼盘、牛肉干及精美下酒小吃。",
    "Riêng tư, chu đáo": "私密尊贵 贴心周到",
    "Nhân viên biết tiếng Trung": "中文专属客服接待",
    "Đội ngũ nhân viên chăm sóc khách hàng biết tiếng Trung, hỗ trợ khách Trung Quốc đặt phòng qua WeChat và trao đổi trực tiếp tại quán.": "专业中文客服团队，支持微信提前预订，到店全程中文沟通无障碍。",
    "Nhân viên chỉ vào phòng khi bạn cần. Nhận trang trí tiệc sinh nhật theo yêu cầu.": "服务员仅在您呼叫时进入。按需提供生日及派对个性化布置。",
    "Hình ảnh thực tế tại Karaoke Kenz Club 202 Trung Kính.": "Karaoke Kenz Club 202 Trung Kính 真实环境实拍。",
    "Liên hệ đặt phòng để nhận ưu đãi": "联系预订 即享独家礼遇",
    "Đặt phòng trước qua hotline, Zalo hoặc form đặt bàn để được nhận ngay các ưu đãi của quán.": "通过热线、微信/Zalo 或在线表单提前预订，即刻享受本店多重好礼。",
    "Tặng hoa quả": "免费赠送水果拼盘",
    "Đĩa trái cây tươi cho phòng của bạn.": "为您的包厢送上新鲜丰富的水果拼盘。",
    "Tặng bánh sinh nhật": "赠送精美生日蛋糕",
    "Ghi chú khi đặt phòng để quán chuẩn bị.": "预订时备注，门店将悉心为您准备。",
    "Và nhiều ưu đãi hấp dẫn khác": "更多惊喜优惠礼遇",
    "Gọi hotline để được tư vấn chi tiết.": "欢迎拨打热线咨询各项套餐详情。",
    "Xem ảnh khuyến mãi cỡ lớn": "查看优惠海报大图",
    "👑 HỆ THỐNG KARAOKE KTV HÀ NỘI & LIÊN TỈNH": "👑 河内及跨省KTV连锁系统",
    "Chuỗi 36+ phòng hát Karaoke KTV sang trọng, đẳng cấp trải khắp các quận thủ đô Hà Nội và TP. Hồ Chí Minh. Dàn âm thanh công suất lớn, ánh sáng laser sân khấu hiện đại, phục vụ chu đáo 24/7.": "分布于河内各郡及胡志明市的36+高端豪华KTV连锁。大功率震撼音响、动感激光舞台灯效，24/7全天候贴心服务。",
    "Mạng lưới 36+ quán Karaoke KTV đỉnh cao trải khắp thủ đô Hà Nội & Sài Gòn.": "覆盖首都河内及西贡的36+高端豪华KTV连锁网络。",
    "👑 Chuỗi Liên Kết Đẳng Cấp": "👑 尊贵连锁网络",

    # 5. Search & Filters
    "Tìm kiếm theo tên quán hoặc tên đường (VD: Paris Club, Nguyễn Khang, Trần Thái Tông, Tố Hữu...)": "按店名或路名搜索（例如：Paris Club, Nguyễn Khang, Trần Thái Tông, Tố Hữu...）",
    "Không tìm thấy quán nào phù hợp": "未找到相符的KTV分店",
    "Thử tìm với từ khóa khác (ví dụ: Cầu Giấy, Nguyễn Khang, Trần Thái Tông...) hoặc chọn mục \"Tất cả\".": "请尝试其他关键词（例如：Cầu Giấy, Nguyễn Khang, Trần Thái Tông...）或点击“全部”。",
    "Địa chỉ:": "地址：",
    "🔊 Âm thanh cực đã": "🔊 顶级震撼音效",
    "💡 Phòng VIP LED": "💡 炫彩LED包厢",
    "⚡ Phục vụ 24/7": "⚡ 24/7全天候服务",
    "Phục vụ 24/7": "24/7全天候服务",
    "👑 Cơ sở trung tâm": "👑 中心旗舰总店",
    "👑 Cơ sở Kenz VIP": "👑 Kenz VIP总店",
    "Xem chi tiết quán": "查看分店详情",
    "Xem chi tiết": "查看详情",
    "Gọi hotline": "拨打热线",
    "30 Phòng Hát": "30间豪华包厢",
    "Âm thanh đỉnh cao": "顶级巅峰音效",
    "Âm thanh châu Âu": "欧洲顶级高保真音响",
    "Phòng Party lớn": "大型豪华派对房",
    "Phòng VIP LED": "炫彩LED包厢",
    "Phòng hát đẳng cấp": "豪华顶级包厢",
    "Phòng VIP sofa da": "真皮沙发VIP包厢",
    "Phòng bàn tiệc": "宴会桌豪华包厢",
    "Phòng dài · màn LED": "长形LED大屏包厢",
    "Phòng tông đỏ": "奢华红调包厢",
    "Đĩa trái cây": "新鲜水果拼盘",
    "Không gian quán": "店内包厢环境",

    # 6. 4 Golden Commitments / Guarantees
    "💎 ĐẶC QUYỀN KHÁCH HÀNG": "💎 尊贵客户专享特权",
    "4 Cam Kết Vàng Khi Đặt Phòng Qua KTV Hà Nội": "通过河内KTV预订的4大黄金承诺",
    "Chúng tôi liên kết chặt chẽ với ban quản lý từng cơ sở để bảo đảm trải nghiệm tốt nhất.": "我们与各分店管理层直接联动，保障为您提供至臻品质与优先待遇。",
    "Giữ Đúng Phòng VIP Đẹp Nhất": "确保保留最佳VIP包厢",
    "Được xếp phòng theo đúng sở thích (Phòng Party LED, Cổ Điển hoàng gia, hoặc phòng tiệc riêng tư). Không bao giờ lo hết phòng.": "按您的喜好精准安排包厢（律动LED房、欧式古典房或私密宴会房），绝无满房担忧。",
    "Giá Niêm Yết Minh Bạch 100%": "100% 公开透明明码标价",
    "Bảng giá giờ hát và đồ uống công khai, không thu phụ phí bất thường. Xuất hoá đơn VAT đầy đủ cho doanh nghiệp.": "包厢小时费及酒水餐饮全公开，绝不产生隐形费用。可为企业开具正规发票。",
    "Tặng Tiệc Sinh Nhật & Hoa Quả": "免费赠送生日派对布置与果盘",
    "Tặng ngay đĩa hoa quả tươi đầy đặn. Nhận trang trí tiệc sinh nhật, bóng bay nghệ thuật và tặng bánh kem khi đặt trước.": "即刻赠送新鲜丰富的水果大拼盘。提前预订尊享生日气球造型布置及定制生日蛋糕。",
    "Xác Nhận Giữ Chỗ Trong 30s": "30秒极速确认留房",
    "Hệ thống gửi đơn trực tiếp đến quản lý cơ sở. Nhân viên liên hệ xác nhận và hướng dẫn chỗ đỗ ô tô tận tình.": "系统直联各店经理，客服人员迅速致电确认并热情指引专属停车位。",

    # 7. Venue Detail Page Specs
    "Quy mô": "包厢规模",
    "Nhân viên": "服务团队",
    "Bài hát": "点歌曲库",
    "Phòng": "间包厢",
    "Phục vụ": "位员工服务",
    "🎤 Đặt phòng ngay tại cơ sở này": "🎤 立即预订此分店",
    "Gọi: 0342 092 999": "致电：0342 092 999",
    "💬 Nhắn Zalo": "💬 Zalo 在线咨询",
    "Đặc quyền nổi bật tại": "独家特色特权",
    "🔊 Dàn Loa JBL / BMB Cực Khủng": "🔊 顶级 JBL / BMB 震撼音响系统",
    "Công suất lớn, bass chắc nịch, micro cao cấp chống hú rè tuyệt đối.": "大功率输出、低音浑厚强劲，无线麦克风绝不啸叫。",
    "💡 Ánh Sáng Laser 3D Vũ Trường": "💡 3D 激光舞厅舞台灯光",
    "Màn LED cảm ứng theo giai điệu nhạc cực bắt mắt và hiện đại.": "LED大屏幕随音乐节奏律动变幻，炫丽夺目充满现代科技感。",
    "🛡️ Cách Âm Chuẩn Tiêu Chuẩn 100%": "🛡️ 100% 国际专业标准隔音",
    "Tường cách âm chuyên dụng, đảm bảo không gian riêng tư trọn vẹn.": "高规格专业隔音墙体结构，完全保障私密欢聚自由。",
    "🍹 Menu Rượu Ngoại & Tiệc Chu Đáo": "🍹 名品洋酒与精致餐饮服务",
    "Hoa quả tươi, đồ ăn nóng sốt và các loại đồ uống hảo hạng phục vụ tận nơi.": "鲜切水果大拼盘、热气腾腾的特色佳肴及高档进口酒水直供包厢。",
    "📸 Không gian phòng hát thực tế": "📸 真实包厢环境实景",
    "Không gian phòng hát thực tế": "真实包厢环境实景",
    "(Bấm vào ảnh để phóng to toàn màn hình)": "（点击图片可全屏高清放大预览）",
    "💰 Bảng giá phòng tham khảo": "💰 包厢参考价格表",
    "Bảng giá": "价格表",
    "BẢNG GIÁ": "价格表",
    "BẢNG GIÁ PHÒNG KARAOKE CAO CẤP": "高端KTV包厢价格表",
    "BẢNG GIÁ PHÒNG CAO CẤP": "高端KTV包厢价格表",
    "👑 BẢNG GIÁ PHÒNG KARAOKE CAO CẤP": "👑 高端KTV包厢价格表",
    "👑 BẢNG GIÁ PHÒNG CAO CẤP": "👑 高端KTV包厢价格表",
    "👑 DỊCH VỤ ĐẲNG CẤP THƯỢNG LƯU": "👑 尊荣顶级奢华服务",
    "✨ Không gian sang trọng – Dịch vụ đẳng cấp – Trải nghiệm thượng lưu": "✨ 奢华空间 – 尊贵服务 – 顶级体验",
    "✨ Không gian sang trọng – Dịch vụ đẳng cấp – Trải nghiệm thượng lưu tại Karaoke Kenz 202 Trung Kính.": "✨ 奢华空间 – 尊贵服务 – Karaoke Kenz 202 Trung Kính 顶级欢唱体验。",
    "PHÒNG DELUXE": "DELUXE 豪华包厢",
    "💎 PHÒNG DELUXE (5–10 khách)": "💎 DELUXE 豪华包厢 (5–10人)",
    "💎 PHÒNG DELUXE": "💎 DELUXE 豪华包厢",
    "Sức chứa: 5 – 10 khách": "容纳人数：5 – 10位",
    "500.000đ – 540.000đ": "500.000đ – 540.000đ",
    "500.000đ – 540.000đ/giờ": "500.000đ – 540.000đ/小时",
    "500.000đ – 540.000đ / giờ": "500.000đ – 540.000đ/小时",
    "/ giờ hát": "/ 欢唱小时",
    "Không gian riêng tư, hiện đại, phù hợp cho những buổi gặp gỡ và giải trí cùng bạn bè, gia đình.": "私密现代空间，适合朋友、家庭聚会与温馨娱乐。",
    "Không gian riêng tư, hiện đại, phù hợp cho những buổi gặp gỡ và giải trí ấm cúng cùng bạn bè, gia đình.": "私密现代空间，适合朋友、家庭聚会与温馨娱乐。",
    "Dàn âm thanh JBL tiêu chuẩn cao cấp": "JBL 高端标准专业音响系统",
    "Màn hình LED chọn bài cảm ứng thế hệ mới": "新一代触控式高清选歌LED屏",
    "Cách âm chuyên dụng chuẩn phòng thu": "录音棚级专业隔音设计",
    "Đầy đủ menu đồ uống & đĩa trái cây tươi": "酒水齐全与精选新鲜水果拼盘",
    "Đặt Phòng Deluxe": "预订 Deluxe 豪华包厢",
    "👑 ĐƯỢC CHỌN NHIỀU NHẤT": "👑 最受宾客青睐",
    "PHÒNG VIP LUXURY": "VIP LUXURY 尊享包厢",
    "👑 PHÒNG VIP LUXURY (10–20 khách)": "👑 VIP LUXURY 尊享包厢 (10–20人)",
    "👑 PHÒNG VIP LUXURY": "👑 VIP LUXURY 尊享包厢",
    "Sức chứa: 10 – 20 khách": "容纳人数：10 – 20位",
    "620.000đ – 760.000đ": "620.000đ – 760.000đ",
    "620.000đ – 760.000đ/giờ": "620.000đ – 760.000đ/小时",
    "620.000đ – 760.000đ / giờ": "620.000đ – 760.000đ/小时",
    "Không gian rộng rãi, sang trọng, mang đến trải nghiệm giải trí đẳng cấp cho những cuộc vui đáng nhớ.": "宽敞奢华空间，为您带来难忘的高端娱乐体验与欢唱盛宴。",
    "Hệ thống âm thanh biểu diễn BMB / JBL khủng": "BMB / JBL 顶级现场震撼音响",
    "Ánh sáng Laser 3D vũ trường cảm biến theo nhạc": "智能声控3D激光与舞台动感灯效",
    "Sofa hoàng gia bọc da cao cấp cực êm ái": "高端真皮皇家舒适豪华沙发",
    "Ưu tiên chọn phòng view đẹp & nhân viên phục vụ riêng": "优先挑选极佳景观包厢及专属管家服务",
    "🎤 Đặt Phòng VIP Luxury": "🎤 预订 VIP Luxury 包厢",
    "PHÒNG SUPER VIP PARTY": "SUPER VIP 派对包厢",
    "🔥 PHÒNG SUPER VIP PARTY (20–40 khách)": "🔥 SUPER VIP 派对包厢 (20–40人)",
    "🔥 PHÒNG SUPER VIP PARTY": "🔥 SUPER VIP 派对包厢",
    "Sức chứa: 20 – 40 khách": "容纳人数：20 – 40位",
    "850.000đ": "850.000đ",
    "850.000đ/giờ": "850.000đ/小时",
    "850.000đ / giờ": "850.000đ/小时",
    "Từ 500.000đ - 850.000đ / giờ": "从 500.000đ - 850.000đ/小时",
    "Không gian tiệc tùng hoành tráng, lựa chọn lý tưởng cho sinh nhật, liên hoan và các sự kiện đặc biệt.": "盛大派对空间，生日狂欢、公司团建及特别盛宴的绝佳之选。",
    "Không gian tiệc tùng hoành tráng, lựa chọn lý tưởng cho sinh nhật, liên hoan công ty và các sự kiện đặc biệt.": "盛大派对空间，生日狂欢、公司团建及特别盛宴的绝佳之选。",
    "Sức chứa lớn lên tới 40+ khách có sân khấu mini": "40+人超大容量配备独立微型舞台",
    "Tặng gói trang trí bóng bay sinh nhật khi đặt trước": "提前预订免费赠送生日派对气球布置",
    "Hỗ trợ setup màn chiếu & nhạc sống theo yêu cầu": "支持按需提供高清投影与现场乐队配置",
    "TIÊU CHUẨN VIP": "标准VIP",
    "PHÒNG HOT NHẤT": "最热门包厢",
    "ĐẠI TIỆC LIÊN HOAN": "大型欢聚宴会",
    "Bảng So Sánh Quyền Lợi & Dịch Vụ Các Hạng Phòng": "各包厢等级权益与服务对比表",
    "Hạng Phòng": "包厢等级",
    "Sức Chứa": "容纳人数",
    "Hệ Thống Âm Thanh": "音响系统",
    "Đặc Quyền Kèm Theo": "专属特权",
    "Giá Tham Khảo": "参考价格",
    "100% Giá Niêm Yết": "100% 公开标价",
    "Không phụ phí ẩn, xuất hóa đơn VAT": "无隐形消费 可开增值税发票",
    "Bãi Đỗ Xe Tiện Lợi": "便利专属停车场",
    "Ô tô & xe máy bảo vệ trông miễn phí": "汽车摩托车全天候专人免费看管",
    "Hotline 24/7: 0342 092 999": "24小时热线：0342 092 999",
    "💬 Nhắn Zalo Giữ Phòng": "💬 Zalo 极速留房",
    "Dàn âm thanh JBL tiêu chuẩn cao cấp, bass sâu êm": "JBL 高端标准专业音响系统，低音醇厚震撼",
    "Màn hình cảm ứng chọn bài thế hệ mới cực nhạy": "新一代高清电容触控点歌屏，反应灵敏极速",
    "Cách âm chuyên dụng 100% chuẩn phòng thu": "100% 录音棚级专业多层隔音结构",
    "Menu đồ uống, bia nhập khẩu & đĩa trái cây tươi ngon": "进口名酒啤酒齐全，现切丰富新鲜水果拼盘",
    "Phục vụ chu đáo, bấm chuông gọi nhân viên 24/7": "周到贴心服务，包厢配备一键呼叫管家",
    "Hệ thống âm thanh biểu diễn BMB / JBL cực khủng": "BMB / JBL 顶级震撼现场演艺级音响",
    "Sofa hoàng gia bọc da cao cấp cực kỳ êm ái": "欧式皇家豪华真皮沙发，尊贵舒适",
    "Tặng gói trang trí tiệc sinh nhật khi đặt phòng trước": "提前预订免费尊享生日主题气球场景布置",
    "Sức chứa lớn lên tới 40+ khách, có sân khấu mini biểu diễn": "40+人超大容量配备独立微型演艺舞台",
    "Tặng trọn gói trang trí bóng bay sinh nhật & bánh kem": "免费赠送生日主题气球场景布置与精美生日蛋糕",
    "Hỗ trợ setup màn chiếu & nhạc sống, DJ theo yêu cầu": "支持按需提供高清投影、专业现场乐队与DJ",
    "Menu rượu ngoại hảo hạng, bia nhập khẩu & đồ tiệc nóng sốt": "名贵洋酒、进口啤酒及精致热气宴席佳肴",
    "Đội ngũ nhân viên và quản lý hỗ trợ xuyên suốt buổi tiệc": "专业店长与专属服务团队全程尊崇侍应",
    "🎁 ĐẶT PHÒNG SỚM – ƯU TIÊN PHÒNG ĐẸP": "🎁 提前预订 – 优先选好包厢",
    "📌 Giá tham khảo có thể thay đổi theo khung giờ, cuối tuần và dịp lễ.": "📌 参考价格可能根据时段、周末及节假日有所调整。",
    "📌 Giá tham khảo có thể thay đổi theo khung giờ, cuối tuần và dịp lễ. Quý khách vui lòng đặt trước để nhận phòng đẹp nhất.": "📌 参考价格可能根据时段、周末及节假日有所调整。请提前预订以确保留存最佳位置包厢。",
    "📞 Hotline tư vấn & giữ chỗ: 0342 092 999": "📞 咨询与预订热线：0342 092 999",
    "📞 Hotline hỗ trợ & giữ chỗ: 0342 092 999": "📞 支持与预订热线：0342 092 999",
    "📞 Gọi 0342 092 999": "📞 致电 0342 092 999",
    "Phòng Tiêu Chuẩn (5-10 người)": "标准包厢（5-10人）",
    "Phòng VIP (10-20 người)": "豪华VIP包厢（10-20人）",
    "Phòng Super VIP Party (20-40 người)": "超级派对包厢（20-40人）",
    "* Giá có thể thay đổi tùy khung giờ và dịp lễ. Quý khách vui lòng đặt trước để nhận phòng đẹp nhất.": "* 价格可能随时间段及节假日略有浮动。请提前预订以确保留存最佳位置包厢。",
    "⚡ Đặt phòng nhanh 24/7": "⚡ 24/7 极速预订通道",
    "Giữ chỗ miễn phí 100%, nhân viên gọi xác nhận trong 3 phút.": "100% 免费留房，客服将在3分钟内致电与您确认。",
    "Hoặc gọi hotline trực tiếp:": "或直接拨打预订专线：",
    "Các quán Karaoke KTV khác tại": "该区域其他推荐KTV分店",
    "Đẳng cấp phòng hát, nâng tầm trải nghiệm.": "尊贵包厢品质，升华欢唱体验。",

    # 8. FAQs
    "❓ HỎI ĐÁP DỊCH VỤ": "❓ 常见预订问答",
    "Câu Hỏi Thường Gặp Khi Đặt Phòng KTV": "KTV预订常见问题解答",
    "Đặt phòng qua website có mất phí hay phải đặt cọc trước không?": "在网站上预订包厢需要手续费或提前付定金吗？",
    "Đặt phòng có mất phí không?": "预订包厢需要付费吗？",
    "Đặt phòng có mất phí hay phải đặt cọc trước không?": "预订包厢需要付费或付押金吗？",
    "Hoàn toàn": "完全",
    "KHÔNG MẤT PHÍ": "无需付费",
    "KHÔNG CẦN CỌC TRƯỚC": "无需提前付定金",
    "đối với các ngày trong tuần. Quý khách chỉ cần điền họ tên, số điện thoại và giờ dự kiến đến, quán sẽ chủ động giữ phòng và chuẩn bị đón tiếp chu đáo.": "工作日完全免费且无需提前付定金。您只需填写姓名、电话及预计到店时间，门店将主动留房并悉心迎接。",
    ". Quý khách chỉ cần để lại họ tên, số điện thoại và giờ dự kiến đến hát. Quán sẽ chủ động gọi điện hoặc nhắn Zalo xác nhận và giữ phòng VIP đẹp nhất.": "。您只需留下姓名、联系电话与预定时间，我们将致电或发消息确认留房。",
    "Hoàn toàn KHÔNG MẤT PHÍ và KHÔNG CẦN CỌC TRƯỚC đối với các ngày trong tuần. Quý khách chỉ cần điền họ tên, số điện thoại và giờ dự kiến đến, quán sẽ chủ động giữ phòng và chuẩn bị đón tiếp chu đáo.": "工作日完全免费且无需提前付定金。您只需填写姓名、电话及预计到店时间，门店将主动为您保留优质包厢并悉心迎接。",
    "Không. Bạn chỉ cần để lại họ tên, số điện thoại và giờ muốn hát. Quán sẽ gọi hoặc nhắn Zalo để xác nhận.": "不需要。您只需留下姓名、联系电话与预定时间，我们将会致电或通过微信/Zalo与您确认留房。",
    "Giá phòng hát Karaoke KTV tại Hà Nội được tính như thế nào?": "河内KTV包厢价格是如何计算的？",
    "Giá phòng được tính theo giờ hát thực tế: Phòng tiêu chuẩn (5-10 người) từ 250k - 350k/h; Phòng VIP (10-20 người) từ 400k - 650k/h; Phòng Super VIP Party (20-40 người) từ 700k - 1.200k/h. Menu đồ uống bia, rượu ngoại và hoa quả được niêm yết rõ ràng tại menu phòng.": "房费按实际使用小时计算：标准房（5-10人）25万-35万越盾/小时；豪华VIP房（10-20人）40万-65万越盾/小时；超级派对房（20-40人）70万-120万越盾/小时。酒水与果盘均在包厢内明码标价。",
    "Quán có chỗ đỗ ô tô và bảo vệ trông xe không?": "门店有汽车停车位和专职保安看守吗？",
    "100% tất cả 36 cơ sở trong hệ thống đều có chỗ đỗ xe máy và bãi đỗ ô tô rộng rãi, có bảo vệ trông giữ xe an toàn 24/24h miễn phí cho khách hàng.": "全系统36家门店均配备宽敞平整的摩托车及汽车专用停车场，24小时专职保安免费看管护卫。",
    "Quán có khu vực đỗ xe máy và bãi đậu ô tô thuận tiện, có nhân viên bảo vệ điều phối và trông coi xe miễn phí suốt thời gian quý khách sử dụng dịch vụ.": "门店具备便利的摩托车与汽车停车区，欢唱期间由保安人员免费调度看管。",
    "Nếu tôi muốn tổ chức sinh nhật hoặc liên hoan công ty thì có ưu đãi gì?": "如果想举办生日聚会或公司团建，能享受什么专属优惠？",
    "Quán tặng gói trang trí tiệc sinh nhật (bóng chữ, phông nền), tặng đĩa hoa quả tươi và bánh kem sinh nhật cho đoàn đặt trước từ 8 người. Quý khách vui lòng ghi chú \"Tổ chức sinh nhật\" trong phần ghi chú khi gửi đơn đặt.": "提前预订8人以上团队，免费赠送生日主题布置（字母气球、背景板）、鲜果大拼盘及生日蛋糕。提交表单时请在备注中注明“举办生日”。",
    "Có mang bánh kem sinh nhật vào được không?": "可以自带生日蛋糕进包厢吗？",
    "Có được mang bánh kem sinh nhật vào quán không?": "可以自带生日蛋糕进包厢吗？",
    "Được. Ghi chú khi đặt phòng để quán chuẩn bị trang trí.": "完全可以。预订时请备注，我们还可协助准备餐具及生日气氛布置。",
    "Hoàn toàn được. Quý khách chỉ cần ghi chú trong form đặt phòng, quán sẽ chuẩn bị dao đĩa, nến và hỗ trợ trang trí bóng bay sinh nhật chu đáo.": "完全可以。预订时请备注，我们还可协助准备餐具及生日气氛布置。",
    "Huỷ phòng hoặc đổi giờ hát như thế nào?": "如何取消或更改欢唱时间？",
    "Huỷ hoặc đổi giờ thế nào?": "如何取消或更改时间？",
    "Quý khách chỉ cần nhắn tin qua Zalo hoặc gọi hotline": "您只需通过 Zalo 发送信息或致电热线",
    "Quý khách chỉ cần nhắn tin qua Zalo hoặc gọi hotline 0342 092 999 trước giờ hẹn ít nhất 1 tiếng kèm mã đặt phòng (VD: KZ-8291) để quản lý điều chỉnh linh hoạt.": "请于预约时间前至少1小时致电热线 0342 092 999 或发送 Zalo 并提供预订码（如：KZ-8291），以便店长灵活为您调整。",
    "trước giờ hẹn ít nhất 1 tiếng kèm mã đặt phòng (VD: KZ-8291) để quản lý điều chỉnh linh hoạt.": "请在预约时间前至少1小时告知并附上预订编号（如：KZ-8291），以便灵活调整。",
    "Nhắn Zalo hoặc gọi hotline trước giờ hẹn ít nhất 1 tiếng, kèm mã đặt phòng.": "请在预约时间前至少1小时通过 Zalo 或热线告知，并附上预订编号即可。",
    "Quán có phòng cho nhóm đông không?": "有适合多人聚会的超大包厢吗？",
    "Quán có phòng hát cho đoàn tiệc đông người không?": "门店有适合多人聚会的大包厢吗？",
    "Có. Quán có hệ thống phòng gia đình (5-10 người), phòng Party và phòng Siêu VIP cho tiệc đông người. Hãy báo số khách khi đặt, quán sẽ xếp phòng phù hợp.": "有的。我们拥有适合小团队的家庭房、适合中型聚会的Party房以及可容纳40-50人的超级VIP宴会房。预订时请说明人数即可。",
    "Có. Quán có hệ thống phòng gia đình (5-10 người), phòng Party (15-25 người) và phòng Super VIP (30-50 người) cực kỳ rộng rãi, thoải mái cho các buổi liên hoan công ty và sinh nhật.": "有的。我们拥有适合小团队的家庭包厢（5-10人）、派对包厢（15-25人）及可容纳30-50人的超级VIP宴会包厢，宽敞舒适。",
    "Có. Quán có hệ thống phòng tiệc lớn sức chứa từ 20 đến 45 khách, nhận set up tiệc sinh nhật, liên hoan công ty trọn gói với loa kéo bổ trợ, ánh sáng sân khấu và màn chiếu theo yêu cầu.": "有的。门店配备可容纳20至45位宾客的大型宴会包厢，全包式承办生日聚会及公司团建，并按需提供辅助音响、舞台灯光与投影设备。",

    # 9. Booking Modal & States
    "Hệ Thống Karaoke KTV Hà Nội": "河内豪华KTV连锁系统",
    "Thông tin đặt chỗ": "填写预订信息",
    "Cơ sở đặt": "预订分店",
    "Cơ sở": "分店",
    "Cơ sở / Quán đã chọn:": "已选分店：",
    "Không cần thanh toán. Nhân viên sẽ gọi hoặc nhắn Zalo để xác nhận và xếp phòng cho bạn.": "无需提前付款。客服将致电或发消息确认并为您预留包厢。",
    "Họ và tên": "姓名",
    "Họ và tên *": "姓名 *",
    "Họ tên": "姓名",
    "Số điện thoại": "电话号码",
    "Số điện thoại *": "电话号码 *",
    "Điện thoại": "电话号码",
    "Ngày đặt": "预订日期",
    "Ngày đặt *": "预订日期 *",
    "Giờ đến": "预计到店时间",
    "Giờ đến *": "预计到店时间 *",
    "Thời gian": "预订时间",
    "Ghi chú thêm (nếu có)": "特殊要求备注（选填）",
    "Ghi chú": "备注",
    "Nhập tên của bạn...": "请输入您的称呼 / 姓名...",
    "Nhập số điện thoại...": "请输入您的手机号码...",
    "VD: 19:30": "例如：19:30",
    "Yêu cầu trang trí tiệc, số lượng người, phòng VIP…": "派对布置需求、预计人数、包厢风格偏好等…",
    "Gửi yêu cầu đặt bàn": "提交预订申请",
    "Đang gửi…": "正在提交…",
    "Đã gửi yêu cầu đặt bàn": "预订申请已成功提交",
    "Chụp lại mã này. Nhân viên sẽ liên hệ xác nhận trong ít phút.": "请截图保存此预订码。客服经理将在数分钟内与您联系确认。",
    "Nhắn Zalo xác nhận giữ phòng ngay": "立即通过 Zalo 发送预订码确认留房",
    "Bấm để tự động mở Zalo và gửi mã đặt phòng cho quản lý": "点击将自动打开 Zalo 并向店长发送预订凭证",
    "Đặt thêm": "再订一间",
    "Xong": "完成关闭",
    "Nhập họ tên để nhân viên gọi xác nhận.": "请输入姓名以便客服致电确认。",
    "Số điện thoại chưa đúng, ví dụ 0912345678.": "手机号码格式不正确，例如 0912345678。",
    "Chọn ngày đặt.": "请选择预订日期。",
    "Ngày đặt đã qua, chọn lại ngày khác.": "所选日期已过，请重新选择日期。",
    "Nhập giờ đến, ví dụ 19:30.": "请输入预计到店时间，例如 19:30。",
    "Giờ này đã qua, vui lòng chọn giờ hoặc ngày khác.": "该时间段已过，请选择其他时间或日期。",
    "Đã sao chép nội dung đặt phòng, đang chuyển đến Zalo...": "已复制预订凭证信息，正在前往 Zalo...",

    # 10. Contact Info & Sidebars
    "Thông tin": "门店详情",
    "Địa chỉ & liên hệ": "地址与联系方式",
    "Địa chỉ": "详细地址",
    "Hotline": "预订热线",
    "Wi-Fi miễn phí": "全店高速免费 Wi-Fi",
    "Chỗ đỗ ô tô & xe máy": "宽敞汽车与摩托车停车场",
    "Trang trí sinh nhật": "专业派对生日布置",
    "Xuất hoá đơn VAT": "可开具增值税正规发票",
    "Chỉ đường trên Google Maps": "在 Google 地图中查看导航",
    "Nhắn Zalo cho quán": "向门店发送 Zalo 咨询",
    "Hỏi phòng trống, đặt tiệc, đổi giờ.": "咨询空房、预订派对、更改时间。",
    "Mở Zalo": "打开 Zalo",
    "Sao chép số": "复制号码",
    "Sao chép ID": "复制 ID",
    "Quét mã QR bằng WeChat để kết bạn với quán.": "请使用微信扫描二维码添加本店为好友。",
    "Mã QR WeChat – Karaoke Kenz Club": "Karaoke Kenz Club 微信二维码",
    "Mã QR WeChat của quán": "本店微信二维码",
    "Khách nói gì về quán": "宾客心声与评价",
    "Đánh giá 5 sao từ khách trên Google Maps.": "来自 Google Maps 真实宾客的 5 星好评认证。",
    "Sinh Nhật hát ở đây rất oki giá hợp lý nv chu đáo không thái độ làm việc chuyên nghiệp": "在这里过生日体验非常棒，价格公道，员工贴心周到，态度极为专业！",
    "Đồ ăn 5 · Dịch vụ 5 · Bầu không khí 5": "餐食 5分 · 服务 5分 · 氛围 5分",
    "quán sạch sẽ nv phục vụ tốt chuyên nghiệp": "店面干净整洁，服务人员非常专业热情！",
    "Phản hồi của quán:": "店长回函：",
    "Cảm ơn quý khách đã đánh giá 5 sao kenz Club": "衷心感谢贵客为 Kenz Club 留下的五星殊荣与好评！",
    "Trải nghiệm rất tốt giá hợp lý": "欢唱体验极佳，性价比非常高！",
    "Nhân viên xinh": "服务员漂亮大方热情！",
    "2 tuần trước": "2周前",
    "1 tuần trước": "1周前",
    "3 tuần trước": "3周前",

    # 11. Image Alts & Details
    "Mặt tiền Karaoke Kenz Club, 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 门店外观实景",
    "Phòng VIP sofa da – Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 欧式真皮沙发VIP包厢",
    "Phòng dài · màn LED – Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 长形LED大屏包厢",
    "Phòng bàn tiệc – Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 宴会桌豪华包厢",
    "Phòng tông đỏ – Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 奢华红调包厢",
    "Đĩa trái cây – Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 新鲜丰富水果拼盘",
    "Chương trình khuyến mãi Karaoke Kenz Club: tặng hoa quả, tặng bánh sinh nhật": "Karaoke Kenz Club 独家优惠：免费赠送果盘与精美生日蛋糕",
    "Mã QR WeChat của quán để được hỗ trợ nhanh nhất": "扫描微信二维码获取专属客服极速协助",
    "Phòng VIP Karaoke Kenz 202 Trung Kính tiếp khách trang trọng": "Karaoke Kenz 202 Trung Kính 商务接待尊荣VIP包厢",
    "Không gian phòng VIP sofa da sang trọng, cách âm tuyệt đối tại 202 Trung Kính": "202 Trung Kính 奢华真皮沙发VIP包厢，顶级专业隔音",
    "Mã QR WeChat Karaoke Kenz Club": "Karaoke Kenz Club 微信二维码",
    "Liên hệ WeChat": "联系微信客服",
    "Liên hệ Zalo": "联系Zalo客服",
    "Hotline đặt phòng": "预订专线热线",
    "Yêu cầu đặc biệt về trang trí, bánh kem, số người…": "特殊需求备注：派对布置、生日蛋糕、预订人数等…",

    # 12. News & Tips Articles
    "Góc chia sẻ Karaoke Kenz": "Karaoke Kenz 经验与攻略专栏",
    "Tin tức & kinh nghiệm": "新闻与攻略",
    "Ưu đãi mới, kinh nghiệm tổ chức sinh nhật, liên hoan và những điều nên biết khi đi hát karaoke ở Cầu Giấy.": "最新优惠、生日派对举办指南、团建聚餐及纸桥郡KTV欢唱必知技巧。",
    "Karaoke cho khách Trung Quốc ở Hà Nội: đặt phòng qua WeChat tại Karaoke Kenz": "河内专接中国客户的豪华KTV：在Karaoke Kenz使用微信便捷预订",
    "Đi hát cùng đối tác, bạn bè người Trung Quốc? Karaoke Kenz có nhân viên chăm sóc khách hàng biết tiếng Trung, hỗ trợ đặt phòng qua WeChat.": "与中国商务伙伴或好友欢唱？Karaoke Kenz配备中文专属客服，全程支持微信预订与中文沟通。",
    "Xem thêm →": "查看更多 →",
    "Top bài hát karaoke sôi động 2026: danh sách “quẩy” cực cháy cùng hội bạn": "2026年度火爆KTV金曲盘点：与好友一起嗨翻全场的必备歌单",
    "Nhạc trẻ mới, bài “quốc dân”, remix và song ca nam nữ – playlist giúp cả phòng cùng hát, cùng nhảy tại Karaoke Kenz 202 Trung Kính.": "新潮流行乐、全民传唱金曲、劲爆Remix与男女对唱——让全场气氛沸腾的精选歌单。",
    "Bí quyết hát karaoke hay: 8 mẹo giữ giọng, hát “cháy” hết mình": "KTV麦霸进阶秘籍：8个科学护嗓与激情欢唱的实用技巧",
    "Không cần học thanh nhạc: chọn đúng tông, cầm micro đúng cách và vài mẹo giữ giọng là đủ để tự tin cầm mic tại Karaoke Kenz.": "无需专业声乐基础：选对降升调、掌握握麦姿势与护嗓小诀窍，即可在Kenz自信开嗓。",
    "Tổ chức sinh nhật ở karaoke Cầu Giấy: kinh nghiệm và ưu đãi tặng bánh": "在纸桥郡举办KTV生日派对：全攻略及免费赠送生日蛋糕特权",
    "Chọn phòng theo số người, chuẩn bị bánh kem, trang trí… và cách nhận bánh sinh nhật miễn phí khi đặt phòng tại Karaoke Kenz.": "按人数挑选包厢、准备蛋糕布置… 以及提前在Karaoke Kenz预订获取免费生日蛋糕的秘诀。",
    "← Quay lại Trang Chủ": "← 返回首页",
    "Kinh nghiệm": "攻略心得",
    "Dịch vụ & Tiếp khách quốc tế": "涉外接待与高端服务",
    "Karaoke Cho Khách Trung Quốc ở Hà Nội: Đặt Phòng Qua WeChat Tại Karaoke Kenz": "河内专接中国客户的豪华KTV：在Karaoke Kenz使用微信便捷预订",
    "Bởi Ban Quản Trị Kenz Club": "由 Kenz Club 管理团队发布",
    "Đặt Phòng Hát Nhận Ưu Đãi Ngay Hôm Nay": "即刻预订包厢 尊享今日专属礼遇",
    "Tặng ngay đĩa hoa quả tươi ngon và ưu đãi giảm giá theo đoàn khi liên hệ đặt bàn trước qua Hotline hoặc Zalo.": "通过热线、微信或Zalo提前预订，即赠新鲜丰富果盘及团队专属满减折扣。",
    "Khách Trung Quốc": "中国宾客专栏",

    # 13. Admin Test Panel
    "Quản Lý Đơn Đặt Bàn (Win Test) – Karaoke Kenz": "预订管理后台 (Windows 测试) – Karaoke Kenz",
    "Dành Cho Kiểm Thử Cục Bộ Trên Windows": "用于 Windows 本地测试与管理",
    "Danh Sách Đơn Đặt Bàn": "客户预订工单列表",
    "← Về Trang Chủ": "← 返回首页",
    "+ Thêm Đơn Mẫu": "+ 添加测试订单",
    "Xuất File CSV": "导出 CSV 表格",
    "Xóa Hết Đơn": "清空所有订单",
    "Tổng đơn đặt": "总订单数",
    "Đơn mới cần gọi": "待致电新订单",
    "Đã xác nhận phòng": "已确认留房",
    "🔔 Tính Năng Thông Báo Tức Thì": "🔔 即时订单推送通知",
    "Thử Nghiệm Gửi Thông Báo Về Telegram Điện Thoại": "测试推送预订通知至手机 Telegram",
    "📖 Xem hướng dẫn lấy Token": "📖 查看 Token 获取教程",
    "3 bước cực kỳ đơn giản để điện thoại của bạn nhận tin nhắn mỗi khi có khách đặt bàn:": "仅需3个简单步骤，即可在有新订单时让手机接收实时提醒：",
    "Mở app Telegram trên điện thoại, tìm bot": "打开手机上的 Telegram 应用，搜索机器用户",
    "gửi tin": "发送指令",
    "và làm theo hướng dẫn để lấy": "并按提示获取",
    "Bot Token": "机器人 Token",
    "Tìm bot": "搜索机器用户",
    "gửi bất kỳ chữ gì để xem": "发送任意消息以查看",
    "Id (Chat ID)": "您的聊天 ID (Chat ID)",
    "của bạn.": "您的专属ID。",
    "Dán Bot Token và Chat ID vào 2 ô bên dưới, bấm": "将 Bot Token 与 Chat ID 填入下方输入框，点击",
    "\"Thử gửi tin nhắn\"": "“测试发送消息”",
    "để kiểm tra!": "以验证连接！",
    "Bot Token Telegram:": "Telegram 机器人 Token：",
    "Ví dụ: 789123456:AAFlB...": "例如：789123456:AAFlB...",
    "Chat ID Của Bạn:": "您的 Chat ID：",
    "Ví dụ: 123456789": "例如：123456789",
    "🚀 Thử Gửi Tin Nhắn": "🚀 测试发送通知",
    "💬 Tự Động Nhắn Zalo Bằng Nick Phụ": "💬 通过副号自动发送 Zalo 消息",
    "Dịch Vụ Zalo Bot Tự Động Gửi Đơn Sang Zalo Của Bạn": "Zalo Bot 自动转发新订单至您的 Zalo",
    "🔍 Kiểm Tra Kết Nối Cổng 5000": "🔍 检查 5000 端口服务状态",
    "Chạy file": "运行脚本",
    "trên máy tính để khởi động dịch vụ tự động nhắn tin. Xem tài liệu tại": "以启动自动发送服务。查看详细说明：",
    "Tất Cả Đơn": "全部订单",
    "Đơn Mới Cần Gọi": "待致电订单",
    "Đã Xác Nhận": "已确认订单",
    "Mã Đơn": "订单编号",
    "Cơ Sở / Quán": "预订分店",
    "Họ Tên": "客户姓名",
    "Số Điện Thoại": "联系电话",
    "Ngày & Giờ Đến": "预订到店时间",
    "Ghi Chú": "特殊备注",
    "Thời Gian Đặt": "提交时间",
    "Trạng Thái": "处理状态",
    "Thao Tác": "操作",
    "Chưa có đơn đặt phòng nào. Hãy thử đặt phòng tại trang chủ!": "暂无预订订单。请在首页尝试提交预订！"
}

# 36 Venues Full Chinese Mapping with Hanzi annotations
VENUE_NAME_ZH = {
    "Karaoke Paris Club 69 Trần Thái Tông": "Karaoke Paris Club 69 Trần Thái Tông (巴黎顶级俱乐部)",
    "Paris Club 69 Trần Thái Tông": "Paris Club 69 Trần Thái Tông (巴黎顶级俱乐部)",
    "Karaoke Royal 31-33 Nguyễn Khang": "Karaoke Royal 31-33 Nguyễn Khang (皇家贵族KTV)",
    "Royal 31-33 Nguyễn Khang": "Royal 31-33 Nguyễn Khang (皇家贵族KTV)",
    "Karaoke Raptor - 116 Bùi Thị Xuân": "Karaoke Raptor - 116 Bùi Thị Xuân (猛禽豪华KTV)",
    "Raptor 116 Bùi Thị Xuân": "Raptor 116 Bùi Thị Xuân (猛禽豪华KTV)",
    "Karaoke T KTV – Dương Nội": "Karaoke T KTV – Dương Nội (T 豪华KTV)",
    "New The Wann Quận 1": "New The Wann 第一郡 (The Wann 潮流俱乐部)",
    "New The Wann Quận 1 (TP.HCM)": "New The Wann 第一郡 (The Wann 潮流俱乐部)",
    "Karaoke London – Phú Lương": "Karaoke London – Phú Lương (伦敦英伦KTV)",
    "Karaoke Lucky – 10 Hoà Mã": "Karaoke Lucky – 10 Hoà Mã (幸运星级KTV)",
    "Lucky 10 Hoà Mã": "Lucky 10 Hoà Mã (幸运星级KTV)",
    "Karaoke MC QEEN – 29 La Thành": "Karaoke MC QEEN – 29 La Thành (女王尊享KTV)",
    "Karaoke Titan 244 Võ Chí Công": "Karaoke Titan 244 Võ Chí Công (泰坦顶级KTV)",
    "Titan 244 Võ Chí Công": "Titan 244 Võ Chí Công (泰坦顶级KTV)",
    "Karaoke The Voice Quan Hoa": "Karaoke The Voice Quan Hoa (好声音流行KTV)",
    "The Voice Quan Hoa": "The Voice Quan Hoa (好声音流行KTV)",
    "Karaoke Kenz Club 202 Trung Kính": "Karaoke Kenz Club 202 Trung Kính 旗舰店",
    "Karaoke Tip Top 85G Nguyễn Khang": "Karaoke Tip Top 85G Nguyễn Khang (顶尖品质KTV)",
    "Tip Top 85G Nguyễn Khang": "Tip Top 85G Nguyễn Khang (顶尖品质KTV)",
    "Karaoke 85 Hoàng Gia - Cầu Giấy": "Karaoke 85 Hoàng Gia - Cầu Giấy (85皇家豪华KTV)",
    "85 Hoàng Gia Cầu Giấy": "85 Hoàng Gia Cầu Giấy (85皇家豪华KTV)",
    "Karaoke F5 Plus - 5 Trần Duy Hưng": "Karaoke F5 Plus - 5 Trần Duy Hưng (F5 Plus 豪华KTV)",
    "F5 Plus 5 Trần Duy Hưng": "F5 Plus 5 Trần Duy Hưng (F5 Plus 豪华KTV)",
    "Karaoke V-POP 50 Trung Hòa": "Karaoke V-POP 50 Trung Hòa (V-POP 流行KTV)",
    "V-POP 50 Trung Hòa": "V-POP 50 Trung Hòa (V-POP 流行KTV)",
    "Karaoke Level 36 Vũ Trọng Khánh": "Karaoke Level 36 Vũ Trọng Khánh (Level 36 豪华KTV)",
    "Level 36 Vũ Trọng Khánh": "Level 36 Vũ Trọng Khánh (Level 36 豪华KTV)",
    "Karaoke Let's Sing 89 Tân Triều": "Karaoke Let's Sing 89 Tân Triều (畅享欢乐KTV)",
    "Karaoke F5 Plus - 66 Tố Hữu": "Karaoke F5 Plus - 66 Tố Hữu (F5 Plus 豪华KTV)",
    "F5 Plus 66 Tố Hữu": "F5 Plus 66 Tố Hữu (F5 Plus 豪华KTV)",
    "Karaoke X-MEN Club 402 Đê La Thành": "Karaoke X-MEN Club 402 Đê La Thành (X战警动感俱乐部)",
    "X-MEN Club 402 Đê La Thành": "X-MEN Club 402 Đê La Thành (X战警动感俱乐部)",
    "Karaoke LONDON 20 Lê Trọng Tấn": "Karaoke LONDON 20 Lê Trọng Tấn (伦敦英伦KTV)",
    "LONDON 20 Lê Trọng Tấn": "LONDON 20 Lê Trọng Tấn (伦敦英伦KTV)",
    "Karaoke SING KTV 66 Tố Hữu": "Karaoke SING KTV 66 Tố Hữu (SING 唱享KTV)",
    "SING KTV 66 Tố Hữu": "SING KTV 66 Tố Hữu (SING 唱享KTV)",
    "Karaoke AMIGO 233 Lê Đức Thọ": "Karaoke AMIGO 233 Lê Đức Thọ (阿米戈尊贵KTV)",
    "AMIGO 233 Lê Đức Thọ": "AMIGO 233 Lê Đức Thọ (阿米戈尊贵KTV)",
    "Karaoke GRAND 300 Xã Đàn": "Karaoke GRAND 300 Xã Đàn (盛大皇室KTV)",
    "GRAND 300 Xã Đàn": "GRAND 300 Xã Đàn (盛大皇室KTV)",
    "Karaoke S 69 Trần Thái Tông": "Karaoke S 69 Trần Thái Tông (S 时尚俱乐部)",
    "Karaoke V-Party 5 Hồ Đắc Di": "Karaoke V-Party 5 Hồ Đắc Di (V-Party 派对KTV)",
    "V-Party 5 Hồ Đắc Di": "V-Party 5 Hồ Đắc Di (V-Party 派对KTV)",
    "Karaoke Royal Club 97 Cầu Giấy": "Karaoke Royal Club 97 Cầu Giấy (皇家旗舰俱乐部)",
    "Karaoke Thượng Hải KTV 229 Tây Sơn": "Karaoke Thượng Hải KTV 229 Tây Sơn (上海风情KTV)",
    "Karaoke Sing KTV 65 Thái Thịnh": "Karaoke Sing KTV 65 Thái Thịnh (Sing 唱享KTV)",
    "Sing KTV 65 Thái Thịnh": "Sing KTV 65 Thái Thịnh (Sing 唱享KTV)",
    "Karaoke LONDON 28 Thành Thái": "Karaoke LONDON 28 Thành Thái (伦敦英伦KTV)",
    "Karaoke A999 - 51 Nguyễn Hoàng": "Karaoke A999 - 51 Nguyễn Hoàng (A999 豪华KTV)",
    "A999 51 Nguyễn Hoàng": "A999 51 Nguyễn Hoàng (A999 豪华KTV)",
    "Karaoke V-MAX - 402 Đê La Thành": "Karaoke V-MAX - 402 Đê La Thành (V-MAX 巅峰KTV)",
    "A9 Club - 37 Nguyễn Hoàng": "A9 Club - 37 Nguyễn Hoàng (A9 顶级俱乐部)",
    "A PLUS CLUB 78 Yên Phụ": "A PLUS CLUB 78 Yên Phụ (A+ 顶级俱乐部)",
    "CLUB 78 Yên Phụ": "CLUB 78 Yên Phụ (A+ 顶级俱乐部)",
    "VOLUME CLUB - KDT HATECO APOLLO Xuân Phương": "VOLUME CLUB - KDT HATECO APOLLO Xuân Phương (VOLUME 动感俱乐部)",
    "VOLUME CLUB Hateco Apollo": "VOLUME CLUB Hateco Apollo (VOLUME 动感俱乐部)",
    "Karaoke Matrix 124 126 Đường 9A": "Karaoke Matrix 124 126 Đường 9A (黑客帝国KTV)",
    "Bar Empire Club Quận 1": "Bar Empire Club 第一郡 (帝国顶级俱乐部)",
    "Karaoke Summit 64 Trần Thái Tông": "Karaoke Summit 64 Trần Thái Tông (巅峰皇家KTV)",
    "Summit 64 Trần Thái Tông": "Summit 64 Trần Thái Tông (巅峰皇家KTV)",
    "Karaoke Zozo 12 Trần Kim Xuyến": "Karaoke Zozo 12 Trần Kim Xuyến (佐佐时尚KTV)",
    "Zozo 12 Trần Kim Xuyến": "Zozo 12 Trần Kim Xuyến (佐佐时尚KTV)",
    "Karaoke Flamenco KTV 16-18 Vũ Phạm Hàm": "Karaoke Flamenco KTV 16-18 Vũ Phạm Hàm (弗拉门戈豪华KTV)",
    "Flamenco 16-18 Vũ Phạm Hàm": "Flamenco 16-18 Vũ Phạm Hàm (弗拉门戈豪华KTV)"
}

# Street Address Chinese Annotations
STREET_ZH = {
    "69 Trần Thái Tông": "69 Trần Thái Tông (陈太宗街69号)",
    "33 Nguyễn Khang": "33 Nguyễn Khang (阮康街33号)",
    "31-33 Nguyễn Khang": "31-33 Nguyễn Khang (阮康街31-33号)",
    "116 Bùi Thị Xuân": "116 Bùi Thị Xuân (裴氏春街116号)",
    "300 Xã Đàn": "300 Xã Đàn (社坛街300号)",
    "29 La Thành": "29 La Thành (罗城街29号)",
    "402 Đê La Thành": "402 Đê La Thành (罗城堤402号)",
    "36 Vũ Trọng Khánh": "36 Vũ Trọng Khánh (武重庆街36号)",
    "37 Nguyễn Hoàng": "37 Nguyễn Hoàng (阮黄街37号)",
    "51 Nguyễn Hoàng": "51 Nguyễn Hoàng (阮黄街51号)",
    "233 Lê Đức Thọ": "233 Lê Đức Thọ (黎德寿街233号)",
    "66 Tố Hữu": "66 Tố Hữu (素友街66号)",
    "20 Lê Trọng Tấn": "20 Lê Trọng Tấn (黎重晋街20号)",
    "28 Thành Thái": "28 Thành Thái (成泰街28号)",
    "5 Trần Duy Hưng": "5 Trần Duy Hưng (陈维兴街5号)",
    "10 Hoà Mã": "10 Hoà Mã (和马街10号)",
    "244 Võ Chí Công": "244 Võ Chí Công (武志公街244号)",
    "85G Nguyễn Khang": "85G Nguyễn Khang (阮康街85G号)",
    "89 Tân Triều": "89 Tân Triều (新朝街89号)",
    "97 Cầu Giấy": "97 Cầu Giấy (纸桥街97号)",
    "229 Tây Sơn": "229 Tây Sơn (西山街229号)",
    "124 126 Đường 9A": "124-126 Đường 9A (9A路124-126号)",
    "KDT HATECO APOLLO Xuân Phương": "KDT HATECO APOLLO Xuân Phương (春芳Hateco新区)",
    "Party 5 Hồ Đắc Di": "Party 5 Hồ Đắc Di (胡得怡街5号)",
    "POP 50 Trung Hòa": "POP 50 Trung Hòa (中和街50号)",
    "MAX - 402 Đê La Thành": "MAX - 402 Đê La Thành (罗城堤402号)",
    "KTV 66 Tố Hữu": "KTV 66 Tố Hữu (素友街66号)",
    "KTV 65 Thái Thịnh": "KTV 65 Thái Thịnh (泰盛街65号)",
    "MEN Club 402 Đê La Thành": "MEN Club 402 Đê La Thành (罗城堤402号)",
    "69 Trần Thái Tông, Cầu Giấy, Hà Nội": "河内纸桥郡陈太宗街69号 (69 Trần Thái Tông, Cầu Giấy)",
    "31-33 Nguyễn Khang, Trung Hòa, Cầu Giấy": "河内纸桥郡中和坊阮康街31-33号 (31-33 Nguyễn Khang, Trung Hòa)",
    "64 Trần Thái Tông": "64 Trần Thái Tông (陈太宗街64号)",
    "64 Trần Thái Tông, Dịch Vọng Hậu, Cầu Giấy, Hà Nội": "河内纸桥郡陈太宗街64号 (64 Trần Thái Tông)",
    "12 Trần Kim Xuyến": "12 Trần Kim Xuyến (陈金川街12号)",
    "12 Trần Kim Xuyến, Yên Hoà, Cầu Giấy, Hà Nội": "河内纸桥郡陈金川街12号 (12 Trần Kim Xuyến)",
    "16-18 Vũ Phạm Hàm": "16-18 Vũ Phạm Hàm (武范涵街16-18号)",
    "16 18 Vũ Phạm Hàm": "16 18 Vũ Phạm Hàm (武范涵街16-18号)",
    "16 - 18 Vũ Phạm Hàm, Trung Hòa, Cầu Giấy, Hà Nội": "河内纸桥郡武范涵街16-18号 (16-18 Vũ Phạm Hàm)"
}

for k, v in VENUE_NAME_ZH.items():
    ZH_MAP[k] = v

for k, v in STREET_ZH.items():
    ZH_MAP[k] = v

js_code = f"""/**
 * =========================================================================
 * BỘ XỬ LÝ CHUYỂN ĐỔI SONG NGỮ (VIỆT - TRUNG) TOÀN DIỆN 1000% - KARAOKE KENZ WEB
 * =========================================================================
 * - Dịch 1000% toàn bộ nội dung DOM: Menu, Hero, 36 quán KTV, Guarantees, FAQ.
 * - Lưu lựa chọn ngôn ngữ vào localStorage ("karaoke_lang").
 * - Hỗ trợ font Noto Sans SC mượt mà chuẩn văn phong tiếng Trung bản ngữ.
 * =========================================================================
 */

(function () {{
  const ZH_DICTIONARY = {json.dumps(ZH_MAP, ensure_ascii=False, indent=2)};

  const ZH_WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
  const VI_WEEKDAYS = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];

  let currentLang = "vi";
  const originalTextMap = new WeakMap();

  function loadZhFont() {{
    if (document.getElementById("zh-font-link")) return;
    const link = document.createElement("link");
    link.id = "zh-font-link";
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;800&display=swap";
    document.head.appendChild(link);
  }}

  function translate(str) {{
    if (!str) return "";
    const clean = str.trim().replace(/\\s+/g, " ");
    if (currentLang === "zh") {{
      return smartTranslateZh(clean);
    }}
    return str;
  }}

  // Thuật toán dịch thông minh cho chuỗi động hoặc có tiền tố/hậu tố
  function smartTranslateZh(text) {{
    if (!text) return "";
    const trimmed = text.trim();
    const cleanKey = trimmed.replace(/\\s+/g, " ");

    // 1. Khớp từ điển chính xác
    if (ZH_DICTIONARY[cleanKey]) {{
      return ZH_DICTIONARY[cleanKey];
    }}

    let result = cleanKey;

    // 2. Mẫu tiền tố động
    if (result.startsWith("Giới thiệu về ")) {{
      return "关于 " + result.substring("Giới thiệu về ".length);
    }}
    if (result.startsWith("Đặc quyền nổi bật tại ")) {{
      return result.substring("Đặc quyền nổi bật tại ".length) + " 独家特色特权";
    }}
    if (result.startsWith("Những câu hỏi thường gặp về ")) {{
      return "关于 " + result.substring("Những câu hỏi thường gặp về ".length) + " 的常见问题";
    }}
    if (result.startsWith("Cơ sở ") && result.includes("có hỗ trợ đoàn đông người và tổ chức tiệc không?")) {{
      const venue = result.replace("Cơ sở ", "").replace(" có hỗ trợ đoàn đông người và tổ chức tiệc không?", "");
      return venue + " 支持大型聚会与派对吗？";
    }}
    if (result.startsWith("Chỗ đỗ ô tô tại ") && result.endsWith("như thế nào?")) {{
      const venue = result.replace("Chỗ đỗ ô tô tại ", "").replace(" như thế nào?", "");
      return venue + " 的停车位情况如何？";
    }}
    if (result.startsWith("🎤 Đặt phòng tại ")) {{
      return "🎤 预订 " + result.substring("🎤 Đặt phòng tại ".length) + " 包厢";
    }}
    if (result.startsWith("🎤 Đặt phòng ngay tại ")) {{
      return "🎤 立即预订 " + result.substring("🎤 Đặt phòng ngay tại ".length) + " 包厢";
    }}
    if (result.startsWith("Các quán Karaoke KTV khác tại ")) {{
      const district = result.substring("Các quán Karaoke KTV khác tại ".length);
      return district + " 的其他KTV推荐分店";
    }}
    if (result.startsWith("Gọi: ")) {{
      return "致电：" + result.substring(5);
    }}
    if (result.startsWith("Gọi hotline ")) {{
      return "拨打预订专线 " + result.substring("Gọi hotline ".length);
    }}
    if (result.startsWith("Xem chi tiết ")) {{
      return "查看 " + result.substring("Xem chi tiết ".length) + " 分店详情";
    }}

    // 3. Quy mô / nhân viên / bài hát / giá tiền
    if (/^\\d+\\+\\s*Phòng$/.test(result)) {{
      return result.replace("Phòng", "间包厢");
    }}
    if (/^\\d+\\+\\s*Phục vụ$/.test(result)) {{
      return result.replace("Phục vụ", "位员工服务");
    }}
    if (/^\\d+\\s*quán$/.test(result)) {{
      return result.replace("quán", "家分店");
    }}
    if (/^\\d+\\s*tuần trước$/.test(result)) {{
      return result.replace("tuần trước", "周前");
    }}
    if (result.endsWith("/ giờ") || result.endsWith("/h")) {{
      return result.replace("/ giờ", "越盾/小时").replace("/h", "越盾/小时");
    }}

    // 4. Mẫu tiêu đề trang chi tiết
    if (result.endsWith(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP Hà Nội")) {{
      const prefix = result.replace(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP Hà Nội", "");
      return prefix + " – 包厢价格、环境实拍与极速预订";
    }}
    if (result.endsWith(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP")) {{
      const prefix = result.replace(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP", "");
      return prefix + " – 包厢价格、环境实拍与极速预订";
    }}
    if (result.endsWith(" – Đặt Phòng VIP Hà Nội")) {{
      const prefix = result.replace(" – Đặt Phòng VIP Hà Nội", "");
      return prefix + " – 顶级VIP包厢极速预订";
    }}
    if (result.endsWith(" – Phòng Hát Karaoke VIP Đẹp")) {{
      const prefix = result.replace(" – Phòng Hát Karaoke VIP Đẹp", "");
      return prefix + " – 顶级豪华VIP包厢实拍";
    }}
    if (result.endsWith(" – Phòng Hát Karaoke KTV VIP")) {{
      const prefix = result.replace(" – Phòng Hát Karaoke KTV VIP", "");
      return prefix + " – 顶级豪华KTV包厢";
    }}
    if (result.endsWith(" phòng VIP")) {{
      return result.replace(" phòng VIP", " 豪华VIP包厢");
    }}
    if (result.endsWith(" phòng sofa da hoàng gia")) {{
      return result.replace(" phòng sofa da hoàng gia", " 欧式皇家真皮沙发包厢");
    }}
    if (result.endsWith(" phòng LED party vũ trường")) {{
      return result.replace(" phòng LED party vũ trường", " 炫彩LED动感派对包厢");
    }}

    // 5. Mẫu giới thiệu quán (Descriptions)
    if (result.includes("tự hào mang đến cho quý khách không gian vui chơi giải trí đỉnh cao") ||
        result.includes("tự hào mang đến cho Hà Nội không gian vui chơi giải trí đỉnh cao") ||
        result.includes("Đẳng cấp phòng hát, nâng tầm trải nghiệm.")) {{
      return "致力于为尊贵宾客打造顶级娱乐欢唱空间。店内配备现代豪华包厢、出众的专业隔音系统、震撼的JBL音响与炫彩动感LED舞台灯光。专业亲切的服务团队全程提供贴心周到的接待，确保您的每一次欢聚与宴会都倍感尊崇与舒适。诚邀您亲临体验——与亲朋好友共度奢华欢畅的美好时光！";
    }}

    return text;
  }}

  function setLanguage(lang) {{
    if (!window._origDocTitle) {{
      window._origDocTitle = document.title;
    }}

    currentLang = lang;
    if (lang === "zh") {{
      loadZhFont();
      document.documentElement.lang = "zh-CN";
      if (document.title.includes("Karaoke Cho Khách Trung Quốc")) {{
        document.title = "河内专接中国客户的豪华KTV：在Karaoke Kenz使用微信便捷预订 – Karaoke Kenz 202 Trung Kính";
      }} else if (document.title.includes("Tin tức & Kinh nghiệm") || document.title.includes("Tin tức & kinh nghiệm")) {{
        document.title = "新闻与欢唱攻略 – Karaoke Kenz 202 Trung Kính";
      }} else if (document.title.includes("– Bảng Giá, Hình Ảnh & Đặt Phòng VIP")) {{
        document.title = document.title.replace("– Bảng Giá, Hình Ảnh & Đặt Phòng VIP Hà Nội", "– 包厢价格、实景环境与极速预订")
                                       .replace("– Bảng Giá, Hình Ảnh & Đặt Phòng VIP", "– 包厢价格、实景环境与极速预订");
      }} else if (document.title.includes("Karaoke KTV Hà Nội") || document.title.includes("Hệ Thống Karaoke KTV Hà Nội")) {{
        document.title = "河内KTV系统 – 36+家顶级豪华KTV全名单与极速预订";
      }} else if (document.title.includes("Karaoke Kenz 202 Trung Kính")) {{
        document.title = "Karaoke Kenz 202 Trung Kính – 河内纸桥郡30间超级VIP豪华KTV包厢";
      }} else if (document.title.includes("Quản Lý Đơn Đặt Bàn")) {{
        document.title = "预订管理后台 (Windows 测试) – Karaoke Kenz";
      }}
    }} else {{
      document.documentElement.lang = "vi";
      if (window._origDocTitle) {{
        document.title = window._origDocTitle;
      }}
    }}

    // 1. Duyệt qua tất cả Text Nodes để đổi văn bản
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {{
        acceptNode: (node) => {{
          if (node.parentElement && node.parentElement.closest("script, style, [data-no-i18n]")) {{
            return NodeFilter.FILTER_REJECT;
          }}
          return NodeFilter.FILTER_ACCEPT;
        }}
      }}
    );

    let textNode;
    while ((textNode = walker.nextNode())) {{
      if (!originalTextMap.has(textNode)) {{
        originalTextMap.set(textNode, textNode.nodeValue);
      }}
      const original = originalTextMap.get(textNode);
      if (lang === "zh") {{
        textNode.nodeValue = smartTranslateZh(original);
      }} else {{
        textNode.nodeValue = original;
      }}
    }}

    // 2. Cập nhật các thuộc tính HTML (placeholder, alt, aria-label, title)
    document.querySelectorAll("[placeholder], [alt], [aria-label], [title]").forEach((el) => {{
      ["placeholder", "alt", "aria-label", "title"].forEach((attr) => {{
        if (!el.hasAttribute(attr)) return;
        const dataKey = "i18n" + attr.replace("-", "");
        if (!(dataKey in el.dataset)) {{
          el.dataset[dataKey] = el.getAttribute(attr);
        }}
        const origVal = el.dataset[dataKey];
        if (lang === "zh") {{
          el.setAttribute(attr, smartTranslateZh(origVal));
        }} else {{
          el.setAttribute(attr, origVal);
        }}
      }});
    }});

    // 3. Cập nhật nút bấm chuyển ngôn ngữ
    const btn = document.getElementById("lang-btn");
    if (btn) {{
      btn.textContent = lang === "zh" ? "Tiếng Việt" : "中文";
      btn.setAttribute("aria-label", lang === "zh" ? "Chuyển sang Tiếng Việt" : "切换到中文");
    }}

    try {{
      localStorage.setItem("karaoke_lang", lang);
    }} catch (e) {{}}
  }}

  function initI18n() {{
    const saved = localStorage.getItem("karaoke_lang");
    const urlParam = new URLSearchParams(window.location.search).get("lang");
    const initialLang = urlParam === "zh" || urlParam === "vi" ? urlParam : (saved === "zh" ? "zh" : "vi");

    const langBtn = document.getElementById("lang-btn");
    if (langBtn) {{
      langBtn.addEventListener("click", () => {{
        setLanguage(currentLang === "zh" ? "vi" : "zh");
      }});
    }}

    if (initialLang === "zh") {{
      setLanguage("zh");
    }}
  }}

  // Xuất ra phạm vi toàn cục (Global API)
  window.T = translate;
  window.getCurrentLang = () => currentLang;
  window.setLanguage = setLanguage;
  window.getI18nWeekday = (dayIndex) => currentLang === "zh" ? ZH_WEEKDAYS[dayIndex] : VI_WEEKDAYS[dayIndex];

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", initI18n);
  }} else {{
    initI18n();
  }}
}})();
"""

with open("js/i18n.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print(f"Generated js/i18n.js with {len(ZH_MAP)} dictionary entries + comprehensive regex patterns!")
