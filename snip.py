import tkinter as tk
from PIL import ImageGrab
import pyautogui
import time

class SnippingTool:
    def __init__(self):
        #intialize the main window
        self.root = tk.Tk()
        self.root.title("Snipping Tool") # set the window title
        self.root.geometry("300x100") # set the window size
        

        # create variables for storing coordinates 
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.is_snipping = False

        # create a button to start_snipping
        self.snip_button = tk.Button(self.root, text="start snipping", command=self.start_snipping)
        self.snip_button.pack(pady=30) # add padding to position the button

        # start the Tkinter event loop
        self.root.mainloop()


    def start_snipping(self):
        self.root.withdraw() # hide the main window
        
        self.is_snipping = True

        # self.screen_image = pyautogui.screenshot() # Get full-screen screenshot to draw on
        # self.screen_image.show() # show the image to the user to select

        self.snip_window = tk.Toplevel(self.root)
        #self.snip_window.attributes("-fullscreen", True)
        self.snip_window.state('zoomed')
        self.snip_window.attributes("-alpha", 0.3) # will make the window semi-transparent
        self.snip_window.attributes("-topmost", True) # the window stays on top of every other windows
        self.snip_window.bind("<Button-1>", self.on_mouse_down) # on_mouse_down is called when user clicks on left button of mouse
        self.snip_window.bind("<B1-Motion>", self.on_mouse_drag) # on_mouse_drag is called when user drags mouse
        self.snip_window.bind("<ButtonRelease-1>", self.on_mouse_up) # when left button is released

        # Draw canvas to show selection rectangle
        self.canvas = tk.Canvas(self.snip_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = None

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect) # this deletes previous rectangle so that drawing updates smoothly
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        # Set the snipping flag to False
        self.is_snipping = False

        # Capture the final coordinates before destroying the snip window
        x1 = self.snip_window.winfo_rootx() + self.start_x
        y1 = self.snip_window.winfo_rooty() + self.start_y
        x2 = self.snip_window.winfo_rootx() + event.x
        y2 = self.snip_window.winfo_rooty() + event.y

        # Close the snip window after getting the coordinates
        self.snip_window.destroy()

        # Capture the selected region
        self.capture_snip(x1, y1, x2, y2)


    def capture_snip(self, x1, y1, x2, y2):
        # Capture the region of interest using Pillow
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Capture the selected region
        image.save("./images/snipped_image.png")  # Save the image file
        print("Snip saved as 'snipped_image.png'")  # Output message to console

        # Optionally show the captured snip (opens the image)
        image.show()
        self.root.deiconify()


if __name__ == "__main__":
    SnippingTool()