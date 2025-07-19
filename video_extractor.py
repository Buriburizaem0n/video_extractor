#!/usr/bin/env python3
"""
series_extractor.py

递归扫描下载目录，识别电影和电视剧文件，分别提取到指定目录并创建软链接，而不移动原文件。
其他文件原地保留。

依赖：
  - guessit（pip install guessit）

用法：
  python series_extractor.py <downloads_root> [--movie-root MOVIE_DIR] [--series-root SERIES_DIR] [-n]

选项：
  --movie-root    电影目标根目录，默认 /mnt/external/movie
  --series-root   电视剧目标根目录，默认 /mnt/external/series
  -n, --dry-run   预演模式，只打印操作，不实际创建链接
"""
import os
import re
import argparse
from guessit import guessit

MEDIA_EXTENSIONS = re.compile(r'\.(mkv|mp4|avi|mov|ts|m4v)$', re.IGNORECASE)
EP_PATTERN = re.compile(r'(?:[sS](?P<season>\d{1,2})[eE](?P<episode>\d{1,2})|[eE](?P<ep_only>\d{1,2}))')

def sanitize(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def parse_episode(fname: str):
    m = EP_PATTERN.search(fname)
    if not m:
        return None, None
    if m.group('season') and m.group('episode'):
        return int(m.group('season')), int(m.group('episode'))
    return 1, int(m.group('ep_only'))

def process_file(fpath: str, movie_root: str, series_root: str, dry_run: bool):
    fname = os.path.basename(fpath)
    if not MEDIA_EXTENSIONS.search(fname):
        return
    info = guessit(fname)
    ftype = info.get('type')
    ext = info.get('container') or os.path.splitext(fname)[1].lstrip('.')

    if ftype == 'episode':
        season, episode = parse_episode(fname)
        if season is None or episode is None:
            return
        title = info.get('title') or 'Unknown'
        series_name = sanitize(title).title()
        season_folder = f"Season {season:02d}"
        dest_dir = os.path.join(series_root, series_name, season_folder)
        dest_fname = f"{series_name} - S{season:02d}E{episode:02d}.{ext}"
    elif ftype == 'movie':
        title = info.get('title') or 'Unknown'
        year = info.get('year')
        movie_name = sanitize(title).title()
        if year:
            dir_name = f"{movie_name} ({year})"
            dest_fname = f"{movie_name} ({year}).{ext}"
        else:
            dir_name = movie_name
            dest_fname = f"{movie_name}.{ext}"
        dest_dir = os.path.join(movie_root, dir_name)
    else:
        return

    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, dest_fname)
    if os.path.exists(dest_path):
        print(f"Skipping existing link: {dest_path}")
    else:
        print(f"Linking: {fpath} -> {dest_path}")
        if not dry_run:
            try:
                os.symlink(fpath, dest_path)
            except FileExistsError:
                pass

def main():
    parser = argparse.ArgumentParser(description='提取下载目录中的电影和电视剧并创建软链接')
    parser.add_argument('root', help='下载根目录路径')
    parser.add_argument('--movie-root', default='/mnt/external/movie', help='电影目标根目录')
    parser.add_argument('--series-root', default='/mnt/external/series', help='电视剧目标根目录')
    parser.add_argument('-n', '--dry-run', action='store_true', help='仅打印操作，不实际创建链接')
    args = parser.parse_args()

    for dirpath, _, filenames in os.walk(args.root):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            process_file(fpath, args.movie_root, args.series_root, args.dry_run)

if __name__ == '__main__':
    main()
