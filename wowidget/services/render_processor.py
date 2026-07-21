from io import BytesIO
from pathlib import Path
from threading import RLock
from typing import Final

import requests
from PIL import Image

from wowidget.storage.database import get_app_data_directory

CANVAS_WIDTH: Final[int] = 800
CANVAS_HEIGHT: Final[int] = 800

BASE_CHARACTER_HEIGHT: Final[int] = 1650

DEFAULT_SCALE_PERCENT: Final[int] = 100
DEFAULT_X_OFFSET: Final[int] = 170
DEFAULT_Y_OFFSET: Final[int] = 650

BOUNDING_PADDING: Final[int] = 12

GENERATED_DIRECTORY: Final[Path] = get_app_data_directory() / "generated"


class RenderProcessor:
    """Downloads, composes, previews, and saves character portraits."""

    def __init__(
        self,
        output_directory: Path = GENERATED_DIRECTORY,
    ) -> None:
        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._source_cache: dict[
            int,
            Image.Image,
        ] = {}

        self._cache_lock = RLock()

    def fetch_character_source(
        self,
        *,
        source_url: str,
        character_id: int,
    ) -> Path:
        if not source_url:
            raise ValueError("Blizzard character render URL is missing.")

        if not character_id:
            raise ValueError("Blizzard character ID is missing.")

        source_image = self._download_image(source_url)

        cropped_image = self._crop_transparent_padding(
            source_image,
            padding=BOUNDING_PADDING,
        )

        source_path = self._source_path(character_id)

        cropped_image.save(
            source_path,
            format="PNG",
            optimize=True,
        )

        with self._cache_lock:
            self._source_cache[character_id] = cropped_image.copy()

        return source_path

    def generate_preview_bytes(
        self,
        *,
        character_id: int,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> dict:
        source_image = self._get_source_image(character_id)

        portrait_image = self._create_portrait(
            source_image,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
            resampling=Image.Resampling.BILINEAR,
        )

        return {
            "image_bytes": portrait_image.tobytes(
                "raw",
                "RGBA",
            ),
            "width": portrait_image.width,
            "height": portrait_image.height,
        }

    def save_final_portrait(
        self,
        *,
        character_id: int,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> Path:
        source_image = self._get_source_image(character_id)

        portrait_image = self._create_portrait(
            source_image,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
            resampling=Image.Resampling.LANCZOS,
        )

        output_path = self._final_path(character_id)

        portrait_image.save(
            output_path,
            format="PNG",
            optimize=True,
        )

        return output_path

    def has_cached_source(
        self,
        character_id: int,
    ) -> bool:
        if not character_id:
            return False

        with self._cache_lock:
            if character_id in self._source_cache:
                return True

        return self._source_path(character_id).is_file()

    def clear_memory_cache(
        self,
        character_id: int | None = None,
    ) -> None:
        with self._cache_lock:
            if character_id is None:
                self._source_cache.clear()
                return

            self._source_cache.pop(
                character_id,
                None,
            )

    def get_existing_portrait_path(
        self,
        character_id: int,
    ) -> Path | None:
        if not character_id:
            return None

        output_path = self._final_path(character_id)

        if not output_path.is_file():
            return None

        return output_path

    def _source_path(
        self,
        character_id: int,
    ) -> Path:
        return self.output_directory / f"{character_id}-source.png"

    def _final_path(
        self,
        character_id: int,
    ) -> Path:
        return self.output_directory / f"{character_id}-character-model.png"

    def _get_source_image(
        self,
        character_id: int,
    ) -> Image.Image:
        with self._cache_lock:
            cached_image = self._source_cache.get(character_id)

            if cached_image is not None:
                return cached_image.copy()

        source_path = self._source_path(character_id)

        if not source_path.is_file():
            raise RuntimeError(
                "Generate the portrait before adjusting " "or saving its composition."
            )

        try:
            with Image.open(source_path) as source_image:
                loaded_image = source_image.convert("RGBA")
        except Exception as error:
            raise RuntimeError(
                "The cached character render " "could not be opened."
            ) from error

        with self._cache_lock:
            self._source_cache[character_id] = loaded_image.copy()

        return loaded_image

    @staticmethod
    def _download_image(
        source_url: str,
    ) -> Image.Image:
        try:
            response = requests.get(
                source_url,
                timeout=(10, 30),
            )
            response.raise_for_status()

        except requests.Timeout as error:
            raise RuntimeError(
                "The Blizzard character render download timed out."
            ) from error

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to download the Blizzard " f"character render: {error}"
            ) from error

        try:
            image = Image.open(BytesIO(response.content))

            return image.convert("RGBA")

        except Exception as error:
            raise RuntimeError(
                "The downloaded Blizzard render " "could not be opened as an image."
            ) from error

    @staticmethod
    def _crop_transparent_padding(
        image: Image.Image,
        *,
        padding: int,
    ) -> Image.Image:
        alpha_channel = image.getchannel("A")
        bounding_box = alpha_channel.getbbox()

        if bounding_box is None:
            raise RuntimeError(
                "The Blizzard character render " "contains no visible pixels."
            )

        left, top, right, bottom = bounding_box

        left = max(
            0,
            left - padding,
        )
        top = max(
            0,
            top - padding,
        )
        right = min(
            image.width,
            right + padding,
        )
        bottom = min(
            image.height,
            bottom + padding,
        )

        return image.crop(
            (
                left,
                top,
                right,
                bottom,
            )
        )

    @staticmethod
    def _resize_to_height(
        image: Image.Image,
        target_height: int,
        *,
        resampling: Image.Resampling,
    ) -> Image.Image:
        if image.height <= 0:
            raise RuntimeError("The character render has an invalid height.")

        scale = target_height / image.height
        target_width = round(image.width * scale)

        return image.resize(
            (
                target_width,
                target_height,
            ),
            resampling,
        )

    @staticmethod
    def _place_on_canvas(
        image: Image.Image,
        *,
        canvas_width: int,
        canvas_height: int,
        x_offset: int,
        y_offset: int,
    ) -> Image.Image:
        canvas = Image.new(
            "RGBA",
            (
                canvas_width,
                canvas_height,
            ),
            (
                0,
                0,
                0,
                0,
            ),
        )

        x_position = canvas_width - image.width + x_offset

        y_position = canvas_height - image.height + y_offset

        canvas.alpha_composite(
            image,
            (
                x_position,
                y_position,
            ),
        )

        return canvas

    def _create_portrait(
        self,
        source_image: Image.Image,
        *,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
        resampling: Image.Resampling,
    ) -> Image.Image:
        safe_scale_percent = max(
            40,
            min(
                180,
                int(scale_percent),
            ),
        )

        target_height = round(BASE_CHARACTER_HEIGHT * safe_scale_percent / 100)

        resized_image = self._resize_to_height(
            source_image,
            target_height,
            resampling=resampling,
        )

        return self._place_on_canvas(
            resized_image,
            canvas_width=CANVAS_WIDTH,
            canvas_height=CANVAS_HEIGHT,
            x_offset=int(x_offset),
            y_offset=int(y_offset),
        )
