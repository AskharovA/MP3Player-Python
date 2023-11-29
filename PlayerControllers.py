from customtkinter import CTkButton, CTkImage
from PIL import Image
from pygame import mixer
import time
from Songs import Song


class PlayerControllers:
    def init(self):
        self.play_button = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/play.png"),
                size=(20, 20)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.play,
            width=25
        )
        self.play_button.grid(row=0, column=2)

        self.stop_button = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/stop.png"),
                size=(20, 20)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.stop,
            width=25
        )
        self.stop_button.grid(row=0, column=3)

        self.prev_button = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/prev.png"),
                size=(15, 15)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.prev,
            width=25
        )
        self.prev_button.grid(row=0, column=0)

        self.back_btn = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/back.png"),
                size=(15, 15)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.back,
            width=25
        )
        self.back_btn.grid(row=0, column=1)

        self.next_btn = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/next.png"),
                size=(15, 15)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.next,
            width=25
        )
        self.next_btn.grid(row=0, column=5)

        self.forward_btn = CTkButton(
            self.controllers,
            image=CTkImage(
                Image.open("media/controllers/forward.png"),
                size=(15, 15)
            ),
            hover=False,
            fg_color="transparent",
            text="",
            command=self.forward,
            width=25
        )
        self.forward_btn.grid(row=0, column=4)

    def play(self, event=None, double_clicked=False):
        if self.player_is_stopped:
            self.reset_timeline()
        if self.current_playing_song and not double_clicked:
            if self.player_is_paused:
                mixer.music.unpause()
                self.play_button.configure(image=self.pause_btn_image)
                self.player_is_paused = False
                return
            mixer.music.pause()
            self.player_is_paused = True
            self.play_button.configure(image=self.play_btn_image)
            return
        if self.song_box.size() > 0:
            if not self.song_box.curselection():
                self.song_box.activate(0)
            song: Song = self.playlist.get_song(self.song_box.get())
            mixer.music.load(song.path)
            mixer.music.play()
            self.current_playing_song: Song = song
            self.main_slider.configure(to=song.length)
            self.player_is_stopped = False
            self.playing_song_index = self.song_box.curselection()
            self.show_playing_song_name()
            self.show_album_art()
            song_length_time = time.strftime(
                '%M:%S',
                time.gmtime(self.current_playing_song.length)
            )
            self.total_song_length_info.configure(text=song_length_time)
            self.play_button.configure(image=self.pause_btn_image)

    def stop(self, next_=False):
        if self.current_playing_song:
            mixer.music.stop()
            self.reset_timeline()
            self.current_playing_song = None
            self.player_is_stopped = True
            self.play_button.configure(image=self.play_btn_image)
            self.playing_song_name.configure(text="")
            self.album_frame_image.configure(image=self.DEFAULT_ALBUM_IMG)
            if not next_:
                self.playing_song_index = -1

    def next(self, event=None):
        if self.song_box.size() - 1 > self.playing_song_index:
            self.stop(next_=True)
            idx = self.playing_song_index + 1
            self.song_box.activate(idx)
            self.play()

    def prev(self, event=None):  # TODO
        if self.playing_song_index > 0:
            self.stop(next_=True)
            idx = self.playing_song_index - 1
            self.song_box.activate(idx)
            self.play()

    def forward(self, event=None):  # TODO
        if not self.player_is_stopped:
            self.main_slider.set(self.main_slider.get() + 5)
            self.timeline_slide()

    def back(self, event=None):  # TODO
        if not self.player_is_stopped:
            self.main_slider.set(self.main_slider.get() - 5)
            self.timeline_slide()
