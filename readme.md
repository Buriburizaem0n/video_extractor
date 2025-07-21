# series_extractor

[English](https://github.com/Buriburizaem0n/video_extractor/blob/main/readme_en.md)
---
一个 Python 脚本，用于递归扫描下载目录，将电影和电视剧根据元数据自动提取到不同目标目录，其他文件原地保留，并对目标目录创建指向原始文件的软连接，方便后续添加到 Jellyfin 或其他媒体库。

## 功能

- 递归扫描指定下载根目录中的常见视频文件（`.mkv`, `.mp4`, `.avi`, `.mov`, `.ts`, `.m4v`）
- 使用 `guessit` 提取元数据，自动识别：
  - **电视剧**（`type='episode'`）：按 `SxxEyy` 或 `Exx` 模式解析季号/集号
  - **电影**（`type='movie'`）：解析片名和年份
- **提取并创建软连接**：
  - 电视剧：在 `<series_root>/<Series Title>/Season XX/` 下创建 `Series Title - SXXEYY.ext` 的软连接
  - 电影：在 `<movie_root>/<Movie Title> (Year)/`（若无年份，则为 `<Movie Title>/`）下创建 `Movie Title (Year).ext` 或 `Movie Title.ext` 的软连接
- **其他非媒体文件**保留在原下载目录，不做删除或移动
- 支持自定义目标根目录：
  - `--movie-root`（默认 `/mnt/external/movie`）
  - `--series-root`（默认 `/mnt/external/series`）
- 支持预演模式：`-n` / `--dry-run`，仅打印将执行的操作，不实际创建软连接

## 环境要求

- Python 3.6 及以上
- `guessit` 库：
  ```bash
  pip install guessit
  ```

## 安装与配置

```bash
# 克隆仓库并进入目录
git clone https://github.com/Buriburizaem0n/video_extractor.git
cd video_extractor

# 可选：创建并激活虚拟环境
python3 -m venv env
source env/bin/activate

# 安装依赖
echo "guessit>=3.0.0" > requirements.txt
pip install -r requirements.txt
```

## 使用示例

```bash
# 预演：仅打印操作，不实际创建链接
python series_extractor.py /path/to/downloads -n

# 正式执行：创建软连接到指定目录
python series_extractor.py /path/to/downloads \
  --movie-root /mnt/external/movie \
  --series-root /mnt/external/series
```

### 示例输出

```
Linking: /downloads/Inception.2010.1080p.mkv -> /mnt/external/movie/Inception (2010)/Inception (2010).mkv
Linking: /downloads/This.is.Us.S01E01.mkv -> /mnt/external/series/This Is Us/Season 01/This Is Us - S01E01.mkv
Skipping non-media file: /downloads/readme.txt
```

## 致谢

特别感谢 **GPT o4-mini-high** 的思路和脚本指导！ 🎉(因为3o额度用完了)
