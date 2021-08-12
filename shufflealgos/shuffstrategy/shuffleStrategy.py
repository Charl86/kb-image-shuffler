"""Module that contains the implementations of the Strategy pattern.

Module that contains the abstraction and implementation of the
Strategy pattern centered around shuffling algorithms.

Implementations
---------------
KeyBasedShuffleStrategy
NoShuffleStrategy
"""

from shufflealgos import abc, TYPE_CHECKING
from shufflealgos import numpy


if TYPE_CHECKING:
    from shufflealgos.image.image import Image
    from shufflealgos.image.image import KeyBasedImage
    from shufflealgos.image.key import Key


class ShuffleStrategy(metaclass=abc.ABCMeta):
    """Strategy pattern interface for shuffling algorithms.

    This is an interface that follows the strategy design pattern.
    It encapsulates shuffling algorithm implementations. If a new
    shuffling algorithm is desired, a class in a new file should
    be created that implement this interface.
    """

    @staticmethod
    @abc.abstractstaticmethod
    def scramble(image_obj: "Image"):
        """Scrambles the parameter `image_obj`.

        Any concrete class implementation may ask the 2D-array
        representation of the image through `image_obj`, among other
        attributes using its getters.
        """
        pass

    @staticmethod
    @abc.abstractstaticmethod
    def unscramble(image_obj: "Image"):
        """Unscrambles the parameter `image_obj`.

        Any concrete class implementation may ask the 2D-array
        representation of the image through `image_obj`, among other
        attributes using its getters.
        """
        pass


class NoShuffleStrategy(ShuffleStrategy):
    """Class that implements a null object pattern for the strategy pattern."""

    @staticmethod
    def scramble(image_obj: "Image"):
        """Do nothing."""
        pass

    @staticmethod
    def unscramble(image_obj: "Image"):
        """Do nothing."""
        pass


class KeyBasedShuffleStrategy(ShuffleStrategy):
    """Strategy class for the key-based shuffling algorithm."""

    @staticmethod
    def scramble(image_obj: "KeyBasedImage"):
        """Scramble algorithm using key-based scrambling."""
        # Initialize needed variables
        currimg_array: numpy.ndarray = image_obj.array
        key_values: "Key" = image_obj.key_values
        absmin_rowidx: int = image_obj.minimum_lmark_rowidx
        absmax_rowidx: int = image_obj.maximum_lmark_rowidx
        absmin_colidx: int = image_obj.minimum_lmark_colidx
        absmax_colidx: int = image_obj.maximum_lmark_colidx

        # The distance between absmax_rowidx and absmin_rowidx inclusively
        rows_magnitude: int = absmax_rowidx - absmin_rowidx + 1

        # Shift and extend the key to contain values in the range of row
        # indices and to contain the same amount of terms as rows needed
        # to scramble.
        extended_key: Key = key_values.shift_to_range(
            absmin_rowidx, absmax_rowidx).get_extended_key(rows_magnitude)

        # For each row i, swap with i-th term of the key
        for rowidx, swap_rowidx in zip(range(absmin_rowidx, absmax_rowidx + 1),
                                       extended_key.values):
            for colidx in range(absmin_colidx, absmax_colidx + 1):
                temp_pixel = currimg_array[rowidx, colidx].copy()
                currimg_array[rowidx, colidx] = currimg_array[swap_rowidx,
                                                              colidx].copy()
                currimg_array[swap_rowidx, colidx] = temp_pixel

    @staticmethod
    def unscramble(image_obj: "KeyBasedImage"):
        """Unscramble algorithm using key-based unscrambling."""
        currimg_array: numpy.ndarray = image_obj.array
        key_values: "Key" = image_obj.key_values
        absmin_rowidx: int = image_obj.minimum_lmark_rowidx
        absmax_rowidx: int = image_obj.maximum_lmark_rowidx
        absmin_colidx: int = image_obj.minimum_lmark_colidx
        absmax_colidx: int = image_obj.maximum_lmark_colidx

        rows_magnitude: int = absmax_rowidx - absmin_rowidx + 1

        extended_key: Key = key_values.shift_to_range(
            absmin_rowidx, absmax_rowidx).get_extended_key(rows_magnitude)

        # For each row i, reversed, swap with i-th term of key
        for rowidx, swap_rowidx in reversed(list(zip(
                range(absmin_rowidx, absmax_rowidx + 1),
                extended_key.values))):
            for colidx in range(absmin_colidx, absmax_colidx + 1):
                temp_pixel = currimg_array[rowidx, colidx].copy()
                currimg_array[rowidx, colidx] = currimg_array[swap_rowidx,
                                                              colidx].copy()
                currimg_array[swap_rowidx, colidx] = temp_pixel
