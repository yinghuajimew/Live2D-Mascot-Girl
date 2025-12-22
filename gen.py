import os
import json

# 设定我们要扫描的文件夹名字
TARGET_DIR = 'assets'
# 输出的文件位置
OUTPUT_FILE = os.path.join(TARGET_DIR, 'model_list.json')

models_list = []
messages_list = []

print(f"🚀 开始扫描 {TARGET_DIR} 文件夹...")

# 遍历目录
for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        # 寻找所有 .model.json 结尾的文件 (有些旧模型是 model.json)
        if file.endswith('.model.json') or file == 'model.json':
            
            # 1. 获取文件的完整路径
            full_path = os.path.join(root, file)
            
            # 2. 转换成相对路径 (变成 assets/xxx/xxx.json)
            # 我们需要把路径里的 \ 替换成 / (防止 Windows/Android 路径差异)
            normalized_path = full_path.replace('\\', '/')
            
            # 3. 关键：去掉开头的 "assets/"，因为 autoload.js 会自动拼上 assets
            # 如果路径是 assets/moc3/22/model.json，我们要的是 moc3/22/model.json
            if normalized_path.startswith(TARGET_DIR + '/'):
                rel_path = normalized_path[len(TARGET_DIR) + 1:]
            else:
                rel_path = normalized_path

            # 4. 提取名字（用上一级文件夹的名字作为角色名）
            model_name = os.path.basename(os.path.dirname(full_path))
            
            # 5. 存入列表
            models_list.append(rel_path)
            messages_list.append(f"Loaded: {model_name}")
            
            print(f"✅ [发现] {model_name}")

# 构建 JSON 结构
data = {
    "models": models_list,
    "messages": messages_list
}

# 写入文件
try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("-" * 30)
    print(f"🎉 成功！共扫描到 {len(models_list)} 个模型。")
    print(f"📁 文件已生成在: {OUTPUT_FILE}")
except Exception as e:
    print(f"❌ 写入文件失败: {e}")