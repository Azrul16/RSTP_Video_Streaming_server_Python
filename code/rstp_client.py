import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Function to fetch and display frames
def update_frame():
    # Replace with the actual IP of your server
    response = requests.get('http://192.168.1.10:5000/video_feed', stream=True)  # Use your server's IP here
    img_bytes = b''
    
    # Continuously read chunks of the stream
    for chunk in response.iter_content(chunk_size=1024):
        img_bytes += chunk
        
        # Find the start and end of the JPEG image
        a = img_bytes.find(b'\xff\xd8')  # JPEG header
        b = img_bytes.find(b'\xff\xd9')  # JPEG footer
        
        if a != -1 and b != -1:
            jpg = img_bytes[a:b + 2]
            img_bytes = img_bytes[b + 2:]
            
            # Open the image with Pillow
            img = Image.open(BytesIO(jpg))
            img = ImageTk.PhotoImage(img)  # Convert to format tkinter can use
            
            # Update the tkinter label with the new frame
            label.config(image=img)
            label.image = img
            
    # Update the frame every 10 ms
    root.after(10, update_frame)

# Create the tkinter window
root = tk.Tk()
root.title('Live Video Stream')

# Label to display the video
label = tk.Label(root)
label.pack()

# Call the function to start updating frames
update_frame()

# Run the tkinter mainloop
root.mainloop()
