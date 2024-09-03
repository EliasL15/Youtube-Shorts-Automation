import os
from moviepy.editor import VideoFileClip, clips_array
import moviepy.config as mpconfig
from PIL import Image
from pytube import YouTube
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import whisper
from google.oauth2 import service_account
from googleapiclient.discovery import build
import yt_dlp
import os
import moviepy.editor as mp
import whisper
from moviepy.video.tools.subtitles import SubtitlesClip
import moviepy.config as mpconfig
mpconfig.change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/magick"})

def download_video(video_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'downloaded_video.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return 'downloaded_video.mp4'

def split_video(video_file,type=""):
    shorts = []
    video = VideoFileClip(video_file)
    duration = video.duration
    num_clips = 5
    short_duration = 45  # Seconds

    # Calculate total duration in seconds
    total_duration = min(duration, num_clips * short_duration)

    for i in range(num_clips):
        start_time = i * short_duration
        end_time = min(start_time + short_duration, total_duration)
        short_clip = video.subclip(start_time, end_time)
        short_file = f'short_{type}{i+1}.mp4'
        short_clip.write_videofile(short_file, codec="libx264", fps=24, audio_codec="aac")
        shorts.append(short_file)
    
    return shorts

def extract_audio(video_file, audio_file):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)

# Transcribe audio to text using Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")  # Load the Whisper model
    result = model.transcribe(audio_file)
    return result['segments']

# Write subtitles to SRT file
def write_srt(segments, srt_file):
    with open(srt_file, 'w') as f:
        for i, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            if text:  # Only write non-empty subtitles
                f.write(f"{i + 1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def overlay_subtitles(video_file, srt_file, output_file):
    video = mp.VideoFileClip(video_file)
    
    # Read the subtitles from the SRT file
    with open(srt_file, 'r') as f:
        subtitle_lines = f.readlines()
    
    # Create a list of TextClip objects
    subtitles = []
    for i in range(0, len(subtitle_lines), 4):
        start_time = subtitle_lines[i + 1].split(' --> ')[0].strip()
        end_time = subtitle_lines[i + 1].split(' --> ')[1].strip()
        text = subtitle_lines[i + 2].strip()
        
        # Convert time format from '00:00:00,000' to seconds
        start_seconds = convert_srt_time_to_seconds(start_time)
        end_seconds = convert_srt_time_to_seconds(end_time)

        subtitle = mp.TextClip(text, fontsize=60, color='white',method = 'caption',size = video.size, align = "South")  # No bg_color

        subtitle = subtitle.set_duration(end_seconds - start_seconds)\
                           .set_position(('center', 'bottom'))\
                           .set_start(start_seconds)
        subtitles.append(subtitle)
    
    # Overlay the subtitles on the video
    final_video = mp.CompositeVideoClip([video] + subtitles)
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

def convert_srt_time_to_seconds(srt_time):
    """Convert SRT time format 'HH:MM:SS,mmm' to seconds."""
    hours, minutes, seconds = srt_time.replace(',', '.').split(':')
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


# Main function to generate and display subtitles
def generate_and_display_subtitles(video_file, output_file):
    audio_file = "extracted_audio.wav"
    srt_file = "subtitles.srt"
    
    extract_audio(video_file, audio_file)
    segments = transcribe_audio(audio_file)
    write_srt(segments, srt_file)

    overlay_subtitles(video_file, srt_file, output_file)

    # Clean up temporary files
    os.remove(audio_file)
    os.remove(srt_file)


def upload_shorts_to_youtube(shorts, credentials_file):
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    youtube = build('youtube', 'v3', credentials=credentials)

    for short in shorts:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": f"Short from {os.path.basename(short)}",
                    "description": "This is an auto-uploaded short.",
                    "tags": ["shorts"],
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False,
                }
            },
            media_body=short
        )
        response = request.execute()
        print(f"Uploaded {short} to YouTube: {response['id']}")

def create_combined_video(landscape_path, portrait_path, output_path):
    # Load the landscape and portrait videos
    landscape_clip = VideoFileClip(landscape_path)
    portrait_clip = VideoFileClip(portrait_path)

    # Resize the landscape video to fit the bottom half of the 9:16 aspect ratio
    landscape_height = 650
    landscape_clip = landscape_clip.resize(height=landscape_height)

    # Resize the portrait video to fit the top half of the 9:16 aspect ratio
    portrait_clip = portrait_clip.resize(height=1920 - landscape_height)

    # Create a new video with the portrait on top and landscape on the bottom
    final_video = clips_array([[landscape_clip], [portrait_clip]])

    # Set the audio of the final video to the audio of the landscape video
    final_video = final_video.set_audio(landscape_clip.audio)

    # Write the result to a file, ensuring the output is in 9:16 aspect ratio
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

    # Close the clips to free up resources
    landscape_clip.close()
    portrait_clip.close()
    final_video.close()


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=cEJOhcKVSDI"

    # Download video
    video_file = download_video(video_url)

    game_video = "minecraft_short.mp4"

    # Split video into shorts
    shorts = split_video(video_file)

    game_videos = split_video(game_video,"game")

    # Generate captions and overlay captions for each short
    captioned_shorts = []
    for i in range(len(shorts)):
        generate_and_display_subtitles(shorts[i], "captioned_" + shorts[i])
        create_combined_video("captioned_" + shorts[i], game_videos[i], "combined_" + shorts[i])

    for short in shorts:
        os.remove(short)

    for game in game_videos:
        os.remove(game)

    for captioned_short in captioned_shorts:
        os.remove(captioned_short)