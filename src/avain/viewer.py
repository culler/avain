#import tkinter_embedded as tkinter
#from tkinter_embedded import ttk
import tkinter as tkinter
from tkinter import ttk
from .totp import TOTPGenerator

clipssh = None # Will be initialized after there is a Tk interpreter

class Credential:
    def __init__(self, tv: ttk.Treeview)-> None:
        item_id = cursor = tv.focus()
        item_dict = tv.item(item_id)
        self.name = item_dict['text']
        values = item_dict['values']
        self.value = values[0] if values else None 
        while True:
            if tv.parent(cursor):
                cursor = tv.parent(cursor)
                continue
            break
        self.account = tv.item(cursor)['text']

    def __str__(self):
        return f' {self.account} :: {self.name} -> {self.value}'
        
class AccountViewer(tkinter.Toplevel):

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)
        self.title('GPass Accounts')
        top_frame = ttk.Frame(self)
        top_frame.columnconfigure(2, weight=1)
        self.edit_button = ttk.Button(top_frame, text='Edit Account ...')
        self.edit_button.grid(row=0, column=0, padx=10)
        ttk.Label(top_frame, text='Clip:').grid(row=0, column=1, sticky='e', padx=5)
        self.status_var = tkinter.StringVar()
        self.copy_status = ttk.Entry(top_frame, width=20, state='readonly',
                                     textvariable=self.status_var)
        self.copy_status.grid(row=0, column=2, sticky='w')
        top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.treeview = tv = ttk.Treeview(self, columns=('value'))
        sb = ttk.Scrollbar(self, command=tv.yview)
        tv.configure(yscroll=sb.set)
        tv.column('#0', stretch=False)
        tv.heading('#0', text = 'Credential Item')
        tv.heading('value', text='Value')
        tv.tag_configure('account', foreground='blue')
        tv.tag_configure('cred', foreground = 'red')   # copy to clipboard
        tv.bind('<<TreeviewSelect>>', self.item_selected)
        tv.grid(row=1, column=0, sticky='nsew')
        sb.grid(row=1, column=1, sticky='ns')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.config(menu=app.menubar)

    def close(self):
        self.app.account_viewer = None
        self.destroy()
        
    def item_selected(self, event) -> None:
        global clipssh
        if clipssh is None:
            import tk_clipssh
            clipssh = tk_clipssh.clipssh
        credential = Credential(self.treeview)
        if credential.name == 'password':
            clipssh(credential.value)
            self.status_var.set(credential.value)
        elif credential.name =='totp_key':
            G = TOTPGenerator(credential.value)
            token = G.current_token()
            clipssh(token)
            self.status_var.set(token)

    def handle_paste(self, event=None):
        self.status_var.set('')

    def load_dict(self, account_dict: dict) -> None:
        tv = self.treeview
        # Each account name is a key with dict value.
        for account, data in account_dict.items():
            id = tv.insert('', 'end', text=account, tag='account')
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        xid = tv.insert(id, 'end', text=key, tags='cred')
                        for subitem in value:
                            tv.insert(xid, 'end', text=subitem, tags='sub')
                    else:
                        self.treeview.insert(
                            id, 'end', text=key, values=[value], tag='cred')
