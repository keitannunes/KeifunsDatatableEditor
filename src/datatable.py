from dataclasses import dataclass, fields, field
from typing import List, Dict
import json
import os

@dataclass
class Song:
    id: str = ""
    uniqueId: int = 0
    songNameList: List[str] = field(default_factory=lambda: ['', '', '', '', ''])
    songSubList: List[str] = field(default_factory=lambda: ['', '', '', '', ''])
    songDetailList: List[str] = field(default_factory=lambda: ['', '', '', '', ''])
    genreNo: int = 0
    songFileName: str = ""
    new: bool = False
    ura: bool = False
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
    shinutiScoreEasy: int = 0
    shinutiScoreNormal: int = 0
    shinutiScoreHard: int = 0
    shinutiScoreMania: int = 0
    shinutiScoreUra: int = 0
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
    aiEasy: int = 3
    aiNormal: int = 3
    aiHard: int = 3
    aiOni: int = 3
    aiUra: int = 3
    aiOniLevel11: str = ""
    aiUraLevel11: str = ""
    musicOrder: List[int] = field(default_factory=lambda: [0,-1,-1,-1,-1,-1,-1,-1])

@dataclass
class DatatableIndices:
    """For keeping track of where each song is"""
    wordlist_name: int
    wordlist_sub: int
    wordlist_detail: int
    musicinfo: int
    music_attribute: int
    music_ai_section: int
    music_usbsetting: int


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
    chineseSText: str = ""
    chineseSFontType: int = 0
    koreanText: str = ""
    koreanFontType: int = 0


