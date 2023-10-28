import os
import sys

from urllib.error import URLError
from urllib.parse import urlparse
from argparse import ArgumentParser

import cmd2

from adiauthcli import Client
from src import BlobService, Visibility
from src import exceptions


__usage__ = f"Usage: python \"{__file__}\" [auth_api] [blobs_api]"

def _url(url: str) -> str:
    result = urlparse(url)
    if all([result.scheme, result.netloc]):
        return url
    raise URLError

login_parser = cmd2.Cmd2ArgumentParser()
login_parser.add_argument(
    "user",
    type=str)
login_parser.add_argument(
    "password",
    type=str)

new_parser = cmd2.Cmd2ArgumentParser()
new_parser.add_argument(
    "file",
    type=str)

upload_parser = cmd2.Cmd2ArgumentParser()
upload_parser.add_argument(
    "blob_id",
    type=str)
upload_parser.add_argument(
    "file",
    type=str)

needid_parser = cmd2.Cmd2ArgumentParser()
needid_parser.add_argument(
    "blob_id",
    type=str)

username_blobid_parser = cmd2.Cmd2ArgumentParser()
username_blobid_parser.add_argument(
    "username",
    type=str)
username_blobid_parser.add_argument(
    "blob_id",
    type=str)

visibility_parser = cmd2.Cmd2ArgumentParser()
visibility_parser.add_argument(
    "blob_id",
    type=str)
visibility_parser.add_argument(
    "visibility",
    type=str,
    choices=list(Visibility))

property_parser = cmd2.Cmd2ArgumentParser()
property_parser.add_argument(
    "blob_id",
    type=str)
property_parser.add_argument(
    "property",
    type=str,
    choices=["accessURL", "allowedUsers", "isPrivate"])

class APDICli(cmd2.Cmd):

    def __init__(self) -> None:
        super().__init__()

        self.blobsURL = os.getenv("BLOBS_URL")
        self.usersURL = os.getenv("AUTH_URL")

        self.user = Client(self.usersURL)
        self.blobService = BlobService(self.blobsURL)

        self.update_prompt()

    def do_exit(self, _) -> bool:
        return True

    @cmd2.with_argparser(login_parser)
    def do_login(self, args) -> None:
        user, password = args.user, args.password

        self.user.login(user, password)
        self.blobService = BlobService(self.blobsURL, self.user.auth_token)

        self.pfeedback(f"Logged in as {user}")

        self.update_prompt()

    @cmd2.with_argparser(new_parser)
    def do_new(self, args) -> None:
        file = args.file

        blob = self.blobService.createBlob(file)

        self.pfeedback(f"Created new blob with id: {blob.blobId}")

    def do_logout(self, _) -> None:
        self.user.logout()
        self.blobService = BlobService(self.blobsURL)

        self.pfeedback("Logged out")

        self.update_prompt()

    def do_blobs(self, _) -> None:
        blobs = self.blobService.getBlobs()

        self.pfeedback("\n".join([f"{i}. {blob_id}" for i, blob_id in enumerate(blobs, start=1)]))

    @cmd2.with_argparser(needid_parser)
    def do_download(self, args) -> None:
        blob_id = args.blob_id

        blob = self.blobService.getBlob(blob_id)
        blob.dumpToFile(f"{blob_id}.download")

        self.pfeedback(f'Downloaded blob to "{blob_id}.download"')

    @cmd2.with_argparser(upload_parser)
    def do_upload(self, args) -> None:
        blob_id, file = args.blob_id, args.file

        blob = self.blobService.getBlob(blob_id)

        try:
            blob.uploadFromFile(file)
        except FileNotFoundError:
            self.perror(f'File "{file}" not found')
            return

        self.pfeedback(f'Uploaded "{file}" to blob {blob_id}')

    @cmd2.with_argparser(needid_parser)
    def do_md5(self, args) -> None:
        blob_id = args.blob_id

        blob = self.blobService.getBlob(blob_id)

        self.pfeedback(blob.md5)

    @cmd2.with_argparser(needid_parser)
    def do_sha256(self, args) -> None:
        blob_id = args.blob_id

        blob = self.blobService.getBlob(blob_id)

        self.pfeedback(blob.sha256)

    @cmd2.with_argparser(visibility_parser)
    def do_visibility(self, arg) -> None:
        blob_id, visibility = arg.blob_id, arg.visibility

        blob = self.blobService.getBlob(blob_id)

        isPrivate = visibility == Visibility.PRIVATE.value
        blob.setVisibility(isPrivate)

        self.pfeedback(
            f'Visibility of blob {blob_id} set to {"private" if isPrivate else "public"}')

    @cmd2.with_argparser(username_blobid_parser)
    def do_allow(self, arg) -> None:
        username, blob_id = arg.username, arg.blob_id

        blob = self.blobService.getBlob(blob_id)
        blob.allowUser(username)

        self.pfeedback(f'User {username} can now access blob {blob_id}')

    @cmd2.with_argparser(username_blobid_parser)
    def do_revoke(self, args) -> None:
        username, blob_id = args.username, args.blob_id

        blob = self.blobService.getBlob(blob_id)
        blob.revokeUser(username)

        self.pfeedback(f'User {username} can no longer access blob {blob_id}')

    @cmd2.with_argparser(needid_parser)
    def do_delete(self, args) -> None:
        blob_id = args.blob_id

        blob = self.blobService.getBlob(blob_id)
        blob.delete()

        self.pfeedback(f'Deleted blob {blob_id}')

    @cmd2.with_argparser(property_parser)
    def do_property(self, args) -> None:
        blob_id, property_ = args.blob_id, args.property

        blob = self.blobService.getBlob(blob_id)

        value = getattr(blob, property_)

        self.pfeedback(value)

    def onecmd(self, statement: str, *args, **kwargs) -> bool:
        try:
            return super().onecmd(statement, *args, **kwargs)
        except exceptions.InvalidBlob:
            self.perror("Blob not found")
        except exceptions.Unauthorized:
            self.perror("Session expired. login again")
            self.user.logout()
        return False

    def update_prompt(self) -> None:
        username = self.user._user_ if self.user._user_ is not None else "anon"
        self.prompt = f"APDI@{username}:$ "

def _parse_args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "auth_api",
        type=_url)

    parser.add_argument(
        "blobs_api",
        type=_url)

    return parser.parse_args()

if __name__ == "__main__":
    try:
        args_ = _parse_args()
    except URLError:
        print(f"[!] Invalid URL.\n{__usage__}")
        sys.exit(1)

    _argv = [sys.argv[0]]
    sys.argv = _argv

    os.environ["AUTH_URL"] = args_.auth_api
    os.environ["BLOBS_URL"] = args_.blobs_api

    APDICli().cmdloop(r"""
  ____  ____  ___    ____        ____   _       ___   ____    _____
 /    ||    \|   \  |    |      |    \ | |     /   \ |    \  / ___/
|  o  ||  o  )    \  |  | _____ |  o  )| |    |     ||  o  )(   \_ 
|     ||   _/|  D  | |  ||     ||     || |___ |  O  ||     | \__  |
|  _  ||  |  |     | |  ||_____||  O  ||     ||     ||  O  | /  \ |
|  |  ||  |  |     | |  |       |     ||     ||     ||     | \    |
|__|__||__|  |_____||____|      |_____||_____| \___/ |_____|  \___|
                                                                   
""")
