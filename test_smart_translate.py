import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('extracted_texts.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)

# Load current ZH_MAP from build_full_i18n.py
import build_full_i18n
zh_dict = build_full_i18n.ZH_MAP

# Add more exact phrases to zh_dict
extra_phrases = {
    "Hát hết mình,": "尽情欢唱，",
    "quẩy nhiệt tình": "嗨翻全场",
    "Hình ảnh thực tế tại Karaoke Kenz Club 202 Trung Kính.": "Karaoke Kenz Club 202 Trung Kính 实景实拍。",
    "Hệ Thống": "连锁系统",
    "Hệ Thống 36+ Quán Karaoke KTV Hà Nội": "河内 36+ KTV 豪华连锁系统",
    "Mạng lưới 36+ quán Karaoke KTV đỉnh cao trải khắp thủ đô Hà Nội & Sài Gòn.": "覆盖首都河内及西贡的 36+ 顶级豪华 KTV 连锁网络。",
    "Quản trị test": "后台管理测试",
    "wxid_0oxdncgq75g312": "wxid_0oxdncgq75g312",
    "© 2026": "© 2026",
    "© Karaoke Kenz Club 202 Trung Kính": "© Karaoke Kenz Club 202 Trung Kính",
    "· Cam kết dịch vụ phòng hát chất lượng cao.": "· 承诺提供高品质包厢与尊贵服务。",
    "· Cam kết phục vụ chu đáo, chất lượng âm thanh đỉnh cao.": "· 承诺贴心周到服务，顶级震撼音响。",
    "Cơ sở đặt": "预订门店",
    "Cơ sở / Quán đã chọn:": "已选分店：",
    "Hotline đặt phòng": "预订热线",
    "Hotline điều phối 24/7:": "24小时调度专线：",
    "Hotline đặt phòng VIP 24/7:": "24/7 VIP 预订专线：",
    "Hotline điều phối & đặt phòng VIP 24/7:": "24/7 VIP 预订及调度专线：",
    "Bấm để tự động mở Zalo và gửi mã đặt phòng cho quản lý": "点击将自动打开 Zalo 并发送预订码给店长",
    "Chụp lại mã này. Nhân viên sẽ liên hệ xác nhận trong ít phút.": "请截图保存此预订编号。客服经理将在数分钟内与您联系确认。",
    "Đã gửi yêu cầu đặt bàn": "预订申请已成功提交",
    "Yêu cầu trang trí tiệc, số lượng người, phòng VIP…": "派对布置要求、欢唱人数、包厢风格偏好等…",
    "Nhắn Zalo xác nhận giữ phòng ngay": "立即通过 Zalo 发送预订凭证确认留房",
    "Đặt thêm": "再订一间",
    "Xong": "完成关闭",
    "Giữ chỗ miễn phí 100%, nhân viên gọi xác nhận trong 3 phút.": "100% 免费留房，客服将在3分钟内致电确认。",
    "Hoặc gọi hotline trực tiếp:": "或直接拨打热线电话：",
    "Xem tất cả 36 cơ sở →": "查看全部36家分店 →",
    "Xem tất cả 36 quán KTV": "查看全部36家KTV",
    "Xem tất cả 36 quán →": "查看全部36家分店 →",
    "Xem đầy đủ 36 quán KTV Hà Nội & Sài Gòn": "查看河内及胡志明市全部36家KTV",
    "Xem chi tiết quán": "查看分店详情",
    "Xem chi tiết": "查看详情",
    "Đặt phòng": "预订包厢",
    "Gọi điện": "致电热线",
    "Gọi hotline": "拨打热线",
    "Âm thanh đỉnh cao": "顶级巅峰音效",
    "Âm thanh châu Âu": "欧洲顶级高保真音响",
    "Phòng Party lớn": "大型豪华派对房",
    "Phòng VIP LED": "炫彩LED包厢",
    "Phòng hát đẳng cấp": "豪华顶级包厢",
    "Phục vụ 24/7": "24/7 全天候服务",
    "Quy mô": "包厢规模",
    "Nhân viên": "服务团队",
    "Bài hát": "点歌曲库",
    "Không gian phòng hát thực tế": "真实包厢环境实景实拍",
    "(Bấm vào ảnh để phóng to toàn màn hình)": "（点击任意图片可全屏高清放大预览）",
    "💰 Bảng giá phòng tham khảo": "💰 包厢参考价格表",
    "Phòng Tiêu Chuẩn (5-10 người)": "标准包厢（5-10人）",
    "Phòng VIP (10-20 người)": "VIP包厢（10-20人）",
    "Phòng Super VIP Party (20-40 người)": "超级派对包厢（20-40人）",
    "* Giá có thể thay đổi tùy khung giờ và dịp lễ. Quý khách vui lòng đặt trước để nhận phòng đẹp nhất.": "* 价格可能随时间段及节假日略有浮动。请提前预订以确保留存最佳位置包厢。",
    "⚡ Đặt phòng nhanh 24/7": "⚡ 24/7 极速预订通道",
    "⚡ Phục vụ 24/7": "⚡ 24/7 全天候服务",
    "⭐ 5.0 VIP": "⭐ 5.0 VIP",
    "🌟 Tất cả": "🌟 全部",
    "💎 ĐẶC QUYỀN KHÁCH HÀNG": "💎 尊贵客户专享特权",
    "👑 Chuỗi Liên Kết Đẳng Cấp": "👑 尊贵连锁网络",
    "👑 Cơ sở Kenz VIP": "👑 Kenz VIP总店",
    "👑 Cơ sở trung tâm": "👑 中心旗舰总店",
    "👑 HỆ THỐNG 36+ QUÁN KARAOKE KTV VIP": "👑 36+ 顶级豪华KTV连锁系统",
    "👑 HỆ THỐNG KARAOKE KTV HÀ NỘI & LIÊN TỈNH": "👑 河内及跨省KTV连锁系统",
    "💡 Phòng VIP LED": "💡 炫彩LED包厢",
    "💡 Ánh Sáng Laser 3D Vũ Trường": "💡 3D 激光舞厅舞台灯光",
    "💬 Nhắn Zalo": "💬 Zalo 在线咨询",
    "🔊 Dàn Loa JBL / BMB Cực Khủng": "🔊 顶级 JBL / BMB 震撼音响系统",
    "🔊 Âm thanh cực đã": "🔊 顶级震撼音质",
    "🛡️ Cách Âm Chuẩn Tiêu Chuẩn 100%": "🛡️ 100% 国际专业标准隔音",
    "🍹 Menu Rượu Ngoại & Tiệc Chu Đáo": "🍹 名品洋酒与精致餐饮服务",
    "❓ HỎI ĐÁP DỊCH VỤ": "❓ 常见预订问答",
    "ĐANG MỞ CỬA 24/24H": "24小时营业中",
    "30 Phòng Hát": "30间豪华包厢",
    "36 quán": "36家分店",
    "1000+": "1000+",
    "50.000+": "50,000+",
    "1000+ Phòng hát đẳng cấp": "1000+ 间豪华包厢",
    "24/24h Đặt bàn giữ chỗ": "24小时预订留房",
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
    "Địa chỉ:": "地址：",
    "Trang chủ": "首页",
    "Hệ thống KTV Hà Nội": "河内KTV系统",
    "Tin tức": "新闻资讯",
    "Tin tức & kinh nghiệm hát karaoke": "新闻与欢唱攻略",
    "Giới thiệu": "关于我们",
    "KTV HÀ NỘI": "河内KTV",
    "Hình ảnh": "图片环境",
    "Ưu đãi": "优惠活动",
    "Liên hệ": "联系我们",
    "Đánh giá": "顾客评价",
    "Đặt phòng ngay": "立即预订",
    "Đặt bàn": "预订留座",
    "Gọi điện": "致电热线",
    "Zalo": "Zalo",
    "WeChat": "微信",
    "Tiếng Việt": "Tiếng Việt",
    "中文": "中文",
    "HOT": "热门"
}

zh_dict.update(extra_phrases)

def test_smart(text):
    clean = text.strip()
    if clean in zh_dict:
        return True, zh_dict[clean]
    
    # Check prefixes
    prefixes = [
        ("Giới thiệu về ", "关于 "),
        ("Đặc quyền nổi bật tại ", " 独家特色特权"),
        ("Những câu hỏi thường gặp về ", "关于 "),
        ("Các quán Karaoke KTV khác tại ", " 的其他KTV推荐分店"),
        ("Cơ sở ", ""),
        ("Chỗ đỗ ô tô tại ", ""),
        ("🎤 Đặt phòng tại ", "🎤 预订 "),
        ("🎤 Đặt phòng ngay tại ", "🎤 立即预订 "),
        ("Gọi: ", "拨打：")
    ]
    for p, _ in prefixes:
        if clean.startswith(p):
            return True, "Dynamic prefix matched"

    # Regex patterns
    if re.match(r'^\d+\+\s*Phòng$', clean):
        return True, "Rooms count"
    if re.match(r'^\d+\+\s*Phục vụ$', clean):
        return True, "Staff count"
    if re.match(r'^\d+\s*quán$', clean):
        return True, "Venues count"
    if re.match(r'^\d+\s*tuần trước$', clean):
        return True, "Weeks ago"
    if re.match(r'^[\d\s.,+-]+$', clean) or clean.startswith('tel:') or clean.startswith('http'):
        return True, "Number/Phone/URL"

    # Venue names / addresses (proper nouns)
    if any(clean.startswith(prefix) for prefix in ['Karaoke ', 'Bar ', 'A PLUS ', 'A9 ', 'AMIGO ', 'F5 ', 'GRAND ', 'Kenz ', 'LONDON ', 'Level ', 'Lucky ', 'Paris ', 'Raptor ', 'Royal ', 'SING ', 'Sing ', 'The Voice ', 'Tip Top ', 'Titan ', 'VOLUME ', 'X-MEN ']):
        return True, "Brand/Venue Name"

    return False, clean

matched = 0
unmatched = []

for t in texts:
    ok, res = test_smart(t)
    if ok:
        matched += 1
    else:
        unmatched.append(t)

print(f"Total strings: {len(texts)}")
print(f"Matched & Translated: {matched} ({matched/len(texts)*100:.1f}%)")
print(f"Unmatched strings: {len(unmatched)}")
for u in unmatched[:30]:
    print("  [UNMATCHED]", repr(u))
