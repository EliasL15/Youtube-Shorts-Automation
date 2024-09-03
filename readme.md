# YouTube Shorts Generator

A Python tool for automating the download of YouTube videos, splitting them into clips, generating subtitles with Whisper, combining them with game footage, and uploading the final shorts to YouTube.

## Features

- **Download**: Fetch YouTube videos in high quality using `yt_dlp`.
- **Split**: Divide videos into short clips (default: 5 clips, 45 seconds each).
- **Transcribe**: Generate subtitles using Whisper.
- **Overlay**: Add subtitles to video clips.
- **Combine**: Merge captioned clips with game footage in a 9:16 aspect ratio.
- **Upload**: Automatically upload the shorts to YouTube.

## Installation

1. **Clone the Repo**
    ```bash
    git clone https://github.com/EliasL15/Youtube-Shorts-Automation.git
    cd youtube-shorts-generator
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    Ensure `ImageMagick` is installed and properly configured.

3. **Set Up API Credentials**
    - Place your Google service account credentials in the project directory.

## Usage

1. **Process Video**: Modify the `video_url` and `game_video` in `main.py` and run the script.
    ```bash
    python main.py
    ```

2. **Customization**: Adjust video splitting, subtitle settings, or combination layouts in the script.

## Workflow

1. Download and split the video.
2. Extract audio and generate subtitles.
3. Overlay subtitles and combine with game footage.
4. Upload the final videos to YouTube.

## Requirements

- Python 3.7+
- [ImageMagick](https://imagemagick.org)
- YouTube Data API v3 (Google Service Account)

## License

Licensed under the MIT License. 

## Acknowledgements

- [yt_dlp](https://github.com/yt-dlp/yt-dlp)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Whisper](https://github.com/openai/whisper)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
