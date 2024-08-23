from dataclasses import dataclass
from typing import List
import json
import os

@dataclass
class MusicinfoItem:
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
class MusicAttributeItem:
    id: str = ""
    uniqueId: int = 0
    new: bool = False
    canPlayUra: bool = False
    doublePlay: bool = False
    tag1: str = ""
    tag2: str = ""
    tag3: str = ""
    tag4: str = ""
    tag5: str = ""
    tag6: str = ""
    tag7: str = ""
    tag8: str = ""
    tag9: str = ""
    tag10: str = ""
    ensoPartsID1: int = 0 #TODO: If 0, don't write back into JSON
    ensoPartsID2: int = 0 #TODO: If 0, don't write back into JSON
    donBg1p: str = ""
    donBg2p: str = ""
    dancerDai: str = ""
    dancer: str = ""
    danceNormalBg: str = ""
    danceFeverBg: str = ""
    rendaEffect: str = ""
    fever: str = ""
    donBg1p1: str = ""
    donBg2p1: str = ""
    dancerDai1: str = ""
    dancer1: str = ""
    danceNormalBg1: str = ""
    danceFeverBg1: str = ""
    rendaEffect1: str = ""
    fever1: str = ""

@dataclass
class MusicOrderItem:
    genreNo: int = 0
    id: str = ""
    uniqueId: int = 0
    closeDispType: int = 0

@dataclass
class MusicAISectionItem:
    id: str = ""
    uniqueId: int = 0
    easy: int = 0
    normal: int = 0
    hard: int = 0
    oni: int = 0
    ura: int = 0
    oniLevel11: str = ""
    uraLevel11: str = ""

@dataclass
class MusicUsbsettingItem:
    id: str = ""
    uniqueId: int = 0
    usbVer: str = ""

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
    musicinfo: List[MusicinfoItem]
    musicAttribute: List[MusicAttributeItem]
    musicOrder: List[MusicOrderItem]
    musicAISection: List[MusicAISectionItem]
    musicUsbsetting: List[MusicUsbsettingItem]


    def __init__(self, filepath: str):
        self.filepath = filepath

        self.parse_musicinfo()
        self.parse_wordlist()
        self.parse_music_attribute()
        self.parse_music_order()
        self.parse_music_AI_section()
        self.parse_music_usbsetting()

    def parse_musicinfo(self):
        with open(os.path.join(self.filepath, 'musicinfo.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicinfoItem().__dict__  # Use default values from the dataclass

        self.musicinfos = []
        # Convert the list of dictionaries to a list of musicinfoItem objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicinfoItem using the merged dictionary
                musicinfo_item = MusicinfoItem(**full_item)
                self.musicinfos.append(musicinfo_item)
            except TypeError as e:
                print(f"Failed to create musicinfoItem from {item['id']}: {e}")

    def parse_music_attribute(self):
        with open(os.path.join(self.filepath, 'music_attribute.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAttributeItem().__dict__  # Use default values from the dataclass

        self.musicAttribute = []
        # Convert the list of dictionaries to a list of musicattributeItem objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicattributeItem using the merged dictionary
                music_attribute_item = MusicAttributeItem(**full_item)
                self.musicAttribute.append(music_attribute_item)
            except TypeError as e:
                print(f"Failed to create MusicAttributeItem from {item['id']}: {e}")

    def parse_music_order(self):
        with open(os.path.join(self.filepath, 'music_order.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicOrderItem().__dict__

        self.musicOrder = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_order_item = MusicOrderItem(**full_item)
                self.musicOrder.append(music_order_item)
            except TypeError as e:
                print(f"Failed to create MusicOrderItem from {item['id']}: {e}")
        
    def parse_music_AI_section(self):
        with open(os.path.join(self.filepath, 'music_ai_section.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAISectionItem().__dict__

        self.musicAISection = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_ai_section_item = MusicAISectionItem(**full_item)
                self.musicAISection.append(music_ai_section_item)
            except TypeError as e:
                print(f"Failed to create MusicAISectionItem from {item['id']}: {e}")

    def parse_music_usbsetting(self):
        with open(os.path.join(self.filepath, 'music_usbsetting.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicUsbsettingItem().__dict__

        self.musicUsbsetting = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_usbsetting_item = MusicUsbsettingItem(**full_item)
                self.musicUsbsetting.append(music_usbsetting_item)
            except TypeError as e:
                print(f"Failed to create MusicUsbsettingItem from {item['id']}: {e}")

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
                print(f"Failed to create WordlistItem from {item['id']}: {e}")




if __name__ == '__main__':
    dt = Datatable('C:\\Users\\knunes\\Downloads\\out\\KeifunsDatatableEditor\\datatable')
