from app.database import engine, Base

# 确保所有数据表已创建
Base.metadata.create_all(bind=engine)
print("✅ 数据库初始化完成")
