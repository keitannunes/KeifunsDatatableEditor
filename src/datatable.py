from dataclasses import dataclass, fields, field
from typing import List, Dict
import json
import os
from src import encryption, config

from dataclasses import dataclass, field, asdict
from typing import List

"""
When adding a new attribute:
    1. If new file: 
        create dataclass, variable in class, parser function,
        add index attribute to indices class, add search function in get_indices(),
        *also double check if update_uid() is affected
    2. Add attribute to Song class
    3. Update get_song_info()
    4. Update set_song_info()
    5. Update export_datatable() (if new file)
"""
@dataclass
class Song:
    id: str = ""
    uniqueId: int = 0
    songNameList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 1), ('', 2), ('', 3)])
    songSubList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 1), ('', 2), ('', 3)])
    songDetailList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 1), ('', 2), ('', 3)])
    genreNo: int = 0
    songFileName: str = ""
    new: bool = False
    doublePlay: bool = False
    papamama: bool = False
    dancer: str = "000_default"
    branch: List[bool] = field(default_factory=lambda: [False, False, False, False, False])
    star: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_score: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_duet: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_score_duet: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    onpu_num: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    renda_time: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    fuusen_total: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    spike_on: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    music_ai_section: List[int] = field(default_factory=lambda: [5, 5, 5, 5, 5])
    aiOniLevel11: str = ""
    aiUraLevel11: str = ""
    musicOrder: List[tuple[int,int]] = field(default_factory=lambda: [(0,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0)])


@dataclass
class DatatableIndices:
    """For keeping track of where each song is"""
    wordlist_name: int = -1
    wordlist_sub: int = -1
    wordlist_detail: int = -1
    musicinfo: int = -1
    music_attribute: int = -1
    music_ai_section: int = -1
    music_usbsetting: int = -1

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
    spikeOnEasy: int = 0
    spikeOnNormal: int = 0
    spikeOnHard: int = 0
    spikeOnOni: int = 0
    spikeOnUra: int = 0


@dataclass
class MusicAttributeItem:
    id: str = ""
    uniqueId: int = 0
    new: bool = False
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
    ensoPartsID1: int = 0
    ensoPartsID2: int = 0
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
    easy: int = 5
    normal: int = 5
    hard: int = 5
    oni: int = 5
    ura: int = 5
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
    englishUsFontType: int = 1
    chineseTText: str = ""
    chineseTFontType: int = 2
    koreanText: str = ""
    koreanFontType: int = 3

