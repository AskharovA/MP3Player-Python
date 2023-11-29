from customtkinter import CTkFrame, CTkButton, CTkImage, CTkLabel
from PIL import Image
from pygame import mixer


class VolumeButtons:
    def init(self):
        self.volume_controllers_frame = CTkFrame(
            self,
            fg_color="transparent"
        )

        self.vl_up_btn = CTkButton(
            self.volume_controllers_frame,
            text="",
            image=CTkImage(Image.open("media/controllers/v_up.png")),
            width=18,
            height=15,
            fg_color="transparent",
            hover=False,
            command=self.volume_up
        )
        self.vl_up_btn.grid(row=0, column=0)

        self.vl_down_btn = CTkButton(
            self.volume_controllers_frame,
            text="",
            image=CTkImage(Image.open("media/controllers/v_down.png")),
            width=18,
            height=15,
            fg_color="transparent",
            hover=False,
            command=self.volume_down
        )
        self.vl_down_btn.grid(row=2, column=0)

        self.vl_text = CTkLabel(
            self.volume_controllers_frame,
            text="VOL",
            text_color=self.default_text_color,
            font=("Impact", 16)
        )
        self.vl_text.grid(row=1, column=0)

        self.volume_controllers_frame.place(x=746, y=340)

        self.volume_frame = CTkFrame(self, fg_color="transparent")

        self.volume_lvl = 10
        self.volume_buttons = []
        for i in range(11):
            vl_btn = CTkButton(
                self.volume_frame,
                width=18,
                height=9,
                corner_radius=1,
                fg_color=self.default_active_color,
                text="",
                command=lambda x=self.volume_lvl: self.set_volume(x),
                hover_color=self.default_hover_color
            )
            self.volume_lvl -= 1
            vl_btn.grid(row=i, column=0, pady=(5, 0))
            self.volume_buttons.append(vl_btn)

        self.volume_frame.place(x=755, y=170)

        self.set_volume(8)

    def set_volume(self, x):
        mixer.music.set_volume(x/10)
        self.reset_volume_buttons()
        for btn in self.volume_buttons[::-1][:x+1]:
            btn.configure(fg_color=self.default_active_color)

    def reset_volume_buttons(self):
        for button in self.volume_buttons:
            button.configure(fg_color=self.default_widgets_color)

    def volume_up(self, event=None):
        new_vol = mixer.music.get_volume()+0.1
        new_vol = (round(new_vol, 1))*10
        if new_vol > 10:
            return
        self.set_volume(int(new_vol))

    def volume_down(self, event=None):
        new_vol = mixer.music.get_volume() - 0.1

        new_vol = (round(new_vol, 1)) * 10
        if new_vol < 0:
            return
        self.set_volume(int(new_vol))