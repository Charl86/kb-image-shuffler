#!/usr/bin/env python3

"""Image Shuffler.

This scripts allows the user to, mainly, scramble or unscramble an image.
It also allows a functionaly for encoding a given set of images and
for performing face recognition on an input image, given the
aforementioned encoding.

This script requires the following libraries: `opencv-python`,
`face_recognition`, `dlib`, `imutils`, as well as the custom package
`shufflealgos`.
"""

import argparse
import pathlib
import shufflealgos.command.command as c


app_parser = argparse.ArgumentParser(
    prog="imagshuffle",
    description=__doc__)
subparsers = app_parser.add_subparsers(
    title="subcommands",
    required=True,
    dest="subcommand")

common_args_parser = argparse.ArgumentParser(add_help=False)
common_args_parser.add_argument(
    "-o", "--output", type=pathlib.Path,
    help="image files output directory")

image_args_parser = argparse.ArgumentParser(add_help=False)
image_args_parser.add_argument(
    "image",
    type=pathlib.Path,
    help="path to target image")
shuffling_args_parser = argparse.ArgumentParser(add_help=False)
shuffling_args_parser.add_argument(
    "key", nargs='+', type=int,
    help="a sequence of positive integers. Values must be numbers from 1 "
         "to 200 (inclusive) and the sequence must have a minimum length of 10"
         " and a maximum length of 100")

scramble_parser = subparsers.add_parser(
    "scramble", parents=[common_args_parser, image_args_parser,
                         shuffling_args_parser])

unscramble_parser = subparsers.add_parser(
    "unscramble", parents=[common_args_parser, image_args_parser,
                           shuffling_args_parser])
unscramble_parser.add_argument(
    "lm_top",
    type=int,
    help="the upmost y-coordinate of landmarks of facial image")
unscramble_parser.add_argument(
    "lm_bottom",
    type=int,
    help="the bottommost y-coordinate of landmarks of facial image")
unscramble_parser.add_argument(
    "lm_left",
    type=int,
    help="the leftmost x-coordinate of landmarks of facial image")
unscramble_parser.add_argument(
    "lm_right",
    type=int,
    help="the rightmost x-coordinate of landmarks of facial image")

recognize_parser = subparsers.add_parser(
    "recognize", parents=[image_args_parser])
recognize_parser.add_argument(
    "encodings",
    type=pathlib.Path,
    help="path to file containing the encodings."
         " It must have the .pickle extension")
recognize_parser.add_argument(
    "-d", "--detection-method", type=str, default="hog",
    choices=["hog", "cnn"],
    help="detection method for face recognition")

encode_parser = subparsers.add_parser(
    "encode")
encode_parser.add_argument(
    "dataset", type=pathlib.Path,
    help=("path to dataset. "
          "Images are labeled using their parent directory name"))
encode_parser.add_argument(
    "encodings", type=pathlib.Path,
    help="path to file to create or append encodings."
         " It must have the .pickle extension")
encode_parser.add_argument(
    "-d", "--detection-method", type=str, default="hog",
    choices=["hog", "cnn"],
    help="detection method for face recognition")


subcommand_parsers = {
    "scramble": scramble_parser,
    "unscramble": unscramble_parser,
    "recognize": recognize_parser,
    "encode": encode_parser
}


if __name__ == "__main__":
    args = app_parser.parse_args()
    subcmd_selected: str = args.subcommand
    subcmd_parser = subcommand_parsers[subcmd_selected]

    subcommand: c.CmdlCommand = None
    if subcmd_selected == "scramble":
        subcommand = c.ScrambleCommand(args, subcmd_parser)
    elif subcmd_selected == "unscramble":
        subcommand = c.UnscrambleCommand(args, subcmd_parser)
    elif subcmd_selected == "recognize":
        subcommand = c.RecognizeCommand(args, subcmd_parser)
    elif subcmd_selected == "encode":
        subcommand = c.EncodeCommand(args, subcmd_parser)
    subcommand.execute()
