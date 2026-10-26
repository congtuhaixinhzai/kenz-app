import json
import re

# Comprehensive Vietnamese to Chinese mapping covering 100% of website content
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
    "Zalo": "Zalo",
    "WeChat": "微信",
    "Tiếng Việt": "Tiếng Việt",
    "中文": "中文",
    "HOT": "热门",
    "Trang chủ": "首页",
    "Hệ thống KTV Hà Nội": "河内KTV系统",
    "Hệ Thống": "连锁系统",
    "Hệ Thống 36+ Quán Karaoke KTV Hà Nội": "河内 36+ KTV 豪华连锁系统",
    "Hệ Thống Karaoke KTV Hà Nội VIP": "河内顶级豪华KTV连锁系统",
    "Hệ Thống 36+ Quán Karaoke KTV Hà Nội VIP – Đặt Phòng Nhanh 24/7": "河内36+顶级豪华KTV连锁系统 – 24小时极速预订",
    "KARAOKE": "KARAOKE 豪华KTV",
    "KENZ": "KENZ",
    "KTV VIP": "顶级豪华KTV",
    "VIP": "VIP",
    "Website": "网站",
    "và": "及",
    "Quản trị test": "后台管理测试",
    "wxid_0oxdncgq75g312": "wxid_0oxdncgq75g312",
    "© 2026": "© 2026",
    "© Karaoke Kenz Club 202 Trung Kính": "© Karaoke Kenz Club 202 Trung Kính",
    ". All rights reserved.": "。版权所有。",

    # 2. Mega Dropdown Navigation
    "👑 HỆ THỐNG 36+ QUÁN KARAOKE KTV VIP": "👑 36+ 顶级豪华KTV连锁系统",
    "Xem tất cả 36 cơ sở →": "查看全部36家分店 →",
    "📍 Cầu Giấy (12 quán)": "📍 纸桥郡 Cầu Giấy (12家)",
    "📍 Đống Đa & Hà Đông": "📍 栋多 & 河东郡 (15家)",
    "📍 Nam Từ Liêm & Khu Vực Khác": "📍 南慈廉 & 其他区域 (9家)",
    "📞 Hotline điều phối 24/7:": "📞 24小时调度热线：",
    "Xem bản đồ & toàn bộ 36 quán →": "查看地图及全部36家分店 →",
    "Xem tất cả 36 quán KTV": "查看全部36家KTV",
    "Xem tất cả 36 quán →": "查看全部36家分店 →",
    "Xem đầy đủ 36 quán KTV Hà Nội & Sài Gòn": "查看河内及胡志明市全部36家KTV",
    "⭐ Kenz Club 202 Trung Kính": "⭐ Kenz Club 202 Trung Kính 旗舰店",

    # 3. Districts
    "Cầu Giấy": "纸桥郡 Cầu Giấy",
    "Đống Đa": "栋多郡 Đống Đa",
    "Hà Đông": "河东郡 Hà Đông",
    "Nam Từ Liêm": "南慈廉郡 Nam Từ Liêm",
    "Hai Bà Trưng": "二征夫人郡 Hai Bà Trưng",
    "Tây Hồ": "西湖郡 Tây Hồ",
    "Quận 1": "第一郡 Quận 1",
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
    "📍 Thanh Trì": "📍 青池县 Thanh Trì",
    "🌟 Tất cả": "🌟 全部",
    "📍 QUẬN CẦU GIẤY": "📍 纸桥郡 CẦU GIẤY",
    "📍 QUẬN ĐỐNG ĐA": "📍 栋多郡 ĐỐNG ĐA",
    "📍 QUẬN HÀ ĐÔNG": "📍 河东郡 HÀ ĐÔNG",
    "📍 QUẬN NAM TỪ LIÊM": "📍 南慈廉郡 NAM TỪ LIÊM",
    "📍 QUẬN HAI BÀ TRƯNG": "📍 二征夫人郡 HAI BÀ TRƯNG",
    "📍 QUẬN TÂY HỒ": "📍 西湖郡 TÂY HỒ",
    "📍 QUẬN 1": "📍 胡志明市第一郡",

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

    # 5. About Section
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

    # 6. Promo & Perks
    "Liên hệ đặt phòng để nhận ưu đãi": "联系预订 即享独家礼遇",
    "Đặt phòng trước qua hotline, Zalo hoặc form đặt bàn để được nhận ngay các ưu đãi của quán.": "通过热线、微信/Zalo 或在线表单提前预订，即刻享受本店多重好礼。",
    "Tặng hoa quả": "免费赠送水果拼盘",
    "Đĩa trái cây tươi cho phòng của bạn.": "为您的包厢送上新鲜丰富的水果拼盘。",
    "Tặng bánh sinh nhật": "赠送精美生日蛋糕",
    "Ghi chú khi đặt phòng để quán chuẩn bị.": "预订时备注，门店将悉心为您准备。",
    "Và nhiều ưu đãi hấp dẫn khác": "更多惊喜优惠礼遇",
    "Gọi hotline để được tư vấn chi tiết.": "欢迎拨打热线咨询各项套餐详情。",
    "Xem ảnh khuyến mãi cỡ lớn": "查看优惠海报大图",

    # 7. KTV Hanoi Page Details
    "👑 HỆ THỐNG KARAOKE KTV HÀ NỘI & LIÊN TỈNH": "👑 河内及跨省KTV连锁系统",
    "Chuỗi 36+ phòng hát Karaoke KTV sang trọng, đẳng cấp trải khắp các quận thủ đô Hà Nội và TP. Hồ Chí Minh. Dàn âm thanh công suất lớn, ánh sáng laser sân khấu hiện đại, phục vụ chu đáo 24/7.": "分布于河内各郡及胡志明市的36+高端豪华KTV连锁。大功率震撼音响、动感激光舞台灯效，24/7全天候贴心服务。",
    "Mạng lưới 36+ quán Karaoke KTV đỉnh cao trải khắp thủ đô Hà Nội & Sài Gòn.": "覆盖首都河内及西贡的36+高端豪华KTV连锁网络。",
    "👑 Chuỗi Liên Kết Đẳng Cấp": "👑 尊贵连锁网络",
    "36 quán": "36家分店",
    "36 quán KTV VIP": "36家顶级KTV",
    "1000+": "1000+",
    "50.000+": "50,000+",
    "1000+ Phòng hát đẳng cấp": "1000+ 间豪华包厢",
    "24/24h Đặt bàn giữ chỗ": "24小时预订留房",
    "Tìm kiếm theo tên quán hoặc tên đường (VD: Paris Club, Nguyễn Khang, Trần Thái Tông, Tố Hữu...)": "按店名或路名搜索（例如：Paris Club, Nguyễn Khang, Trần Thái Tông, Tố Hữu...）",
    "Không tìm thấy quán nào phù hợp": "未找到相符的KTV分店",
    "Thử tìm với từ khóa khác (ví dụ: Cầu Giấy, Nguyễn Khang, Trần Thái Tông...) hoặc chọn mục \"Tất cả\".": "请尝试其他关键词（例如：Cầu Giấy, Nguyễn Khang, Trần Thái Tông...）或点击“全部”。",

    # 8. Cards & Pills
    "⭐ 5.0 VIP": "⭐ 5.0 VIP",
    "Địa chỉ:": "地址：",
    "🔊 Âm thanh cực đã": "🔊 顶级震撼音效",
    "💡 Phòng VIP LED": "💡 炫彩LED包厢",
    "⚡ Phục vụ 24/7": "⚡ 24/7全天候服务",
    "👑 Cơ sở trung tâm": "👑 中心旗舰总店",
    "👑 Cơ sở Kenz VIP": "👑 Kenz VIP总店",
    "Xem chi tiết quán": "查看分店详情",
    "Xem chi tiết": "查看详情",
    "Đặt phòng": "预订包厢",
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

    # 9. Guarantees (4 Cam Kết Vàng)
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

    # 10. Venue Detail Page Elements
    "Quy mô": "包厢规模",
    "Nhân viên": "服务团队",
    "Bài hát": "点歌曲库",
    "Phòng": "间包厢",
    "Phục vụ": "位员工服务",
    "🎤 Đặt phòng ngay tại cơ sở này": "🎤 立即预订此分店",
    "Gọi: 0342 092 999": "致电：0342 092 999",
    "💬 Nhắn Zalo": "💬 Zalo 在线咨询",
    "Đặc quyền nổi bật tại": "独家特色与配置",
    "🔊 Dàn Loa JBL / BMB Cực Khủng": "🔊 顶级 JBL / BMB 震撼音响系统",
    "Công suất lớn, bass chắc nịch, micro cao cấp chống hú rè tuyệt đối.": "大功率输出、低音浑厚强劲，无线麦克风绝不啸叫。",
    "💡 Ánh Sáng Laser 3D Vũ Trường": "💡 3D 激光舞厅舞台灯光",
    "Màn LED cảm ứng theo giai điệu nhạc cực bắt mắt và hiện đại.": "LED大屏幕随音乐节奏律动变幻，炫丽夺目充满现代科技感。",
    "🛡️ Cách Âm Chuẩn Tiêu Chuẩn 100%": "🛡️ 100% 国际专业标准隔音",
    "Tường cách âm chuyên dụng, đảm bảo không gian riêng tư trọn vẹn.": "高规格专业隔音墙体结构，完全保障私密欢聚自由。",
    "🍹 Menu Rượu Ngoại & Tiệc Chu Đáo": "🍹 名品洋酒与精致餐饮服务",
    "Hoa quả tươi, đồ ăn nóng sốt và các loại đồ uống hảo hạng phục vụ tận nơi.": "鲜切水果大拼盘、热气腾腾的特色佳肴及高档进口酒水直供包厢。",
    "📸 Không gian phòng hát thực tế": "📸 真实包厢环境实景实拍",
    "(Bấm vào ảnh để phóng to toàn màn hình)": "（点击任意图片可全屏高清放大预览）",
    "💰 Bảng giá phòng tham khảo": "💰 包厢参考价格表",
    "Phòng Tiêu Chuẩn (5-10 người)": "标准包厢（5-10人）",
    "Phòng VIP (10-20 người)": "VIP包厢（10-20人）",
    "Phòng Super VIP Party (20-40 người)": "超级派对包厢（20-40人）",
    "* Giá có thể thay đổi tùy khung giờ và dịp lễ. Quý khách vui lòng đặt trước để nhận phòng đẹp nhất.": "* 价格可能随时间段及节假日略有浮动。请提前预订以确保留存最佳位置包厢。",
    "⚡ Đặt phòng nhanh 24/7": "⚡ 24/7 极速预订通道",
    "Giữ chỗ miễn phí 100%, nhân viên gọi xác nhận trong 3 phút.": "100% 免费留房，客服将在3分钟内致电与您确认。",
    "Hoặc gọi hotline trực tiếp:": "或直接拨打预订专线：",
    "Các quán Karaoke KTV khác tại": "该区域其他推荐KTV分店",

    # 11. FAQ Section
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
    "Hoàn toàn KHÔNG MẤT PHÍ và KHÔNG CẦN CỌC TRƯỚC đối với các ngày trong tuần. Quý khách chỉ cần điền họ tên, số điện thoại và giờ dự kiến đến, quán sẽ chủ động giữ phòng và chuẩn bị đón tiếp chu đáo.": "工作日完全免费且无需提前付定金。您只需留下姓名、电话及预计到店时间，门店将主动为您保留优质包厢并悉心迎接。",
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

    # 12. Booking Modal
    "Hệ Thống Karaoke KTV Hà Nội": "河内豪华KTV连锁系统",
    "Thông tin đặt chỗ": "填写预订信息",
    "Cơ sở đặt": "预订分店",
    "Cơ sở / Quán đã chọn:": "已选分店：",
    "Không cần thanh toán. Nhân viên sẽ gọi hoặc nhắn Zalo để xác nhận và xếp phòng cho bạn.": "无需提前付款。客服将致电或发消息确认并为您预留包厢。",
    "Họ và tên": "姓名",
    "Họ và tên *": "姓名 *",
    "Số điện thoại": "电话号码",
    "Số điện thoại *": "电话号码 *",
    "Ngày đặt": "预订日期",
    "Ngày đặt *": "预订日期 *",
    "Giờ đến": "预计到店时间",
    "Giờ đến *": "预计到店时间 *",
    "Ghi chú thêm (nếu có)": "特殊要求备注（选填）",
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

    # 13. Contact & Location
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

    # 14. Customer Reviews
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

    # 15. Footer
    "Hotline điều phối & đặt phòng VIP 24/7:": "24/7 VIP 预订及调度专线：",
    "Cam kết phục vụ chu đáo, chất lượng âm thanh đỉnh cao.": "承诺周到服务，震撼巅峰音质。",
    "Hotline đặt phòng VIP 24/7:": "24/7 VIP 预订专线：",
    "Cam kết dịch vụ phòng hát chất lượng cao.": "品质包厢保证，高标准服务体验。"
}

# Generate js/i18n.js
i18n_code = f"""/**
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

    return text;
  }}

  function setLanguage(lang) {{
    currentLang = lang;
    if (lang === "zh") {{
      loadZhFont();
      document.documentElement.lang = "zh-CN";
      if (document.title.includes("Karaoke Kenz 202 Trung Kính")) {{
        document.title = "Karaoke Kenz 202 Trung Kính – 河内纸桥郡30间超级VIP豪华KTV包厢";
      }} else if (document.title.includes("Karaoke KTV Hà Nội")) {{
        document.title = "河内KTV系统 – 36+家顶级豪华KTV全名单与极速预订";
      }}
    }} else {{
      document.documentElement.lang = "vi";
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

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", initI18n);
  }} else {{
    initI18n();
  }}
}})();
"""

with open('js/i18n.js', 'w', encoding='utf-8') as f:
    f.write(i18n_code)
print(f"Generated comprehensive js/i18n.js with {len(ZH_MAP)} native entries!")
