// Quote CSV fields and neutralize spreadsheet formulas in user-entered text.
export const csvCell = (value) => {
  let text = String(value ?? '')
  if (/^[\s]*[=+@-]/.test(text)) text = "'" + text
  return `"${text.replace(/"/g, '""')}"`
}

export async function copyText(text) {
  if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(text)
  const field = document.createElement('textarea')
  field.value = text
  field.style.position = 'fixed'
  field.style.opacity = '0'
  document.body.appendChild(field)
  field.select()
  try {
    if (!document.execCommand('copy')) throw new Error('浏览器不支持复制，请手动选择文本')
  } finally { field.remove() }
}
