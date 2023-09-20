# [Degrees of Lewdity][dol] 模组编写小助手

## 简介
由于原游戏引擎面向字符串编程的特性，以及变量文本硬编码的困难，编写模组十分困难，因此简单十分钟手搓一个帮助编写模组的小脚本。

## 食用方法
注意：由于 `main.py` 中的 `mod.cover_source_files()` 方法会覆盖游戏源文件，因此推荐注释掉此行，自行备份好源文件后手动覆盖游戏源文件。

1. 需要 Python 3.10+
2. 在根目录使用 `pip install -r requirements.txt` 安装依赖库
3. 需要 `https://gitgud.io/Vrelnir/degrees-of-lewdity` 游戏源码，请自行下载，默认将 `degrees-of-lewdity-master` 放在根目录下
4. 编写你自己的模组
5. 运行 `main.py` (`python -m main`)
6. 结果会生成在 `results` 文件夹中，接下来请使用 `https://github.com/Lyoko-Jeremie/sugarcube-2-ModLoader` 进行下一步操作
- 注：如果需要频繁改动测试，随改随测，请在 `main.py` 中阅读对应注释操作

## 编写自己模组的注意事项
### 名词解释 ###

- __“段落”__
  - 在 .twee 文件中形如 `:: PASSAGE_NAME [WIDGET]` 的内容为段落的开头，从此开始一直到下一个段落开头均为此段落的内容

### 注意事项 ###
1. 请在 `<根目录>/mods/<模组名或作者名>` 文件夹下编写你的模组，或者将你正在编写的模组文件夹按照下方结构放进 `<根目录>/mods` 文件夹中
2. 请尽量在英文源码的基础上编写模组，因为汉化版仍在润色以及修复可能存在的问题，因此如果基于汉化版原版制作模组可能出现今天做的模组明天就和游戏内容对不上的问题。基于英文源码制作模组，覆盖原文件后仍然可以覆写汉化。
   * 注：基于英文源码制作模组指的是当出现改动源码内容时请复制英文版源码的内容后改动，而不是说要用英文写模组。
3. 本项目文件夹结构应该类似于：
```text
<根目录>
├── data
├── degrees-of-lewdity-master
├── mods
│   └── Number_Sir
│       ├── info.json <这个文件是必需的>
│       ├── img
│       │   └── <这里放图片，css 代码等，参照原游戏目录>
│       ├── game
│       │   └── <这里放 twee 和 js 代码，参照原游戏目录>
│       └── modules
│          └── css
│              └── <这里面放 css, js 等文件，参照原游戏目录>
├── results
└── src
```
注意 `img`, `game`, `css` 三个文件夹并不是都必需的，比如你只想做类似美化的模组，就可以只有 `img` 文件夹，等等。

请在 `info.json` 文件中填写以下信息：
```json
{
  "name": "<这个模组的名称>",
  "version": "<这个模组的版本>"
}
```

请遵循以下格式：
   1. 对于完全新建、自创的内容，请注意不要和原游戏内容重名，比如：
      * 图片命名、路径不要和原游戏内容重复
      * `.twee`, `.js`, `.css` 文件命名不要和原游戏内容重复
      * `.twee` 文件中的段落名不要和原游戏有的重复

   2. 对于想覆盖原游戏的已有的内容：
      * 图片命名、路径请和原游戏文件夹中的完全一致
      * `.twee` 中的段落，请把原游戏中的整段内容(从 `:: PASSAGE_NAME` 开始到下一个 `:: PASSAGE_NAME` 的上一行结束)全部复制出来到你的文件中，然后进行改动
      * `.js`, `.css` 命名、路径请和原游戏文件夹中的完全一致
      * __不推荐图片、js、css 文件覆盖原游戏内容，请尽量创建新的图片、js、css 文件。__

   3. 注意你写在自己模组内容中的所有段落都应该是相比于源代码中有所改动的，如果你复制了一个段落出来但没有做改动，记得把它删掉。

## 对于自己模组仓库的建议
如果希望创建自己的模组仓库并上传文件，建议如下：
1. 建议按照上述注意事项中 `mods` 文件夹结构创建仓库目录结构，即你的仓库目录应该形如：
      ```text
      <根目录>
      ├── .gitignore
      ├── Number_Sir
      │   ├── info.json <这个文件是必需的>
      │   ├── img
      │   │   └── <这里放图片，css 代码等，参照原游戏目录>
      │   ├── game
      │   │   └── <这里放 twee 和 js 代码，参照原游戏目录>
      │   └── modules
      │      └── css
      │          └── <这里面放 css, js 等文件，参照原游戏目录>
      ├── README.md
      ...
      ```
2. 建议尽量少改动原游戏已有的段落，多新增段落，以减少可能存在的bug、未来更新时可能有的麻烦以及未来可能有的多模组兼容性问题

[dol]: https://gitgud.io/Vrelnir/degrees-of-lewdity