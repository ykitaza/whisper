from typing import List
from yt_dlp import YoutubeDL
from pathlib import Path
import whisper
import ffmpeg
import subprocess
from pathlib import Path

class YoutubeDownloader:
    def __init__(self, output_path: str):
        self.output_path = self.prepare_directory(output_path)
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.output_path + '/%(title)s.%(ext)s',
            'quiet': True,
        }

    def prepare_directory(self, output_path: str):
        output_path = str(Path(output_path))
        Path(output_path).mkdir(parents=True, exist_ok=True)
        return output_path

    def download(self, *urls: str):
        for url in urls:
            video_info = self.get_video_info(url)
            print(f"Downloading: {video_info['title']}")
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])

    def get_video_info(self, video_url: str):
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
        return info_dict


class AudioConverter:
    def convert_to_wav(self, input_path: str, output_path: str):
        if Path(output_path).is_file():
            print(f"{output_path}はすでに存在します。上書き保存はしませんでした")
            return
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path)
            ffmpeg.run(stream)
        except ffmpeg.Error as e:
            print(f"エラーが発生しました：{e}")

class Transcriber:
    def transcribe(self, path: str):
        model = whisper.load_model("small")
        result = model.transcribe(path)
        return result

    def print_result(self, transcription_result):
        segments = transcription_result["segments"]
        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            print(f"Start: {start}, End: {end}, Text: {text}")
