"""一次性迁移脚本：为 novel_chapters 表添加树结构字段"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'ai_novel.db')

if not os.path.exists(db_path):
    print("数据库文件不存在，首次启动时会自动创建表结构，无需迁移")
    exit(0)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# 检查是否已有 node_type 列
c.execute("PRAGMA table_info(novel_chapters)")
existing_cols = {col[1] for col in c.fetchall()}

if 'node_type' in existing_cols:
    print("已迁移过，跳过")
    conn.close()
    exit(0)

# 备份旧数据
c.execute("SELECT * FROM novel_chapters")
rows = c.fetchall()
print(f"备份了 {len(rows)} 条章节记录")

# 添加新列
columns_to_add = [
    ("node_type", "VARCHAR(20) DEFAULT 'chapter'"),
    ("parent_id", "VARCHAR(36) REFERENCES novel_chapters(id)"),
    ("is_expanded", "BOOLEAN DEFAULT 1"),
    ("sort_order", "INTEGER DEFAULT 0"),
]

for col_name, col_def in columns_to_add:
    try:
        c.execute(f"ALTER TABLE novel_chapters ADD COLUMN {col_name} {col_def}")
        print(f"✅ 添加列: {col_name}")
    except sqlite3.OperationalError as e:
        print(f"⚠️ {col_name}: {e}")

# 为已有章节设置 sort_order = chapter_number
c.execute("UPDATE novel_chapters SET sort_order = chapter_number")

conn.commit()

# 验证
c.execute("PRAGMA table_info(novel_chapters)")
print("\n更新后的表结构:")
for col in c.fetchall():
    print(f"  {col[1]} ({col[2]})")

c.execute("SELECT id, title, node_type, parent_id, sort_order FROM novel_chapters")
for row in c.fetchall():
    print(f"  数据: {row}")

conn.close()
print("\n✅ 迁移完成")
