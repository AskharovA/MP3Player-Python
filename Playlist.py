from Songs import Song


class Playlist:
    def __init__(self):
        self.name: str = ""
        self.songs_list: dict = {}
        self.size: int = 0

    def get_song(self, name: str):
        return self.songs_list[name]

    def add_song(self, song: Song):
        self.songs_list[song.name] = song
        self.size += 1

    def delete_song(self, name: str):
        del self.songs_list[name]
        self.size -= 1
