# Mods for Degrees of Lewdity

下载见 releases。

## Eliminate Spaces / 消灭空格

尽量删除多出的空格。

### 原理

目前游戏中多出空格的原因：

- 有文字输出的 widget 内换行（`\n`）和缩进（`\t` 或空格）
- 无文字输出的 widget
- 正文中 `switch`、`if` 代码块内换行和缩进

故结合使用以下方法删去：

- 删去有文字输出的 widget 内的换行和缩进
- 在无文字输出的 widget 内使用 `<<silently>>`
- 根据实际显示删除正文内换行和缩进

### TODO

- `preload.js` 根据数据自动生成
