import cmd2

from src import User
from src import Visibility


class APDICli(cmd2.Cmd):

    def __init__(self) -> None:
        super().__init__()
        self.user = User()
        self.update_prompt()

    def do_exit(self, _) -> bool:
        return True

    def do_login(self, arg) -> None:
        self.user.login("test", "test")
        self.update_prompt()

    def do_logout(self, _) -> None:
        self.user.logout()
        self.user = User()
        self.update_prompt()

    def do_blobs(self, _) -> None:
        blobs = self.user.blobs
        self.poutput("\n".join([f"{i}. {blob_id}" for i, blob_id in enumerate(blobs, start=1)]))

    def do_download(self, arg) -> None:
        download_path = self.user.download(arg, f"{arg}.download")
        self.poutput(f'Downloaded blob to "{download_path}"')

    def do_upload(self, arg) -> None:
        blob_id, file = arg.split(" ")
        with open(file, "rb") as f:
            self.user.upload(blob_id, f)

    def do_hash(self, arg) -> None:
        blob_id, *types = arg.split(" ")
        buf = '\n'.join([f'{_type}: "{hash}"' for _type, hash in self.user.hash(blob_id, *types).items()])
        self.poutput(buf)

    def do_delete(self, arg) -> None:
        self.user.delete(arg)

    def do_new(self, arg) -> None:
        visibility, file = arg.split(" ")
        with open(file, "rb") as f:
            blob_id = self.user.new_blob(visibility=Visibility(visibility), content=f)
        self.poutput(f"Created new blob with id: {blob_id}")

    def update_prompt(self) -> None:
        username = self.user.username if self.user.username is not None else "anon"
        self.prompt = f"APDI@{username}:$ "

if __name__ == "__main__":
    APDICli().cmdloop(r"""
  ____  ____  ___    ____        ____   _       ___   ____    _____
 /    ||    \|   \  |    |      |    \ | |     /   \ |    \  / ___/
|  o  ||  o  )    \  |  | _____ |  o  )| |    |     ||  o  )(   \_ 
|     ||   _/|  D  | |  ||     ||     || |___ |  O  ||     | \__  |
|  _  ||  |  |     | |  ||_____||  O  ||     ||     ||  O  | /  \ |
|  |  ||  |  |     | |  |       |     ||     ||     ||     | \    |
|__|__||__|  |_____||____|      |_____||_____| \___/ |_____|  \___|
                                                                   
""")
