"""
数据库查询示例脚本
演示如何查询数据库中的各种数据
"""
from app.core.database import SessionLocal
from app.models import models
from sqlalchemy import func
import json

def example_queries():
    """示例查询"""
    db = SessionLocal()
    
    try:
        # 示例 1: 查询所有用户
        print("=== 示例 1: 查询所有用户 ===")
        users = db.query(models.User).all()
        for user in users:
            print(f"用户: {user.username}, 医院: {user.hospital}")
        
        # 示例 2: 查询特定用户
        print("\n=== 示例 2: 查询特定用户 ===")
        user = db.query(models.User).filter(models.User.username == "testuser").first()
        if user:
            print(f"找到用户: {user.username}")
        else:
            print("用户不存在")
        
        # 示例 3: 查询所有评估记录
        print("\n=== 示例 3: 查询所有评估记录 ===")
        evaluations = db.query(models.Evaluation).all()
        for eval in evaluations:
            print(f"评估: {eval.name}, 价值: {eval.total_value}")
        
        # 示例 4: 查询特定评估的指标明细
        print("\n=== 示例 4: 查询评估的指标明细 ===")
        if evaluations:
            for ind in json.loads(evaluations[0].indicators or '[]'):
                print(f"类别 {ind['category']}: {ind['item_name']} = {ind['amount']}")

        # 示例 5: 统计查询
        print("\n=== 示例 5: 统计信息 ===")
        total_users = db.query(func.count(models.User.id)).scalar()
        total_evaluations = db.query(func.count(models.Evaluation.id)).scalar()
        total_value = db.query(func.sum(models.Evaluation.total_value)).scalar() or 0
        
        print(f"用户总数: {total_users}")
        print(f"评估总数: {total_evaluations}")
        print(f"总价值: {total_value}")
        
    except Exception as e:
        print(f"查询错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    example_queries()
