import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Video stream class
class VideoStream:
    def __init__(self, path):
        self.path = path
        self.capture = None
        self.running = False

    def start(self):
        self.capture = cv2.VideoCapture(self.path)
        if not self.capture.isOpened():  # Check if video opened successfully
            print("Error: Unable to open video file.")
            self.running = False
        else:
            self.running = True

    def stop(self):
        self.running = False
        if self.capture is not None:
            self.capture.release()

    def get_frame(self):
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:  # If frame reading fails, restart the video
                print("End of video, restarting...")
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind to the beginning
                ret, frame = self.capture.read()
            if ret:
                return frame
            else:
                print("Error: Unable to read frame.")
        return None


# GUI class for displaying the video
class VideoApp:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Video Stream")
        self.video_path = video_path

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        # Initialize the video stream
        self.video_stream = VideoStream(self.video_path)
        self.video_stream.start()

        # Start updating the frames
        self.update_frame()

    def update_frame(self):
        if self.video_stream.running:
            frame = self.video_stream.get_frame()
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                frame = Image.fromarray(frame)  # Convert to Pillow Image
                photo = ImageTk.PhotoImage(image=frame)  # Convert to Tkinter PhotoImage

                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.root.after(10, self.update_frame)  # Continue updating the frame
            else:
                print("No frame captured.")
        else:
            print("Video stream is not running.")

    def stop(self):
        self.video_stream.stop()
        print("Video stream stopped.")


# Threaded function to run the GUI
def run_gui():
    video_path = 'D:/Github/RSTP_Video_Streaming_server_Python/file.mp4'  # Replace with your video file path
    root = tk.Tk()
    app = VideoApp(root, video_path)
    root.mainloop()


# Run the GUI in a separate thread
if __name__ == "__main__":
    video_thread = threading.Thread(target=run_gui)
    video_thread.start()
