-- 为「我的评估」仅显示当前用户记录：给 evaluations 表增加 username 列
-- 若表已存在且没有该列，在 MySQL 或 Navicat 中执行下面两句（先选中你的数据库，如 healthdata_valuator）
-- 若已执行过或列已存在，请勿重复执行，否则会报“列已存在”

ALTER TABLE evaluations ADD COLUMN username VARCHAR(50) NULL DEFAULT NULL;
CREATE INDEX ix_evaluations_username ON evaluations (username);
