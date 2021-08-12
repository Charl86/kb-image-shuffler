import os
import re
import abc
import cv2
import numpy
import dlib
from typing import List, Tuple, Dict, TYPE_CHECKING, Union


project_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