class Datatable:
    filepath: str
    indices: Dict[str, DatatableIndices]
    wordlist: List[WordlistItem]
    musicinfo: List[MusicinfoItem]
    music_attribute: List[MusicAttributeItem]
    music_order: List[MusicOrderItem]
    music_ai_section: List[MusicAISectionItem]
    music_usb_setting: List[MusicUsbsettingItem]


    def __init__(self, filepath: str):
        self.filepath = filepath
        
        self.indices = dict()

        self.parse_musicinfo()
        self.parse_wordlist()
        self.parse_music_attribute()
        self.parse_music_order()
        self.parse_music_AI_section()
        self.parse_music_usbsetting()

    def get_indices(self, id: str) -> DatatableIndices:
        indices: DatatableIndices
        if id in self.indices:
            indices = self.indices[id]
        else:
            """Loop over datatable objects to find indices"""
            musicinfo_index = -1
            for i,e in enumerate(self.musicinfo):
                if e.id == id:
                    musicinfo_index = i
                    break
            
            if musicinfo_index == -1:
                raise Exception(f"song {id} not found")
            
            wordlist_name_index = -1
            wordlist_sub_index = -1
            wordlist_detail_index = -1
            for i,e in enumerate(self.wordlist):
                if e.key == f"song_{id}": #You can't use f strings in switch statement?
                    wordlist_name_index = i
                elif e.key == f"song_sub_{id}":
                    wordlist_sub_index = i
                elif e.key == f"song_detail_{id}":
                    wordlist_detail_index = i
                else:
                    continue #No point in checking if condition below if current element isn't a match
                if wordlist_detail_index != -1 and wordlist_sub_index != -1 and wordlist_name_index != -1:
                    break
            
            music_attribute_index = -1
            for i,e in enumerate(self.music_attribute):
                if e.id == id:
                    music_attribute_index = i
                    break
            
            music_ai_section_index = -1
            for i,e in enumerate(self.music_ai_section):
                if e.id == id:
                    music_ai_section_index = i
                    break

            music_usbsetting_index = -1
            for i,e in enumerate(self.music_usbsetting):
                if e.id == id:
                    music_usbsetting_index = i
                    break
            
            indices = DatatableIndices(
                wordlist_name_index,
                wordlist_sub_index,
                wordlist_detail_index,
                musicinfo_index,
                music_attribute_index,
                music_ai_section_index,
                music_usbsetting_index
            )

            for field in fields(indices):
                if getattr(indices, field.name) == -1:
                    raise Exception(f"Could not find {id} in {field.name[:field.name.index('index')-1]}") #-1 for underscore
            
            self.indices[id] = indices
        return indices

    def get_song_info(self, id: str) -> Song:
        
        indices = self.get_indices(id)

        wordlist_name_item = self.wordlist[indices.wordlist_name]
        wordlist_sub_item = self.wordlist[indices.wordlist_sub]
        wordlist_detail_item = self.wordlist[indices.wordlist_detail]
        musicinfo_item = self.musicinfo[indices.musicinfo]
        music_attribute_item = self.music_attribute[indices.music_attribute]
        music_ai_section_item = self.music_ai_section[indices.music_ai_section]
        
        return Song(
            id,
            musicinfo_item.uniqueId,
            [wordlist_name_item.japaneseText, wordlist_name_item.englishUsText, wordlist_name_item.chineseTText, wordlist_name_item.chineseSText, wordlist_name_item.koreanText],
            [wordlist_sub_item.japaneseText, wordlist_sub_item.englishUsText, wordlist_sub_item.chineseTText, wordlist_sub_item.chineseSText, wordlist_sub_item.koreanText],
            [wordlist_detail_item.japaneseText, wordlist_detail_item.englishUsText, wordlist_detail_item.chineseTText, wordlist_detail_item.chineseSText, wordlist_detail_item.koreanText],
            musicinfo_item.genreNo,
            musicinfo_item.songFileName,
            music_attribute_item.new,
            music_attribute_item.canPlayUra,
            musicinfo_item.branchEasy,
            musicinfo_item.branchNormal,
            musicinfo_item.branchHard,
            musicinfo_item.branchMania,
            musicinfo_item.branchUra,
            musicinfo_item.starEasy,
            musicinfo_item.starNormal,
            musicinfo_item.starHard,
            musicinfo_item.starMania,
            musicinfo_item.starUra,
            musicinfo_item.shinutiEasy,
            musicinfo_item.shinutiNormal,
            musicinfo_item.shinutiHard,
            musicinfo_item.shinutiMania,
            musicinfo_item.shinutiUra,
            musicinfo_item.shinutiScoreEasy,
            musicinfo_item.shinutiScoreNormal,
            musicinfo_item.shinutiScoreHard,
            musicinfo_item.shinutiScoreMania,
            musicinfo_item.shinutiScoreUra,
            musicinfo_item.easyOnpuNum,
            musicinfo_item.normalOnpuNum,
            musicinfo_item.hardOnpuNum,
            musicinfo_item.maniaOnpuNum,
            musicinfo_item.uraOnpuNum,
            musicinfo_item.rendaTimeEasy,
            musicinfo_item.rendaTimeNormal,
            musicinfo_item.rendaTimeHard,
            musicinfo_item.rendaTimeMania,
            musicinfo_item.rendaTimeUra,
            musicinfo_item.fuusenTotalEasy,
            musicinfo_item.fuusenTotalNormal,
            musicinfo_item.fuusenTotalHard,
            musicinfo_item.fuusenTotalMania,
            musicinfo_item.fuusenTotalUra,
            music_ai_section_item.easy,
            music_ai_section_item.normal,
            music_ai_section_item.hard,
            music_ai_section_item.oni,
            music_ai_section_item.ura,
            music_ai_section_item.oniLevel11,
            music_ai_section_item.uraLevel11,
            [] #TODO: musicorder
        )

    def parse_musicinfo(self):
        with open(os.path.join(self.filepath, 'musicinfo.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicinfoItem().__dict__  # Use default values from the dataclass

        self.musicinfo = []
        # Convert the list of dictionaries to a list of musicinfoItem objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicinfoItem using the merged dictionary
                musicinfo_item = MusicinfoItem(**full_item)
                self.musicinfo.append(musicinfo_item)
            except TypeError as e:
                print(f"Failed to create musicinfoItem from {item['id']}: {e}")

    def parse_music_attribute(self):
        with open(os.path.join(self.filepath, 'music_attribute.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAttributeItem().__dict__  # Use default values from the dataclass

        self.music_attribute = []
        # Convert the list of dictionaries to a list of musicattributeItem objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicattributeItem using the merged dictionary
                music_attribute_item = MusicAttributeItem(**full_item)
                self.music_attribute.append(music_attribute_item)
            except TypeError as e:
                print(f"Failed to create MusicAttributeItem from {item['id']}: {e}")

    def parse_music_order(self):
        with open(os.path.join(self.filepath, 'music_order.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicOrderItem().__dict__

        self.music_order = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_order_item = MusicOrderItem(**full_item)
                self.music_order.append(music_order_item)
            except TypeError as e:
                print(f"Failed to create MusicOrderItem from {item['id']}: {e}")
        
    def parse_music_AI_section(self):
        with open(os.path.join(self.filepath, 'music_ai_section.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAISectionItem().__dict__

        self.music_ai_section = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_ai_section_item = MusicAISectionItem(**full_item)
                self.music_ai_section.append(music_ai_section_item)
            except TypeError as e:
                print(f"Failed to create MusicAISectionItem from {item['id']}: {e}")

    def parse_music_usbsetting(self):
        with open(os.path.join(self.filepath, 'music_usbsetting.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicUsbsettingItem().__dict__

        self.music_usbsetting = []
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_usbsetting_item = MusicUsbsettingItem(**full_item)
                self.music_usbsetting.append(music_usbsetting_item)
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
    print(dt.get_song_info('id1297'))
