# JM工具箱小程序 - 部署成功

**时间**: 2026-04-19 14:58 GMT+8
**目标**: 微信小程序「JM的工具箱」(wx92d88f2ddf8bad27) 自动部署

## 结果

✅ 部署成功！版本 1.0.13 已上传到微信后台体验版。

## 关键历程

1. **创建项目**: 全部源码从头创建，路径 `C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\jm-toolbox\`
2. **GitHub 仓库**: `jm6-lang/jm-toolbox`，49个文件
3. **部署方式**: GitHub Actions + miniprogram-ci JS API
4. **踩坑过程**:
   - `npx miniprogram-ci upload` 只输出版本号不执行（需用 JS API 而非 CLI）
   - CLI 参数名错误（`--private-key` 应为 `--private-key-path`）
   - JS API 需要先创建 `Project` 实例再传给 `upload()`
   - IP 白名单问题：GitHub Actions 用 Azure 动态 IP，每次不同（51.8.152.227 → 172.208.153.226），需关闭微信后台 IP 白名单

## 最终 deploy.yml 方案

```yaml
# 关键：用 miniprogram-ci JS API 而非 CLI
const { upload, Project } = require('miniprogram-ci');
const project = new Project({ appid, type, projectPath, privateKey, ignores });
upload({ project, version, desc });
```

## 私钥安全

- 私钥存储在 GitHub Secrets: `MINIPROGRAM_UPLOAD_PRIVATE_KEY`
- 原始文件: `C:\Users\Administrator\Desktop\新建文件夹\private.wx92d88f2ddf8bad27.key`
- 微信后台已关闭 IP 白名单限制

## 后续操作

- push 到 main 分支自动触发部署
- 版本号格式: `1.0.{github.run_number}`
