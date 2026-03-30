/**
 * 若 backend/.env 不存在，则从 backend/.env.example 复制一份，减少手动步骤。
 */
const fs = require('fs')
const path = require('path')

const root = path.join(__dirname, '..')
const src = path.join(root, 'backend', '.env.example')
const dst = path.join(root, 'backend', '.env')

if (!fs.existsSync(src)) {
  console.error('未找到 backend/.env.example，请确认仓库完整。')
  process.exit(1)
}
if (fs.existsSync(dst)) {
  console.log('backend/.env 已存在，未覆盖。如需重置请手动删除后再运行 npm run init-env')
  process.exit(0)
}
fs.copyFileSync(src, dst)
console.log('已生成 backend/.env，请用编辑器打开并填写 DB_PASSWORD 等 MySQL 配置。')
