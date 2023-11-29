from dataclasses import dataclass
from PIL import Image
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO


@dataclass
class Song:
    name: str
    path: str
    default_album_size = 350, 370

    def __post_init__(self):
        self.album = self.set_album()
        self.length = self.define_audio_length()

    def set_album(self) -> Image:
        audio = ID3(self.path)
        for k, v in audio.items():
            if "APIC" in k:
                art = v.data
                image = Image.open(BytesIO(art))
                # album_image = CTkImage(image, size=self.default_album_size)
                return image
        else:
            return self.get_default_art()

    def define_audio_length(self) -> int:
        audio_length = int(
            MP3(self.path).info.length)
        return audio_length

    def get_default_art(self) -> Image:
        # return CTkImage(
        #     Image.open("media/DEFAULT_ALBUM.png"), size=self.default_album_size)
        return Image.open("media/DEFAULT_ALBUM.png")