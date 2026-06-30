import sys
import os

# 确保 backend 目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base

# 确保所有数据表已创建
Base.metadata.create_all(bind=engine)
print("✅ 数据库初始化完成")
