from dataclasses import dataclass
from typing import List
import json
import os

@dataclass
class musicinfoItem:
    id: str = ""
    uniqueId: int = 0
    genreNo: int = 0
    songFileName: str = ""
    papamama: bool = False
    branchEasy: bool = False
    branchNormal: bool = False
    branchHard: bool = False
    branchMania: bool = False
    branchUra: bool = False
    starEasy: int = 0
    starNormal: int = 0
    starHard: int = 0
    starMania: int = 0
    starUra: int = 0
    shinutiEasy: int = 0
    shinutiNormal: int = 0
    shinutiHard: int = 0
    shinutiMania: int = 0
    shinutiUra: int = 0
    shinutiEasyDuet: int = 0
    shinutiNormalDuet: int = 0
    shinutiHardDuet: int = 0
    shinutiManiaDuet: int = 0
    shinutiUraDuet: int = 0
    shinutiScoreEasy: int = 0
    shinutiScoreNormal: int = 0
    shinutiScoreHard: int = 0
    shinutiScoreMania: int = 0
    shinutiScoreUra: int = 0
    shinutiScoreEasyDuet: int = 0
    shinutiScoreNormalDuet: int = 0
    shinutiScoreHardDuet: int = 0
    shinutiScoreManiaDuet: int = 0
    shinutiScoreUraDuet: int = 0
    easyOnpuNum: int = 0
    normalOnpuNum: int = 0
    hardOnpuNum: int = 0
    maniaOnpuNum: int = 0
    uraOnpuNum: int = 0
    rendaTimeEasy: float = 0.0
    rendaTimeNormal: float = 0.0
    rendaTimeHard: float = 0.0
    rendaTimeMania: float = 0.0
    rendaTimeUra: float = 0.0
    fuusenTotalEasy: int = 0
    fuusenTotalNormal: int = 0
    fuusenTotalHard: int = 0
    fuusenTotalMania: int = 0
    fuusenTotalUra: int = 0

@dataclass
class WordlistItem:
    key: str = ""
    japaneseText: str = ""
    japaneseFontType: int = 0
    englishUsText: str = ""
    englishUsFontType: int = 0
    chineseTText: str = ""
    chineseTFontType: int = 0
    koreanText: str = ""
    koreanFontType: int = 0
    chineseSText: str = ""
    chineseSFontType: int = 0


class Datatable:
    filepath: str
    wordlist: List[WordlistItem]
    musicinfo: List[musicinfoItem]


    def __init__(self, filepath: str):
        self.filepath = filepath

        self.parse_musicinfo()
        self.parse_wordlist()

    def parse_musicinfo(self):
        with open(os.path.join(self.filepath, 'musicinfo.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = musicinfoItem().__dict__  # Use default values from the dataclass

        self.musicinfos = []
        # Convert the list of dictionaries to a list of musicinfoItem objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicinfoItem using the merged dictionary
                musicinfo_item = musicinfoItem(**full_item)
                self.musicinfos.append(musicinfo_item)
            except TypeError as e:
                print(f"Failed to create musicinfoItem from {item['id']}: {e}")

    def parse_wordlist(self):

        with open(os.path.join(self.filepath, 'wordlist.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = WordlistItem().__dict__

        self.wordlist = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                wordlist_item = WordlistItem(**full_item)
                self.wordlist.append(wordlist_item)
            except TypeError as e:
                print(f"Failed to create WordlistItem from {item}: {e}")




if __name__ == '__main__':
    dt = Datatable('C:\\Users\\knunes\\Downloads\\out\\KeifunsDatatableEditor\\datatable')
