import json
import pathlib
import tkinter.filedialog as tf
import customtkinter as ctk
from pygame import mixer
import time
from CTkListbox import *
from PIL import Image
import webbrowser
from tkinterdnd2 import TkinterDnD, DND_ALL
from Songs import Song
from Playlist import Playlist
from YouTube import YouTubeDownload
from VolumeButtons import VolumeButtons
from PlayerControllers import PlayerControllers


class CTK(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


ctk.deactivate_automatic_dpi_awareness()

mixer.init()


class Player(CTK, PlayerControllers, VolumeButtons, Playlist, YouTubeDownload):
    playlist = Playlist()
    playing_song_index: int = -1
    player_is_paused: bool = False
    player_is_stopped: bool = True
    current_playing_song: any = None

    default_active_color = "#C1272D"
    default_widgets_color = "#333333"
    default_hover_color = "#C1272D"
    default_text_color = "gray80"

    app_buttons = []
    animate_pl: int = 0
    animate_other: int = 0

    play_btn_image = ctk.CTkImage(Image.open("media/controllers/play.png"), size=(20, 20))
    pause_btn_image = ctk.CTkImage(Image.open("media/controllers/pause.png"), size=(20, 20))
    app_logo = ctk.CTkImage(Image.open("media/logo.png"), size=(35, 35))

    export_pl = []

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("DarkPlayer")
        self.resizable(False, False)
        self.iconbitmap('media/favicon.ico')
        self.configure(fg_color="#1A1A1A")
        self._set_appearance_mode("dark")
        self.drop_target_register(DND_ALL)
        self.dnd_bind("<<Drop>>", self.add_song)
        self.app_logo_frame = ctk.CTkLabel(
            self,
            image=self.app_logo,
            fg_color="transparent",
            text=""
        )
        self.app_logo_frame.pack_propagate()
        self.app_logo_frame.place(x=750, y=115)

        self.song_box = CTkListbox(
            self,
            width=291,
            height=368,
            fg_color="#282121",
            border_width=0,
            text_color=self.default_text_color,
            font=("Impact", 14),
            select_color=self.default_active_color,
            hover_color=self.default_hover_color,
            scrollbar_button_hover_color=self.default_active_color
        )
        self.song_box.place(x=420, y=50)

        self.album_frame = ctk.CTkFrame(
            self,
            width=360,
            height=380,
            fg_color="#333333"
        )
        self.album_frame.pack_propagate(False)
        self.album_frame.place(x=35, y=50)

        self.top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.top_frame.place(y=12, x=38)

        self.github_button = ctk.CTkButton(
            self.top_frame,
            width=170,
            text="GitHub",
            command=self.open_github
        )
        self.ytb_button = ctk.CTkButton(
            self.top_frame,
            width=240,
            text="Download song from YouTube",
            command=self.youtube
        )
        self.settings_button = ctk.CTkButton(
            self.top_frame,
            width=126,
            text="Settings"
        )
        self.about_app_button = ctk.CTkButton(
            self.top_frame,
            width=121,
            text="About App",
            command=self.show_about,
        )
        self.app_buttons += [self.github_button,
                             self.ytb_button,
                             self.settings_button,
                             self.about_app_button]

        self.timeline = ctk.CTkFrame(self, fg_color="#1A1A1A")
        self.timeline.place(x=38, y=510)

        self.main_slider = ctk.CTkSlider(
            self.timeline,
            width=608,
            orientation=ctk.HORIZONTAL,
            from_=0,
            to=100,
            button_color=self.default_active_color,
            progress_color=self.default_active_color,
            button_hover_color="gray25",
            command=self.timeline_slide,
            height=3,
            button_length=0,
            fg_color=self.default_widgets_color
        )
        self.main_slider.grid(row=0, column=1, padx=10)
        self.main_slider.set(0)

        self.current_time_info = ctk.CTkLabel(
            self.timeline,
            text="00:00",
            text_color=self.default_text_color,
            font=("Impact", 15),
            width=50
        )
        self.current_time_info.pack_propagate(False)
        self.current_time_info.grid(row=0, column=0)

        self.total_song_length_info = ctk.CTkLabel(
            self.timeline,
            text="00:00",
            text_color=self.default_text_color,
            font=("Impact", 15),
            width=50
        )
        self.current_time_info.pack_propagate(False)
        self.total_song_length_info.grid(row=0, column=2)

        self.controllers = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.controllers.place(x=116, y=442)

        self.DEFAULT_ALBUM_IMG = ctk.CTkImage(
            Image.open("media/DEFAULT_ALBUM.png"),
            size=Song.default_album_size
        )

        self.album_frame_image = ctk.CTkLabel(
            self.album_frame,
            image=self.DEFAULT_ALBUM_IMG,
            text=""
        )
        self.album_frame_image.pack(expand=True)

        self.playing_song_name = ctk.CTkLabel(
            self,
            text="",
            font=("Impact", 14),
            text_color="gray75",
        )

        for number, button in enumerate(self.app_buttons):
            button.configure(
                height=23,
                text_color=self.default_text_color,
                fg_color=self.default_widgets_color,
                corner_radius=4,
                font=("Impact", 16),
                hover_color=self.default_hover_color
            )
            button.pack_propagate(False)
            button.grid(row=0, column=number, padx=(0, 10))
        self.ytb_button.configure(fg_color=self.default_active_color)

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.add_song_button = ctk.CTkButton(
            self.bottom_frame,
            width=142,
            height=23,
            text_color=self.default_text_color,
            text="Add songs",
            fg_color=self.default_widgets_color,
            hover_color=self.default_hover_color,
            font=("Impact", 16),
            command=self.add_song,
            corner_radius=4
        )
        self.add_song_button.pack_propagate(False)
        self.add_song_button.grid(row=0, column=0, padx=(0, 10))

        self.delete_song_button = ctk.CTkButton(
            self.bottom_frame,
            width=142,
            height=23,
            text_color=self.default_text_color,
            text="Delete song",
            fg_color=self.default_widgets_color,
            hover_color=self.default_hover_color,
            font=("Impact", 16),
            corner_radius=4,
            command=self.delete
        )
        self.delete_song_button.pack_propagate(False)
        self.delete_song_button.grid(row=0, column=1)

        self.add_playlist_button = ctk.CTkButton(
            self.bottom_frame,
            width=142,
            height=23,
            text_color=self.default_text_color,
            text="Load playlist",
            fg_color=self.default_widgets_color,
            hover_color=self.default_hover_color,
            font=("Impact", 16),
            corner_radius=4,
            command=self.load_playlist
        )
        self.add_playlist_button.pack_propagate(False)
        self.add_playlist_button.grid(row=1, column=0, pady=(10,), padx=(0, 10))

        self.save_playlist_button = ctk.CTkButton(
            self.bottom_frame,
            width=142,
            height=23,
            text_color=self.default_text_color,
            text="Save playlist",
            fg_color=self.default_widgets_color,
            hover_color=self.default_hover_color,
            font=("Impact", 16),
            corner_radius=4,
            command=self.save_playlist
        )
        self.save_playlist_button.pack_propagate(False)
        self.save_playlist_button.grid(row=1, column=1)

        self.bottom_frame.place(x=427, y=442)

        self.song_box.bind("<Double-1>", self.double_click_play)

        self.bind("<Right>", self.forward)
        self.bind("<Left>", self.back)
        self.bind("<Up>", self.volume_up)
        self.bind("<Down>", self.volume_down)
        self.bind("<space>", self.play)

        PlayerControllers.init(self)
        VolumeButtons.init(self)

    def add_song(self, event=None, youtube_: Song = False):
        if youtube_:
            self.playlist.add_song(song=youtube_)
            self.song_box.insert(ctk.END, youtube_.name)
            return
        if event:
            files = event.data.replace("{C:", "C:").replace(".mp3}", ".mp3")
            songs = files.replace(" C:", "||C:").split("||")
        else:
            songs = tf.askopenfilenames(
                initialdir='/',
                title='Choose songs',
                filetypes=(
                    ('mp3 files', '*.mp3'),
                )
            )
        for song in songs:
            directory, name = song.rsplit('/', 1)
            name = name[:-4]
            self.playlist.add_song(Song(
                path=f"{directory}/{name}.mp3",
                name=name
            ))
            self.song_box.insert(ctk.END, name)

    def timeline_slide(self, x=None):
        if not self.player_is_stopped:
            mixer.music.load(self.current_playing_song.path)
            mixer.music.play(loops=0, start=int(self.main_slider.get()))

    def play_time(self):
        if self.player_is_stopped or self.player_is_paused:
            pass
        else:
            next_time = self.main_slider.get() + 0.2
            self.main_slider.set(next_time)

            if self.main_slider.get() >= self.current_playing_song.length:
                if self.song_box.size() - 1 == self.playing_song_index:
                    self.stop()
                else:
                    self.next()

            current_time = time.strftime('%M:%S', time.gmtime(self.main_slider.get()))
            self.current_time_info.configure(text=current_time)

        self.after(200, self.play_time)

    def show_playing_song_name(self):
        self.playing_song_name.configure(
            text=("Playing now: " + self.current_playing_song.name)[:100]
        )
        self.playing_song_name.place(y=545, x=100)

    def show_album_art(self):
        art = ctk.CTkImage(self.current_playing_song.album, size=Song.default_album_size)
        self.album_frame_image.configure(
            image=art
        )

    def reset_timeline(self):
        self.main_slider.configure(to=10)
        self.main_slider.set(0)
        self.current_time_info.configure(text="00:00")
        self.total_song_length_info.configure(text="00:00")

    def show_about(self):  # TODO
        with open("data/about app.txt", encoding="utf-8") as file:
            text = file.read()
        top_window = ctk.CTkToplevel(
            self
        )
        top_window.wm_attributes("-topmost", True)
        top_window.title("About DarkPlayer")
        top_window.after(250, lambda: top_window.iconbitmap('media/favicon.ico'))
        top_frame = ctk.CTkScrollableFrame(
            top_window,
            width=780,
            height=600,
            scrollbar_button_hover_color=self.default_active_color
        )
        text_label = ctk.CTkLabel(
            top_frame,
            text_color=self.default_text_color,
            font=("Calibri", 18),
            text=text,
            wraplength=700,
            justify=ctk.LEFT
        )
        text_label.pack(padx=10, pady=10)
        top_frame.pack(expand=True)

    def double_click_play(self, event):
        if self.song_box.size() == 1 and not self.current_playing_song:
            self.reset_timeline()
            self.play(double_clicked=True)
            return
        if not self.current_playing_song:
            self.reset_timeline()
            self.play(double_clicked=True)
        if event in self.playlist.songs_list and event not in self.current_playing_song.name:
            self.reset_timeline()
            self.play(double_clicked=True)

    @staticmethod
    def open_github():  # TODO
        link = "https://github.com/AskharovA/MP3Player-Python"
        webbrowser.open_new(link)

    def delete(self):
        if self.song_box.curselection() == self.playing_song_index:
            return
        elif self.song_box.size() > 0:
            self.playlist.delete_song(self.song_box.get())
            self.song_box.delete(self.song_box.curselection())

    def save_playlist(self):
        window = ctk.CTkInputDialog(
            title="Save playlist",
            text="Введите название плейлиста",
            button_fg_color=self.default_active_color,
            button_hover_color=self.default_hover_color
        )
        window.after(250, lambda: window.iconbitmap('media/favicon.ico'))
        pl_name = window.get_input()
        if not pl_name:
            return
        self.export_playlist(name=pl_name)

    def load_playlist(self):  # FIXME
        playlists = self.get_saved_playlists()
        self.load_window = ctk.CTkToplevel()
        top_frame = ctk.CTkScrollableFrame(self.load_window, width=500, height=500)
        top_frame.pack()
        self.load_window.title("Load playlist")
        self.load_window.grab_set()
        self.load_window.wm_attributes("-topmost", True)
        self.load_window.after(250, lambda: self.load_window.iconbitmap('media/favicon.ico'))
        for pl in playlists:
            pl_btn = ctk.CTkButton(
                top_frame,
                text=pl,
                fg_color=self.default_widgets_color,
                border_color="gray15",
                border_width=2,
                corner_radius=5,
                hover_color=self.default_hover_color,
                font=("Calibri", 20),
                width=480,
                height=50,
                command=lambda plst=playlists[pl]: self.load_selected_playlist(plst)
            )
            pl_btn.pack(padx=10, pady=(5, ))

    def load_selected_playlist(self, pl):
        self.stop()
        self.playlist = Playlist()

        for elem in pl:
            song = Song(
                name=elem["name"],
                path=elem["path"]
            )
            self.playlist.add_song(song)

        self.export_pl = pl
        while self.song_box.size() != 0:
            self.song_box.delete(0)
        for song in self.playlist.songs_list.values():
            self.song_box.insert(ctk.END, song.name)
        self.load_window.destroy()

    def export_playlist(self, name: str):
        self.export_pl = []
        for song in self.playlist.songs_list.values():
            self.export_pl += [
                {
                    "name": song.name,
                    "path": song.path
                }
            ]

        self.name = name
        with open(f"data/saved_playlists/{name}.json", mode="w") as file:
            json.dump(self.export_pl, file)

    @staticmethod
    def get_saved_playlists() -> dict:
        pathlib.Path("data/saved_playlists").mkdir(parents=True, exist_ok=True)
        playlists = {}
        for elem in pathlib.Path('data/saved_playlists').iterdir():
            with open(elem.absolute(), "r", encoding="utf-8") as file:
                pl = json.load(file)
                playlists[elem.name.replace(".json", "")] = pl
        return playlists


if __name__ == '__main__':
    app = Player()
    app.play_time()
    app.mainloop()
