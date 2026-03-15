"""
查看数据库内容的脚本
运行方式: python view_database.py
"""
from app.core.database import SessionLocal
from app.models import models
from sqlalchemy import text

def view_database():
    """查看数据库中的所有数据"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("数据库内容查看")
        print("=" * 60)
        
        # 1. 查看用户表
        print("\n【用户表 (users)】")
        print("-" * 60)
        users = db.query(models.User).all()
        if users:
            for user in users:
                print(f"ID: {user.id}")
                print(f"  用户名: {user.username}")
                print(f"  医院: {user.hospital or '未设置'}")
                print()
        else:
            print("  暂无用户数据")
        
        # 2. 查看评估表
        print("\n【评估表 (evaluations)】")
        print("-" * 60)
        evaluations = db.query(models.Evaluation).all()
        if evaluations:
            for eval in evaluations:
                print(f"ID: {eval.id}")
                print(f"  评估名称: {eval.evaluation_name}")
                print(f"  总价值: {eval.total_value}")
                print(f"  状态: {eval.status}")
                print(f"  创建时间: {eval.created_at}")
                print()
        else:
            print("  暂无评估数据")
        
        # 3. 查看指标明细表
        print("\n【指标明细表 (indicator_data)】")
        print("-" * 60)
        indicators = db.query(models.IndicatorData).all()
        if indicators:
            for ind in indicators:
                print(f"ID: {ind.id}")
                print(f"  评估ID: {ind.evaluation_id}")
                print(f"  类别: {ind.category}")
                print(f"  项目名称: {ind.item_name}")
                print(f"  金额: {ind.amount}")
                print()
        else:
            print("  暂无指标数据")
        
        # 4. 统计信息
        print("\n【统计信息】")
        print("-" * 60)
        user_count = db.query(models.User).count()
        eval_count = db.query(models.Evaluation).count()
        indicator_count = db.query(models.IndicatorData).count()
        
        print(f"用户总数: {user_count}")
        print(f"评估总数: {eval_count}")
        print(f"指标明细总数: {indicator_count}")
        
        if eval_count > 0:
            total_value = db.query(models.Evaluation).with_entities(
                db.func.sum(models.Evaluation.total_value)
            ).scalar() or 0
            print(f"总评估价值: {total_value}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    view_database()
