import os
import tomllib
#import tkinter_embedded as tkinter
#from tkinter_embedded import ttk
#from tkinter_embedded.font import Font
import tkinter
from tkinter import ttk
from tkinter.font import Font
from chacha import ChaChaContext, BadPassphrase
from .viewer import AccountViewer
from .totp import TOTPGenerator

clipssh = None # Initialized after the interpreter is created

shortcuts = {'Open'   : u'\t\t\u2318O',
             'New'    : u'\t\t\u2318N',
             'SaveAs' : u'\t\u2318\u21e7S',
             'Quit'   : u'\t\t   \u2318Q',
             'Cut'    : u'\t\t\u2318X',
             'Copy'   : u'\t\u2318C',
             'Paste'  : u'\t\u2318V'}

class PasswordCommand:
    def __init__(self, password):
        self.password = password

    def __call__(self):
        clipssh(self.password)

class TOTPCommand:
    def __init__(self, totp_key):
        self.totp_key = totp_key

    def __call__(self):
        G = TOTPGenerator(self.totp_key)
        clipssh(G.current_token())

class AvainApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Avain')
        global clipssh
        if clipssh is None:
            import tk_clipssh
            clipssh = tk_clipssh.clipssh
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
        self._init_menus()
        self.text.focus()

    def _init_menus(self):
        self.menubar = menubar = tkinter.Menu(self)
        menubar = tkinter.Menu(self)
        Application_menu = tkinter.Menu(menubar, name="apple")
        menubar.add_cascade(label='Avain', menu=Application_menu)
        Application_menu.insert_command(0, label='About Avain ...',
            command=self.about)
        Application_menu.insert_separator(0)

        #file_menu = tkinter.Menu(menubar, name="file")
        #file_menu.add_command(label='Open...' + shortcuts['Open'],
        #                      command=self.file_open)
        #file_menu.add_command(label='New...' + shortcuts['New'],
        #                      command=self.file_new)
        #menubar.add_cascade(label='File', menu=file_menu)
        
        edit_menu = tkinter.Menu(menubar, name="file")
        edit_menu.add_command(label='Accounts ...',
                              command=self.edit_accounts)
        menubar.add_cascade(label='Edit', menu=edit_menu)

        self.password_menu = tkinter.Menu(menubar, name='passwords')
        menubar.add_cascade(label='Passwords', menu=self.password_menu)

        self.totp_menu = tkinter.Menu(menubar, name='totp')
        menubar.add_cascade(label='TOTP', menu=self.totp_menu)

        #window_menu = tkinter.Menu(menubar, name='window')
        #menubar.add_cascade(label='Window', menu=window_menu)
        self.config(menu=menubar)

    def populate_menus(self):
        for account, account_dict in sorted(self.data.items()):
            command = PasswordCommand(account_dict['password'])
            self.password_menu.add_command(label=account, command=command)
            if 'totp_key' in account_dict:
                command = TOTPCommand(account_dict['totp_key'])
                self.totp_menu.add_command(label=account, command=command)

    def check(self):
        passphrase = self.text.get('0.0', 'end').strip('\n').encode('utf-8')
        self.context = ChaChaContext(passphrase)
        home = os.environ['HOME']
        filename = os.path.join(home, '.accounts.cha')
        try:
            decrypted = self.context.decrypt_file_to_bytes(filename)
        except BadPassphrase:
            print('Incorrect Pass Phrase')
            self.text.delete('0.0', 'end')
            self.text.focus()
            return
        self.data = data = tomllib.loads(decrypted.decode('utf-8'))
        self.account_viewer = None
        self.populate_menus()
        self.withdraw()

    def edit_accounts(self):
        if not self.account_viewer:
            self.account_viewer = AccountViewer()
            self.account_viewer.load_dict(self.data)
            self.bind('<<ClipsshPaste>>', self.account_viewer.handle_paste)
        else:
            self.account_viewer.deiconify()

    def file_open(self):
        print('Open')

    def file_new(self):
        print('New')
        
    def about(self):
        print('About')

    def run(self):
        self.mainloop()

def main():
    app = AvainApp()
    app.run()

if __name__ == '__main__':
    main()
