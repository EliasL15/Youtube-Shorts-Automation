# Shorts Generator

A Python tool for splitting videos into clips, generating subtitles with Whisper, and combining them with game footage.

## Features

- **Split**: Divide videos into short clips (default: 5 clips, 45 seconds each).
- **Transcribe**: Generate subtitles using Whisper.
- **Overlay**: Add subtitles to video clips.
- **Combine**: Merge captioned clips with game footage in a 9:16 aspect ratio.

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

## Usage

1. **Process Video**: Place your video file in the project directory, update the `video_file` and `game_video` paths in `generate.py`, and run the script.
    ```bash
    python generate.py
    ```

2. **Customization**: Adjust video splitting, subtitle settings, or combination layouts in the script.

## Workflow

1. Split the video into short clips.
2. Extract audio and generate subtitles.
3. Overlay subtitles and combine with game footage.

## Requirements

- Python 3.7+
- [ImageMagick](https://imagemagick.org)

## License

Licensed under the MIT License. 

## Acknowledgements

- [MoviePy](https://zulko.github.io/moviepy/)
- [Whisper](https://github.com/openai/whisper)
