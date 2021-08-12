"""Module that contains the identify_landmarks function."""

from shufflealgos import Dict, Tuple, cv2, numpy, dlib, project_dir, os


def identify_landmarks(image: numpy.ndarray) -> Dict[int, Tuple[int, int]]:
    """Find the coordinates of the landmarks of a facial image."""
    copy_img = image.copy()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.path.join(
        project_dir, "shufflealgos", "image", "landmarks",
        "shape_predictor_68_face_landmarks.dat"))

    gray_img_array = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found_face = detector(gray_img_array)

    face_lmarks: Dict[int, Tuple[int, int]] = dict()

    # Assume only one face is found for our purposes
    for idx, face in enumerate(found_face, start=1):
        landmarks = predictor(gray_img_array, face)

        for n in range(68):
            lmx = landmarks.part(n).x
            lmy = landmarks.part(n).y

            face_lmarks[n + 1] = (lmx, lmy)

            cv2.circle(copy_img, (lmx, lmy), 1, (50, 50, 255), -1)

            cv2.putText(
                copy_img, str(n), (lmx, lmy - 5),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 0, 255), 1)

    return face_lmarks
