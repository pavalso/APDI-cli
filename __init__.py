from src import User


if __name__ == "__main__":

    user = User()
    user.login("test", "test")

    #with open("C:/Users/71359204/Videos/juano_terrorista.mp4", "rb") as fp:
    #    blob = user.new_blob("public", fp)

    #print(blob.download("juano_terrorista.mp4"))

    #print(blob.download())
    blob = user.fetch_blob("TdujBWfESHDDBRYdRnG-Rajcxjsmml3lrlm9T3Fr")

    blob.download("juano_terrorista.mp4")

    #print(blob.md5)

    #blob.delete()
