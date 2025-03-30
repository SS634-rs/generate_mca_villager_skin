import os


SKIN_BASE_PATH = os.path.join("resources", "skins", "skin")
FACE_BASE_PATH = os.path.join("resources", "skins", "face", "normal")
HAIR_BASE_PATH = os.path.join("resources", "skins", "hair")
CLOTHING_BASE_PATH = os.path.join("resources", "skins", "clothing", "normal")
COLOR_MAP_BASE_PATH = os.path.join("resources", "colormap")

GENDER_TABLE = {"male": "男", "female": "女"}

PROFESSION_TABLE = {
    "archer": "弓兵",
    "armorer": "防具鍛冶",
    "baby": "赤ちゃん",
    "baker": "パン屋",
    "butcher": "肉屋",
    "cartographer": "製図家",
    "child": "子ども",
    "cleric": "聖職者",
    "cultist": "カルト信者",
    "farmer": "農民",
    "fisherman": "釣り人",
    "fletcher": "矢師",
    "guard": "衛兵",
    "leatherworker": "革細工師",
    "librarian": "司書",
    "mason": "石工",
    "miner": "鉱夫",
    "nitwit": "ニート",
    "none": "無職",
    "shepherd": "羊飼い",
    "toddler": "幼児",
    "toolsmith": "道具鍛冶",
    "weaponsmith": "武器鍛冶",
}

PARAM_DESC_LIST = {
    "gender": "性別",
    "skin": "素体",
    "face": "顔(目)",
    "hair": "髪型",
    "hetero": "ヘテロクロミア(オッドアイ)",
    "albinism": "アルビノ",
    "hemoglobin": "ヘモグロビン(肌の色を決定する要素)",
    "melanin": "メラニン(肌の色を決定する要素)",
    "eumelanin": "ユーメラニン(髪の色を決定する要素)",
    "pheomelanin": "フェオメラニン(髪の色を決定する要素)",
    "hair_color_blue": "髪の色(青)",
    "hair_color_green": "髪の色(緑)",
    "hair_color_red": "髪の色(赤)",
    "clothing": "服装",
}
