import tkinter as tk
from PIL import ImageGrab
import pyautogui
import time
from datetime import datetime
from models import LLamaModel
from extract_text import TextExtractor


class SnippingTool:
    def __init__(self, text_extractor, llm):

        #model settings
        self.text_extractor = text_extractor()
        self.llm = llm()

        #intialize the main window
        self.root = tk.Tk()
        self.root.title("SnipQuest") # set the window title
        self.root.geometry("600x400") # set the window size
        

        # create variables for storing coordinates 
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.is_snipping = False

        # create a button to start_snipping
        self.snip_button = tk.Button(self.root, text="start snipping", command=self.start_snipping)
        self.snip_button.pack(pady=30) # add padding to position the button

        # Create a text widget to display the LLM-processed output
        self.result_text = tk.Text(self.root, height=10, width=70, wrap="word")
        self.result_text.pack(padx=10, pady=20, expand=True, fill=tk.BOTH)  # Ensure it expands and fills the window

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
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        image_path = f"./images/snipped_image_{timestamp}.png"
        image.save(image_path)  # Save the image file
        print("Snip saved as")  # Output message to console

        # Show the snipping window again
        self.root.deiconify()  # Make the snipping window visible again

        # Display "Loading..." in the text widget while processing the text
        self.result_text.delete(1.0, tk.END)  # Clear previous text
        self.result_text.insert(tk.END, "Processing... Please wait...")  # Set loading text

        # Update the UI immediately to reflect the loading message
        self.root.update()

        # Extract text from the snipped image 
        extracted_text = self.text_extractor.extract_text_from_image(image_path)

        #get the output from llm
        llm_out = self.llm.llm_output(extracted_text)

        # Display the processed text in the text widget
        self.result_text.delete(1.0, tk.END)  # Clear previous text
        self.result_text.insert(tk.END, llm_out)  # Insert new processed text

        self.root.update()


if __name__ == "__main__":
    SnippingTool(text_extractor=TextExtractor, llm=LLamaModel)