"""Shared validation and ownership helpers for the active API."""
import json
from decimal import Decimal
from fastapi import HTTPException
from app.models.models import Evaluation

def owned_evaluation(db, eval_id, username):
    record = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
    if not record or (username != 'admin' and record.username != username):
        raise HTTPException(status_code=404, detail='评估不存在或无权访问')
    return record

def serialize_indicators(items):
    keys = [(i.category, i.item_name) for i in items]
    if len(set(keys)) != len(keys):
        raise HTTPException(status_code=422, detail='同一类别不能重复提交相同成本项')
    total = sum((i.amount for i in items), Decimal('0.00'))
    if total <= 0:
        raise HTTPException(status_code=422, detail='请至少填写一项正数成本')
    raw = [dict(category=i.category, item_name=i.item_name, amount=float(i.amount)) for i in items]
    payload = json.dumps(raw, ensure_ascii=False, separators=(',', ':'))
    if len(payload) > 5000:
        raise HTTPException(status_code=422, detail='指标数据超过存储长度，请减少成本项或缩短名称')
    return payload, float(total)
