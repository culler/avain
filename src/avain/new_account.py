from tkinter import Toplevel

class NewAccountDialog(Toplevel):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.account = {}
        super().__init__(app, *args, **kwargs)
        self.title("New Avain Account")
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.focus_set()
        self.grab_set()
        self.wait_window(self)

    def cancel(self):
        self.destroy()

    def done(self):
        return
        
