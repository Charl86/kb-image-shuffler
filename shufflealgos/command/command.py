"""Module that contains the Command pattern implementations.

Module that contains the Command pattern abstraction and implementations.

Implementations
---------------
CmdlCommand
DisplayImgCommand
SaveScramImgCommand
SaveUnscramImgCommand
ScrambleImgCommand
UnscrambleImgCommand
"""

import abc
import pathlib
import shufflealgos.helpers as helpers
from shufflealgos.image.image import Image, KeyBasedImage, Key, cv2


class Command(abc.ABC):
    """Command pattern interface."""

    @abc.abstractmethod
    def execute(self) -> None:
        """Perform the execute action on a possible receiver."""
        pass


class DisplayImgCommand(Command):
    """Command class that displays the current image array."""

    def __init__(self, image_obj: Image) -> None:
        """Initialize object with overriden constructor.

        Parameter
        ---------
        image_obj Image
            The image object which will act as the receiver
        """
        self.__image_obj: Image = image_obj

    def execute(self) -> None:
        """Display the current image array."""
        self.__image_obj.perform_displayimg()


class SaveImgCommand(Command):
    """Command that saves the current image."""

    def __init__(self, image_obj: Image) -> None:
        """Initialize object with overriden constructor.

        Parameter
        ---------
        image_obj Image
            The image object which will act as the receiver
        """
        self.__image_obj: Image = image_obj

    def execute(self) -> None:
        """Save the current state of the image array.

        Saving the current state of the image. The image object takes
        care of where to save the image, depending on what actions were
        performed on said iamge. This implies that the current 2D-array
        version of the image object will be serialized to its respective
        file.
        """
        self.__image_obj.perform_save()


class ScrambleImgCommand(Command):
    """Command that executes a scrambling algorithm on an image."""

    def __init__(self, image_obj: Image) -> None:
        """Initialize object with overriden constructor.

        Parameter
        ---------
        image_obj Image
            The image object which will act as the receiver
        """
        self.__image_obj: Image = image_obj

    def execute(self) -> None:
        """Execute the scrambling algorithm loaded into `self.__image_obj`."""
        self.__image_obj.perform_scramble()


class UnscrambleImgCommand(Command):
    """Command that executes a unscrambling algorithm on an image."""

    def __init__(self, image_obj: Image) -> None:
        """Initialize object with overriden constructor.

        Parameter
        ---------
        image_obj Image
            The image object which will act as the receiver
        """
        self.__image_obj: Image = image_obj

    def execute(self) -> None:
        """Run the unscrambling algorithm loaded into `self.__image_obj`."""
        self.__image_obj.perform_unscramble()


class WriteLmarkDimCommand(Command):
    """Command that writes the dimension of the landmarks to a file."""

    def __init__(self, image_obj: Image) -> None:
        """Initialize object with overriden constructor.

        Parameter
        ---------
        image_obj Image
            The image object that will receive the command action
        """
        self.__image_obj: Image = image_obj

    def execute(self) -> None:
        """Write the dimensions of subarray containing landmarks to file."""
        self.__image_obj.perform_save_ldimensions()


class CmdlCommand(Command, abc.ABC):
    """Abstract class for commandline commands."""

    def __init__(self, cmd_args, parser) -> None:
        """Initialize commandline variables.

        Parameters
        ----------
        cmd_args :
            The args object from argparse
        parser :
            Parser of the subcommand called
        """
        self._cmd_args = cmd_args
        self._parser = parser


class ShuffleCommand(CmdlCommand, abc.ABC):
    """Abstract class that serves as Template for shuffling commands."""

    def _create_image(self) -> KeyBasedImage:
        """Validate needed input for Image object and returns it."""
        if not 10 <= len(self._cmd_args.key) <= 100:
            self._parser.error(
                "key length is not between 10 and 100 (inclusive)")
        if any([not 1 <= key_val <= 200 for key_val in self._cmd_args.key]):
            self._parser.error("key value not in range [1, 200]")
        user_key: Key = Key(values=self._cmd_args.key)

        output_dir: pathlib.Path = self._cmd_args.output
        if output_dir is not None:
            if not output_dir.exists():
                self._parser.error("output directory does not exist")
            elif not output_dir.is_dir():
                self._parser.error("output path provided is not a directory")

        try:
            target_image: KeyBasedImage = KeyBasedImage(
                str(self._cmd_args.image), user_key, output_dir)
        except IOError as e:
            self._parser.error(e)

        return target_image


class ScrambleCommand(ShuffleCommand):
    """Commandline Command that invokes scrambling operation on image."""

    def execute(self) -> None:
        """Invoke ScrambleImgCommand."""
        target_image: KeyBasedImage = self._create_image()
        ScrambleImgCommand(target_image).execute()
        SaveImgCommand(target_image).execute()
        WriteLmarkDimCommand(target_image).execute()


class UnscrambleCommand(ShuffleCommand):
    """Commandline Command that invokes unscrambling operation on image."""

    def execute(self) -> None:
        """Invoke UnscrambleImgCommand."""
        target_image: KeyBasedImage = self._create_image()
        target_image.minimum_lmark_rowidx = self._cmd_args.lm_top
        target_image.maximum_lmark_rowidx = self._cmd_args.lm_bottom
        target_image._minimum_lmark_colidx = self._cmd_args.lm_left
        target_image.maximum_lmark_colidx = self._cmd_args.lm_right

        UnscrambleImgCommand(target_image).execute()
        SaveImgCommand(target_image).execute()


class RecognizeCommand(CmdlCommand):
    """Commandline Command that invokes facial recognition on an image."""

    def execute(self) -> None:
        """Call function to perform facial recognition on image."""
        try:
            encodings_fpath: str = self._cmd_args.encodings.name
            if not encodings_fpath.endswith(".pickle"):
                raise ValueError(
                    "encodings file must end with .pickle extension")
            encodings_file = open(encodings_fpath, "rb")
        except ValueError as ve:
            self._parser.error(ve)
        except FileNotFoundError as fnfe:
            self._parser.error(fnfe)

        image_array = cv2.imread(str(self._cmd_args.image))
        if image_array is None:
            self._parser.error(
                "image path file does not exist or has unsupported extension")
        detection_method: str = self._cmd_args.detection_method

        helpers.recognize_faces(image_array, encodings_file, detection_method)


class EncodeCommand(CmdlCommand):
    """Commandline Command that invokes encoding of facial images."""

    def execute(self) -> None:
        """Call function to encode information about facial images."""
        try:
            encodings_fpath: str = self._cmd_args.encodings.name
            if not encodings_fpath.endswith(".pickle"):
                raise ValueError(
                    "encodings file must end with .pickle extension")
            encodings_file = open(encodings_fpath, "wb")
        except ValueError as ve:
            self._parser.error(ve)
        except FileNotFoundError as fnfe:
            self._parser.error(fnfe)

        try:
            dataset: pathlib.Path = self._cmd_args.dataset
            if not dataset.exists():
                raise ValueError("dataset path does not exist")
            if not dataset.is_dir():
                raise ValueError("dataset path is not a directory")
        except ValueError as ve:
            self._parser.error(ve)
        dataset_path: str = str(dataset)
        detection_method: str = self._cmd_args.detection_method

        helpers.encode_images(dataset_path, encodings_file, detection_method)
