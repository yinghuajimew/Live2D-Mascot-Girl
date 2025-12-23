import os
import json

TARGET_DIR = 'assets'
OUTPUT_FILE = 'assets/model_list.json'

models = []
messages = []

print(f"正在扫描 {TARGET_DIR} ...")

for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith('.model.json') or file == 'model.json':
            # 获取完整路径
            full_path = os.path.join(root, file)
            
            # 转换路径分隔符 (Windows兼容)
            path = full_path.replace('\\\\', '/')
            
            # 掐头去尾，只保留 assets/ 后面的部分
            # 比如: "GirlsFrontline/95type_405/model.json"
            if path.startswith(TARGET_DIR + '/'):
                clean_path = path[len(TARGET_DIR)+1:]
                
                models.append(clean_path)
                
                # 提取角色名做提示语
                name = clean_path.split('/')[1] 
                messages.append(f"Load: {name}")
                print(f"✅ 收录: {clean_path}")

data = {
    "models": models,
    "messages": messages
}

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\n🎉 扫描完成！共收录 {len(models)} 个模型。")