import os
import re
import sys
import json
from html.parser import HTMLParser

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Parse ZH_DICTIONARY from js/i18n.js
with open("js/i18n.js", "r", encoding="utf-8") as f:
    i18n_content = f.read()

dict_match = re.search(r"const ZH_DICTIONARY\s*=\s*(\{[\s\S]*?\n\s*\});", i18n_content)
if not dict_match:
    print("Could not find ZH_DICTIONARY in js/i18n.js")
    sys.exit(1)

zh_dict_str = dict_match.group(1)
# convert to valid json if needed, or eval/parse json
# The dictionary keys and values are standard JSON strings
try:
    zh_dict = json.loads(zh_dict_str)
except Exception as e:
    print("Error parsing ZH_DICTIONARY json, trying line-by-line:", e)
    zh_dict = {}
    for line in zh_dict_str.splitlines():
        m = re.match(r'^\s*"([^"]+)":\s*"([^"]+)",?', line)
        if m:
            zh_dict[m.group(1)] = m.group(2)

print(f"Loaded {len(zh_dict)} dictionary entries from js/i18n.js")

def smart_translate(text):
    if not text:
        return ""
    trimmed = text.strip()
    clean_key = re.sub(r"\s+", " ", trimmed)
    if clean_key in zh_dict:
        return zh_dict[clean_key]
    
    # Prefix rules
    if clean_key.startswith("Giới thiệu về "):
        return "关于 " + clean_key[len("Giới thiệu về "):]
    if clean_key.startswith("Đặc quyền nổi bật tại "):
        return clean_key[len("Đặc quyền nổi bật tại "):] + " 独家特色特权"
    if clean_key.startswith("Những câu hỏi thường gặp về "):
        return "关于 " + clean_key[len("Những câu hỏi thường gặp về "):] + " 的常见问题"
    if clean_key.startswith("Cơ sở ") and "có hỗ trợ đoàn đông người và tổ chức tiệc không?" in clean_key:
        v = clean_key.replace("Cơ sở ", "").replace(" có hỗ trợ đoàn đông người và tổ chức tiệc không?", "")
        return v + " 支持大型聚会与派对吗？"
    if clean_key.startswith("Chỗ đỗ ô tô tại ") and clean_key.endswith("như thế nào?"):
        v = clean_key.replace("Chỗ đỗ ô tô tại ", "").replace(" như thế nào?", "")
        return v + " 的停车位情况如何？"
    if clean_key.startswith("🎤 Đặt phòng tại "):
        return "🎤 预订 " + clean_key[len("🎤 Đặt phòng tại "):] + " 包厢"
    if clean_key.startswith("🎤 Đặt phòng ngay tại "):
        return "🎤 立即预订 " + clean_key[len("🎤 Đặt phòng ngay tại "):] + " 包厢"
    if clean_key.startswith("Các quán Karaoke KTV khác tại "):
        return clean_key[len("Các quán Karaoke KTV khác tại "):] + " 的其他KTV推荐分店"
    if clean_key.startswith("Gọi: "):
        return "致电：" + clean_key[5:]
    if clean_key.startswith("Gọi hotline "):
        return "拨打预订专线 " + clean_key[len("Gọi hotline "):]
    if clean_key.startswith("Xem chi tiết "):
        return "查看 " + clean_key[len("Xem chi tiết "):] + " 分店详情"
    if re.match(r"^\d+\+\s*Phòng$", clean_key):
        return clean_key.replace("Phòng", "间包厢")
    if re.match(r"^\d+\+\s*Phục vụ$", clean_key):
        return clean_key.replace("Phục vụ", "位员工服务")
    if re.match(r"^\d+\s*quán$", clean_key):
        return clean_key.replace("quán", "家分店")
    if re.match(r"^\d+\s*tuần trước$", clean_key):
        return clean_key.replace("tuần trước", "周前")
    if clean_key.endswith("/ giờ") or clean_key.endswith("/h"):
        return clean_key.replace("/ giờ", "越盾/小时").replace("/h", "越盾/小时")
    if clean_key.endswith(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP Hà Nội"):
        return clean_key.replace(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP Hà Nội", " – 包厢价格、环境实拍与极速预订")
    if clean_key.endswith(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP"):
        return clean_key.replace(" – Bảng Giá, Hình Ảnh & Đặt Phòng VIP", " – 包厢价格、环境实拍与极速预订")
    if clean_key.endswith(" – Đặt Phòng VIP Hà Nội"):
        return clean_key.replace(" – Đặt Phòng VIP Hà Nội", " – 顶级VIP包厢极速预订")
    if clean_key.endswith(" – Phòng Hát Karaoke VIP Đẹp"):
        return clean_key.replace(" – Phòng Hát Karaoke VIP Đẹp", " – 顶级豪华VIP包厢实拍")
    if clean_key.endswith(" – Phòng Hát Karaoke KTV VIP"):
        return clean_key.replace(" – Phòng Hát Karaoke KTV VIP", " – 顶级豪华KTV包厢")
    if clean_key.endswith(" phòng VIP"):
        return clean_key.replace(" phòng VIP", " 豪华VIP包厢")
    if clean_key.endswith(" phòng sofa da hoàng gia"):
        return clean_key.replace(" phòng sofa da hoàng gia", " 欧式皇家真皮沙发包厢")
    if clean_key.endswith(" phòng LED party vũ trường"):
        return clean_key.replace(" phòng LED party vũ trường", " 炫彩LED动感派对包厢")
    if "tự hào mang đến cho quý khách không gian vui chơi giải trí đỉnh cao" in clean_key or \
       "tự hào mang đến cho Hà Nội không gian vui chơi giải trí đỉnh cao" in clean_key or \
       "Đẳng cấp phòng hát, nâng tầm trải nghiệm." in clean_key:
        return "致力于为尊贵宾客打造顶级娱乐欢唱空间。店内配备现代豪华包厢、出众的专业隔音系统、震撼的JBL音响与炫彩动感LED舞台灯光。专业亲切的服务团队全程提供贴心周到的接待，确保您的每一次欢聚与宴会都倍感尊崇与舒适。诚邀您亲临体验——与亲朋好友共度奢华欢畅的美好时光！"
        
    return clean_key

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_ignored = False
        self.ignored_tags = {"script", "style", "noscript"}

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignored_tags:
            self.in_ignored = True
        attr_dict = dict(attrs)
        for a in ["placeholder", "alt", "aria-label", "title"]:
            if a in attr_dict and attr_dict[a].strip():
                self.texts.append((attr_dict[a], self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag.lower() in self.ignored_tags:
            self.in_ignored = False

    def handle_data(self, data):
        if not self.in_ignored:
            s = data.strip()
            if s and not re.match(r"^[0-9\s\.\,\:\-\+\(\)\/\*·→—]+$", s):
                self.texts.append((data, self.getpos()[0]))

html_files = [f for f in os.listdir(".") if f.endswith(".html")]

untranslated_report = {}
total_strings = 0
translated_strings = 0

for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    parser = TextExtractor()
    parser.feed(content)
    
    for raw_text, line_no in parser.texts:
        clean = re.sub(r"\s+", " ", raw_text.strip())
        if not clean or len(clean) < 2:
            continue
        # Skip pure symbols, numbers, phones, URLs
        if re.match(r"^(0\d{9,10}|https?://.*|\d+|\d+\.\d+|\+84\d+)$", clean):
            continue
        total_strings += 1
        tr = smart_translate(clean)
        # Has it been translated? (contains Chinese characters or different text)
        is_zh = bool(re.search(r"[\u4e00-\u9fff]", tr))
        if is_zh:
            translated_strings += 1
        else:
            if clean not in untranslated_report:
                untranslated_report[clean] = []
            untranslated_report[clean].append(f"{hf}:{line_no}")

print(f"\n--- AUDIT RESULTS ---")
print(f"Total evaluated text occurrences: {total_strings}")
print(f"Translated to Chinese: {translated_strings}")
print(f"Untranslated distinct strings: {len(untranslated_report)}")
print(f"\nSample of untranslated strings:")
for k, locs in list(untranslated_report.items())[:50]:
    print(f"  [{k}] -> found in {len(locs)} places (e.g. {locs[0]})")
