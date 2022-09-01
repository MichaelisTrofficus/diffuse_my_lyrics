from typing import List
import shutil
from huggingface_hub import notebook_login


def auth_hugging_face():
    notebook_login()


def parse_lyrics(path: str, prompt: str) -> List[str]:
    """
    Parses the lyrics plain file into a list of verses

    Args:
        path: The lyrics path
        prompt: Extra params

    Returns:
        A list of verses
    """
    with open(path) as f:
        verses = f.readlines()

    verses_clean = []
    for verse in verses:
        verse = verse.replace("\n", "")
        verse = verse.replace(".", "")
        if verse:
            verse += f" {prompt}"
            verses_clean.append(verse)
    return verses_clean


def zip_folder(folder_path: str, zip_path: str):
    shutil.make_archive(zip_path, 'zip', folder_path)
