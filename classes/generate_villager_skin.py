import cv2
import os
import numpy as np

from PIL import Image

import classes.const as const
from classes.skin_info import SkinInfo, Gender


class GenerateVillagerSkin:
    def __init__(self, skin_info: SkinInfo) -> None:
        self.__skin_info = skin_info
        self.__skin_color = cv2.imread(
            os.path.join(const.COLOR_MAP_BASE_PATH, "villager_skin.png")
        )
        self.__hair_color = cv2.imread(
            os.path.join(const.COLOR_MAP_BASE_PATH, "villager_hair.png")
        )
        return

    def generate(self) -> Image:
        # 素体レンダリング
        gender = Gender(self.__skin_info.param["gender"]).name.lower()
        org_skin_path = os.path.join(
            const.SKIN_BASE_PATH, gender, f"{self.__skin_info.param["skin"]}.png"
        )
        albinism = 0.1 if self.__skin_info.param["albinism"] else 1.0
        skin_img = self.__skin_color_change(
            org_skin_path,
            self.__skin_info.param["melanin"],
            self.__skin_info.param["hemoglobin"],
            albinism,
        )

        # 目のレンダリング
        skin_img = self.__render_eye(
            skin_img,
            gender,
            self.__skin_info.param["face"],
            self.__skin_info.param["hetero"],
        )

        # 髪のレンダリング
        skin_img = self.__render_hair(skin_img, gender, albinism)

        # 服のレンダリング
        skin_img = self.__render_clothing(skin_img, self.__skin_info.param["clothing"])
        img = Image.fromarray(cv2.cvtColor(skin_img, cv2.COLOR_BGRA2RGBA))
        return img

    def __multiply(self, img: np.ndarray, color: np.ndarray) -> np.ndarray:
        # 色を乗算する
        height, width = img.shape[:2]
        for x in range(width):
            for y in range(height):
                for c in range(3):
                    img[x, y][c] = int(color[c] * (img[x, y][c] / 255))

        return img

    def __render(self, base_img: np.ndarray, overlay_img: np.ndarray) -> np.ndarray:
        cv_rgb_bg_image = cv2.cvtColor(base_img, cv2.COLOR_BGRA2RGBA)
        pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert("RGBA")

        cv_rgb_ol_image = cv2.cvtColor(overlay_img, cv2.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert("RGBA")

        pil_rgba_bg_temp = Image.new("RGBA", pil_rgba_bg_image.size, (255, 255, 255, 0))
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, (0, 0), pil_rgba_ol_image)
        result_image = Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)
        return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

    def __skin_color_change(
        self,
        skin_path: str,
        melanin: float,
        hemoglobin: float,
        albinism: float,
    ) -> np.ndarray:
        # 素体読み込み
        img = cv2.imread(skin_path, cv2.IMREAD_UNCHANGED)

        # メラニンとヘモグロビンから肌の色を決定する
        colormap_height, colormap_width = self.__skin_color.shape[:2]
        x = int(self.__clamp_floor(melanin * albinism, colormap_width - 1))
        y = int(self.__clamp_floor(hemoglobin * albinism, colormap_height - 1))
        color = self.__skin_color[x, y]

        # 肌の色を乗算する
        return self.__multiply(img, color)

    def __render_eye(
        self, skin_img: np.ndarray, gender, face: int, hetero: bool
    ) -> np.ndarray:
        # 目を読み込む
        hetero = "_hetero" if hetero else ""
        eye_path = os.path.join(const.FACE_BASE_PATH, gender, f"{face}{hetero}.png")
        eye_img = cv2.imread(eye_path, cv2.IMREAD_UNCHANGED)

        # 目をレンダリング
        return self.__render(skin_img, eye_img)

    def __render_clothing(self, skin_img: np.ndarray, clothing_path: str) -> np.ndarray:
        # 服のレンダリング
        clothes_img = cv2.imread(clothing_path, cv2.IMREAD_UNCHANGED)
        return self.__render(skin_img, clothes_img)

    def __render_hair(
        self, skin_img: np.ndarray, gender: str, albinism: float
    ) -> np.ndarray:
        # 髪を読み込む
        hair_path = os.path.join(
            const.HAIR_BASE_PATH, gender, f"{self.__skin_info.param["hair"]}.png"
        )
        hair_img = cv2.imread(hair_path, cv2.IMREAD_UNCHANGED)

        # 髪の色を乗算する
        hair_img = self.__multiply(hair_img, self.__get_hair_color(albinism))

        # 髪をレンダリング
        return self.__render(skin_img, hair_img)

    def __get_hair_color(self, albinism: float) -> np.ndarray:
        # 髪の色が設定済みの場合、その色を使用する
        if (
            (self.__skin_info.param["hair_color_blue"] > 0.0)
            or (self.__skin_info.param["hair_color_green"] > 0.0)
            or (self.__skin_info.param["hair_color_red"] > 0.0)
        ):
            b = int(self.__clamp_floor(self.__skin_info.param["hair_color_blue"], 255))
            g = int(self.__clamp_floor(self.__skin_info.param["hair_color_green"], 255))
            r = int(self.__clamp_floor(self.__skin_info.param["hair_color_red"], 255))
            return np.array([b, g, r])

        # ユーメラニン、フェオメラニンから髪の色を決定する
        colormap_height, colormap_width = self.__hair_color.shape[:2]
        x = int(
            self.__clamp_floor(
                self.__skin_info.param["eumelanin"] * albinism, colormap_width - 1
            )
        )
        y = int(
            self.__clamp_floor(
                self.__skin_info.param["pheomelanin"] * albinism, colormap_height - 1
            )
        )
        return self.__hair_color[x, y]

    def __clamp_floor(self, val, max_val):
        return min(max_val, max(val * max_val, 0))
