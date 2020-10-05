import numpy as np
import cv2
import permutation as perm
import iterations as it
import diffusion as diff
import subprocess as sub

def encryption_process(x_0, y_0, z_0, video_filename):
    rotation = get_rotation(video_filename)
    cap = cv2.VideoCapture(video_filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if rotation == "90" or rotation == "270":
        frameSize = (int(cap.get(4)), int(cap.get(3)))
    else:
        frameSize = (int(cap.get(3)), int(cap.get(4)))
    higher = max(frameSize)

    out = cv2.VideoWriter("EncryptedVideo.mp4", fourcc , fps, frameSize)   

    encrypted_frames = []
    x_list, y_list, z_list = it.generate_iterations(x_0, y_0, z_0, higher)
    results = [x_list, y_list, z_list]

    diffusion_matrices = [diff.diffusion_matrix(x_list, y_list, frameSize[1], frameSize[0]), 
                          diff.diffusion_matrix(y_list, z_list, frameSize[1], frameSize[0]),
                          diff.diffusion_matrix(z_list, x_list, frameSize[1], frameSize[0])]

    currentFrame = 0

    while(True):
        hasFrame, frame = cap.read()
        if not hasFrame:
            break

        if rotation == "90":
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == "180":
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotation == "270":
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        print("encrypting frame " + str(currentFrame))
        encrypted_frames.append(frame_encryption(results, frame, diffusion_matrices))
        currentFrame = currentFrame + 1

    for frame in encrypted_frames:
        out.write(np.uint8(frame))

    out.release()
    cap.release()

def get_rotation(video_filename):
    exe = "exiftool"
    metadata = {}
    process = sub.Popen([exe, video_filename], stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)

    for output in process.stdout:
        line = output.strip().split(":")
        metadata[line[0].strip()] = line[1].strip()

    return metadata.get("Rotation")

def frame_encryption(results, image, diffusion_matrices):
    layers = [image[:, :, 0], image[:, :, 1], image[:, :, 2]]
    encrypted_layers = []

    for layer in layers:
        i = 0
        permuted_matrix = perm.permutation(results[i], results[(i+1)%3], layer)
        encrypted_matrix = diff.diffusion_process(results[i], results[(i+1)%3], permuted_matrix, diffusion_matrices[i])
        encrypted_layers.append(encrypted_matrix)
        i += 1

    return np.dstack(tuple(encrypted_layers))
