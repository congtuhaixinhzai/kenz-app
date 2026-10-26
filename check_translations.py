import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('extracted_texts.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)

with open('js/i18n.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract keys from ZH_DICTIONARY
dict_keys = set()
matches = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', content)
for k, v in matches:
    dict_keys.add(k)

missing = [t for t in texts if t not in dict_keys and not t.isdigit() and len(t) > 2]
print(f"Total extracted strings: {len(texts)}")
print(f"Currently in dictionary: {len(dict_keys)}")
print(f"Missing translations: {len(missing)}")

with open('missing_translations.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)

print("Saved missing strings to missing_translations.json")
