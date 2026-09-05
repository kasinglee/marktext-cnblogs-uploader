# MarkText 博客园图片上传器

将 MarkText 中的本地图片直接上传到博客园，并把图片 URL 返回给 [MarkText](https://github.com/marktext/marktext)。

当前版本：`v1.0.0`

## 功能

- 支持 MarkText 的 CLI Script 图片上传方式。
- 调用博客园 MetaWeblog `newMediaObject` 接口上传图片。
- 提供可直接使用的 `cnblog_uploader.exe`，也可以从 Python 源码构建。
- 只上传图片，不上传或修改文章内容。

## 快速开始

1. 从 [Releases](https://github.com/kasinglee/marktext-cnblogs-uploader/releases) 下载 `cnblog_uploader.exe`，并下载仓库中的已脱敏 `config.json`。
2. 按下方说明填写 `config.json`。
3. 在 MarkText 中选择该目录下的 `cnblog_uploader.exe`。

## 配置博客园

登录博客园后台的[设置页面](https://i.cnblogs.com/settings)，确认已经开启 **允许 MetaWeblog 博客客户端访问**，然后获取 MetaWeblog 信息。

| 配置项 | 填写内容 |
| --- | --- |
| `blog_url` | 页面底部的 MetaWeblog 访问地址，例如 `https://rpc.cnblogs.com/metaweblog/your-blog-name` |
| `blog_id` | MetaWeblog 地址最后一段，例如上例中的 `your-blog-name` |
| `username` | 页面显示的 MetaWeblog 登录名，不一定等于博客昵称 |
| `access_token` | 博客园生成的 MetaWeblog 访问令牌 |

示例：

```json
{
  "blog_url": "https://rpc.cnblogs.com/metaweblog/你的博客名",
  "blog_id": "你的博客名",
  "username": "你的 MetaWeblog 登录名",
  "access_token": "你的 MetaWeblog 访问令牌"
}
```

访问令牌可在博客园账号的[令牌设置页面](https://account.cnblogs.com/settings/tokens)查看或生成。不要把普通登录密码填入 `access_token`。

仓库中的 `config.json` 只包含脱敏占位内容。请在本地填写真实令牌，发布或提交代码前确认没有把真实令牌写入 Git 历史。

## 在 MarkText 中使用

打开 `文件 -> 偏好设置 -> 图片`，选择 `上传到云端 -> CLI 脚本`，脚本路径选择本目录中的 `cnblog_uploader.exe`。建议在文件选择器中使用 exe 的绝对路径。

MarkText 会把图片路径作为命令行参数传给程序；上传成功时程序只向标准输出打印图片 URL，供 MarkText 自动插入 Markdown。

## 命令行使用

直接上传一张图片：

```powershell
.\cnblog_uploader.exe "C:\path\to\image.png"
```

查看版本：

```powershell
.\cnblog_uploader.exe --version
```

源码运行时可以使用 `--config` 指定配置文件，也可以设置 `CNBLOG_CONFIG` 环境变量：

```powershell
python .\cnblog_uploader.py --config .\config.json "C:\path\to\image.png"
```

## 从源码构建

构建环境：Windows、Python 3.10 或更高版本、PowerShell 和 PyInstaller。

```powershell
python -m pip install pyinstaller
.\build.ps1
```

构建脚本会生成 `dist\cnblog_uploader.exe`，并将它复制到项目根目录覆盖旧版本。构建产物 `build`、`dist` 和 `*.spec` 不需要提交到仓库。

## 故障排查

- XML-RPC `401`：确认已开启 MetaWeblog 服务，并重新生成访问令牌。
- 找不到配置文件：确认 `config.json` 与 exe 位于同一目录，或使用 `--config` 指定路径。
- 图片上传失败：检查网络、图片路径和博客园接口地址。

## 版本

版本号定义在 `cnblog_uploader.py` 的 `VERSION` 常量中。发布新版本时请同步更新该常量和本 README 中的版本号，并在 GitHub 创建对应的 Release。
详细变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
