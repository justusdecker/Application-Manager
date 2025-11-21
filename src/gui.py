from src.constants import *
from src.data import *

class UI(tk.LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text = text)
        self.pack()  

class JobOverview(tk.Frame):
    def __init__(self):
        pass

class TextInput(UI):
    def __init__(self, parent, text, default = None):
        super().__init__(parent, text)
        self.var = tk.StringVar(value= default)
        self.entry = ttk.Entry(self, textvariable=self.var)
        self.entry.pack()
        self.pack()
            
class TextInputMultiline(UI):
    def __init__(self, parent, text, default = None, nullable = True):
        super().__init__(parent, text)
        self.entry = tk.Text(self,height=10)
        if default is not None:
            self.entry.insert(1.0,default)
        self.nullable = nullable
        self.entry.pack()
        
    @property
    def var(self) -> str:
        return self.entry.get(1.0, tk.END)

class DropDown(UI):
    def __init__(self, parent, text, vals: list, default = None, nullable = True):
        super().__init__(parent,text)
        self.label = ttk.Label(self, text=text)
        self.var = tk.StringVar(value= default)
        self.entry = ttk.OptionMenu(self, self.var,default, *vals)

        self.nullable = nullable
        self.label.grid(column=0,row=0)
        self.entry.grid(column=1, row=0)

class JobIdAdder(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.job_title = TextInput(self, 'Job Title: ')
        self.send_button = tk.Button(self,text='add job',command=self.update)
        self.send_button.pack()
    def update(self):
        add_job_id(
            JobIds(
                name = self.job_title.var.get()
            )
        )
        
class JobApplication(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.company = TextInput(self, 'Company: ')
        
        self.job_title = DropDown(self, 'JobTitle: ', get_job_names(),'None')
        self.url = TextInput(self, 'Url: ')
        self.phone_number = TextInput(self, 'Phone Number: ')
        self.mail = TextInput(self, 'Mail: ')
        self.description = TextInputMultiline(self,'Description: ')
        self.send_button = tk.Button(self,text='add job',command=self.update)
        self.send_button.pack()
    def update(self, *_):
        company = self.company.var.get()
        job_title = get_job_id(self.job_title.var.get())
        url = self.url.var.get()
        phone_number = self.phone_number.var.get()
        mail = self.mail.var.get()
        description = self.description.var
        
        add_job(
            Jobs(
                company = company,
                title_id = job_title,
                url = url,
                phone_number = phone_number,
                mail = mail,
                description = description
            )
        )

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application-Manager")
        self.geometry("1024x768")
        self.is_running = True
        self.menu = tk.Menu(self)
        
        self.config(menu=self.menu)
        
        self.application_menu = tk.Menu(self.menu,tearoff=0)
        
        self.application_menu.add_command(label='Add Job', command=self.update_jobs)
        self.application_menu.add_command(label='Add JobTitle', command=self.update_job_ids)
        self.application_menu.add_command(label='Add ApplicationPreset')
        self.menu.add_cascade(label='Applications',menu=self.application_menu)
    def update_jobs(self):

        JobApplication()
    def update_job_ids(self):
        JobIdAdder()