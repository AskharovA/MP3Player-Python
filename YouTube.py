from customtkinter import CTkInputDialog
from CTkMessagebox import CTkMessagebox
from Songs import Song
from pytube import YouTube
from moviepy.editor import AudioFileClip


class YouTubeDownload:
    def youtube(self):
        try:
            dialog = CTkInputDialog(
                title="Загрузка с YouTube",
                text="Вставьте ссылку на ролик",
                button_fg_color=self.default_active_color,
                button_hover_color=self.default_hover_color
            )
            dialog.after(250, lambda: dialog.iconbitmap('media/favicon.ico'))
            link = dialog.get_input()
            if "&list" in link:
                link, _ = link.split("&list")
            yt = YouTube(link)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path="downloads\\temp\\")

            video_title = video.default_filename.replace(".mp4", "")
            video_file = "downloads/temp/" + video.default_filename
            audio_file = "downloads/" + video_title + ".mp3"

            self.mp4_to_mp3(video_file, audio_file)
            audio = Song(path=audio_file, name=audio_file.replace("downloads/", "")[:-4])

            self.add_song(youtube_=audio)
            return
        except Exception as e:
            print(e)
            CTkMessagebox(
                title="Ошибка загрузки",
                message="Не удалось загрузить видео.",
                icon="cancel",
                button_color=self.default_active_color,
                fg_color=self.default_widgets_color,
                text_color=self.default_text_color,
                font=("Impact", 16),
                button_hover_color=self.default_hover_color
            )

    @staticmethod
    def mp4_to_mp3(mp4, mp3):
        file_to_convert = AudioFileClip(mp4)
        file_to_convert.write_audiofile(mp3)
        file_to_convert.close()
