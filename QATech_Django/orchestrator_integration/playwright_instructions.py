"""
Playwright 脚本生成指令

用于 Agent Loop 模式下的自动化脚本生成任务。
"""

PLAYWRIGHT_SCRIPT_INSTRUCTION = """

## 【强制要求】自动化脚本生成

**重要：本次任务必须在执行完所有测试步骤后，生成并保存 Playwright 脚本！这是强制要求，不可跳过！**

### 任务流程（必须按顺序完成）
1. ✅ 执行所有测试步骤（使用 Playwright MCP 工具）
2. ✅ 为每个步骤截图并上传
3. ⚠️ **【必须】生成 Playwright Python 脚本**（根据执行过程）
4. ⚠️ **【必须】调用 `save_playwright_script` 保存脚本**
5. ✅ 返回测试结果 JSON

**如果没有调用 `save_playwright_script` 保存脚本，本次任务视为未完成！**

## 自动化脚本管理工具

你可以使用以下工具管理自动化脚本：

### 可用工具列表
- `save_playwright_script(script_content, test_case_id, description)` - 保存新的 Playwright 脚本
- `list_playwright_scripts(test_case_id, keyword, limit)` - 列出脚本列表
- `get_playwright_script(script_id)` - 获取脚本详情和代码
- `update_playwright_script(script_id, script_content, description)` - 更新已有脚本
- `execute_playwright_script(script_id, headless, record_video)` - 执行脚本
- `get_script_execution_result(execution_id, script_id)` - 获取执行结果

### 执行流程
1. **执行测试步骤**：使用 Playwright MCP 工具执行测试用例中的所有步骤
2. **生成脚本**：所有步骤执行完成后，根据执行过程生成完整的 Playwright Python 脚本
3. **保存脚本**：调用 `save_playwright_script` 工具保存脚本

### 脚本要求
生成的脚本必须是**标准的自动化测试脚本**，包含：
- `from playwright.sync_api import sync_playwright, expect` 导入
- `run()` 函数定义
- 所有测试步骤对应的 Playwright Python 代码
- 使用准确的选择器（根据实际执行时使用的选择器）
- 适当的错误处理（try/finally 确保浏览器关闭）
- **每个关键步骤后添加截图**（用于执行报告）
- **适当的 print 输出**（记录执行进度）
- **断言验证**（验证每个操作的预期结果）
- 脚本必须是 **Python** 语法，不是 JavaScript
- 使用 `page.get_by_role()`, `page.locator()` 等方法
- 在所有测试步骤执行完成后再生成脚本
- **禁止在脚本中使用 emoji 字符**（如 ✅ ❌ 等），使用纯文本描述
- **每个步骤后必须截图**，截图文件名格式: `step{N}_{action}.png`
- **每个步骤后必须 print**，输出格式: `步骤{N}: {描述}成功`
- **关键操作必须有断言**，验证操作的预期结果
- **生成后必须执行脚本，验证脚本的可执行性

### 断言示例
使用 Playwright 的 `expect` API 进行断言：
- `expect(page).to_have_url("...")` - 验证 URL
- `expect(page).to_have_title("...")` - 验证标题
- `expect(page.locator("...")).to_be_visible()` - 验证元素可见
- `expect(page.locator("...")).to_have_text("...")` - 验证文本内容
- `expect(page.locator("...")).to_have_count(n)` - 验证元素数量
- `expect(page.locator("...")).to_be_enabled()` - 验证元素可用

### 断言规则（非常重要）
1. **禁止猜测 URL**：断言中的 URL 必须使用执行步骤时**实际观察到的 URL**，不要自己编造或猜测
2. **禁止使用通配符模式**：不要使用 `**/dashboard` 这样的模式，必须使用完整的实际 URL
3. **断言必须来源于实际结果**：所有断言值（URL、标题、文本等）必须是执行过程中**实际看到的值**
4. **如果不确定实际值，使用 to_be_visible() 代替**：当无法确定元素的具体文本时，优先使用可见性断言

### 正确示例
```python
# 正确：使用实际执行时看到的完整 URL
expect(page).to_have_url("http://localhost:5173/project-management")

# 正确：使用实际看到的标题
expect(page).to_have_title("项目管理 - WHartTest")
```

### 错误示例（禁止这样做）
```python
# 错误：自己猜测的 URL
expect(page).to_have_url("https://example.com/dashboard")

# 错误：使用通配符模式
expect(page).to_have_url("**/dashboard")

# 错误：编造的标题
expect(page).to_have_title("Dashboard Page")
```

### 脚本模板（仅供参考结构，所有值必须替换为实际执行时观察到的值）
**重要：以下模板中的所有 URL、选择器、文本都是占位符示例，你必须替换为执行测试步骤时实际看到的值！**

```python
from playwright.sync_api import sync_playwright, expect


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.set_default_timeout(30000)

        step = 0

        try:
            # 步骤1: 打开页面
            step += 1
            # 【替换为实际URL】下面的URL必须是你执行goto时使用的真实URL
            page.goto("【替换为实际目标URL】")
            # 【替换为实际标题】下面的标题必须是页面打开后你实际看到的标题
            expect(page).to_have_title("【替换为实际页面标题】")
            print(f"步骤{step}: 打开页面成功")
            page.screenshot(path=f"step{step}_open_page.png")

            # 步骤2: 输入内容（示例）
            step += 1
            # 【替换为实际选择器】使用你执行fill操作时实际使用的选择器
            page.get_by_role("textbox", name="【替换为实际placeholder或label】").fill("【替换为实际输入值】")
            print(f"步骤{step}: 输入内容成功")
            page.screenshot(path=f"step{step}_input.png")

            # 步骤3: 点击按钮（示例）
            step += 1
            # 【替换为实际选择器】使用你执行click操作时实际使用的选择器
            page.get_by_role("button", name="【替换为实际按钮文本】").click()
            # 【替换为实际URL】如果点击后会跳转，使用实际跳转后的完整URL
            expect(page).to_have_url("【替换为跳转后的实际完整URL】")
            print(f"步骤{step}: 点击按钮成功")
            page.screenshot(path=f"step{step}_click.png")

            print(f"测试执行成功, 共执行 {step} 个步骤, 所有断言通过")
        except Exception as e:
            print(f"步骤{step}执行失败: {e}")
            page.screenshot(path="error_screenshot.png")
            raise
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    run()
```

### 重要提示
- 脚本必须是 **Python** 语法，不是 JavaScript
- 使用 `page.get_by_role()`, `page.locator()` 等方法
- 在所有测试步骤执行完成后再生成脚本
- **禁止在脚本中使用 emoji 字符**（如 ✅ ❌ 等），使用纯文本描述
- **每个步骤后必须截图**，截图文件名格式: `step{N}_{action}.png`
- **每个步骤后必须 print**，输出格式: `步骤{N}: {描述}成功`
- **关键操作必须有断言**，验证操作的预期结果
- **生成后必须执行脚本**，验证脚本的可执行性
- **禁止使用虚构的选择器**：如 `.welcome-message`、`#main-content` 等，必须使用执行时实际使用的选择器
- **禁止照抄模板占位符**：模板中的 `【替换为...】` 只是提示，必须替换为实际值


### Python Playwright 语法规范（非常重要）
**注意：Python 版本的 Playwright 与 JavaScript 版本语法不同！**

#### 定位器方法语法
Python 使用**关键字参数**，不是 JavaScript 的对象语法：

```python
# ✅ 正确的 Python 语法：使用关键字参数 name=
page.get_by_role("textbox", name="请输入用户名")
page.get_by_role("button", name="登录")
page.get_by_role("link", name="首页")

# ❌ 错误的 JavaScript 语法：不要使用 { } 对象
page.get_by_role('textbox', { 'name': '请输入用户名' })  # 错误！
page.get_by_role("button", { name: "登录" })  # 错误！
```

#### 其他定位器示例
```python
# 正确的 Python 语法
page.get_by_label("用户名")
page.get_by_placeholder("请输入密码")
page.get_by_text("欢迎")
page.get_by_test_id("submit-button")
page.locator("css=.button-class")
page.locator("xpath=//button[@id='submit']")
```

#### 错误处理
如果遇到定位器参数问题，请使用以下方式：
```python
# 方式1：使用 get_by_role + name 关键字参数
page.get_by_role("textbox", name="用户名").fill("admin")

# 方式2：使用 locator + CSS 选择器
page.locator("input[placeholder='用户名']").fill("admin")

# 方式3：使用 get_by_placeholder
page.get_by_placeholder("用户名").fill("admin")
```
"""
