# series_extractor

A Python script that recursively scans a download directory and extracts movies and TV series into separate target directories based on metadata, while leaving other files in place—ideal for organizing content before adding to Jellyfin or another media library.

## Features

- Recursively scan a specified download root for common video file extensions (`.mkv`, `.mp4`, `.avi`, `.mov`, `.ts`, `.m4v`).
- Use `guessit` to extract metadata and automatically identify:
  - **TV series** (`type='episode'`): parse season and episode numbers from `SxxEyy` or `Exx` patterns.
  - **Movies** (`type='movie'`): parse title and release year.
- **Extract and rename** files according to Jellyfin conventions:
  - TV series: move to `<series_root>/<Series Title>/Season XX/Series Title - SXXEYY.ext`
  - Movies: move to `<movie_root>/<Movie Title> (Year)/Movie Title (Year).ext` (if year is unavailable, `Movie Title.ext`)
- **Non-media files** remain in the original download location—no deletion or movement.
- Support custom target roots:
  - `--movie-root` (default: `/mnt/external/movie`)
  - `--series-root` (default: `/mnt/external/series`)
- Support dry-run mode (`-n` / `--dry-run`) to preview actions without making any changes.

## Requirements

- Python 3.6+
- `guessit` library:
  ```bash
  pip install guessit
  ```

## Installation & Setup

```bash
# Clone repository and cd into it
git clone https://github.com/Buriburizaem0n/video_extractor.git
cd video_extractor

# (Optional) Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
echo "guessit>=3.0.0" > requirements.txt
pip install -r requirements.txt
```

## Usage Examples

```bash
# Dry-run: preview without moving files
python series_extractor.py /path/to/downloads -n

# Actual extraction: specify movie and series targets
python series_extractor.py /path/to/downloads \
  --movie-root /mnt/external/movie \
  --series-root /mnt/external/series
```

### Sample Output

```
Moving: /downloads/Inception.2010.1080p.mkv -> /mnt/external/movie/Inception (2010)/Inception (2010).mkv
Moving: /downloads/This.is.Us.S01E01.mkv -> /mnt/external/series/This Is Us/Season 01/This Is Us - S01E01.mkv
Skipping non-media file: /downloads/readme.txt
```

## Acknowledgments

Special thanks to **GPT o4-mini-high** for the guidance and script design! 🎉
