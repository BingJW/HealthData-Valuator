import { readFile } from 'node:fs/promises'
import { test } from 'node:test'
import assert from 'node:assert/strict'
const source = await readFile(new URL('../src/utils/export.js', import.meta.url), 'utf8')
const { csvCell } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'))
test('CSV preserves text, commas, quotes and numeric zero', () => {
  assert.equal(csvCell('医院,"数据"'), '"医院,""数据"""')
  assert.equal(csvCell(0), '"0"')
  assert.equal(csvCell(null), '""')
})
test('CSV user-controlled spreadsheet formulas are neutralized', () => {
  for (const value of ['=1+1', '+SUM(A1)', '-1+2', '@SUM(A1)', '  =1+1', '\t=1+1']) {
    assert.equal(csvCell(value).startsWith('"\''), true)
  }
})
