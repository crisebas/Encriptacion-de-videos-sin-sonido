import encryption as enc
from time import time

def main():
    video_filename = "OriginalVideo.mp4"
    x_0 = float(input("El valor inicial de x será: "))
    y_0 = float(input("El valor inicial de y será: "))
    z_0 = float(input("El valor inicial de z será: "))

    start_time = time()
    enc.encryption_process(x_0, y_0, z_0, video_filename)
    elapsed_time = time() - start_time
    print(elapsed_time)

if __name__ == "__main__":
    main()