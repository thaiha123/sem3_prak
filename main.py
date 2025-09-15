import tkinter as tk
from tkinter import filedialog, ttk
from my_lib import *

# Center windows
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# number checking function
def is_number(str):
    return str.replace('.','',1).isdigit()

class lesson1:
    def __init__(self, main):
        # Init window
        self.root = tk.Toplevel(main)
        self.root.title("seminar 1")

        # Init important variables
        self.text = None
        self.clean_text = None
        self.total = None
        self.freq = None
        self.bow = None

        # Init widgets
        # Labels
        self.lb = tk.Label(self.root, text="BAG OF WORDS", font=('Arial, 14'))
        # Buttons
        self.btnText = tk.Button(self.root, text='choose text file', command= self.open_text)
        self.btnBow = tk.Button(self.root, text='generate bow', command= self.ngram_process)
        self.btnExport = tk.Button(self.root, text='export bow to csv file', command= self.to_csv)
        self.btnDraw = tk.Button(self.root, text='draw a word', command= self.draw)
        self.btnClear = tk.Button(self.root, text='clear', command= self.clear)
        self.btnExit = tk.Button(self.root, text='EXIT', command= self.close_window)
        # Option menu
        self.value_inside = tk.StringVar(self.root)
        self.value_inside.set('1')
        self.optionNgram = tk.OptionMenu(self.root, self.value_inside, *['1', '2', '3', '4', '5'])
        # Treeview table
        # Create table
        self.table = ttk.Treeview(self.root, columns=('col1', 'col2', 'col3', ), show='headings')
        self.table.heading('col1', text='ngram')
        self.table.heading('col2', text='frequency')
        self.table.heading('col3', text='total appearance')
        # Create scroll bar
        self.scroller = ttk.Scrollbar(self.root, orient='vertical', command= self.table.yview)
        self.table.configure(yscrollcommand=self.scroller.set)
        # Text boxes
        self.tboxNgram = tk.Entry(self.root, state=tk.DISABLED, width=0)
        self.tboxNgram.configure(disabledbackground='white', disabledforeground='black', width=0)
        self.tboxSentences = tk.Text(self.root, state=tk.DISABLED)

        # Packing widget
        # Define grid
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=8)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=2)
        self.root.columnconfigure(4, weight=6)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(7, weight=1)
        self.root.rowconfigure(8, weight=1)
        self.root.rowconfigure(9, weight=1)
        # Placing widgets
        self.lb.grid(row=0, column=0, columnspan=5, sticky='nsew')
        # Buttons and option menu
        self.btnText.grid(row=1, column=0, rowspan=3, padx=2, pady=2, sticky='nsew')
        self.optionNgram.grid(row=4, column=0, padx=2, pady=1, sticky='ew')
        self.btnBow.grid(row=5, column=0,  rowspan=2, padx=2, pady=2, sticky='nsew')
        self.btnExit.grid(row=7, column=0, rowspan=3, padx=2, pady=2, sticky='nsew')
        self.btnExport.grid(row=9, column=1, columnspan=2, padx=2, pady=2, sticky='nsew')
        self.btnDraw.grid(row=1, column=3, padx=1, pady=2, sticky='nsew')
        self.btnClear.grid(row=8, column=3, rowspan=2, columnspan=2, padx=2, pady=2, sticky='nsew')
        # Table
        #self.tableFrame.pack(fill='both', expand='true')
        self.table.grid(row=1, column=1, rowspan=8, sticky='nsew')
        self.scroller.grid(row=1, column=2, rowspan=8, sticky='ns')
        # Text boxes
        self.tboxNgram.grid(row=1, column=4, padx=1, pady=2, sticky='nsew')
        self.tboxSentences.grid(row=2, column=3, rowspan=6, columnspan=2, padx=2, pady=2, sticky='nsew')

        # Place window in center of the screen
        center_window(self.root)
        # Freeze main menu and focus on new window
        self.root.transient(main)
        self.root.grab_set()

        self.root.mainloop()

    def open_text(self):
        path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
        if path:
            self.text = open(path, 'r', encoding='utf8').read()
            self.clean_text = preprocessing(self.text)

    def ngram_process(self):
        if self.text != None and self.clean_text != None:
            n = self.value_inside.get()
            if int(n) <= len(self.clean_text):
                self.freq, self.total = ngram_letter_count(int(n), self.clean_text)
                # Create BOW
                self.bow = create_BOW(self.freq, self.total)
                # Clear table
                for item in self.table.get_children():
                    self.table.delete(item)
                # Load data into table for display
                df = to_df(self.freq, self.total)
                for index, row in df.iterrows():
                    self.table.insert('', 'end', values=[row['n_gram'], row['frequency'], int(round(row['total_ngrams']))])

    def to_csv(self):
        if self.freq != None or self.total != None:
            to_file(self.freq, self.total)

    def draw(self):
        # Randomly draw a word from bow and string together a sentence
        # Ngram display
        if self.bow != None:
            ngram = sample(self.bow, 1)[0]
            self.tboxNgram.config(state=tk.NORMAL)
            self.tboxNgram.delete(0, tk.END)
            self.tboxNgram.insert(tk.END, ngram)
            self.tboxNgram.config(state=tk.DISABLED)
            # sentence string
            if ngram[-1] == 'E':
                ngram += '\n'
            self.tboxSentences.config(state=tk.NORMAL)
            self.tboxSentences.insert(tk.END, ngram)
            self.tboxSentences.config(state=tk.DISABLED)

    def clear(self):
        self.tboxNgram.config(state=tk.NORMAL)
        self.tboxSentences.config(state=tk.NORMAL)
        self.tboxNgram.delete(0, tk.END)
        self.tboxSentences.delete(1.0, tk.END)
        self.tboxNgram.config(state=tk.DISABLED)
        self.tboxSentences.config(state=tk.DISABLED)
    
    def close_window(self):
        self.root.destroy()
        
