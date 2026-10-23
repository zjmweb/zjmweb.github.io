# Vicky / Jinman Zhang — 个人网站

第三版 Peach & Sky 视觉的多页面版本。无需安装依赖，无需数据库，适用于 GitHub Pages。现已按旧作品集精选四件作品，并加入真实项目画面与独立案例页。

## 本地打开

最方便：双击 `启动预览.cmd`，保留打开的窗口，在浏览器访问 http://127.0.0.1:8001 。关闭该窗口后，本地服务会停止，此时刷新会显示“连接被拒绝”；重新启动即可。若提示端口被占用，先访问该地址，已有预览可能正在运行。

1. VS Code → 文件 → 打开文件夹 → 选择整个 `vicky-portfolio` 文件夹。
2. 直接双击 `index.html`，或在 VS Code 用 Live Server 打开。
3. 也可在该文件夹终端运行 `python -m http.server 8000`，访问 http://localhost:8000 。

直接打开 HTML 时网页和导航正常运行；复制邮箱功能若受浏览器限制，可手动复制或点击发送邮件。字体联网加载，离线时使用系统备用字体。

## 页面

- `index.html`：Home，个人简介与精选内容入口
- `research.html`：Research，研究方向、两篇出版物及 DOI
- `portfolio.html`：Portfolio，作品筛选、可展开项目详情
- `cv.html`：CV，学历、技能、原始 PDF 下载
- `work.html`：Work，新东方工作与 CGTN 实习
- `student_work.py`：Work 页八个学生案例的署名、学校、介绍与展开图；图片位于 `assets/students/`
- `contact.html`：Contact，邮箱与复制地址
- `cultural-relics.html`：文物教育游戏案例
- `cowardice.html`：COWARDICE 交互装置案例
- `fontworld.html`：FontWorld 网站设计与开发案例
- `everlasting-feelings.html`：飞花令游戏补充案例
- `styles.css`：配色、字体、排版及手机适配
- `script.js`：手机菜单、作品筛选、复制邮箱
- `assets/`：本地 Figma 插图、图标、CV 文件

## 修改内容

简单修改可以直接编辑对应 HTML；不过 `build.py` 是页面的统一生成入口，`portfolio_content.py` 保存精选作品内容。建议长期在这两个文件修改后运行 `python build.py`，让共享导航、页脚和页面内容同步生成。脚本只使用 Python 标准库。图片尺寸记录在 `assets/projects/dimensions.json`。

改配色请编辑 `styles.css` 顶部的 `:root`。真实项目截图在 `assets/projects/`，来源与筛选理由见 `CURATION.md`。首页故事之门仍为概念插图。作品视频按点击后加载，同时有 YouTube 直接链接；离线可查看全部本地图片和文字。

## GitHub Pages 上线

1. 创建自己的公开 GitHub 仓库。
2. 把**此文件夹内的文件**上传到仓库根目录，确保根目录有 `index.html`。
3. Settings → Pages → Deploy from a branch → main → /(root) → Save。
4. 等发布完成，使用 GitHub 提供的网址查看。
5. 之后修改文件并提交，会触发更新。

路径均为相对路径，兼容用户主页和项目子目录。已包含 `.nojekyll`。独立域名购买后再绑定即可，目前没有填写任何虚构域名。

## 内容说明

网页使用原始 CV 及对话中确认的更新：Durham CS PhD、预计 2029 毕业、导师 Stuart James 与 Giles Gasper、新东方明星导师 2023–2026。未填写未经确认的博士入学年份。没有添加虚构实验室、成果或作品链接。

`assets/CV-Jinman-Zhang.pdf` 为原始上传版，仍含旧经历及个人联系方式。CV 页面明确注明版本差异；正式上线前建议换成更新过的公开版简历。新文件使用同名覆盖即可。网站目前只展示电子邮箱，没有将 CV 中的手机号直接放到网页。

Figma 插图已下载保存为本地 SVG，网站不依赖临时 Figma 资源网址。Google Fonts 为可选外部字体服务，有 Georgia / Arial 备用字体。
