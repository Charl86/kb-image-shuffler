"""Module that contains functions associated with face recognition."""

from shufflealgos import os, List, Dict, numpy
import pickle
import cv2
import face_recognition
from imutils import paths


def encode_images(dataset: str, encodings_file,
                  detection_method: str = "hog") -> None:
    """Encode facial images in a directory or subdirectories.

    Encode facial images and store encoding in `encodings_file`.
    The `dataset` can be either one directory that contains images
    associated with one single user, or a directory of subdirectories,
    each subdirectory containing images associated with a unique and
    respective user. This function is abstracted from the user.

    Parameters
    ----------
    dataset : str
        Path to directory or directory of subdirectories containing
        images to be encoded
    encodings_file : binary file object
        A binary file object used to write the encodings in the associated
        encodings file
    detection_method : str
        Face detection method. It can be either `hog` or `cnn`
    """
    print("[INFO] quantifying faces...")
    image_paths: List[str] = list(paths.list_images(dataset))

    known_encodings: List[numpy.ndarray] = list()
    known_users: List[str] = list()
    for i, image_path in enumerate(image_paths):
        print(f"[INFO] processing image {i + 1}/{len(image_paths)}")
        name: str = image_path.split(os.path.sep)[-2]

        curr_image: numpy.ndarray = cv2.imread(image_path)
        curr_img_rgb: numpy.ndarray = cv2.cvtColor(
            curr_image, cv2.COLOR_BGR2RGB)

        faces_boxes = face_recognition.face_locations(
            curr_img_rgb, model=detection_method)

        encodings: List[numpy.ndarray] = face_recognition.face_encodings(
            curr_img_rgb, faces_boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_users.append(name)

    print("[INFO] serializing encodings...")
    faces_data = {"encodings": known_encodings, "names": known_users}
    encodings_file.write(pickle.dumps(faces_data))
    encodings_file.close()


def recognize_faces(image_array, encodings_file,
                    detection_method: str = "hog") -> None:
    """Recognize face from its image array representation.

    Parameters
    ----------
    image_array : numpy.ndarray
        Image array of target facial image
    encodings_file : binary file object
        Binary file that stores the contents of its associated encodings file
    detection_method : str
        Face detection method. It can be either `hog` or `cnn`
    """
    target_img_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    faces_data = pickle.loads(encodings_file.read())
    encodings_file.close()

    faces_boxes = face_recognition.face_locations(
        target_img_rgb, model=detection_method)
    encodings: List[numpy.ndarray] = face_recognition.face_encodings(
        target_img_rgb, faces_boxes)

    names: List[str] = list()
    for encoding in encodings:
        matches: List = face_recognition.compare_faces(
            faces_data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_idxs: List[int] = [i for (i, b) in enumerate(matches) if b]
            counts: Dict[str, int] = dict()

            for matched_idx in matched_idxs:
                name = faces_data["names"][matched_idx]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(faces_boxes, names):
        cv2.rectangle(image_array, (left, top),
                      (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image_array, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    if not names:
        print("No match")
    else:
        print(f"{names[0]}")