class lesson3:
    def __init__(self, main):
        # Init window
        self.root = tk.Toplevel(main)
        self.root.title("seminar 3")        

        # Init important variables
        self.texts = []
        self.clean_texts = []
        self.tfidf = None

        # Init widgets
        # Labels
        self.lbTitle = tk.Label(self.root, text="TF-IDF", font=('Arial, 14'))
        self.lbNCD = tk.Label(self.root, text="choose 2 text to calculate NCD score", font="Arial, 8")
        # Buttons
        self.btnText = tk.Button(self.root, text='add text', command=self.add_text)
        self.btnDel = tk.Button(self.root, text='delete text', command=self.del_text)
        self.btnNCD = tk.Button(self.root, text='calculate NCD', command=self.get_NCD)
        self.btnEXIT = tk.Button(self.root, text='EXIT', command=self.close_window)
        # Option menus
        self.selectedOptionDel = tk.StringVar(self.root, "choose a text")
        self.selectedOption1 = tk.StringVar(self.root, "choose a text")
        self.selectedOption2 = tk.StringVar(self.root, "choose a text")
        self.optTextDel = tk.OptionMenu(self.root, self.selectedOptionDel, *["choose a text"], command=self.display)
        self.optText1 = tk.OptionMenu(self.root, self.selectedOption1, *["choose a text"])
        self.optText2 = tk.OptionMenu(self.root, self.selectedOption2, *["choose a text"])
        # Text boxes
        self.tboxInput = tk.Text(self.root, width=0)
        self.tboxDisplay = tk.Text(self.root, state=tk.DISABLED, width=0)
        self.tboxTFIDF = tk.Entry(self.root)
        self.tboxTFIDF.insert(tk.END, '0.0')
        self.tboxNCD = tk.Entry(self.root, state=tk.DISABLED)
        self.tboxNCD.configure(disabledbackground='white', disabledforeground='black')
        # Tables
        # Table frame
        self.tableFrame = tk.Frame(self.root)
        # Treeview tables
        self.tableTF = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableTF.heading('col1', text='word')
        self.tableTF.heading('col2', text='TF value')
        self.tableIDF = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableIDF.heading('col1', text='word')
        self.tableIDF.heading('col2', text='IDF value')
        self.tableTFIDF = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableTFIDF.heading('col1', text='word')
        self.tableTFIDF.heading('col2', text='TF-IDF value')
        # Scrollbar
        self.scroller1 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableTF.yview)
        self.tableTF.configure(yscrollcommand=self.scroller1.set)
        self.scroller2 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableIDF.yview)
        self.tableIDF.configure(yscrollcommand=self.scroller2.set)
        self.scroller3 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableTFIDF.yview)
        self.tableTFIDF.configure(yscrollcommand=self.scroller3.set)

        # Packing widgets
        # Packing tables and scrollbar into table frame
        self.tableTF.grid(row=0, column=0, padx=2, pady=4, sticky='nsew')
        self.scroller1.grid(row=0, column=1, pady=4, sticky='ns')
        self.tableIDF.grid(row=0, column=2, padx=2, pady=4, sticky='nsew')
        self.scroller2.grid(row=0, column=3, pady=4, sticky='ns')
        self.tableTFIDF.grid(row=0, column=4, padx=2, pady=4, sticky='nsew')
        self.scroller3.grid(row=0, column=5, pady=4, sticky='ns')
        # Define grid 10x3
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.columnconfigure(5, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(7, weight=1)
        self.root.rowconfigure(8, weight=1)
        self.root.rowconfigure(9, weight=1)
        self.root.rowconfigure(10, weight=1)
        self.root.rowconfigure(11, weight=1)
        # Labels
        self.lbTitle.grid(row=0, column=0, columnspan=6, sticky='nsew')
        # Buttons
        self.btnText.grid(row=4, column=0, padx=4, pady=4, sticky='nsew')
        self.btnDel.grid(row=4, column=4, padx=4, pady=4, sticky='nsew')
        self.btnNCD.grid(row=11, column=3, padx=4, pady=4, sticky='nsew')
        self.btnEXIT.grid(row=11, column=0, padx=4, pady=4, sticky='nsew')
        # Option menues
        self.optTextDel.grid(row=4, column=5, columnspan=2, padx=4, pady=4, sticky='ew')
        self.optText1.grid(row=10, column=2, columnspan=2, padx=4, pady=4, sticky='ew')
        self.optText2.grid(row=10, column=4, columnspan=2, padx=4, pady=4, sticky='ew')
        # Text boxes
        self.tboxInput.grid(row=1, column=0, rowspan=3, columnspan=3, padx=4, pady=4, sticky='nsew')
        self.tboxDisplay.grid(row=1, column=3, rowspan=3, columnspan=3, padx=4, pady=4, sticky='nsew')
        self.tboxTFIDF.grid(row=11, column=2, padx=4, pady=4, sticky='nsew')
        self.tboxNCD.grid(row=11, column=4, columnspan=2, padx=4, pady=4, sticky='nsew')
        # Table
        self.tableFrame.grid(row=5, column=0, rowspan=5, columnspan=6, padx=4, pady=4, sticky='nsew')

        # Place window in center of the screen
        center_window(self.root)
        # Freeze main menu and focus on new window
        self.root.transient(main)
        self.root.grab_set()

        self.root.mainloop()

    def add_text(self):
        text = self.tboxInput.get(1.0, "end-1c")
        if len(text) != 0 and preprocessing_wlist(text):
            self.texts.append(text)
            text = preprocessing_wlist(text)
            self.clean_texts.append(text)
            dic = corpora.Dictionary(self.clean_texts)
            corpus = [dic.doc2bow(text) for text in self.clean_texts]
            self.tboxInput.delete(1.0, tk.END)
            tf = compute_tf(corpus, dic)
            idf = compute_idf(corpus, dic)
            self.tfidf = compute_tfidf(corpus, dic)
            
            # Update option menus
            listTexts = []
            for i in range(0, len(self.texts)):
                listTexts.append(str(i + 1))
            self.optTextDel['menu'].delete(0, tk.END)
            self.optText1['menu'].delete(0, tk.END)
            self.optText2['menu'].delete(0, tk.END)
            # Reset selected option
            self.selectedOptionDel.set("choose a text")
            self.selectedOption1.set("choose a text")
            self.selectedOption2.set("choose a text")
            for option in listTexts:
                self.optTextDel['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDel, option, self.display))
                self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
            
            
            # Clear table
            for item in self.tableTF.get_children():
                self.tableTF.delete(item)
            for item in self.tableIDF.get_children():
                self.tableIDF.delete(item)
            for item in self.tableTFIDF.get_children():
                self.tableTFIDF.delete(item)
            # Update tables
            for index, row in tf.iterrows():
                self.tableTF.insert('', 'end', values=list(row))
            for index, row in idf.iterrows():
                self.tableIDF.insert('', 'end', values=list(row))
            for index, row in self.tfidf.iterrows():
                self.tableTFIDF.insert('', 'end', values=list(row))

    def display(self, value):
        if value != "choose a text":
            self.tboxDisplay.config(state=tk.NORMAL)
            self.tboxDisplay.delete(1.0, tk.END)
            self.tboxDisplay.insert(tk.END, self.texts[int(value) - 1])
            self.tboxDisplay.config(state=tk.DISABLED)

    def del_text(self):
        selected_text = self.selectedOptionDel.get()
        if selected_text != "choose a text":
            self.texts.pop(int(selected_text) - 1)
            self.clean_texts.pop(int(selected_text) - 1)
            self.tboxDisplay.config(state=tk.NORMAL)
            self.tboxDisplay.delete(1.0, tk.END) 
            self.tboxDisplay.config(state=tk.DISABLED)      
            
            # Reset selected option
            self.selectedOptionDel.set("choose a text")
            self.selectedOption1.set("choose a text")
            self.selectedOption2.set("choose a text")
            self.optTextDel['menu'].delete(0, tk.END)
            self.optText1['menu'].delete(0, tk.END)
            self.optText2['menu'].delete(0, tk.END)
            # Update option menus
            if len(self.texts) == 0:
                option = "choose a text"
                self.optTextDel['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDel, option, self.display))
                self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
            else:
                listTexts = []
                for i in range(0, len(self.texts)):
                    listTexts.append(str(i + 1))
                for option in listTexts:
                    self.optTextDel['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDel, option, self.display))
                    self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                    self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
            
            # Clear table
            for item in self.tableTF.get_children():
                self.tableTF.delete(item)
            for item in self.tableIDF.get_children():
                self.tableIDF.delete(item)
            for item in self.tableTFIDF.get_children():
                self.tableTFIDF.delete(item)
            # Recalculate values
            if len(self.texts) != 0:
                dic = corpora.Dictionary(self.clean_texts)
                corpus = [dic.doc2bow(text) for text in self.clean_texts]
                tf = compute_tf(corpus, dic)
                idf = compute_idf(corpus, dic)
                self.tfidf = compute_tfidf(corpus, dic)
                # Update tables
                for index, row in tf.iterrows():
                    self.tableTF.insert('', 'end', values=list(row))
                for index, row in idf.iterrows():
                    self.tableIDF.insert('', 'end', values=list(row))
                for index, row in self.tfidf.iterrows():
                    self.tableTFIDF.insert('', 'end', values=list(row))

    def get_NCD(self):
        idxText1 = self.selectedOption1.get()
        idxText2 = self.selectedOption2.get()
        threshold = self.tboxTFIDF.get()
        if len(self.texts) != 0 and idxText1 != "choose a text" and idxText2 != "choose a text" and is_number(threshold): 
            if float(threshold) > 1.0:
                threshold = '1.0'
            elif float(threshold) < 0.0:
                threshold = '0,0'
            scoresTFIDF = dict(zip(self.tfidf['word'], self.tfidf['TFIDF']))
            processed_texts = process_tfidf(scoresTFIDF, self.clean_texts, float(threshold))
            text1 = ' '.join(processed_texts[int(self.selectedOption1.get()) - 1])
            text2 = ' '.join(processed_texts[int(self.selectedOption2.get()) - 1])
            valNCD = NCD(text1, text2)
            # Print result to text box
            self.tboxNCD.config(state=tk.NORMAL)
            self.tboxNCD.delete(0, tk.END)
            self.tboxNCD.insert(tk.END, str(valNCD))
            self.tboxNCD.config(state=tk.DISABLED)

    def close_window(self):
        self.root.destroy()

class lesson4:
    def __init__(self, main):
        # Init window
        self.root = tk.Toplevel(main)
        self.root.title("seminar 4")
        
        # Init important variables
        self.texts = []
        self.clean_texts = []
        self.tf_all = []
        self.entropy_all = []

        # Init widgets
        # Labels
        self.lbTitle = tk.Label(self.root, text="SHANNON INFORMATION THEORY", font=('Arial, 14')) 
        # Buttons
        # Buttons
        self.btnText = tk.Button(self.root, text='add text', command=self.add_text)
        self.btnDel = tk.Button(self.root, text='delete text', command=self.del_text) 
        self.btnSplit = tk.Button(self.root, text='split text', command=self.split)
        self.btnCompare = tk.Button(self.root, text='calculate transinfo and NCD', command=self.compare)
        self.btnExit = tk.Button(self.root, text='EXIT', command=self.close_window)
        # Option menus
        self.selectedOptionDisplay = tk.StringVar(self.root, "choose a text")
        self.selectedOption1 = tk.StringVar(self.root, "choose a text")
        self.selectedOption2 = tk.StringVar(self.root, "choose a text")
        self.optTextDisplay = tk.OptionMenu(self.root, self.selectedOptionDisplay, *["choose a text"], command=self.display)
        self.optText1 = tk.OptionMenu(self.root, self.selectedOption1, *["choose a text"])
        self.optText2 = tk.OptionMenu(self.root, self.selectedOption2, *["choose a text"])
        # Text boxes
        self.tboxInput = tk.Text(self.root, width=0)
        self.tboxDisplay = tk.Text(self.root, state=tk.DISABLED, width=0)
        self.tboxTextLength = tk.Entry(self.root)
        self.tboxTextLength.insert(tk.END, '24')
        self.tboxBow = tk.Entry(self.root)
        self.tboxBow.insert(tk.END, '4')
        self.tboxCompare = tk.Entry(self.root, state=tk.DISABLED)
        self.tboxCompare.configure(disabledbackground='white', disabledforeground='black')
        # Tables
        # Table frame
        self.tableFrame = tk.Frame(self.root)
        # Treeview tables
        self.tableEntropy = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableEntropy.heading('col1', text='text')
        self.tableEntropy.heading('col2', text='Entropy value')
        self.tableTF = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableTF.heading('col1', text='word')
        self.tableTF.heading('col2', text='TF value')
        self.tableBow = ttk.Treeview(self.tableFrame, columns=('col1', 'col2'), show='headings')
        self.tableBow.heading('col1', text='BOW')
        self.tableBow.heading('col2', text='Entropy value')
        # Scrollbar
        self.scroller1 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableEntropy.yview)
        self.tableEntropy.configure(yscrollcommand=self.scroller1.set)
        self.scroller2 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableTF.yview)
        self.tableTF.configure(yscrollcommand=self.scroller2.set)
        self.scroller3 = tk.Scrollbar(self.tableFrame, orient='vertical', command=self.tableBow.yview)
        self.tableBow.configure(yscrollcommand=self.scroller3.set)

        # Packing widgets
        # Packing tables and scrollbar into table frame
        self.tableEntropy.grid(row=0, column=0, padx=2, pady=4, sticky='nsew')
        self.scroller1.grid(row=0, column=1, pady=4, sticky='ns')
        self.tableTF.grid(row=0, column=2, padx=2, pady=4, sticky='nsew')
        self.scroller2.grid(row=0, column=3, pady=4, sticky='ns')
        self.tableBow.grid(row=0, column=4, padx=2, pady=4, sticky='nsew')
        self.scroller3.grid(row=0, column=5, pady=4, sticky='ns')
        # Define grid 10x6
        self.root.columnconfigure(0, weight=1, uniform="col")
        self.root.columnconfigure(1, weight=1, uniform="col")
        self.root.columnconfigure(2, weight=1, uniform="col")
        self.root.columnconfigure(3, weight=1, uniform="col")
        self.root.columnconfigure(4, weight=1, uniform="col")
        self.root.columnconfigure(5, weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1, uniform="row")
        self.root.rowconfigure(1, weight=1, uniform="row")
        self.root.rowconfigure(2, weight=1, uniform="row")
        self.root.rowconfigure(3, weight=1, uniform="row")
        self.root.rowconfigure(4, weight=1, uniform="row")
        self.root.rowconfigure(5, weight=1, uniform="row")
        self.root.rowconfigure(6, weight=1, uniform="row")
        self.root.rowconfigure(7, weight=1, uniform="row")
        self.root.rowconfigure(8, weight=1, uniform="row")
        self.root.rowconfigure(9, weight=1, uniform="row")
        # Labels
        self.lbTitle.grid(row=0, column=0, columnspan=6, sticky='nsew')
        # Buttons
        self.btnText.grid(row=1, column=0, padx=4, pady=4, sticky='nsew')
        self.btnDel.grid(row=1, column=3, padx=4, pady=4, sticky='nsew')
        self.btnSplit.grid(row=4, column=5, padx=4, pady=4, sticky='nsew')
        self.btnCompare.grid(row=9, column=2, padx=4, pady=4, sticky='nsew')
        self.btnExit.grid(row=8, column=0, rowspan=2, columnspan=2, padx=20, pady=20, sticky='nsew')
        # Option menus
        self.optTextDisplay.grid(row=4, column=2, columnspan=2, padx=4, pady=4, sticky='ew')
        self.optText1.grid(row=8, column=2, columnspan=2, padx=4, pady=4, sticky='ew')
        self.optText2.grid(row=8, column=4, columnspan=2, padx=4, pady=4, sticky='ew')
        # Text boxes
        self.tboxInput.grid(row=1, column=1, rowspan=3, columnspan=2, padx=4, pady=4, sticky='nsew')
        self.tboxTextLength.grid(row=2, column=0, padx=4, pady=4, sticky='ew')
        self.tboxDisplay.grid(row=1, column=4, rowspan=3, columnspan=2, padx=4, pady=4, sticky='nsew')
        self.tboxBow.grid(row=4, column=4, padx=4, pady=4, sticky='nsew')
        self.tboxCompare.grid(row=9, column=3, columnspan=3, padx=4, pady=4, sticky='nsew')
        # Table
        self.tableFrame.grid(row=5, column=0, rowspan=3, columnspan=6, padx=4, pady=4, sticky='nsew')

        # Place window in center of the screen
        center_window(self.root)
        # Freeze main menu and focus on new window
        self.root.transient(main)
        self.root.grab_set()

    def add_text(self):
        text = self.tboxInput.get(1.0, "end-1c")
        if len(text) != 0 and preprocessing_wlist(text):
            # Preprocess added text, add filler or cut text to fit with text length
            self.texts.append(text)
            clean_text = preprocessing_wlist(text)
            self.clean_texts.append(clean_text)
            # Calculate TF and entropy for added text
            dictionary = corpora.Dictionary([clean_text])
            corpus = [dictionary.doc2bow(text) for text in [clean_text]]
            tf = compute_tf(corpus, dictionary)
            self.tf_all.append(tf)
            self.tboxInput.delete(1.0, tk.END)
            scoresTF = dict(zip(tf['word'], tf['TF']))
            self.entropy_all.append(compute_entropy(scoresTF))
            
            # Update option menus
            listTexts = []
            for i in range(0, len(self.texts)):
                listTexts.append(str(i + 1))
            self.optTextDisplay['menu'].delete(0, tk.END)
            self.optText1['menu'].delete(0, tk.END)
            self.optText2['menu'].delete(0, tk.END)
            # Reset selected option
            self.selectedOptionDisplay.set("choose a text")
            self.selectedOption1.set("choose a text")
            self.selectedOption2.set("choose a text")
            for option in listTexts:
                self.optTextDisplay['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDisplay, option, self.display))
                self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
            
            # Clear tables
            for item in self.tableEntropy.get_children():
                self.tableEntropy.delete(item)
            for item in self.tableTF.get_children():
                self.tableTF.delete(item)
            for item in self.tableBow.get_children():
                self.tableBow.delete(item)
            # Update table
            for i in range(0, len(self.entropy_all)):
                self.tableEntropy.insert('', 'end', values=(str(i + 1), str(self.entropy_all[i])))

    def display(self, value):
        if value != "choose a text":
            # Display choosen text on text box
            self.tboxDisplay.config(state=tk.NORMAL)
            self.tboxDisplay.delete(1.0, tk.END)
            self.tboxDisplay.insert(tk.END, self.texts[int(value) - 1])
            self.tboxDisplay.config(state=tk.DISABLED)
            # Display tf scores of choosen text on table
            for item in self.tableTF.get_children():
                self.tableTF.delete(item)
            for index, row in self.tf_all[int(value) - 1].iterrows():
                self.tableTF.insert('', 'end', values=list(row))
    
    def del_text(self):
        selected_text = self.selectedOptionDisplay.get()
        if selected_text != "choose a text":
            self.texts.pop(int(selected_text) - 1)
            self.clean_texts.pop(int(selected_text) - 1)
            self.tf_all.pop(int(selected_text) - 1)
            self.entropy_all.pop(int(selected_text) - 1)

            # Clear display text box
            self.tboxDisplay.config(state=tk.NORMAL)
            self.tboxDisplay.delete(1.0, tk.END)
            self.tboxDisplay.config(state=tk.DISABLED)
            # Clear option menus and tables
            self.optTextDisplay['menu'].delete(0, tk.END)
            self.optText1['menu'].delete(0, tk.END)
            self.optText2['menu'].delete(0, tk.END)
            # Reset selected option
            self.selectedOptionDisplay.set("choose a text")
            self.selectedOption1.set("choose a text")
            self.selectedOption2.set("choose a text")
            for item in self.tableTF.get_children():
                self.tableTF.delete(item)
            for item in self.tableEntropy.get_children():
                self.tableEntropy.delete(item)
            for item in self.tableBow.get_children():
                self.tableBow.delete(item)

            # Update option menus
            if len(self.texts) == 0:
                option = "choose a text"
                self.optTextDisplay['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDisplay, option, self.display))
                self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
            else:
                listTexts = []
                for i in range(0, len(self.texts)):
                    listTexts.append(str(i + 1))
                for option in listTexts:
                    self.optTextDisplay['menu'].add_command(label=option, command=tk._setit(self.selectedOptionDisplay, option, self.display))
                    self.optText1['menu'].add_command(label=option, command=tk._setit(self.selectedOption1, option))
                    self.optText2['menu'].add_command(label=option, command=tk._setit(self.selectedOption2, option))
                # Update table
                for i in range(0, len(self.entropy_all)):
                    self.tableEntropy.insert('', 'end', values=(str(i + 1), str(self.entropy_all[i])))

    def split(self):
        sizeBow = self.tboxBow.get()
        length = self.tboxTextLength.get()
        idxText = self.selectedOptionDisplay.get()
        if is_number(length) and is_number(sizeBow):
            length = int(length)
            sizeBow = int(sizeBow)
            if int(length) % sizeBow == 0 and sizeBow*2 <= int(length) and idxText != "choose a text":
                text = self.clean_texts[int(idxText) - 1].copy()
                if len(text) < length:
                    for _ in range(0, length - len(text)):
                        text.append('filler')
                elif len(text) > length:
                    text = text[:length]
                entropyBows = compute_bow_entropy(text, sizeBow)
                # Clear table
                for item in self.tableBow.get_children():
                    self.tableBow.delete(item)
                # Update table
                for i in range(0, len(entropyBows)):
                    self.tableBow.insert('', 'end', values=(str(i + 1), str(entropyBows[i])))

    def compare(self):
        idxText1 = self.selectedOption1.get()
        idxText2 = self.selectedOption2.get()
        length = self.tboxTextLength.get()
        if idxText1 != "choose a text" and idxText2 != "choose a text" and is_number(length):
            length = int(length)
            text1 = self.clean_texts[int(idxText1) - 1].copy()
            text2 = self.clean_texts[int(idxText2) - 1].copy()
            for text in [text1, text2]:
                if len(text) < length:
                    for _ in range(0, length - len(text)):
                        text.append('filler')
                elif len(text) > length:
                    text = text[:length]
            scoreTransinfo = compute_transinfo(text1, text2)
            scoreNCD = NCD(' '.join(text1), ' '.join(text2))
            # Display results
            res = "transinformation score: " + str(scoreTransinfo) + "  NCD score: " + str(scoreNCD)
            self.tboxCompare.config(state=tk.NORMAL)
            self.tboxCompare.delete(0, tk.END)
            self.tboxCompare.insert(tk.END, res)
            self.tboxCompare.config(state=tk.DISABLED)

    def close_window(self):
        self.root.destroy()

class main_menu:

    def __init__(self):
        self.root = tk.Tk()
        # Place window in center of the screen
        center_window(self.root)
        self.root.title("main menu")
        self.root.geometry("300x400")

        self.lb1 = tk.Label(self.root, text="algorithmic information theory", font=('Arial, 15'))
        self.lb1.pack(padx=4, anchor='center')
        self.lb2 = tk.Label(self.root, text="in biomedical system", font=('Arial, 15'))
        self.lb2.pack(padx=4, pady=4, anchor='center')
        self.lb = tk.Label(self.root, text="choose a seminar", font=('Arial, 15'))
        self.lb.pack(padx=10, pady=10, anchor='center')

        self.btnGrid = tk.Frame(self.root)
        self.btnGrid.columnconfigure(0, weight=1)

        self.btn1 = tk.Button(self.btnGrid, text='seminar 1', command= self.nav1)
        self.btn1.grid(column=0, row=0, padx=3, pady=3, sticky=tk.E + tk.W)
        self.btn2 = tk.Button(self.btnGrid, text='seminar 3', command=self.nav2)
        self.btn2.grid(column=0, row=1, padx=3, pady=3, sticky=tk.E + tk.W)
        self.btn3 = tk.Button(self.btnGrid, text='seminar 4', command=self.nav3)
        self.btn3.grid(column=0, row=2, padx=3, pady=3, sticky=tk.E + tk.W)

        self.btnGrid.pack(padx=10, pady=10, fill='both', anchor='center')

        self.btnExit = tk.Button(self.root, text='EXIT', command= self.close_window)
        self.btnExit.pack()

        self.root.mainloop()

    def close_window(self):
        self.root.destroy()

    def nav1(self):
        self.lesson1 = lesson1(self.root)

    def nav2(self):
        self.lesson3 = lesson3(self.root)

    def nav3(self):
        self.lesson4 = lesson4(self.root)
        

main_menu()