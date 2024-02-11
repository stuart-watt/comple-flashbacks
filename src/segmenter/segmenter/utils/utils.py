"""OpenCv functions for segmenting the words from an image."""

import cv2


def select_train_images(image):
    """
    User interface for selecting training data from image.

    Click, drag and release to draw a rectangle over desired training area.
    Select as many samples as you want.
    Press 'c' to finish selection.
    Press 'r' to refresh image and select again.

    Returns a list of selected samples from the image
    """
    # pylint: disable=no-member

    starts, ends, ii = [], [], 0
    img_BGR = cv2.imread(image)
    clone = img_BGR.copy()

    # Resize the image to fit the screen before training segment selection.
    # Resize so height is 1000 pixels.
    # Save the original dimensions for conversion back to original resolution.
    scale_factor = img_BGR.shape[0] / 700
    img_BGR = cv2.resize(img_BGR, (0, 0), fx=1 / scale_factor, fy=1 / scale_factor)
    cv2.namedWindow("image")

    def select_region(event, x, y, flags, params):
        nonlocal starts, ends, ii

        if event == cv2.EVENT_LBUTTONDOWN:
            starts.append((x, y))

        elif event == cv2.EVENT_LBUTTONUP:
            ends.append((x, y))

            cv2.rectangle(img_BGR, starts[ii], ends[ii], (0, 255, 0), 2)
            cv2.imshow("image", img_BGR)
            ii += 1

    cv2.setMouseCallback("image", select_region)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", img_BGR)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the training regions
        if key == ord("r"):
            img_BGR = clone.copy()
            starts, ends, ii = [], [], 0

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    cv2.destroyAllWindows()

    tiles = []

    # Scale back the rectangles to match the original image.
    starts = [(int(scale_factor * x), int(scale_factor * y)) for x, y in starts]
    ends = [(int(scale_factor * x), int(scale_factor * y)) for x, y in ends]

    for start, end in zip(starts, ends):
        tiles.append(clone[start[1] : end[1], start[0] : end[0]])

    return tiles
