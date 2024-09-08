import json
import os

class Config:
    datatableKey: str
    fumenKey: str
    gameFilesOutDir: str
    dancers: dict

    def __init__(self) -> None:
        # Define the directory and file paths
        self.appdata_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'KeifunsDatatableEditor')  # type: ignore
        self.config_file_path = os.path.join(self.appdata_dir, 'config.json')

        # Create the directory if it doesn't exist
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)

        default_config = {
            "datatableKey": "",
            "fumenKey": "",
            "gameFilesOutDir": "",
            "dancers": {
                "001_miku": {
                    "ensoPartsID1": 1,
                    "ensoPartsID2": 1,
                    "donBg1p": "lumen/001_miku/enso_normal/enso/donbg/donbg_b_001_1p.nulstb",
                    "donBg2p": "lumen/001_miku/enso_normal/enso/donbg/donbg_b_001_2p.nulstb",
                    "dancerDai": "lumen/001_miku/enso_normal/enso/background/dodai_b_01.nulstb",
                    "dancer": "lumen/001_miku/enso_normal/enso/dancer/dance_b_001.nulstb",
                    "danceNormalBg": "lumen/001_miku/enso_normal/enso/background/bg_nomal_b_001.nulstb",
                    "danceFeverBg": "lumen/001_miku/enso_normal/enso/background/bg_fever_b_001.nulstb",
                    "rendaEffect": "lumen/001_miku/enso_normal/enso/renda_effect/renda_b_001.nulstb",
                    "fever": "lumen/001_miku/enso_normal/enso/fever/fever_b_001.nulstb",
                    "donBg1p1": "lumen/001_miku/enso_normal/enso/donbg/donbg_b_001_1p.nulstb",
                    "donBg2p1": "lumen/001_miku/enso_normal/enso/donbg/donbg_b_001_2p.nulstb",
                    "dancerDai1": "lumen/001_miku/enso_normal/enso/background/dodai_b_01.nulstb",
                    "dancer1": "lumen/001_miku/enso_normal/enso/dancer/dance_b_001.nulstb",
                    "danceNormalBg1": "lumen/001_miku/enso_normal/enso/background/bg_nomal_b_001.nulstb",
                    "danceFeverBg1": "lumen/001_miku/enso_normal/enso/background/bg_fever_b_001.nulstb",
                    "rendaEffect1": "lumen/001_miku/enso_normal/enso/renda_effect/renda_b_001.nulstb",
                    "fever1": "lumen/001_miku/enso_normal/enso/fever/fever_b_001.nulstb"
                },
                "002_toho": {
                    "ensoPartsID1": 2,
                    "ensoPartsID2": 2,
                    "donBg1p": "lumen/002_toho/enso_normal/enso/donbg/donbg_b_002_1p.nulstb",
                    "donBg2p": "lumen/002_toho/enso_normal/enso/donbg/donbg_b_002_2p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/002_toho/enso_normal/enso/dancer/dance_b_002.nulstb",
                    "danceNormalBg": "lumen/002_toho/enso_normal/enso/background/bg_nomal_b_002.nulstb",
                    "danceFeverBg": "lumen/002_toho/enso_normal/enso/background/bg_fever_b_002.nulstb",
                    "rendaEffect": "lumen/002_toho/enso_normal/enso/renda_effect/renda_b_002.nulstb",
                    "fever": "lumen/002_toho/enso_normal/enso/fever/fever_b_002.nulstb",
                    "donBg1p1": "lumen/002_toho/enso_normal/enso/donbg/donbg_b_002_1p.nulstb",
                    "donBg2p1": "lumen/002_toho/enso_normal/enso/donbg/donbg_b_002_2p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/002_toho/enso_normal/enso/dancer/dance_b_002.nulstb",
                    "danceNormalBg1": "lumen/002_toho/enso_normal/enso/background/bg_nomal_b_002.nulstb",
                    "danceFeverBg1": "lumen/002_toho/enso_normal/enso/background/bg_fever_b_002.nulstb",
                    "rendaEffect1": "lumen/002_toho/enso_normal/enso/renda_effect/renda_b_002.nulstb",
                    "fever1": "lumen/002_toho/enso_normal/enso/fever/fever_b_002.nulstb"
                },
                "003_gumi": {
                    "ensoPartsID1": 3,
                    "ensoPartsID2": 3,
                    "donBg1p": "lumen/003_gumi/enso_normal/enso/donbg/donbg_b_003_1p.nulstb",
                    "donBg2p": "lumen/003_gumi/enso_normal/enso/donbg/donbg_b_003_1p.nulstb",
                    "dancerDai": "lumen/003_gumi/enso_normal/enso/background/dodai_b_03.nulstb",
                    "dancer": "lumen/003_gumi/enso_normal/enso/dancer/dance_b_003.nulstb",
                    "danceNormalBg": "lumen/003_gumi/enso_normal/enso/background/bg_nomal_b_003.nulstb",
                    "danceFeverBg": "lumen/003_gumi/enso_normal/enso/background/bg_fever_b_003.nulstb",
                    "rendaEffect": "lumen/003_gumi/enso_normal/enso/renda_effect/renda_b_003.nulstb",
                    "fever": "lumen/003_gumi/enso_normal/enso/fever/fever_b_003.nulstb",
                    "donBg1p1": "lumen/003_gumi/enso_normal/enso/donbg/donbg_b_003_1p.nulstb",
                    "donBg2p1": "lumen/003_gumi/enso_normal/enso/donbg/donbg_b_003_1p.nulstb",
                    "dancerDai1": "lumen/003_gumi/enso_normal/enso/background/dodai_b_03.nulstb",
                    "dancer1": "lumen/003_gumi/enso_normal/enso/dancer/dance_b_003.nulstb",
                    "danceNormalBg1": "lumen/003_gumi/enso_normal/enso/background/bg_nomal_b_003.nulstb",
                    "danceFeverBg1": "lumen/003_gumi/enso_normal/enso/background/bg_fever_b_003.nulstb",
                    "rendaEffect1": "lumen/003_gumi/enso_normal/enso/renda_effect/renda_b_003.nulstb",
                    "fever1": "lumen/003_gumi/enso_normal/enso/fever/fever_b_003.nulstb"      
                },
                "004_ia": {
                    "ensoPartsID1": 4,
                    "ensoPartsID2": 4,
                    "donBg1p": "lumen/004_ia/enso_normal/enso/donbg/donbg_b_004_1p.nulstb",
                    "donBg2p": "lumen/004_ia/enso_normal/enso/donbg/donbg_b_004_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/004_ia/enso_normal/enso/dancer/dance_b_004.nulstb",
                    "danceNormalBg": "lumen/004_ia/enso_normal/enso/background/bg_nomal_b_004.nulstb",
                    "danceFeverBg": "lumen/004_ia/enso_normal/enso/background/bg_fever_b_004.nulstb",
                    "rendaEffect": "lumen/004_ia/enso_normal/enso/renda_effect/renda_b_004.nulstb",
                    "fever": "lumen/004_ia/enso_normal/enso/fever/fever_b_004.nulstb",
                    "donBg1p1": "lumen/004_ia/enso_normal/enso/donbg/donbg_b_004_1p.nulstb",
                    "donBg2p1": "lumen/004_ia/enso_normal/enso/donbg/donbg_b_004_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/004_ia/enso_normal/enso/dancer/dance_b_004.nulstb",
                    "danceNormalBg1": "lumen/004_ia/enso_normal/enso/background/bg_nomal_b_004.nulstb",
                    "danceFeverBg1": "lumen/004_ia/enso_normal/enso/background/bg_fever_b_004.nulstb",
                    "rendaEffect1": "lumen/004_ia/enso_normal/enso/renda_effect/renda_b_004.nulstb",
                    "fever1": "lumen/004_ia/enso_normal/enso/fever/fever_b_004.nulstb"       
                },
                "005_lovelive": {
                    "ensoPartsID1": 5,
                    "ensoPartsID2": 5,
                    "donBg1p": "lumen/005_lovelive/enso_normal/enso/donbg/donbg_b_005_1p.nulstb",
                    "donBg2p": "lumen/005_lovelive/enso_normal/enso/donbg/donbg_b_005_2p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/005_lovelive/enso_normal/enso/dancer/dance_b_005.nulstb",
                    "danceNormalBg": "lumen/005_lovelive/enso_normal/enso/background/bg_nomal_b_005.nulstb",
                    "danceFeverBg": "lumen/005_lovelive/enso_normal/enso/background/bg_fever_b_005.nulstb",
                    "rendaEffect": "lumen/005_lovelive/enso_normal/enso/renda_effect/renda_b_005.nulstb",
                    "fever": "lumen/005_lovelive/enso_normal/enso/fever/fever_b_005.nulstb",
                    "donBg1p1": "lumen/005_lovelive/enso_normal/enso/donbg/donbg_b_005_1p.nulstb",
                    "donBg2p1": "lumen/005_lovelive/enso_normal/enso/donbg/donbg_b_005_2p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/005_lovelive/enso_normal/enso/dancer/dance_b_005.nulstb",
                    "danceNormalBg1": "lumen/005_lovelive/enso_normal/enso/background/bg_nomal_b_005.nulstb",
                    "danceFeverBg1": "lumen/005_lovelive/enso_normal/enso/background/bg_fever_b_005.nulstb",
                    "rendaEffect1": "lumen/005_lovelive/enso_normal/enso/renda_effect/renda_b_005.nulstb",
                    "fever1": "lumen/005_lovelive/enso_normal/enso/fever/fever_b_005.nulstb"
                },
                "006_i7_id7": {
                    "ensoPartsID1": 6,
                    "ensoPartsID2": 6,
                    "donBg1p": "lumen/006_i7_id7/enso_normal/enso/donbg/donbg_b_006_1p.nulstb",
                    "donBg2p": "lumen/006_i7_id7/enso_normal/enso/donbg/donbg_b_006_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/006_i7_id7/enso_normal/enso/dancer/dance_b_006.nulstb",
                    "danceNormalBg": "lumen/006_i7_id7/enso_normal/enso/background/bg_nomal_b_006.nulstb",
                    "danceFeverBg": "lumen/006_i7_id7/enso_normal/enso/background/bg_fever_b_006.nulstb",
                    "rendaEffect": "lumen/006_i7_id7/enso_normal/enso/renda_effect/renda_b_006.nulstb",
                    "fever": "lumen/000_default/enso_normal/enso/fever/fever_effect0.nulstb",
                    "donBg1p1": "lumen/006_i7_id7/enso_normal/enso/donbg/donbg_b_006_1p.nulstb",
                    "donBg2p1": "lumen/006_i7_id7/enso_normal/enso/donbg/donbg_b_006_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/006_i7_id7/enso_normal/enso/dancer/dance_b_006.nulstb",
                    "danceNormalBg1": "lumen/006_i7_id7/enso_normal/enso/background/bg_nomal_b_006.nulstb",
                    "danceFeverBg1": "lumen/006_i7_id7/enso_normal/enso/background/bg_fever_b_006.nulstb",
                    "rendaEffect1": "lumen/006_i7_id7/enso_normal/enso/renda_effect/renda_b_006.nulstb",
                    "fever1": "lumen/000_default/enso_normal/enso/fever/fever_effect0.nulstb"   
                },
                "010_imas": {
                    "ensoPartsID1": 10,
                    "ensoPartsID2": 10,
                    "donBg1p": "lumen/010_imas/enso_normal/enso/donbg/donbg_b_010_1p.nulstb",
                    "donBg2p": "lumen/010_imas/enso_normal/enso/donbg/donbg_b_010_2p.nulstb",
                    "dancerDai": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer": "lumen/010_imas/enso_normal/enso/dancer/dance_b_010.nulstb",
                    "danceNormalBg": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever": "lumen/010_imas/enso_normal/enso/fever/fever_b_010.nulstb",
                    "donBg1p1": "lumen/010_imas/enso_normal/enso/donbg/donbg_b_010_1p.nulstb",
                    "donBg2p1": "lumen/010_imas/enso_normal/enso/donbg/donbg_b_010_2p.nulstb",
                    "dancerDai1": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer1": "lumen/010_imas/enso_normal/enso/dancer/dance_b_010.nulstb",
                    "danceNormalBg1": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg1": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect1": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever1": "lumen/010_imas/enso_normal/enso/fever/fever_b_010.nulstb"    
                },
                "011_imas_cg": {
                    "ensoPartsID1": 11,
                    "ensoPartsID2": 11,
                    "donBg1p": "lumen/011_imas_cg/enso_normal/enso/donbg/donbg_b_011_1p.nulstb",
                    "donBg2p": "lumen/011_imas_cg/enso_normal/enso/donbg/donbg_b_011_2p.nulstb",
                    "dancerDai": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer": "lumen/011_imas_cg/enso_normal/enso/dancer/dance_b_011.nulstb",
                    "danceNormalBg": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever": "lumen/011_imas_cg/enso_normal/enso/fever/fever_b_011.nulstb",
                    "donBg1p1": "lumen/011_imas_cg/enso_normal/enso/donbg/donbg_b_011_1p.nulstb",
                    "donBg2p1": "lumen/011_imas_cg/enso_normal/enso/donbg/donbg_b_011_2p.nulstb",
                    "dancerDai1": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer1": "lumen/011_imas_cg/enso_normal/enso/dancer/dance_b_011.nulstb",
                    "danceNormalBg1": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg1": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect1": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever1": "lumen/011_imas_cg/enso_normal/enso/fever/fever_b_011.nulstb"
                },
                "012_imas_ml": {
                    "ensoPartsID1": 12,
                    "ensoPartsID2": 12,
                    "donBg1p": "lumen/012_imas_ml/enso_normal/enso/donbg/donbg_b_012_1p.nulstb",
                    "donBg2p": "lumen/012_imas_ml/enso_normal/enso/donbg/donbg_b_012_2p.nulstb",
                    "dancerDai": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer": "lumen/012_imas_ml/enso_normal/enso/dancer/dance_b_012.nulstb",
                    "danceNormalBg": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever": "lumen/012_imas_ml/enso_normal/enso/fever/fever_b_012.nulstb",
                    "donBg1p1": "lumen/012_imas_ml/enso_normal/enso/donbg/donbg_b_012_1p.nulstb",
                    "donBg2p1": "lumen/012_imas_ml/enso_normal/enso/donbg/donbg_b_012_2p.nulstb",
                    "dancerDai1": "lumen/010_imas/enso_normal/enso/background/dodai_b_010.nulstb",
                    "dancer1": "lumen/012_imas_ml/enso_normal/enso/dancer/dance_b_012.nulstb",
                    "danceNormalBg1": "lumen/010_imas/enso_normal/enso/background/bg_nomal_b_010.nulstb",
                    "danceFeverBg1": "lumen/010_imas/enso_normal/enso/background/bg_fever_b_010.nulstb",
                    "rendaEffect1": "lumen/010_imas/enso_normal/enso/renda_effect/renda_b_010.nulstb",
                    "fever1": "lumen/012_imas_ml/enso_normal/enso/fever/fever_b_012.nulstb"
                },
                "013_imas_sidem": {
                    "ensoPartsID1": 13,
                    "ensoPartsID2": 13,
                    "donBg1p": "lumen/013_imas_sidem/enso_normal/enso/donbg/donbg_b_013_1p.nulstb",
                    "donBg2p": "lumen/013_imas_sidem/enso_normal/enso/donbg/donbg_b_013_2p.nulstb",
                    "dancerDai": "lumen/013_imas_sidem/enso_normal/enso/background/dodai_b_013.nulstb",
                    "dancer": "lumen/013_imas_sidem/enso_normal/enso/dancer/dance_b_013.nulstb",
                    "danceNormalBg": "lumen/013_imas_sidem/enso_normal/enso/background/bg_nomal_b_013.nulstb",
                    "danceFeverBg": "lumen/013_imas_sidem/enso_normal/enso/background/bg_fever_b_013.nulstb",
                    "rendaEffect": "lumen/013_imas_sidem/enso_normal/enso/renda_effect/renda_b_013.nulstb",
                    "fever": "lumen/013_imas_sidem/enso_normal/enso/fever/fever_b_013.nulstb",
                    "donBg1p1": "lumen/013_imas_sidem/enso_normal/enso/donbg/donbg_b_013_1p.nulstb",
                    "donBg2p1": "lumen/013_imas_sidem/enso_normal/enso/donbg/donbg_b_013_2p.nulstb",
                    "dancerDai1": "lumen/013_imas_sidem/enso_normal/enso/background/dodai_b_013.nulstb",
                    "dancer1": "lumen/013_imas_sidem/enso_normal/enso/dancer/dance_b_013.nulstb",
                    "danceNormalBg1": "lumen/013_imas_sidem/enso_normal/enso/background/bg_nomal_b_013.nulstb",
                    "danceFeverBg1": "lumen/013_imas_sidem/enso_normal/enso/background/bg_fever_b_013.nulstb",
                    "rendaEffect1": "lumen/013_imas_sidem/enso_normal/enso/renda_effect/renda_b_013.nulstb",
                    "fever1": "lumen/013_imas_sidem/enso_normal/enso/fever/fever_b_013.nulstb"
                },
                "014_yokai": {
                    "ensoPartsID1": 14,
                    "ensoPartsID2": 14,
                    "donBg1p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/014_yokai/enso_normal/enso/dancer/dance_b_014.nulstb",
                    "danceNormalBg": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb",
                    "donBg1p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/014_yokai/enso_normal/enso/dancer/dance_b_014.nulstb",
                    "danceNormalBg1": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg1": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect1": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever1": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb"
                },
                "015_yokai_mb": {
                    "ensoPartsID1": 15,
                    "ensoPartsID2": 15,
                    "donBg1p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/015_yokai_mb/enso_normal/enso/dancer/dance_b_015.nulstb",
                    "danceNormalBg": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb",
                    "donBg1p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/015_yokai_mb/enso_normal/enso/dancer/dance_b_015.nulstb",
                    "danceNormalBg1": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg1": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect1": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever1": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb"
                },
                "016_yokai_ht": {
                    "ensoPartsID1": 16,
                    "ensoPartsID2": 16,
                    "donBg1p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/016_yokai_ht/enso_normal/enso/dancer/dance_b_016.nulstb",
                    "danceNormalBg": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb",
                    "donBg1p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "donBg2p1": "lumen/014_yokai/enso_normal/enso/donbg/donbg_b_014_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/016_yokai_ht/enso_normal/enso/dancer/dance_b_016.nulstb",
                    "danceNormalBg1": "lumen/014_yokai/enso_normal/enso/background/bg_nomal_b_014.nulstb",
                    "danceFeverBg1": "lumen/014_yokai/enso_normal/enso/background/bg_fever_b_014.nulstb",
                    "rendaEffect1": "lumen/014_yokai/enso_normal/enso/renda_effect/renda_b_014.nulstb",
                    "fever1": "lumen/014_yokai/enso_normal/enso/fever/fever_b_014.nulstb"
                },
                "019_mario": {
                    "ensoPartsID1": 19,
                    "ensoPartsID2": 19,
                    "donBg1p": "lumen/019_mario/enso_normal/enso/donbg/donbg_b_019_1p.nulstb",
                    "donBg2p": "lumen/019_mario/enso_normal/enso/donbg/donbg_b_019_2p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/019_mario/enso_normal/enso/dancer/dance_b_019.nulstb",
                    "danceNormalBg": "lumen/019_mario/enso_normal/enso/background/bg_nomal_b_019.nulstb",
                    "danceFeverBg": "lumen/019_mario/enso_normal/enso/background/bg_fever_b_019.nulstb",
                    "rendaEffect": "lumen/019_mario/enso_normal/enso/renda_effect/renda_b_019.nulstb",
                    "fever": "lumen/019_mario/enso_normal/enso/fever/fever_b_019.nulstb",
                    "donBg1p1": "lumen/019_mario/enso_normal/enso/donbg/donbg_b_019_1p.nulstb",
                    "donBg2p1": "lumen/019_mario/enso_normal/enso/donbg/donbg_b_019_2p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/019_mario/enso_normal/enso/dancer/dance_b_019.nulstb",
                    "danceNormalBg1": "lumen/019_mario/enso_normal/enso/background/bg_nomal_b_019.nulstb",
                    "danceFeverBg1": "lumen/019_mario/enso_normal/enso/background/bg_fever_b_019.nulstb",
                    "rendaEffect1": "lumen/019_mario/enso_normal/enso/renda_effect/renda_b_019.nulstb",
                    "fever1": "lumen/019_mario/enso_normal/enso/fever/fever_b_019.nulstb"      
                },
                "020_A3": {
                    "ensoPartsID1": 20,
                    "ensoPartsID2": 20,
                    "donBg1p": "lumen/020_A3/enso_normal/enso/donbg/donbg_b_020_1p.nulstb",
                    "donBg2p": "lumen/020_A3/enso_normal/enso/donbg/donbg_b_020_1p.nulstb",
                    "dancerDai": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer": "lumen/020_A3/enso_normal/enso/dancer/dance_b_020.nulstb",
                    "danceNormalBg": "lumen/020_A3/enso_normal/enso/background/bg_nomal_b_020.nulstb",
                    "danceFeverBg": "lumen/020_A3/enso_normal/enso/background/bg_fever_b_020.nulstb",
                    "rendaEffect": "lumen/020_A3/enso_normal/enso/renda_effect/renda_b_020.nulstb",
                    "fever": "lumen/000_default/enso_normal/enso/fever/fever_effect0.nulstb",
                    "donBg1p1": "lumen/020_A3/enso_normal/enso/donbg/donbg_b_020_1p.nulstb",
                    "donBg2p1": "lumen/020_A3/enso_normal/enso/donbg/donbg_b_020_1p.nulstb",
                    "dancerDai1": "lumen/000_default/enso_normal/enso/background/bg_dai_a_00.nulstb",
                    "dancer1": "lumen/020_A3/enso_normal/enso/dancer/dance_b_020.nulstb",
                    "danceNormalBg1": "lumen/020_A3/enso_normal/enso/background/bg_nomal_b_020.nulstb",
                    "danceFeverBg1": "lumen/020_A3/enso_normal/enso/background/bg_fever_b_020.nulstb",
                    "rendaEffect1": "lumen/020_A3/enso_normal/enso/renda_effect/renda_b_020.nulstb",
                    "fever1": "lumen/000_default/enso_normal/enso/fever/fever_effect0.nulstb"     
                }
            }
        }

        # Create the config.json file if it doesn't exist
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w', encoding='utf-8') as config_file:
                json.dump(default_config, config_file, indent=4)

        # Load the configuration from the file
        with open(self.config_file_path, encoding="utf-8") as f:
            d = json.load(f)

        # Check for missing keys and update with defaults if necessary
        updated = False
        if 'datatableKey' not in d:
            d['datatableKey'] = default_config['datatableKey']
            updated = True
        if 'fumenKey' not in d:
            d['fumenKey'] = default_config['fumenKey']
            updated = True
        if 'gameFilesOutDir' not in d:
            d['gameFilesOutDir'] = default_config['gameFilesOutDir']
            updated = True
        if 'dancers' not in d:
            d['dancers'] = default_config['dancers']
            updated = True

        # If any updates were made, write back the updated config
        if updated:
            with open(self.config_file_path, 'w') as config_file:
                json.dump(d, config_file, indent=4)

        # Set class attributes
        self.datatableKey = d['datatableKey']
        self.fumenKey = d['fumenKey']
        self.gameFilesOutDir = d['gameFilesOutDir']
        self.dancers = d['dancers']

    def update_keys(self, datatableKey: str, fumenKey: str) -> None:
        """Update the configuration and save it to the config.json file."""
        # Update the class attributes
        self.datatableKey = datatableKey
        self.fumenKey = fumenKey
        self.write_back_to_json()

    def update_game_files_out_dir(self, game_files_out_dir: str):
        self.gameFilesOutDir = game_files_out_dir
        self.write_back_to_json()

    def write_back_to_json(self):
        # Update the configuration dictionary
        updated_config = {
            "datatableKey": self.datatableKey,
            "fumenKey": self.fumenKey,
            "gameFilesOutDir": self.gameFilesOutDir,
            "dancers": self.dancers
        }

        # Write the updated configuration back to the config.json file
        with open(self.config_file_path, 'w') as config_file:
            json.dump(updated_config, config_file, indent=4)

# Instantiate and use the Config class
config: Config = Config()