class Datatable:
    """Datatable class"""
    filepath: str
    indices: Dict[str, DatatableIndices]
    uid_musicinfo_index_mapping: Dict[int, int]
    wordlist: List[WordlistItem]
    musicinfo: List[MusicinfoItem]
    music_attribute: List[MusicAttributeItem]
    music_order: List[List[MusicOrderItem]]
    music_ai_section: List[MusicAISectionItem]
    music_usbsetting: List[MusicUsbsettingItem]

    def __init__(self, import_path: str):
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datatable')
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        files_to_find = ['musicinfo.bin', 'wordlist.bin', 'music_attribute.bin', 'music_ai_section.bin', 'music_usbsetting.bin', 'music_order.bin']
        for path, subdirs, files in os.walk(import_path):
            for name in files:
                if name not in files_to_find:
                    continue
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    encryption.save_file(
                        file=full_path, #type: ignore
                        outdir=os.path.join(self.filepath, name),
                        encrypt=False
                    )
                files_to_find.remove(name)
        if len(files_to_find) > 0:
            raise Exception(f"Couldn't find: {files_to_find}")
        self.indices = dict()
        self.uid_musicinfo_index_mapping = dict()

        self.parse_musicinfo()
        self.parse_wordlist()
        self.parse_music_attribute()
        self.parse_music_order()
        self.parse_music_AI_section()
        self.parse_music_usbsetting()

    def create_default_item(self, field_name: str):
        if field_name == 'musicinfo':
            return MusicinfoItem()
        elif field_name == 'music_attribute':
            return MusicAttributeItem()
        elif field_name == 'music_ai_section':
            return MusicAISectionItem()
        elif field_name == 'music_usbsetting':
            return MusicUsbsettingItem()
        else:
            raise ValueError(f"Unknown field name: {field_name}")

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
                raise KeyError(f"song {id} not found")
            
            wordlist_name_index = -1
            wordlist_sub_index = -1
            wordlist_detail_index = -1
            for i,e in enumerate(self.wordlist):
                if e.key == f"song_{id}": #You can't use f strings in switch statement?
                    if wordlist_name_index == -1: wordlist_name_index = i
                elif e.key == f"song_sub_{id}":
                    if wordlist_sub_index == -1: wordlist_sub_index = i
                elif e.key == f"song_detail_{id}":
                    if wordlist_detail_index == -1: wordlist_detail_index = i
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
                    # Append a new element
                    if field.name.startswith('wordlist'):
                        new_index = len(self.wordlist)
                        self.wordlist.append(WordlistItem())
                    else:
                        new_index = len(getattr(self, field.name))
                        getattr(self, field.name).append(self.create_default_item(field.name))
                    setattr(indices, field.name, new_index)

            self.indices[id] = indices
        return indices

    def get_song_info(self, id: str) -> Song:
        
        indices = self.get_indices(id)
        print(indices)
        wordlist_name_item = self.wordlist[indices.wordlist_name]
        wordlist_sub_item = self.wordlist[indices.wordlist_sub]
        wordlist_detail_item = self.wordlist[indices.wordlist_detail]
        musicinfo_item = self.musicinfo[indices.musicinfo]
        music_attribute_item = self.music_attribute[indices.music_attribute]
        music_ai_section_item = self.music_ai_section[indices.music_ai_section]
        
        music_order_indices = [(-1,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0), (-1,0)]
        for genre_no, genre_list in enumerate(self.music_order):
            for i, e in enumerate(genre_list):
                if e.id == id:
                    music_order_indices[genre_no] = (i, e.closeDispType)
                    break 
        
        dancer = "000_default"
        for dancer_key, dancer_data in config.config.dancers.items():
            if (music_attribute_item.ensoPartsID1 == dancer_data['ensoPartsID1'] and 
                music_attribute_item.ensoPartsID2 == dancer_data['ensoPartsID2']):
                dancer = dancer_key
                break
    
        return Song(
            id= id,
            uniqueId= musicinfo_item.uniqueId,
            songNameList = [
                (wordlist_name_item.japaneseText, wordlist_name_item.japaneseFontType),
                (wordlist_name_item.englishUsText, wordlist_name_item.englishUsFontType),
                (wordlist_name_item.chineseTText, wordlist_name_item.chineseTFontType),
                (wordlist_name_item.koreanText, wordlist_name_item.koreanFontType)
            ],
            songSubList = [
                (wordlist_sub_item.japaneseText, wordlist_sub_item.japaneseFontType),
                (wordlist_sub_item.englishUsText, wordlist_sub_item.englishUsFontType),
                (wordlist_sub_item.chineseTText, wordlist_sub_item.chineseTFontType),
                (wordlist_sub_item.koreanText, wordlist_sub_item.koreanFontType)
            ],
            songDetailList = [
                (wordlist_detail_item.japaneseText, wordlist_detail_item.japaneseFontType),
                (wordlist_detail_item.englishUsText, wordlist_detail_item.englishUsFontType),
                (wordlist_detail_item.chineseTText, wordlist_detail_item.chineseTFontType),
                (wordlist_detail_item.koreanText, wordlist_detail_item.koreanFontType)
            ],
            genreNo= musicinfo_item.genreNo,
            songFileName= musicinfo_item.songFileName,
            new= music_attribute_item.new,
            doublePlay= music_attribute_item.doublePlay,
            papamama= musicinfo_item.papamama,
            dancer= dancer,
            branch = [
                musicinfo_item.branchEasy, 
                musicinfo_item.branchNormal, 
                musicinfo_item.branchHard, 
                musicinfo_item.branchMania, 
                musicinfo_item.branchUra
            ],
            star = [
                musicinfo_item.starEasy, 
                musicinfo_item.starNormal, 
                musicinfo_item.starHard, 
                musicinfo_item.starMania, 
                musicinfo_item.starUra
            ],
            shinuti = [
                musicinfo_item.shinutiEasy, 
                musicinfo_item.shinutiNormal, 
                musicinfo_item.shinutiHard, 
                musicinfo_item.shinutiMania, 
                musicinfo_item.shinutiUra
            ],
            shinuti_score = [
                musicinfo_item.shinutiScoreEasy, 
                musicinfo_item.shinutiScoreNormal, 
                musicinfo_item.shinutiScoreHard, 
                musicinfo_item.shinutiScoreMania, 
                musicinfo_item.shinutiScoreUra
            ],
            shinuti_duet = [
                musicinfo_item.shinutiEasyDuet, 
                musicinfo_item.shinutiNormalDuet, 
                musicinfo_item.shinutiHardDuet, 
                musicinfo_item.shinutiManiaDuet, 
                musicinfo_item.shinutiUraDuet
            ],
            shinuti_score_duet = [
                musicinfo_item.shinutiScoreEasyDuet, 
                musicinfo_item.shinutiScoreNormalDuet, 
                musicinfo_item.shinutiScoreHardDuet, 
                musicinfo_item.shinutiScoreManiaDuet, 
                musicinfo_item.shinutiScoreUraDuet
            ],
            
            onpu_num = [
                musicinfo_item.easyOnpuNum, 
                musicinfo_item.normalOnpuNum, 
                musicinfo_item.hardOnpuNum, 
                musicinfo_item.maniaOnpuNum, 
                musicinfo_item.uraOnpuNum
            ],
            renda_time = [
                musicinfo_item.rendaTimeEasy, 
                musicinfo_item.rendaTimeNormal, 
                musicinfo_item.rendaTimeHard, 
                musicinfo_item.rendaTimeMania, 
                musicinfo_item.rendaTimeUra
            ],
            fuusen_total = [
                musicinfo_item.fuusenTotalEasy, 
                musicinfo_item.fuusenTotalNormal, 
                musicinfo_item.fuusenTotalHard, 
                musicinfo_item.fuusenTotalMania, 
                musicinfo_item.fuusenTotalUra
            ],
            spike_on = [
                musicinfo_item.spikeOnEasy,
                musicinfo_item.spikeOnNormal,
                musicinfo_item.spikeOnHard,
                musicinfo_item.spikeOnOni,
                musicinfo_item.spikeOnUra
            ],
            music_ai_section = [
                music_ai_section_item.easy, 
                music_ai_section_item.normal, 
                music_ai_section_item.hard, 
                music_ai_section_item.oni, 
                music_ai_section_item.ura
            ],
            aiOniLevel11= music_ai_section_item.oniLevel11,
            aiUraLevel11= music_ai_section_item.uraLevel11,
            musicOrder= music_order_indices
        )
    
    def set_song_info(self, song_info: Song) -> None:
        indices: DatatableIndices
        try:
            indices = self.get_indices(song_info.id)
        except KeyError:
            #Set indices to length of each variable (index of appended item)
            indices = DatatableIndices(
                wordlist_name=len(self.wordlist),
                wordlist_sub=len(self.wordlist)+1,
                wordlist_detail=len(self.wordlist)+2,
                musicinfo=len(self.musicinfo),
                music_attribute=len(self.music_attribute),
                music_ai_section=len(self.music_ai_section),
                music_usbsetting=len(self.music_usbsetting)
            )
            self.indices[song_info.id] = indices

            #Append each item

            self.wordlist.append(WordlistItem(key=f'song_{song_info.id}'))
            self.wordlist.append(WordlistItem(key=f'song_sub_{song_info.id}'))
            self.wordlist.append(WordlistItem(key=f'song_detail_{song_info.id}'))
            self.musicinfo.append(MusicinfoItem(id=song_info.id, uniqueId=song_info.uniqueId))
            self.music_attribute.append(MusicAttributeItem(id=song_info.id, uniqueId=song_info.uniqueId))
            self.music_ai_section.append(MusicAISectionItem(id=song_info.id, uniqueId=song_info.uniqueId))
            self.music_usbsetting.append(MusicUsbsettingItem(id=song_info.id, uniqueId=song_info.uniqueId))

        languages = [
            ('japaneseText', 'japaneseFontType'),
            ('englishUsText', 'englishUsFontType'),
            ('chineseTText', 'chineseTFontType'),
            ('koreanText', 'koreanFontType')
        ]

        # Updating songNameList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songNameList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_name], text_attr, text)
            setattr(self.wordlist[indices.wordlist_name], font_attr, font_type)

        # Updating songSubList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songSubList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_sub], text_attr, text)
            setattr(self.wordlist[indices.wordlist_sub], font_attr, font_type)

        # Updating songDetailList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songDetailList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_detail], text_attr, text)
            setattr(self.wordlist[indices.wordlist_detail], font_attr, font_type)

        if song_info.uniqueId != self.musicinfo[indices.musicinfo].uniqueId:
            self.update_uid(self.musicinfo[indices.musicinfo].uniqueId, song_info.uniqueId)

        self.musicinfo[indices.musicinfo].genreNo = song_info.genreNo
        self.musicinfo[indices.musicinfo].songFileName = song_info.songFileName
        self.musicinfo[indices.musicinfo].papamama = song_info.papamama

        self.music_attribute[indices.music_attribute].new = song_info.new
        self.music_attribute[indices.music_attribute].doublePlay = song_info.doublePlay

        dancer_key = song_info.dancer 
        if dancer_key != "000_default":
            # Get the dancer data from the config
            if dancer_key in config.config.dancers:
                dancer_data = config.config.dancers[dancer_key]
            else:
                print(f"Dancer {dancer_key} not found in config.")
                return
            for field, value in dancer_data.items():
                if hasattr(self.music_attribute[indices.music_attribute], field):
                    setattr(self.music_attribute[indices.music_attribute], field, value)
                else:
                    raise Exception(f'MusicAttribute class has no attribute {field}. Check config.json')

        # For branch
        for i, attribute in enumerate(['branchEasy', 'branchNormal', 'branchHard', 'branchMania', 'branchUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.branch[i])

        # For star
        for i, attribute in enumerate(['starEasy', 'starNormal', 'starHard', 'starMania', 'starUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.star[i])

        # For shinuti
        for i, attribute in enumerate(['shinutiEasy', 'shinutiNormal', 'shinutiHard', 'shinutiMania', 'shinutiUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.shinuti[i])


        # For shinuti_score
        for i, attribute in enumerate(['shinutiScoreEasy', 'shinutiScoreNormal', 'shinutiScoreHard', 'shinutiScoreMania', 'shinutiScoreUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.shinuti_score[i])

        #For Duet
        for i, attribute in enumerate(['shinutiEasyDuet', 'shinutiNormalDuet', 'shinutiHardDuet', 'shinutiManiaDuet', 'shinutiUraDuet']):
            setattr(self.musicinfo[indices.musicinfo], attribute, (song_info.shinuti_duet)[i])

        for i, attribute in enumerate(['shinutiScoreEasyDuet', 'shinutiScoreNormalDuet', 'shinutiScoreHardDuet', 'shinutiScoreManiaDuet', 'shinutiScoreUraDuet']):
            setattr(self.musicinfo[indices.musicinfo], attribute, (song_info.shinuti_score_duet)[i])

        # For onpu_num
        for i, attribute in enumerate(['easyOnpuNum', 'normalOnpuNum', 'hardOnpuNum', 'maniaOnpuNum', 'uraOnpuNum']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.onpu_num[i])

        # For renda_time
        for i, attribute in enumerate(['rendaTimeEasy', 'rendaTimeNormal', 'rendaTimeHard', 'rendaTimeMania', 'rendaTimeUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.renda_time[i])

        # For fuusen_total
        for i, attribute in enumerate(['fuusenTotalEasy', 'fuusenTotalNormal', 'fuusenTotalHard', 'fuusenTotalMania', 'fuusenTotalUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.fuusen_total[i])
        
        # For spike_on
        for i, attribute in enumerate(['spikeOnEasy', 'spikeOnNormal', 'spikeOnHard', 'spikeOnOni', 'spikeOnUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.spike_on[i])
        
        #For ai section
        for i, attribute in enumerate(['easy', 'normal', 'hard', 'oni', 'ura']):
            setattr(self.music_ai_section[indices.music_ai_section], attribute, song_info.music_ai_section[i])
        
        self.music_ai_section[indices.music_ai_section].oniLevel11 = song_info.aiOniLevel11
        self.music_ai_section[indices.music_ai_section].uraLevel11 = song_info.aiUraLevel11

        ### Music Order

        #Delete from music order
        for genre_list in self.music_order:
            genre_list[:] = [item for item in genre_list if item.id != song_info.id]

        for genre_no, (new_position, close_disp_type) in enumerate(song_info.musicOrder):
            if new_position > -1:
                # Create a new MusicOrderItem for this genre if not already present
                song_item = MusicOrderItem(genreNo=genre_no, id=song_info.id, uniqueId=song_info.uniqueId, closeDispType=close_disp_type)
                
                # Insert into the genre list at the specified position
                genre_list = self.music_order[genre_no]
                if new_position >= len(genre_list):
                    # If the new position is beyond the current length of the list, append it
                    genre_list.append(song_item)
                else:
                    # Otherwise, insert at the specific position
                    genre_list.insert(new_position, song_item)

    def delete_song(self, id: str):
        indices = self.get_indices(id)

        # Create a list of (index, attribute) tuples for wordlist items
        wordlist_indices = [
            (indices.wordlist_name, 'wordlist_name'),
            (indices.wordlist_sub, 'wordlist_sub'),
            (indices.wordlist_detail, 'wordlist_detail')
        ]
        wordlist_indices_copy = wordlist_indices[:]
        # Sort by index in descending order
        wordlist_indices.sort(key=lambda x: x[0], reverse=True)

        # Delete wordlist items
        for index, attr in wordlist_indices:
            del self.wordlist[index]
            # Update indices for remaining deletions
            for i, (idx, a) in enumerate(wordlist_indices):
                if idx > index:
                    wordlist_indices[i] = (idx - 1, a)
            # Update the original indices
            setattr(indices, attr, index)

        # Delete other items
        del self.musicinfo[indices.musicinfo]
        del self.music_attribute[indices.music_attribute]
        del self.music_ai_section[indices.music_ai_section]
        del self.music_usbsetting[indices.music_usbsetting]

        # Update indices for all songs
        for song_id, song_indices in self.indices.items():
            if song_id != id:  # Skip the deleted song
                # Update wordlist indices
                for deleted_index, _ in wordlist_indices_copy:
                    for current_song_index, attr in zip([song_indices.wordlist_name, song_indices.wordlist_sub, song_indices.wordlist_detail], ["wordlist_name", "wordlist_sub", "wordlist_detail"]):
                        if current_song_index > deleted_index:
                            setattr(song_indices, attr, current_song_index - 1)

                # Update other indices
                if song_indices.musicinfo > indices.musicinfo:
                    song_indices.musicinfo -= 1
                if song_indices.music_attribute > indices.music_attribute:
                    song_indices.music_attribute -= 1
                if song_indices.music_ai_section > indices.music_ai_section:
                    song_indices.music_ai_section -= 1
                if song_indices.music_usbsetting > indices.music_usbsetting:
                    song_indices.music_usbsetting -= 1

        # Remove the deleted song's indices from the dictionary
        del self.indices[id]

        # Update uid_musicinfo_index_mapping
        updated_mapping = {}
        for uid, index in self.uid_musicinfo_index_mapping.items():
            if index == indices.musicinfo:
                continue  # Skip the deleted song
            elif index > indices.musicinfo:
                updated_mapping[uid] = index - 1
            else:
                updated_mapping[uid] = index
        self.uid_musicinfo_index_mapping = updated_mapping

        # Update music_order list
        for order in self.music_order:
            order[:] = [item for item in order if item.id != id]


    def is_song_id_taken(self, song_id: str) -> bool:
        if song_id in self.indices: return True
        for e in self.musicinfo:
            if e.id == song_id: return True
        return False

    def is_uid_taken(self, uniqueId: int) -> bool:
        if uniqueId in self.uid_musicinfo_index_mapping:
            return True
        for i, e in enumerate(self.musicinfo):
            if e.uniqueId == uniqueId: 
                self.uid_musicinfo_index_mapping[e.uniqueId] = i
                return True
        return False
    
    def update_uid(self, old_uniqueId: int, new_uniqueId: int) -> None: #snake and camel case in one variable name is a first
        """THIS FUNCTION ASSUMES NEW UNIQUE ID IS INDEED UNIQUE!!!!!"""
        if old_uniqueId not in self.uid_musicinfo_index_mapping:
            for i, e in enumerate(self.musicinfo):
                if e.uniqueId == old_uniqueId: 
                    self.uid_musicinfo_index_mapping[e.uniqueId] = i
                    break
        song_id = self.musicinfo[self.uid_musicinfo_index_mapping[old_uniqueId]].id
        indices = self.get_indices(song_id)

        self.musicinfo[self.uid_musicinfo_index_mapping[old_uniqueId]].uniqueId = new_uniqueId
        self.music_attribute[indices.music_attribute].uniqueId = new_uniqueId
        self.music_ai_section[indices.music_ai_section].uniqueId = new_uniqueId
        self.music_usbsetting[indices.music_usbsetting].uniqueId = new_uniqueId
        for l in self.music_order:
            for e in l:
                if e.uniqueId == old_uniqueId:
                    e.uniqueId = new_uniqueId
                    break

        self.uid_musicinfo_index_mapping[new_uniqueId] = self.uid_musicinfo_index_mapping[old_uniqueId]
        del self.uid_musicinfo_index_mapping[old_uniqueId]

    def parse_musicinfo(self) -> None:
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

    def parse_music_attribute(self) -> None:
        with open(os.path.join(self.filepath, 'music_attribute.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAttributeItem().__dict__  # Use default values from the dataclass

        self.music_attribute = []
        # Convert the list of dictionaries to a list of MusicAttributeItem objects
        for item in data_dict['items']:
            try:
                # Remove the 'canPlayUra' field if it exists
                if 'canPlayUra' in item:
                    del item['canPlayUra']
                if 'isNotCopyright' in item:
                    del item['isNotCopyright']

                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the MusicAttributeItem using the merged dictionary
                music_attribute_item = MusicAttributeItem(**full_item)
                self.music_attribute.append(music_attribute_item)
            except TypeError as e:
                print(f"Failed to create MusicAttributeItem from {item.get('id', 'Unknown')}: {e}")


    def parse_music_order(self) -> None:
        with open(os.path.join(self.filepath, 'music_order.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicOrderItem().__dict__

        self.music_order = [[] for _ in range(8)] 
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the MusicOrderItem using the merged dictionary
                music_order_item = MusicOrderItem(**full_item)

                # Append to the appropriate genre list based on genreNo
                genre_no = music_order_item.genreNo
                if 0 <= genre_no < len(self.music_order):
                    self.music_order[genre_no].append(music_order_item)
                else:
                    print(f"Invalid genreNo {genre_no} for item {music_order_item.id}")
            except TypeError as e:
                print(f"Failed to create MusicOrderItem from {item.get('id', 'unknown')}: {e}")

        
    def parse_music_AI_section(self) -> None:
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

    def parse_music_usbsetting(self) -> None:
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

    def parse_wordlist(self) -> None:
        with open(os.path.join(self.filepath, 'wordlist.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = WordlistItem().__dict__

        self.wordlist = []

        # Convert the list of dictionaries to a list of WordlistItem objects
        for item in data_dict['items']:
            try:
                # Remove 'chineseSText' and 'chineseSFontType' if they exist in the JSON data
                item.pop('chineseSText', None)
                item.pop('chineseSFontType', None)

                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the filtered dictionary
                wordlist_item = WordlistItem(**full_item)
                self.wordlist.append(wordlist_item)
            except TypeError as e:
                print(f"Failed to create WordlistItem from {item.get('id', 'unknown')}: {e}")

    def export_datatable(self, folder_path: str) -> None:
        items_list = []
        renda_time_fields = ['rendaTimeEasy', 'rendaTimeNormal', 'rendaTimeHard', 'rendaTimeMania', 'rendaTimeUra']

        for item in self.musicinfo:
            item_dict = asdict(item)
            
            # Check and cast each rendaTime field
            for field in renda_time_fields:
                if item_dict[field].is_integer():
                    item_dict[field] = int(item_dict[field])
        
            items_list.append(item_dict)
        data_dict = {"items": items_list}

        # Write the dictionary to a JSON file
        with open(os.path.join(folder_path, 'musicinfo.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))
        
        # Export wordlist
        items_list = [asdict(item) for item in self.wordlist]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'wordlist.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_attribute
        items_list = [asdict(item) for item in self.music_attribute]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_attribute.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_ai_section
        items_list = [asdict(item) for item in self.music_ai_section]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_ai_section.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_usbsetting
        items_list = [asdict(item) for item in self.music_usbsetting]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_usbsetting.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))
        
        # Flatten the list of lists for music_order
        flattened_music_order = [item for sublist in self.music_order for item in sublist]

        # Convert to list of dictionaries
        items_list = [asdict(item) for item in flattened_music_order]
        data_dict = {"items": items_list}

        # Write the flattened list to a JSON file
        with open(os.path.join(folder_path, 'music_order.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        for path, subdirs, files in os.walk(folder_path):
            for name in files:
                if name not in ['musicinfo.json', 'wordlist.json', 'music_attribute.json', 'music_ai_section.json', 'music_usbsetting.json', 'music_order.json']:
                    continue
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    encryption.save_file(
                        file=full_path, #type: ignore
                        outdir=full_path,
                        encrypt=True,
                    )
                    os.remove(full_path)

        
