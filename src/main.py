import customtkinter as ctk
from gui.knitter import RmdKnitter
import logging
import sys
from io import StringIO
from threading import Thread
import queue

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConsoleRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.queue = queue.Queue()

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass

def main():
    try:
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create and run the application
        app = RmdKnitter()
        
        # Set up console redirector
        console_redirector = ConsoleRedirector(app.console_widget)
        sys.stdout = console_redirector
        sys.stderr = console_redirector
        
        # Start update thread
        def update_console():
            while True:
                try:
                    text = console_redirector.queue.get_nowait()
                    app.console_widget.insert('end', text)
                    app.console_widget.see('end')
                except queue.Empty:
                    app.root.after(100, update_console)
                    break
        
        app.root.after(100, update_console)
        app.root.mainloop()
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()