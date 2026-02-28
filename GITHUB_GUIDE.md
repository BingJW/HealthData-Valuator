
##  团队协作与 GitHub 使用指南

为了确保代码不冲突、开发有序，请团队成员严格遵守以下规范。

### 1. 首次加入项目 (Clone)

在你的本地开发目录下，打开终端执行：

```bash
git clone https://github.com/BingJW/HealthData-Valuator.git
cd HealthData-Valuator

```

### 2. 开发工作流 (Daily Workflow)

在开始写代码前，请务必先拉取最新代码，防止冲突：

```bash
git pull origin main

```

### 3. 提交代码规范 (Commit & Push)

当你完成一个功能点（如：写好了一个接口或设计好了一个表单）后：

1. **查看状态**：确认你修改了哪些文件。
```bash
git status

```


2. **添加到暂存区**：
```bash
git add .

```


3. **本地提交**：**Commit Message 必须清晰**（参考下方格式）。
```bash
git commit -m "feat: 完成数据存储成本计算逻辑"

```


4. **推送到远程**：
```bash
git push origin main

```



### 4. Commit Message 命名规范

为了方便学姐回溯代码，请统一使用以下前缀：

* `feat:` 新功能 (Feature)
* `fix:` 修补 Bug
* `docs:` 文档修改 (Documentation)
* `style:` 格式变动（不影响代码逻辑的缩进、空格等）
* `refactor:` 重构（即不是新增功能，也不是修改 bug 的代码变动）

### 5. 冲突处理 (Conflict)

如果你在 `push` 时遇到报错，通常是因为别人先你一步改了同样的代码。

* **不要强推 (`-f`)！**
* 先 `git pull`，在本地解决冲突（IDE 中会提示冲突位置）。
* 解决后重新 `add`, `commit`, `push`。

---

### 温馨提示：

1. **小步快跑**：不要写了三天的代码才提交一次。建议每完成一个独立的小功能就提交一次，这样即使写错了也方便找回。
2. **环境隔离**：后端开发必须在 `venv` 虚拟环境下进行，严禁直接在全局环境安装包。
3. **接口先行**：前后端开发前，请先查阅 `backend/main.py` 中的 API 定义或 Apifox 文档。

---