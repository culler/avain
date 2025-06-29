import tkinter_embedded as tkinter
from tkinter_embedded import ttk
from tkinter_embedded.font import Font
from .viewer import AccountViewer
from chacha import ChaChaContext
import os
import tomllib

class GPassApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('GPass')
        self.pp_font = Font(family='Arial', size=16)
        self.tv_font = Font(family='Arial', size=14)
        stylist = ttk.Style()
        stylist.configure('Treeview',
                          foreground='blue',
                          font=self.tv_font,
                          rowheight='18p')
        self.top = ttk.Frame(self)
        ttk.Label(self.top,
                  text='Please enter your passphrase below:',
                  padding=(0,10,0,10)).grid(
                      row=0, column=0, sticky='w')
        self.top.grid(row=0, column=0)
        self.text = tkinter.Text(self, width=40, height=10, font=self.pp_font)
        self.text.grid(row=1, column=0, padx=10)
        self.bottom = ttk.Frame(self, padding=(0, 0, 0, 5))
        ttk.Button(self.bottom,
                   text='Start',
                   command=self.check).pack()
        self.bottom.grid(row=2, column=0)
        self.text.focus()

    def check(self):
        passphrase = self.text.get('0.0', 'end').strip('\n').encode('utf-8')
        self.context = ChaChaContext(passphrase)
        home = os.environ['HOME']
        filename = os.path.join(home, '.accounts.cha')
        self.account_viewer = AccountViewer()
        decrypted = self.context.decrypt_file_to_bytes(filename)
        self.data = tomllib.loads(decrypted.decode('utf-8'))
        self.account_viewer.load_dict(self.data)
        self.bind('<<ClipsshPaste>>', self.account_viewer.handle_paste)
        self.withdraw()
        
    def run(self):
        self.mainloop()

def main():
    app = GPassApp()
    app.run()

if __name__ == '__main__':
    main()
