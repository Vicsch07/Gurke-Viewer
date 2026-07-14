from pathlib import Path

class GFile():

    def __init__(self, file_path: str, file_name: str, file_extension: str):
        self.FilePath = file_path
        self.FileName = file_name
        self.FileExtension = file_extension

        self.IsLoaded = False
        