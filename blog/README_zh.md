# Fan Blog (Mizuki Theme Edition)

这是一个基于 Django 框架开发的个人博客系统，集成了美观的 Mizuki UI 主题。本项目是《Python Crash Course》第19章练习项目的扩展版本，实现了完整的用户账户系统、文章管理以及现代化的前端展示效果。

## ✨ 特性 (Features)

*   **用户系统**：
    *   完整的用户注册、登录和注销流程。
    *   权限控制：只有注册用户可以发布文章。
    *   对象级权限：用户只能编辑属于自己的文章。
*   **博客管理**：
    *   文章发布、编辑和查看。
    *   支持 Markdown 格式（视具体实现而定）或纯文本。
    *   文章分类标签（Tags）支持。
    *   文章摘要与封面图支持。
*   **现代化 UI (Mizuki Theme)**：
    *   **动态横幅**：首页顶部带有打字机特效的动态横幅，展示欢迎语或精选文章。
    *   **响应式设计**：完美适配桌面端和移动端。
    *   **视觉特效**：包含毛玻璃导航栏、卡片悬浮效果、平滑滚动等。
    *   **视图切换**：支持列表视图和网格视图切换。
    *   **深色模式**：(如果已集成) 支持系统级或手动的深色模式切换。

## 🛠️ 技术栈 (Tech Stack)

*   **后端**：Python 3.x, Django 6.0
*   **数据库**：SQLite (默认), 可配置为 PostgreSQL/MySQL
*   **前端**：HTML5, CSS3 (Custom Properties), JavaScript (Vanilla)
*   **样式风格**：Mizuki UI (Custom CSS)

## 🚀 快速开始 (Quick Start)

### 1. 环境准备
确保你的系统中已安装 Python 3.10 或更高版本。

### 2. 克隆项目
```bash
git clone <repository-url>
cd blog
```

### 3. 创建虚拟环境
建议使用虚拟环境来管理依赖：
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 数据库迁移
初始化数据库表结构：
```bash
python manage.py migrate
```

### 6. 创建超级用户 (可选)
如果你需要访问 Django 管理后台：
```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器
```bash
python manage.py runserver
```
访问 `http://127.0.0.1:8000/` 即可看到博客主页。

## 📝 使用说明

1.  **注册/登录**：点击侧边栏或导航栏的 "Login/Register" 按钮进行登录。
2.  **发布文章**：登录后，点击侧边栏的 "New Post" 按钮进入发布页面。
3.  **编辑文章**：在文章详情页或列表中，点击编辑按钮（仅限作者本人可见）进行修改。
4.  **管理后台**：访问 `/admin/` 使用超级用户账号登录，可管理所有数据。

## 📄 许可证
本项目基于 MIT 许可证开源。
