import os
import pathlib
import pandas as pd
import random as rd
from typing import Any, List, Dict
from enum import IntEnum
import classes.const as const


class Gender(IntEnum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3


class SkinInfo:
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        self.param = kwargs
        self.__param_value_range = {
            "gender": "1 or 2",
            "hetero": "True or False",
            "albinism": "True or False",
            "hemoglobin": "0.0 ~ 1.0",
            "melanin": "0.0 ~ 1.0",
            "eumelanin": "0.0 ~ 1.0",
            "pheomelanin": "0.0 ~ 1.0",
            "hair_color_blue": "0.0 ~ 1.0",
            "hair_color_green": "0.0 ~ 1.0",
            "hair_color_red": "0.0 ~ 1.0",
            "clothing": "-",
        }
        return

    def __str__(self) -> str:
        out = f"性別: {const.GENDER_TABLE[self.__convert_gender_name()]}\n"
        out += f"職業: {const.PROFESSION_TABLE[self.__get_profession()]}\n"
        out += "特性:"

        if self.param["hetero"]:
            out += " オッドアイ"

        if self.param["albinism"]:
            out += " アルビノ"

        if (not self.param["hetero"]) and (not self.param["albinism"]):
            out += " なし"

        return out

    def to_dataframe(self) -> pd.DataFrame:
        data = {"パラメータ名": [], "説明": [], "値": [], "値の範囲": []}

        for key in self.param.keys():
            data["パラメータ名"].append(key)
            data["説明"].append(const.PARAM_DESC_LIST[key])
            data["値"].append(self.param[key])
            data["値の範囲"].append(self.__param_value_range[key])

        df = pd.DataFrame(data)
        styles = [dict(selector="th", props=[("text-align", "left")])]
        df = df.style.set_properties(**{"text-align": "left"}).set_table_styles(styles)
        return df

    def generate_skin_info(self):
        # 性別の設定
        if (not "gender" in self.param) or (self.param["gender"] == Gender.UNKNOWN):
            self.param["gender"] = Gender(rd.randint(1, 2))

        # 素体の設定
        self.__set_body_param("skin", const.SKIN_BASE_PATH)

        # 顔の設定
        self.__set_body_param("face", const.FACE_BASE_PATH)

        # 髪の設定
        self.__set_body_param("hair", const.HAIR_BASE_PATH)

        # ヘテロクロミア(オッドアイ)とアルビノの設定
        # ※10%の確率で設定する
        for key in ["hetero", "albinism"]:
            if (not key in self.param) or (self.param[key] is None):
                self.param[key] = not bool(rd.randrange(10))

        # 肌の色を決定する要素(ヘモグロビン、メラニン)の設定
        self.__set_pigment_param(["hemoglobin", "melanin"])

        # 髪の色を決定する要素(ユーメラニン、フェオメラニン)の設定
        self.__set_pigment_param(["eumelanin", "pheomelanin"])

        # 10%の確率で4つの要素とは無関係の髪の色を設定する
        self.__set_pigment_param(
            ["hair_color_blue", "hair_color_green", "hair_color_red"],
            (rd.randrange(10) != 0) or (self.param["albinism"]),
        )

        # 服の設定
        neutral = rd.randrange(10)
        cloth_gender = "neutral" if neutral == 0 else self.__convert_gender_name()
        cloth_list = self.__get_clothing_files(cloth_gender)
        self.param["clothing"] = cloth_list[rd.randrange(len(cloth_list))]
        return

    def __convert_gender_name(self) -> str:
        return Gender(self.param["gender"]).name.lower()

    def __get_profession(self) -> str:
        return os.path.basename(os.path.dirname(self.param["clothing"]))

    def __get_png_files(self, base_path: str) -> List[str]:
        str_gender = self.__convert_gender_name()
        p_dir = pathlib.Path(os.path.join(base_path, str_gender))
        return [str(file_path) for file_path in sorted(list(p_dir.glob("**/*.png")))]

    def __get_unique_file_count(self, file_list: List[str]) -> int:
        face_list = []
        for face_file in file_list:
            file_name = os.path.basename(face_file).split(".")[0]
            face_list.append(file_name.split("_")[0])

        face_list = sorted(list(set(face_list)))
        return len(face_list)

    def __get_clothing_files(self, cloth_gender: str) -> List[str]:
        p_dir = pathlib.Path(os.path.join(const.CLOTHING_BASE_PATH, cloth_gender))
        return [str(file_path) for file_path in sorted(list(p_dir.glob("**/*.png")))]

    def __set_body_param(self, key: str, base_path: str) -> None:
        max_count = self.__get_unique_file_count(self.__get_png_files(base_path))
        if (
            (not key in self.param)
            or (self.param[key] == -1)
            or (self.param[key] >= max_count)
        ):
            self.param[key] = rd.randrange(max_count)

        self.__param_value_range[key] = f"0 ~ {max_count - 1}"
        return

    def __set_pigment_param(
        self, key_list: List[str], not_random: bool = False
    ) -> float:
        for key in key_list:
            if (
                (key in self.param)
                and (self.param[key] >= 0.0)
                and (self.param[key] <= 1.0)
            ):
                return

            if (key == "hemoglobin") or (key == "melanin"):
                # ※villager_skinのcolor_mapは濃い色が多いため、薄い色が出やすくなるようにする
                if rd.randrange(4) == 0:
                    self.param[key] = rd.random()
                else:
                    self.param[key] = rd.uniform(0.0, 0.25)
            elif (key == "eumelanin") or (key == "pheomelanin"):
                self.param[key] = rd.random()
            elif (
                (key == "hair_color_blue")
                or (key == "hair_color_green")
                or (key == "hair_color_red")
            ):
                self.param[key] = 0.0 if not_random else rd.random()

        return
