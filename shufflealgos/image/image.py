"""Module that contains the Image abstract class and implementations.

This module contains the Image abstract class, which is a class created
to better aid OpenCV image object managements, speficially tailored for
the scrambling and unscrambling of its concrete classes' instances. It
also contains its implementations.

Implementations
---------------
KeyBasedImage
"""

from shufflealgos import re, os, abc, List, Tuple, Dict, TYPE_CHECKING
from shufflealgos import numpy, cv2
from shufflealgos.image.landmarks.facial_landmarks import identify_landmarks
from shufflealgos.image.key import Key
from shufflealgos.shuffstrategy.shuffleStrategy import KeyBasedShuffleStrategy


if TYPE_CHECKING:
    from shufflealgos.shuffstrategy.shuffleStrategy import (
        ShuffleStrategy)


class Image(abc.ABC):
    """An abstract class to facilitate image file manipulation.

    This class takes care of the image file, its own directory and path
    and the scrambled and unscrambled image file, as well as the 2D-array
    representation of these images. It is meant to be abstract, in the
    case that some concrete classes should implement a method only
    declared here.

    Attribute
    ----------
    _shuffle_strategy : ShuffleStrategy
        An instance variable that contains the current shuffle strategy
        to be used when scramcling/unscrambling an image object. It is
        set to `None`, but it should be “declared” of type ShuffleStrategy
    _path : str
        A relative or absolute path to the associated image
    _array : numpy.ndarray
        A numpy array representation of the current state of the images
    __landmarks : Dict[str, Dict[int, Tuple[int]]]
        Contains the location of the landmarks of the image, if it has any
    _DESTINATION_FILEPATHS : List[str]
        A list of paths in which the current state of the image will be saved
    _selected_path : int
        The selected path to save the image to
        A boolean value that denotes whether the image was recognized or not
    _output_dir : Path
        Path to image files output directory
    """

    _shuffle_strategy: "ShuffleStrategy" = None

    def __init__(self, path: str, output_dir: str = None) -> None:
        """Associate image object to image file given in path.

        Create an image object that stores information associated
        to the image file given in `path`.

        Parameter
        ---------
        path : str
            An absolute or relative path to the image file. It must include
            its extension
        output_filepath : str, optional
            Path to image files output directory`
        """
        self._path = self._array = None
        self._array = None
        self.path = path

        self._output_dir: str = self._abs_path_parent_dir
        if output_dir is not None:
            self._output_dir = os.path.abspath(output_dir)

        self.__landmarks: Dict[int, Tuple[int, int]] \
            = identify_landmarks(self._array)

        self._minimum_lmark_rowidx: int = None
        self._maximum_lmark_rowidx: int = None
        self._minimum_lmark_colidx: int = None
        self._maximum_lmark_colidx: int = None

        if self.__landmarks:
            self._minimum_lmark_rowidx = min(
                self.__landmarks.values(), key=lambda t: t[1])[1]
            self._maximum_lmark_rowidx = max(
                self.__landmarks.values(), key=lambda t: t[1])[1]
            self._minimum_lmark_colidx = min(
                self.__landmarks.values(), key=lambda t: t[0])[0]
            self._maximum_lmark_colidx = max(
                self.__landmarks.values(), key=lambda t: t[0])[0]

        self._DESTINATION_FILEPATHS: List[str] = [
            self._scrambled_path, self._unscrambled_path
        ]
        self._selected_path: int = None

    def set_shuffle_strategy(self, shuffle_strat: "ShuffleStrategy") -> None:
        """Set the shuffling strategy to `shuffle_strat`."""
        self._shuffle_strategy = shuffle_strat

    def perform_scramble(self) -> None:
        """Scramble the image using `self.shuffleStrategy`.

        Sets `self._selected_path` to 0, meaning that the path to which
        the image array will be saved will be to the scrambled image file.
        """
        self._shuffle_strategy.scramble(self)
        self._selected_path = 0

    def perform_unscramble(self) -> None:
        """Unscramble the image using `self.shuffleStrategy`.

        Sets `self._selected_path` to 1, meaning that the path to which
        the image array will be saved will be to the unscrambled image file.
        """
        self._shuffle_strategy.unscramble(self)
        self._selected_path = 1

    def perform_save(self) -> None:
        """Save the current state of the image to the filepath in queue."""
        cv2.imwrite(
            self._DESTINATION_FILEPATHS[self._selected_path],
            self._array)

    def perform_displayimg(self) -> None:
        """Display the current image, i.e. `self._array`."""
        cv2.imshow("Display Window", self._array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def perform_reset(self) -> None:
        """Reset the image to its original version.

        Sets `self._selected_path` to None, meaning that there
        will not be a file to save to if the `perform_save` method is
        called.
        """
        self._array = cv2.imread(self._path)
        # BUG: Crashes if user saves image after resetting. Ameliorate this
        self._selected_path = None

    def perform_save_ldimensions(self) -> None:
        """Save dimensions of landmarks to file named `lmarks_file`."""
        with open(os.path.join(
                self._output_dir,
                f"{self.basename}_Landmarks.txt"), 'w') as lmarks_file:
            lmarks_file.write("{0} {1} {2} {3}".format(
                self._minimum_lmark_rowidx,
                self._maximum_lmark_rowidx,
                self._minimum_lmark_colidx,
                self._maximum_lmark_colidx))

    @property
    def array(self) -> numpy.ndarray:
        """Get the current 2D-array representation of the image."""
        return self._array

    @property
    def landmarks(self) -> Dict[int, Tuple[int, int]]:
        """Get landmarks coordinates of original image."""
        return self.__landmarks

    @property
    def minimum_lmark_rowidx(self) -> int:
        """Get upmost landmark y-coordinate."""
        return self._minimum_lmark_rowidx

    @minimum_lmark_rowidx.setter
    def minimum_lmark_rowidx(self, new_value: int) -> None:
        self._minimum_lmark_rowidx = new_value

    @property
    def maximum_lmark_rowidx(self) -> int:
        """Get bottomost landmark y-coordinate."""
        return self._maximum_lmark_rowidx

    @maximum_lmark_rowidx.setter
    def maximum_lmark_rowidx(self, new_value: int) -> None:
        self._maximum_lmark_rowidx = new_value

    @property
    def minimum_lmark_colidx(self) -> int:
        """Get leftmost landmark x-coordinate."""
        return self._minimum_lmark_colidx

    @minimum_lmark_colidx.setter
    def minimum_lmark_colidx(self, new_value: int) -> None:
        self._minimum_lmark_colidx = new_value

    @property
    def maximum_lmark_colidx(self) -> int:
        """Get rightmost landmark x-coordinate."""
        return self._maximum_lmark_colidx

    @maximum_lmark_colidx.setter
    def maximum_lmark_colidx(self, new_value: int) -> None:
        self._maximum_lmark_colidx = new_value

    @property
    def path(self) -> str:
        """Get image path supplied by user."""
        return self._path

    @path.setter
    def path(self, new_path: str) -> None:
        self._array = cv2.imread(new_path)
        if self._array is None:
            raise IOError(
                "image file does not exist or has unsupported extension")
        else:
            self._path = new_path

    @property
    def rel_path(self) -> str:
        """Get relative path to the image."""
        return os.path.relpath(self._path)

    @property
    def abs_path(self) -> str:
        """Get the absolute path to the image file."""
        return os.path.abspath(self._path)

    @property
    def extension(self) -> str:
        """Get extension of image."""
        return re.search(re.compile(r"\.(.*)$"), self._path).groups()[0]

    @property
    def basename(self) -> str:
        """Get basename of image."""
        return re.search(
            re.compile(r"(.*)\."),
            os.path.basename(self._path)).groups()[0]

    @property
    def _abs_path_parent_dir(self) -> str:
        """Get the absolute path of the parent directory of the image."""
        return os.path.abspath(os.path.dirname(self.abs_path))

    @property
    def _scrambled_path(self) -> str:
        """Get the path to the scrambled image file."""
        filename: str = f"{self.basename}_Scrambled.{self.extension}"
        return os.path.join(self._output_dir, filename)

    @property
    def _unscrambled_path(self) -> str:
        """Get the path to the unscrambled image file."""
        if "_Scrambled" in self.basename:
            fname_noscrampatt = re.compile(
                r"(.*)_Scrambled$")
            fname_noscrampattres = re.search(
                fname_noscrampatt, self.basename)
            filename: str = (f"{fname_noscrampattres.groups()[0]}"
                             f"_Unscrambled.{self.extension}")
        else:
            filename = f"{self.basename}_Unscrambled.{self.extension}"
        return os.path.join(self._output_dir, filename)


class KeyBasedImage(Image):
    """Class that manages images that require a key for scrambling.

    Attributes
    ----------
    __key_vales : Key
        The key object for the shuffling algorithm.
    """

    def __init__(self, path: str, key_values: Key, output_dir: str = None) \
            -> None:
        """Execute parent constructor with new parameter.

        Parameters
        ----------
        path : str
            An absolute or relative path to the image file. It must include
            its extension
        key_values : Key
            The key object that will be used for the shuffling algorithm
        output_filepath : str, optional
            Path to image files output directory
        """
        super().__init__(path, output_dir)

        self._shuffle_strategy = KeyBasedShuffleStrategy()
        self.__key_values: Key = key_values

    @property
    def key_values(self) -> Key:
        """Return key object."""
        return self.__key_values
