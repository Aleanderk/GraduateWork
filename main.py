import glob
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, ttk
import pickle
import pandas as pd
import os
import shutil
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pandastable import Table
import plotly.express as px
import plotly
from html2image import Html2Image
from PIL import ImageTk, Image
import webbrowser
import svgwrite
from sklearn.decomposition import PCA


temp_login = ''
data = pd.DataFrame()
whole_information = dict()


class UserInterface:
    def __init__(self):
        global temp_login
        global data
        global whole_information
        temp_login = ''
        data = pd.DataFrame
        whole_information = dict()
        self.window = Tk()
        self.window.title('Recommendation system with data visualization. Initial Screen')
        self.window.geometry('500x300')
        self.window.iconbitmap('icon.ico')
        self.ShowLoginVisualizationScreen()
        self.window.resizable(width=False, height=False)
        self.window.mainloop()
    def ShowLoginVisualizationScreen(self):
        global whole_information
        self.lbl1 = Label(self.window, text='Input your login:', font=('Times New Roman', 26))
        self.inpt1 = Entry(self.window, width=75)
        self.lbl2 = Label(self.window, text='Input your password:', font=('Times New Roman', 26))
        self.inpt2 = Entry(self.window, width=75)
        self.btn1 = Button(self.window, text='Log in', font=('Times new Roman', 12), width=25, command=self.Clicked_LogIn)
        self.btn2 = Button(self.window, text='Register', font=('Times new Roman', 12), width=25, command=self.Clicked_Register)
        self.lbl1.place(x=132.5, y=5)
        self.inpt1.place(x=25,y=55)
        self.lbl2.place(x=101.5, y=85)
        self.inpt2.place(x=25, y=135)
        self.btn1.place(x= 132.5, y = 175)
        self.btn2.place(x=132.5, y=225)
    def Clicked_Register(self):
        login = self.inpt1.get()
        password = self.inpt2.get()
        self.persons_dict = StateManagmentSubsystem.LoadLogInInformation(self)
        if len(login) < 3 or len(password) < 8:
            tkinter.messagebox.showerror("Register Error",
                                         "The entered username must be at least 3 characters,\n and the password must be at least 8 characters. Check the correctness.")
        elif login in self.persons_dict:
            tkinter.messagebox.showerror("Register Error",
                                         "This login already exists. Try another one.")
        else:
            global temp_login
            temp_login = login
            self.persons_dict[login] = password
            StateManagmentSubsystem().RegisterSave(self.persons_dict)
            self.window.destroy()
            StateTransitionSubsystem().GoToDataLoadingSubsystem()
    def Clicked_LogIn(self):
        login = self.inpt1.get()
        password = self.inpt2.get()
        self.persons_dict = StateManagmentSubsystem.LoadLogInInformation(self)
        if login not in self.persons_dict or (login in self.persons_dict and password != self.persons_dict[login]):
            tkinter.messagebox.showerror("LogIn Error", "There is no such login or password. Check the correctness of the entered data.")
        else:
            self.window.destroy()
            global temp_login
            temp_login = login
            StateTransitionSubsystem().GoToDataLoadingSubsystem()




class DataLoadingSubsystem:
    def __init__(self):
        self.window = Tk()
        self.window.title('Recommendation system with data visualization. Data Loading Screen')
        self.window.geometry('600x300')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(width=False, height=False)
        self.ShowLoadDataScreen()
        self.window.mainloop()
    def ShowLoadDataScreen(self):
        self.lbl1 = Label(self.window, text='Please upload your dataset in Excel format, where the names of the\n recommendation elements will be in the first column,\n and their parameters in the rest.', font=('Times New Roman', 16))
        self.lbl1.place(x=18.5, y=5)
        self.btn1 = Button(self.window, text='Choose file', font=('Times new Roman', 12), width=25,
                           command=self.Clicked_ChooseFile)
        self.btn1.place(x=180.5, y=150)
        self.btn2 = Button(self.window, text='Go to Initial Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToUserInterface)
        self.btn2.place(x=5, y=240)
        self.btn3 = Button(self.window, text='Go to Recommendation Screen', font=('Times new Roman', 12), width=22,
                           command=self.Clicked_GoToRecommendersSubsystem)
        self.btn3.place(x=196, y=240)
        self.btn4 = Button(self.window, text='Go to Visualization Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToVisualizationSubsystem)
        self.btn4.place(x=405, y=240)
    def Clicked_ChooseFile(self):
        global temp_login
        filepath = filedialog.askopenfilename(initialdir='AccountInformation\\' + temp_login + '\\Datasets', parent=self.window)
        if filepath != "":
            if filepath.endswith(".xlsx") or filepath.endswith(".xlsm") or filepath.endswith(".xlsb") or filepath.endswith(".xltx") or filepath.endswith(".xltm") or filepath.endswith(".xls") or filepath.endswith(".xlt") or filepath.endswith(".xml") or filepath.endswith(".xlam") or filepath.endswith(".xla") or filepath.endswith(".xlw") or filepath.endswith(".xlr"):
                excel_data = pd.read_excel(filepath)
                global data
                global whole_information
                whole_information = dict()
                data = pd.DataFrame(excel_data)
                whole_information['data']=data
                StateManagmentSubsystem().SaveWholeInformation()
                StateManagmentSubsystem().SaveDataLoadingSubsystemFile(filepath)
            else:
                tkinter.messagebox.showerror("File Error",

                                             "The wrong file format is selected. Try again.")
    def Data_Check(self):
        global data
        global whole_information
        if os.path.isfile('AccountInformation\\'+temp_login+'\\information.bin'):
            whole_information = StateManagmentSubsystem().DownloadDataLoadingSubsystemWholeInformation()
            data = whole_information['data']
            return True
        else:
            return False

    def Clicked_GoToUserInterface(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToUserInterface()
    def Clicked_GoToVisualizationSubsystem(self):
        if data.empty:
            if self.Data_Check():
                self.window.destroy()
                StateTransitionSubsystem().GoToVisualizationSubsystem()
            else:
                tkinter.messagebox.showerror("File Error",
                                             "The file was not found. Try the selection again.")
        else:
            self.window.destroy()
            StateTransitionSubsystem().GoToVisualizationSubsystem()

    def Clicked_GoToRecommendersSubsystem(self):
        if data.empty:
            if self.Data_Check():
                self.window.destroy()
                StateTransitionSubsystem().GoToRecommendersSubsystem()
            else:
                tkinter.messagebox.showerror("File Error",
                                             "The file was not found. Try the selection again.")
        else:
            self.window.destroy()
            StateTransitionSubsystem().GoToRecommendersSubsystem()




class VisualizationSubsystem:
    def __init__(self):
        self.window = Tk()
        self.window.title('Recommendation system with data visualization. Visualization Screen')
        self.window.geometry('620x590')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(width=False, height=False)
        self.menu_bar = Menu(self.window)
        self.history_menu = Menu(self.menu_bar, tearoff=0)
        self.history_menu.add_command(label="History", command=self.Open_History)
        self.window.config(menu=self.history_menu)
        self.ShowVisualizationScreen()
        self.window.mainloop()
    def ShowVisualizationScreen(self):
        global data
        global temp_login
        global whole_information
        self.checkbutton = BooleanVar()
        self.param_rdbtn = StringVar()
        self.temp_entry = StringVar()
        self.temp_entry.set('')
        self.param_rdbtn.set('<')
        self.checkbutton.set(True)
        self.temp_check = True
        self.check_temp = True
        self.information = dict()
        self.list_of_parameters = list(data.columns.values)
        self.list_of_visualizations = ['histogram', 'barchart', 'piechart', 'scatter']
        self.list_of_type_groups = ['By default','Sum', 'Min', 'Max', 'Avg', 'Count']
        self.lbl1 = Label(self.window,
                          text='Select the type of vizualization:',
                          font=('Times New Roman', 16))
        self.lbl1.place(x=25, y=25)
        self.combobox1 = ttk.Combobox(values=self.list_of_visualizations, state="readonly")
        self.combobox1.place(x=25, y=75)
        self.combobox1.bind('<<ComboboxSelected>>', self.UpdateVisualizationScreen)


        self.btn2 = Button(self.window, text='Go to Initial Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToUserInterface)
        self.btn2.place(x=5, y=530)
        self.btn3 = Button(self.window, text='Go to Data Loading Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToDataLoadingSubsystem)
        self.btn3.place(x=195, y=530)
        self.btn4 = Button(self.window, text='Go to Recommendation Screen', font=('Times new Roman', 12), width=22,
                           command=self.Clicked_GoToRecommendersSubsystem)
        self.btn4.place(x=385, y=530)
        if 'data_recommenders' in whole_information:
            self.btn6 = Button(self.window, text='Show recommendations', font=('Times new Roman', 12), width=20, command=self.Clicked_ShowRecommendations)
            self.btn6.place(x=195, y = 455)

        try:
            self.checkbutton.set(whole_information['visualization']['checkbutton'])
            self.param_rdbtn.set(whole_information['visualization']['rdbtn'])
            self.temp_entry.set(whole_information['visualization']['entry'])
        except:
            None
        try:
            self.combobox1.set(whole_information['visualization']['type_visualization'])
            self.combobox1.event_generate('<<ComboboxSelected>>')
        except:
            None


    def Open_History(self):
        directory = 'AccountInformation\\' + temp_login + '\\Visualizations'
        temp_filepath = filedialog.askopenfilename(initialdir=directory, filetypes = (("JPEG files", "*.jpg"), ("All files", "*.*")), parent=self.window)
        if len(temp_filepath) == 0:
            None
        elif temp_filepath[-3:] != 'jpg':
            tkinter.messagebox.showerror("Open Error",
                                         "You have selected the wrong file format. Select a JPG file.")
        else:
            try:
                os.startfile(temp_filepath)
                try:
                    if os.path.exists(temp_filepath[:-3] + 'html'):
                        webbrowser.open(temp_filepath[:-3] + 'html')
                    else:
                        raise Exception('No file!')
                except:
                    tkinter.messagebox.showerror("Open Error",
                                                 "You have no browser to open interactive visualization or you have no interactive visualization.")
            except:
                self.Make_Window()
                image = Image.open(temp_filepath)
                image = image.resize((600, 300), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                panel = Label(self.window1, image=image)
                panel.place(x=0, y=0)
                try:
                    if os.path.exists(temp_filepath[:-3] + 'html'):
                        webbrowser.open(temp_filepath[:-3] + 'html')
                    else:
                        raise Exception('No file!')
                except:
                    tkinter.messagebox.showerror("Open Error",
                                                 "You have no browser to open interactive visualization or you have no interactive visualization.")


    def dismiss1(self):
        self.window2.grab_release()
        self.window2.destroy()

    def Clicked_ShowRecommendations(self):
        self.window2 = Toplevel()
        self.window2.title('Recommendation system with data visualization. Recommendations')
        self.window2.geometry('600x300')
        self.window2.iconbitmap('icon.ico')
        self.window2.protocol("WM_DELETE_WINDOW", lambda: self.dismiss1())
        self.window2.grab_set()
        self.table2 = Table(self.window2, dataframe=whole_information['data_recommenders'],
                            showtoolbar=False, showstatusbar=False)
        self.table2.show()
        self.table2.redraw()

    def CheckCheckbuttom(self):
        self.temp_check = False
        self.combobox1.event_generate("<<ComboboxSelected>>")

    def Clicked_ShowTheRange(self):
        if self.combobox2.get() == '' or self.combobox3.get() == '':
            tkinter.messagebox.showerror("Input Error",
                                         "Not selected parameters. Try again.")
        else:
            try:
                temp_dataframe = whole_information['data_recommenders'][
                    [self.combobox2.get(), self.combobox3.get()]].copy()
            except:
                temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
            try:
                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                    float)
                min = temp_dataframe[self.combobox3.get()].min()
                max = temp_dataframe[self.combobox3.get()].max()
                tkinter.messagebox.showinfo("Message",
                                             f"The values in the column range from {min} to {max}.")
            except:
                temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                    self.combobox3.get()].count().reset_index()
                temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                    int)
                min = temp_grouped[self.combobox3.get()].min()
                max = temp_grouped[self.combobox3.get()].max()
                tkinter.messagebox.showinfo("Message",
                                            f"The values in the column range from {min} to {max}.")

    def UpdateVisualizationScreen(self, event):
        try:
            if self.temp_check:
                self.lbl2.destroy()
                self.lbl3.destroy()
                self.combobox2.destroy()
                self.combobox3.destroy()
                self.btn5.destroy()
                self.check_temp = False
                self.lbl_type.destroy()
                self.combobox_type.destroy()
            if not self.temp_check:
                self.temp_check = True
                self.rca_label.destroy()
                self.rca_cb.destroy()
                self.lbl_param.destroy()
                self.lbl_behavior.destroy()
                self.entry1.destroy()
                self.rdbtn1.destroy()
                self.rdbtn2.destroy()
                self.rdbtn3.destroy()
                self.rdbtn4.destroy()
                self.rdbtn5.destroy()
                self.lbl_param_explanation.destroy()
                self.btn_diapazon.destroy()
        except:
            None



        self.rca_label = Label(self.window,
                              text='Is it necessary to make grouping:',
                              font=('Times New Roman', 16))
        self.rca_label.place(x=310,y=25)
        self.rca_cb = Checkbutton(self.window, variable=self.checkbutton, command=self.CheckCheckbuttom)
        self.rca_cb.place(x = 590, y = 30)
        if self.checkbutton.get() and self.check_temp:
            self.lbl_param = Label(self.window,
                              text='Enter the float or int number relative\n to which the grouping will be performed:',
                              font=('Times New Roman', 16))
            self.lbl_param.place(x=10, y=230)
            self.lbl_param_explanation = Label(self.window,
                              text='When comparing for grouping, the parameter is on the right.\n Anything that does not satisfy will be grouped into the Others group.\n The grouping is based on the x-axis or the names option parameter.\n The y-axis or the value option parameter is used for comparison.',
                              font=('Times New Roman', 16))
            self.lbl_param_explanation.place(x = 10, y = 330)
            self.entry1 = ttk.Entry(textvariable=self.temp_entry, width=12)
            self.entry1.place(x=380, y=255)
            self.lbl_behavior = Label(self.window, text='Select the behavior of parameter:', font=('Times New Roman', 16))
            self.lbl_behavior.place(x=10, y=295)
            self.rdbtn1 = Radiobutton(self.window, text='<', variable=self.param_rdbtn, value='<')
            self.rdbtn1.place(x=310, y=300)
            self.rdbtn2 = Radiobutton(self.window, text='>', variable=self.param_rdbtn, value='>')
            self.rdbtn2.place(x=360, y=300)
            self.rdbtn3 = Radiobutton(self.window, text='<=', variable=self.param_rdbtn, value='<=')
            self.rdbtn3.place(x=410, y=300)
            self.rdbtn4 = Radiobutton(self.window, text='>=', variable=self.param_rdbtn, value='>=')
            self.rdbtn4.place(x=460, y=300)
            self.rdbtn5 = Radiobutton(self.window, text='=', variable=self.param_rdbtn, value='=')
            self.rdbtn5.place(x=510, y=300)
            self.btn_diapazon = Button(self.window, text='Show the range', font=('Times new Roman', 12), width=12,
                               command=self.Clicked_ShowTheRange)
            self.btn_diapazon.place(x=490, y=248)
        else:
            self.check_temp = True
        if not self.temp_check:
            None
        elif self.combobox1.get() == 'histogram':
            try:
                if whole_information['visualization']['type_visualization'] == 'histogram':
                    self.lbl2 = Label(self.window,
                              text='Select the x-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                              text='Select the y-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.set(whole_information['visualization']['x_axis'])
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.set(whole_information['visualization']['y_axis'])
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                               command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                    self.lbl_type = Label(self.window, text='Select the type of operation to visualize:', font=('Times New Roman', 16))
                    self.lbl_type.place(x=25, y = 190)
                    self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                    self.combobox_type.place(x=400, y=195)
                    self.combobox_type.set(value=whole_information['visualization']['type_groups'])
                else:
                    self.lbl2 = Label(self.window,
                                      text='Select the x-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                                      text='Select the y-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                       command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                    self.lbl_type = Label(self.window, text='Select the type of operation to visualize:', font=('Times New Roman', 16))
                    self.lbl_type.place(x=25, y = 190)
                    self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                    self.combobox_type.place(x=400, y=195)
                    self.combobox_type.set(value=self.list_of_type_groups[0])
            except:
                self.lbl2 = Label(self.window,
                                  text='Select the x-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl2.place(x=25, y=110)
                self.lbl3 = Label(self.window,
                                  text='Select the y-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl3.place(x=325, y=110)
                self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox2.place(x=35, y=150)
                self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox3.place(x=335, y=150)
                self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                   command=self.Clicked_GetVisualization)
                self.btn5.place(x=195, y=490)
                self.lbl_type = Label(self.window, text='Select the type of operation to visualize:',
                                      font=('Times New Roman', 16))
                self.lbl_type.place(x=25, y=190)
                self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                self.combobox_type.place(x=400, y=195)
                self.combobox_type.set(value=self.list_of_type_groups[0])

        elif self.combobox1.get() == 'barchart':
            try:
                if whole_information['visualization']['type_visualization'] == 'barchart':
                    self.lbl2 = Label(self.window,
                              text='Select the x-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                              text='Select the y-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.set(whole_information['visualization']['x_axis'])
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.set(whole_information['visualization']['y_axis'])
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                               command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                else:
                    self.lbl2 = Label(self.window,
                                      text='Select the x-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                                      text='Select the y-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                       command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
            except:
                self.lbl2 = Label(self.window,
                                  text='Select the x-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl2.place(x=25, y=110)
                self.lbl3 = Label(self.window,
                                  text='Select the y-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl3.place(x=325, y=110)
                self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox2.place(x=35, y=150)
                self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox3.place(x=335, y=150)
                self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                   command=self.Clicked_GetVisualization)
                self.btn5.place(x=195, y=490)

        elif self.combobox1.get() == 'piechart':
            try:
                if whole_information['visualization']['type_visualization'] == 'piechart':
                    self.lbl2 = Label(self.window,
                              text='Select the names option:',
                              font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                              text='Select the values option:',
                              font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.set(whole_information['visualization']['names'])
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.set(whole_information['visualization']['values'])
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                               command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                    self.lbl_type = Label(self.window, text='Select the type of operation to visualize:',
                                          font=('Times New Roman', 16))
                    self.lbl_type.place(x=25, y=190)
                    self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                    self.combobox_type.place(x=400, y=195)
                    self.combobox_type.set(value=whole_information['visualization']['type_groups'])
                else:
                    self.lbl2 = Label(self.window,
                                      text='Select the names option:',
                                      font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                                      text='Select the values option:',
                                      font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                       command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                    self.lbl_type = Label(self.window, text='Select the type of operation to visualize:',
                                          font=('Times New Roman', 16))
                    self.lbl_type.place(x=25, y=190)
                    self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                    self.combobox_type.place(x=400, y=195)
                    self.combobox_type.set(value=self.list_of_type_groups[0])
            except:
                self.lbl2 = Label(self.window,
                                  text='Select the names option:',
                                  font=('Times New Roman', 16))
                self.lbl2.place(x=25, y=110)
                self.lbl3 = Label(self.window,
                                  text='Select the values option:',
                                  font=('Times New Roman', 16))
                self.lbl3.place(x=325, y=110)
                self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox2.place(x=35, y=150)
                self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox3.place(x=335, y=150)
                self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                   command=self.Clicked_GetVisualization)
                self.btn5.place(x=195, y=490)
                self.lbl_type = Label(self.window, text='Select the type of operation to visualize:',
                                      font=('Times New Roman', 16))
                self.lbl_type.place(x=25, y=190)
                self.combobox_type = ttk.Combobox(values=self.list_of_type_groups, state='readonly')
                self.combobox_type.place(x=400, y=195)
                self.combobox_type.set(value=self.list_of_type_groups[0])

        elif self.combobox1.get() == 'scatter':
            try:
                if whole_information['visualization']['type_visualization'] == 'scatter':
                    self.lbl2 = Label(self.window,
                              text='Select the x-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                              text='Select the y-axis option:',
                              font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.set(whole_information['visualization']['x_axis'])
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.set(whole_information['visualization']['y_axis'])
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                               command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
                else:
                    self.lbl2 = Label(self.window,
                                      text='Select the x-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl2.place(x=25, y=110)
                    self.lbl3 = Label(self.window,
                                      text='Select the y-axis option:',
                                      font=('Times New Roman', 16))
                    self.lbl3.place(x=325, y=110)
                    self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox2.place(x=35, y=150)
                    self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                    self.combobox3.place(x=335, y=150)
                    self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                       command=self.Clicked_GetVisualization)
                    self.btn5.place(x=195, y=490)
            except:
                self.lbl2 = Label(self.window,
                                  text='Select the x-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl2.place(x=25, y=110)
                self.lbl3 = Label(self.window,
                                  text='Select the y-axis option:',
                                  font=('Times New Roman', 16))
                self.lbl3.place(x=325, y=110)
                self.combobox2 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox2.place(x=35, y=150)
                self.combobox3 = ttk.Combobox(values=self.list_of_parameters, state="readonly")
                self.combobox3.place(x=335, y=150)
                self.btn5 = Button(self.window, text='Get visualization', font=('Times new Roman', 12), width=20,
                                   command=self.Clicked_GetVisualization)
                self.btn5.place(x=195, y=490)

    def dismiss(self):
        self.window1.grab_release()
        self.window1.destroy()

    def Make_Window(self):
        self.window1 = Toplevel()
        self.window1.title('Recommendation system with data visualization. Visualization Screen')
        self.window1.geometry('600x350')
        self.window1.resizable(width=False, height=False)
        self.window1.iconbitmap('icon.ico')
        self.window1.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())
        self.window1.grab_set()

    def Check_Entry(self):
        try:
            int(self.entry1.get())
            return False
        except:
            try:
                float(self.entry1.get())
                return False
            except:
                return True

    def Clicked_GetVisualization(self):
        if self.combobox2.get() == '' or self.combobox3.get() == '' or (self.checkbutton.get() and (len(self.entry1.get()) == 0 or self.entry1.get().isspace())):
            tkinter.messagebox.showerror("Input Error",
                                         "Not selected parameters. Try again.")
        elif self.checkbutton.get() and self.Check_Entry():
            tkinter.messagebox.showerror("Input Error",
                                         "The entered value does not match the format. Try again.")
        else:
            if self.combobox1.get() == 'histogram':
                try:
                    if whole_information['visualization']['type_visualization'] == 'histogram' and \
                            whole_information['visualization']['x_axis'] == self.combobox2.get() and \
                            whole_information['visualization']['y_axis'] == self.combobox3.get() and whole_information['visualization']['type_groups'] == self.combobox_type.get() and whole_information['visualization']['checkbutton']==self.checkbutton.get():
                        if self.checkbutton.get():
                            if whole_information['visualization']['entry'] == self.entry1.get() and whole_information['visualization']['rdbtn'] == self.param_rdbtn.get():
                                self.file_path_img = whole_information['visualization']['image']
                                self.file_path_html = whole_information['visualization']['html']
                            else:
                                raise Exception("Not equal!")
                        else:
                            self.file_path_img = whole_information['visualization']['image']
                            self.file_path_html = whole_information['visualization']['html']

                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()

                    else:
                        raise Exception("Error!")
                except:
                    if self.checkbutton.get():
                        if self.combobox_type.get() == self.list_of_type_groups[0]:
                            try:
                                temp_dataframe = whole_information['data_recommenders'][
                                    [self.combobox2.get(), self.combobox3.get()]].copy()
                            except:
                                temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                if self.param_rdbtn.get() == '<':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] < float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] > float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '<=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] == float(self.entry1.get()), 'Others')

                                grouped = temp_dataframe.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                fig = px.histogram(grouped, x='Groups',
                                                   y=self.combobox3.get())
                                fig.update_layout(yaxis_title=f'{self.combobox_type.get()} of {self.combobox3.get()}')
                                self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                    fig)
                                self.information['type_visualization'] = 'histogram'
                                self.information['x_axis'] = self.combobox2.get()
                                self.information['y_axis'] = self.combobox3.get()
                                self.information['image'] = self.file_path_img
                                self.information['html'] = self.file_path_html
                                self.information['checkbutton'] = self.checkbutton.get()
                                self.information['entry'] = self.temp_entry.get()
                                self.information['rdbtn'] = self.param_rdbtn.get()
                                self.information['type_groups'] = self.combobox_type.get()

                                whole_information['visualization'] = self.information
                                try:
                                    os.startfile(self.file_path_img)
                                    self.Clicked_GetInteractiveVisualization()
                                except:
                                    self.Make_Window()
                                    self.image = Image.open(self.file_path_img)
                                    self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                    self.image = ImageTk.PhotoImage(self.image)
                                    self.panel = Label(self.window1, image=self.image)
                                    self.panel.place(x=0, y=0)
                                    self.Clicked_GetInteractiveVisualization()


                                StateManagmentSubsystem.SaveWholeInformation(self)
                            except:
                                temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                    int)
                                try:
                                    int(self.entry1.get())
                                    if self.param_rdbtn.get() == '<':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '<=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                    grouped = temp_grouped.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                    fig = px.histogram(grouped, x='Groups',
                                                       y=self.combobox3.get())
                                    fig.update_layout(
                                        yaxis_title=f'{self.combobox_type.get()} of {self.combobox3.get()}')
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'histogram'
                                    self.information['x_axis'] = self.combobox2.get()
                                    self.information['y_axis'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()
  

                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "The entered parameter does not match the column type. Try again.")
                        else:
                            try:
                                temp_dataframe = whole_information['data_recommenders'][
                                    [self.combobox2.get(), self.combobox3.get()]].copy()
                            except:
                                temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                            if self.combobox_type.get() != 'Count':
                                try:
                                    temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                        float)
                                    try:
                                        if self.param_rdbtn.get() == '<':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] < float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '>':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] > float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '<=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '>=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] == float(self.entry1.get()),
                                                'Others')

                                        grouped = None
                                        if self.combobox_type.get() == 'Sum':
                                            grouped = temp_dataframe.groupby('Groups')[
                                            self.combobox3.get()].sum().reset_index()
                                        elif self.combobox_type.get() == 'Min':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].min().reset_index()
                                        elif self.combobox_type.get() == 'Max':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].max().reset_index()
                                        elif self.combobox_type.get() == 'Avg':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].avg().reset_index()

                                        fig = px.histogram(grouped, x='Groups',
                                                           y=self.combobox3.get())
                                        fig.update_layout(
                                            yaxis_title=f'{self.combobox_type.get()} of {self.combobox3.get()}')
                                        self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                            fig)
                                        self.information['type_visualization'] = 'histogram'
                                        self.information['x_axis'] = self.combobox2.get()
                                        self.information['y_axis'] = self.combobox3.get()
                                        self.information['image'] = self.file_path_img
                                        self.information['html'] = self.file_path_html
                                        self.information['checkbutton'] = self.checkbutton.get()
                                        self.information['entry'] = self.temp_entry.get()
                                        self.information['rdbtn'] = self.param_rdbtn.get()
                                        self.information['type_groups'] = self.combobox_type.get()

                                        whole_information['visualization'] = self.information
                                        try:
                                            os.startfile(self.file_path_img)
                                            self.Clicked_GetInteractiveVisualization()
                                        except:
                                            self.Make_Window()
                                            self.image = Image.open(self.file_path_img)
                                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                            self.image = ImageTk.PhotoImage(self.image)
                                            self.panel = Label(self.window1, image=self.image)
                                            self.panel.place(x=0, y=0)
                                            self.Clicked_GetInteractiveVisualization()
   

                                        StateManagmentSubsystem.SaveWholeInformation(self)
                                    except:
                                        tkinter.messagebox.showerror("Input Error",
                                                                     "The entered parameter does not match the column type or operation. Try again.")
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "Only the Count or Default operation can be perfomed with these columns. Try again.")
                            else:
                                temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                    int)
                                try:
                                    int(self.entry1.get())
                                    if self.param_rdbtn.get() == '<':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '<=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                    grouped = temp_grouped.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                    fig = px.histogram(grouped, x='Groups',
                                                       y=self.combobox3.get())
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'histogram'
                                    self.information['x_axis'] = self.combobox2.get()
                                    self.information['y_axis'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()
  

                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "The entered parameter does not match the column type. Try again.")
                    else:
                        if self.combobox_type.get() == self.list_of_type_groups[0]:
                            temp_dataframe = None
                            try:
                                temp_dataframe = whole_information['data_recommenders'].copy()
                            except:
                                temp_dataframe = data
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                fig = px.histogram(temp_dataframe, x=self.combobox2.get(),
                                                   y=self.combobox3.get())
                            except:
                                temp_dataframe = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    int)
                                fig = px.histogram(temp_dataframe, x=self.combobox2.get(),
                                                   y=self.combobox3.get())
                                fig.update_layout(
                                    yaxis_title=f'Count of {self.combobox3.get()}')

                            self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                fig)
                            self.information['type_visualization'] = 'histogram'
                            self.information['x_axis'] = self.combobox2.get()
                            self.information['y_axis'] = self.combobox3.get()
                            self.information['image'] = self.file_path_img
                            self.information['html'] = self.file_path_html
                            self.information['checkbutton'] = self.checkbutton.get()
                            self.information['entry'] = self.temp_entry.get()
                            self.information['rdbtn'] = self.param_rdbtn.get()
                            self.information['type_groups'] = self.combobox_type.get()

                            whole_information['visualization'] = self.information
                            try:
                                os.startfile(self.file_path_img)
                                self.Clicked_GetInteractiveVisualization()
                            except:
                                self.Make_Window()
                                self.image = Image.open(self.file_path_img)
                                self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                self.image = ImageTk.PhotoImage(self.image)
                                self.panel = Label(self.window1, image=self.image)
                                self.panel.place(x=0, y=0)
                                self.Clicked_GetInteractiveVisualization()


                            StateManagmentSubsystem.SaveWholeInformation(self)
                        else:
                            temp_dataframe = None
                            try:
                                temp_dataframe = whole_information['data_recommenders'].copy()
                            except:
                                temp_dataframe = data.copy()
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                try:
                                    grouped = None
                                    if self.combobox_type.get() == 'Sum':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].sum().reset_index()
                                    elif self.combobox_type.get() == 'Min':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].min().reset_index()
                                    elif self.combobox_type.get() == 'Max':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].max().reset_index()
                                    elif self.combobox_type.get() == 'Avg':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].avg().reset_index()
                                    elif self.combobox_type.get() == 'Count':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].count().reset_index()

                                    fig = px.histogram(grouped, x=self.combobox2.get(),
                                                       y=self.combobox3.get())
                                    fig.update_layout(
                                        yaxis_title=f'{self.combobox_type.get()} of {self.combobox3.get()}')
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'histogram'
                                    self.information['x_axis'] = self.combobox2.get()
                                    self.information['y_axis'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()
    

                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "Only the Count or Default operation can be perfomed with these columns. Try again.")
                            except:
                                tkinter.messagebox.showerror("Input Error",
                                                             "Only the Count or Default operation can be perfomed with these columns. Try again.")

            elif self.combobox1.get() == 'barchart':
                try:
                    if whole_information['visualization']['type_visualization'] == 'barchart' and \
                            whole_information['visualization']['x_axis'] == self.combobox2.get() and \
                            whole_information['visualization']['y_axis'] == self.combobox3.get() and \
                            whole_information['visualization']['checkbutton'] == self.checkbutton.get():
                        if self.checkbutton.get():
                            if whole_information['visualization']['entry'] == self.entry1.get() and \
                                    whole_information['visualization']['rdbtn'] == self.param_rdbtn.get():
                                self.file_path_img = whole_information['visualization']['image']
                                self.file_path_html = whole_information['visualization']['html']
                            else:
                                raise Exception("Not equal!")
                        else:
                            self.file_path_img = whole_information['visualization']['image']
                            self.file_path_html = whole_information['visualization']['html']

                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()

                    else:
                        raise Exception("Error!")
                except:
                    if self.checkbutton.get():
                        try:
                            temp_dataframe = whole_information['data_recommenders'][
                                [self.combobox2.get(), self.combobox3.get()]].copy()
                        except:
                            temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                        try:
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                float)
                            if self.param_rdbtn.get() == '<':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] < float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '>':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] > float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '<=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '>=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] == float(self.entry1.get()), 'Others')

                            grouped = temp_dataframe.reset_index()

                            fig = px.bar(grouped, x='Groups',
                                               y=self.combobox3.get())
                            self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                fig)
                            self.information['type_visualization'] = 'barchart'
                            self.information['x_axis'] = self.combobox2.get()
                            self.information['y_axis'] = self.combobox3.get()
                            self.information['image'] = self.file_path_img
                            self.information['html'] = self.file_path_html
                            self.information['checkbutton'] = self.checkbutton.get()
                            self.information['entry'] = self.temp_entry.get()
                            self.information['rdbtn'] = self.param_rdbtn.get()

                            whole_information['visualization'] = self.information
                            try:
                                os.startfile(self.file_path_img)
                                self.Clicked_GetInteractiveVisualization()
                            except:
                                self.Make_Window()
                                self.image = Image.open(self.file_path_img)
                                self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                self.image = ImageTk.PhotoImage(self.image)
                                self.panel = Label(self.window1, image=self.image)
                                self.panel.place(x=0, y=0)
                                self.Clicked_GetInteractiveVisualization()


                            StateManagmentSubsystem.SaveWholeInformation(self)
                        except:
                            temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                self.combobox3.get()].count().reset_index()
                            temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                int)
                            try:
                                int(self.entry1.get())
                                if self.param_rdbtn.get() == '<':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '<=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                grouped = temp_grouped.reset_index()

                                fig = px.bar(grouped, x='Groups',
                                                   y=self.combobox3.get())
                                self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                    fig)
                                self.information['type_visualization'] = 'barchart'
                                self.information['x_axis'] = self.combobox2.get()
                                self.information['y_axis'] = self.combobox3.get()
                                self.information['image'] = self.file_path_img
                                self.information['html'] = self.file_path_html
                                self.information['checkbutton'] = self.checkbutton.get()
                                self.information['entry'] = self.temp_entry.get()
                                self.information['rdbtn'] = self.param_rdbtn.get()

                                whole_information['visualization'] = self.information
                                try:
                                    os.startfile(self.file_path_img)
                                    self.Clicked_GetInteractiveVisualization()
                                except:
                                    self.Make_Window()
                                    self.image = Image.open(self.file_path_img)
                                    self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                    self.image = ImageTk.PhotoImage(self.image)
                                    self.panel = Label(self.window1, image=self.image)
                                    self.panel.place(x=0, y=0)
                                    self.Clicked_GetInteractiveVisualization()


                                StateManagmentSubsystem.SaveWholeInformation(self)
                            except:
                                tkinter.messagebox.showerror("Input Error",
                                                             "The entered parameter does not match the column type. Try again.")
                    else:
                        temp_dataframe = None
                        try:
                            temp_dataframe = whole_information['data_recommenders'].copy()
                        except:
                            temp_dataframe = data
                        try:
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                float)
                            fig = px.bar(temp_dataframe, x=self.combobox2.get(),
                                               y=self.combobox3.get())
                        except:
                            temp_dataframe = temp_dataframe.groupby(self.combobox2.get())[
                                self.combobox3.get()].count().reset_index()
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                int)
                            fig = px.bar(temp_dataframe, x=self.combobox2.get(),
                                               y=self.combobox3.get())
                            fig.update_layout(
                                yaxis_title=f'Count of {self.combobox3.get()}')

                        self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                            fig)
                        self.information['type_visualization'] = 'barchart'
                        self.information['x_axis'] = self.combobox2.get()
                        self.information['y_axis'] = self.combobox3.get()
                        self.information['image'] = self.file_path_img
                        self.information['html'] = self.file_path_html
                        self.information['checkbutton'] = self.checkbutton.get()
                        self.information['entry'] = self.temp_entry.get()
                        self.information['rdbtn'] = self.param_rdbtn.get()

                        whole_information['visualization'] = self.information
                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()


                        StateManagmentSubsystem.SaveWholeInformation(self)



            elif self.combobox1.get() == 'piechart':
                try:
                    if whole_information['visualization']['type_visualization'] == 'piechart' and \
                            whole_information['visualization']['names'] == self.combobox2.get() and \
                            whole_information['visualization']['values'] == self.combobox3.get() and \
                            whole_information['visualization']['type_groups'] == self.combobox_type.get() and \
                            whole_information['visualization']['checkbutton'] == self.checkbutton.get():
                        if self.checkbutton.get():
                            if whole_information['visualization']['entry'] == self.entry1.get() and \
                                    whole_information['visualization']['rdbtn'] == self.param_rdbtn.get():
                                self.file_path_img = whole_information['visualization']['image']
                                self.file_path_html = whole_information['visualization']['html']
                            else:
                                raise Exception("Not equal!")
                        else:
                            self.file_path_img = whole_information['visualization']['image']
                            self.file_path_html = whole_information['visualization']['html']

                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()

                    else:
                        raise Exception("Error!")
                except:
                    if self.checkbutton.get():
                        if self.combobox_type.get() == self.list_of_type_groups[0]:
                            try:
                                temp_dataframe = whole_information['data_recommenders'][
                                    [self.combobox2.get(), self.combobox3.get()]].copy()
                            except:
                                temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                if self.param_rdbtn.get() == '<':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] < float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] > float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '<=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '=':
                                    temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                        temp_dataframe[self.combobox3.get()] == float(self.entry1.get()), 'Others')

                                grouped = temp_dataframe.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                fig = px.pie(grouped, names='Groups',
                                                   values=self.combobox3.get())
                                self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                    fig)
                                self.information['type_visualization'] = 'piechart'
                                self.information['names'] = self.combobox2.get()
                                self.information['values'] = self.combobox3.get()
                                self.information['image'] = self.file_path_img
                                self.information['html'] = self.file_path_html
                                self.information['checkbutton'] = self.checkbutton.get()
                                self.information['entry'] = self.temp_entry.get()
                                self.information['rdbtn'] = self.param_rdbtn.get()
                                self.information['type_groups'] = self.combobox_type.get()

                                whole_information['visualization'] = self.information
                                try:
                                    os.startfile(self.file_path_img)
                                    self.Clicked_GetInteractiveVisualization()
                                except:
                                    self.Make_Window()
                                    self.image = Image.open(self.file_path_img)
                                    self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                    self.image = ImageTk.PhotoImage(self.image)
                                    self.panel = Label(self.window1, image=self.image)
                                    self.panel.place(x=0, y=0)
                                    self.Clicked_GetInteractiveVisualization()


                                StateManagmentSubsystem.SaveWholeInformation(self)
                            except:
                                temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                    int)
                                try:
                                    int(self.entry1.get())
                                    if self.param_rdbtn.get() == '<':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '<=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                    grouped = temp_grouped.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                    fig = px.pie(grouped, names='Groups',
                                                       values=self.combobox3.get())
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'piechart'
                                    self.information['names'] = self.combobox2.get()
                                    self.information['values'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()


                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "The entered parameter does not match the column type. Try again.")
                        else:
                            try:
                                temp_dataframe = whole_information['data_recommenders'][
                                    [self.combobox2.get(), self.combobox3.get()]].copy()
                            except:
                                temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                            if self.combobox_type.get() != 'Count':
                                try:
                                    temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                        float)
                                    try:
                                        if self.param_rdbtn.get() == '<':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] < float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '>':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] > float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '<=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '>=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()),
                                                'Others')
                                        elif self.param_rdbtn.get() == '=':
                                            temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                                temp_dataframe[self.combobox3.get()] == float(self.entry1.get()),
                                                'Others')

                                        grouped = None
                                        if self.combobox_type.get() == 'Sum':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].sum().reset_index()
                                        elif self.combobox_type.get() == 'Min':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].min().reset_index()
                                        elif self.combobox_type.get() == 'Max':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].max().reset_index()
                                        elif self.combobox_type.get() == 'Avg':
                                            grouped = temp_dataframe.groupby('Groups')[
                                                self.combobox3.get()].avg().reset_index()

                                        fig = px.pie(grouped, names='Groups',
                                                           values=self.combobox3.get())

                                        self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                            fig)
                                        self.information['type_visualization'] = 'piechart'
                                        self.information['names'] = self.combobox2.get()
                                        self.information['values'] = self.combobox3.get()
                                        self.information['image'] = self.file_path_img
                                        self.information['html'] = self.file_path_html
                                        self.information['checkbutton'] = self.checkbutton.get()
                                        self.information['entry'] = self.temp_entry.get()
                                        self.information['rdbtn'] = self.param_rdbtn.get()
                                        self.information['type_groups'] = self.combobox_type.get()

                                        whole_information['visualization'] = self.information
                                        try:
                                            os.startfile(self.file_path_img)
                                            self.Clicked_GetInteractiveVisualization()
                                        except:
                                            self.Make_Window()
                                            self.image = Image.open(self.file_path_img)
                                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                            self.image = ImageTk.PhotoImage(self.image)
                                            self.panel = Label(self.window1, image=self.image)
                                            self.panel.place(x=0, y=0)
                                            self.Clicked_GetInteractiveVisualization()
 

                                        StateManagmentSubsystem.SaveWholeInformation(self)
                                    except:
                                        tkinter.messagebox.showerror("Input Error",
                                                                     "The entered parameter does not match the column type or operation. Try again.")
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "Only the Count or Default operation can be perfomed with these columns. Try again.")
                            else:
                                temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                    int)
                                try:
                                    int(self.entry1.get())
                                    if self.param_rdbtn.get() == '<':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '<=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '>=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                    elif self.param_rdbtn.get() == '=':
                                        temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                            temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                    grouped = temp_grouped.groupby('Groups')[self.combobox3.get()].sum().reset_index()

                                    fig = px.pie(grouped, names='Groups',
                                                       values=self.combobox3.get())
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'piechart'
                                    self.information['mames'] = self.combobox2.get()
                                    self.information['values'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()
 

                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "The entered parameter does not match the column type. Try again.")
                    else:
                        if self.combobox_type.get() == self.list_of_type_groups[0]:
                            temp_dataframe = None
                            try:
                                temp_dataframe = whole_information['data_recommenders'].copy()
                            except:
                                temp_dataframe = data
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                fig = px.pie(temp_dataframe, names=self.combobox2.get(),
                                                   values=self.combobox3.get())
                            except:
                                temp_dataframe = temp_dataframe.groupby(self.combobox2.get())[
                                    self.combobox3.get()].count().reset_index()
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    int)
                                fig = px.pie(temp_dataframe, names=self.combobox2.get(),
                                                   values=self.combobox3.get())

                            self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                fig)
                            self.information['type_visualization'] = 'piechart'
                            self.information['names'] = self.combobox2.get()
                            self.information['values'] = self.combobox3.get()
                            self.information['image'] = self.file_path_img
                            self.information['html'] = self.file_path_html
                            self.information['checkbutton'] = self.checkbutton.get()
                            self.information['entry'] = self.temp_entry.get()
                            self.information['rdbtn'] = self.param_rdbtn.get()
                            self.information['type_groups'] = self.combobox_type.get()

                            whole_information['visualization'] = self.information
                            try:
                                os.startfile(self.file_path_img)
                                self.Clicked_GetInteractiveVisualization()
                            except:
                                self.Make_Window()
                                self.image = Image.open(self.file_path_img)
                                self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                self.image = ImageTk.PhotoImage(self.image)
                                self.panel = Label(self.window1, image=self.image)
                                self.panel.place(x=0, y=0)
                                self.Clicked_GetInteractiveVisualization()
 
                            StateManagmentSubsystem.SaveWholeInformation(self)
                        else:
                            temp_dataframe = None
                            try:
                                temp_dataframe = whole_information['data_recommenders'].copy()
                            except:
                                temp_dataframe = data.copy()
                            try:
                                temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                    float)
                                try:
                                    grouped = None
                                    if self.combobox_type.get() == 'Sum':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].sum().reset_index()
                                    elif self.combobox_type.get() == 'Min':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].min().reset_index()
                                    elif self.combobox_type.get() == 'Max':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].max().reset_index()
                                    elif self.combobox_type.get() == 'Avg':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].avg().reset_index()
                                    elif self.combobox_type.get() == 'Count':
                                        grouped = temp_dataframe.groupby(self.combobox2.get())[
                                            self.combobox3.get()].count().reset_index()

                                    fig = px.pie(grouped, names=self.combobox2.get(),
                                                 values=self.combobox3.get())
                                    self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                        fig)
                                    self.information['type_visualization'] = 'piechart'
                                    self.information['names'] = self.combobox2.get()
                                    self.information['values'] = self.combobox3.get()
                                    self.information['image'] = self.file_path_img
                                    self.information['html'] = self.file_path_html
                                    self.information['checkbutton'] = self.checkbutton.get()
                                    self.information['entry'] = self.temp_entry.get()
                                    self.information['rdbtn'] = self.param_rdbtn.get()
                                    self.information['type_groups'] = self.combobox_type.get()

                                    whole_information['visualization'] = self.information
                                    try:
                                        os.startfile(self.file_path_img)
                                        self.Clicked_GetInteractiveVisualization()
                                    except:
                                        self.Make_Window()
                                        self.image = Image.open(self.file_path_img)
                                        self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                        self.image = ImageTk.PhotoImage(self.image)
                                        self.panel = Label(self.window1, image=self.image)
                                        self.panel.place(x=0, y=0)
                                        self.Clicked_GetInteractiveVisualization()


                                    StateManagmentSubsystem.SaveWholeInformation(self)
                                except:
                                    tkinter.messagebox.showerror("Input Error",
                                                                 "Only the Count or Default operation can be perfomed with these columns. Try again.")
                            except:
                                tkinter.messagebox.showerror("Input Error",
                                                             "Only the Count or Default operation can be perfomed with these columns. Try again.")

            elif self.combobox1.get() == 'scatter':
                try:
                    if whole_information['visualization']['type_visualization'] == 'scatter' and \
                            whole_information['visualization']['x_axis'] == self.combobox2.get() and \
                            whole_information['visualization']['y_axis'] == self.combobox3.get() and \
                            whole_information['visualization']['checkbutton'] == self.checkbutton.get():
                        if self.checkbutton.get():
                            if whole_information['visualization']['entry'] == self.entry1.get() and \
                                    whole_information['visualization']['rdbtn'] == self.param_rdbtn.get():
                                self.file_path_img = whole_information['visualization']['image']
                                self.file_path_html = whole_information['visualization']['html']
                            else:
                                raise Exception("Not equal!")
                        else:
                            self.file_path_img = whole_information['visualization']['image']
                            self.file_path_html = whole_information['visualization']['html']

                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()
 
                    else:
                        raise Exception("Error!")
                except:
                    if self.checkbutton.get():
                        try:
                            temp_dataframe = whole_information['data_recommenders'][
                                [self.combobox2.get(), self.combobox3.get()]].copy()
                        except:
                            temp_dataframe = data[[self.combobox2.get(), self.combobox3.get()]].copy()
                        try:
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                float)
                            if self.param_rdbtn.get() == '<':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] < float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '>':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] > float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '<=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] <= float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '>=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] >= float(self.entry1.get()), 'Others')
                            elif self.param_rdbtn.get() == '=':
                                temp_dataframe['Groups'] = temp_dataframe[self.combobox2.get()].where(
                                    temp_dataframe[self.combobox3.get()] == float(self.entry1.get()), 'Others')

                            grouped = temp_dataframe.reset_index()

                            fig = px.scatter(grouped, x='Groups',
                                               y=self.combobox3.get())
                            self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                fig)
                            self.information['type_visualization'] = 'scatter'
                            self.information['x_axis'] = self.combobox2.get()
                            self.information['y_axis'] = self.combobox3.get()
                            self.information['image'] = self.file_path_img
                            self.information['html'] = self.file_path_html
                            self.information['checkbutton'] = self.checkbutton.get()
                            self.information['entry'] = self.temp_entry.get()
                            self.information['rdbtn'] = self.param_rdbtn.get()

                            whole_information['visualization'] = self.information
                            try:
                                os.startfile(self.file_path_img)
                                self.Clicked_GetInteractiveVisualization()
                            except:
                                self.Make_Window()
                                self.image = Image.open(self.file_path_img)
                                self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                self.image = ImageTk.PhotoImage(self.image)
                                self.panel = Label(self.window1, image=self.image)
                                self.panel.place(x=0, y=0)
                                self.Clicked_GetInteractiveVisualization()
 
                            StateManagmentSubsystem.SaveWholeInformation(self)
                        except:
                            temp_grouped = temp_dataframe.groupby(self.combobox2.get())[
                                self.combobox3.get()].count().reset_index()
                            temp_grouped[self.combobox3.get()] = temp_grouped[self.combobox3.get()].astype(
                                int)
                            try:
                                int(self.entry1.get())
                                if self.param_rdbtn.get() == '<':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] < int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] > int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '<=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] <= int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '>=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] >= int(self.entry1.get()), 'Others')
                                elif self.param_rdbtn.get() == '=':
                                    temp_grouped['Groups'] = temp_grouped[self.combobox2.get()].where(
                                        temp_grouped[self.combobox3.get()] == int(self.entry1.get()), 'Others')

                                grouped = temp_grouped.reset_index()

                                fig = px.scatter(grouped, x='Groups',
                                                   y=self.combobox3.get())
                                self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                                    fig)
                                self.information['type_visualization'] = 'scatter'
                                self.information['x_axis'] = self.combobox2.get()
                                self.information['y_axis'] = self.combobox3.get()
                                self.information['image'] = self.file_path_img
                                self.information['html'] = self.file_path_html
                                self.information['checkbutton'] = self.checkbutton.get()
                                self.information['entry'] = self.temp_entry.get()
                                self.information['rdbtn'] = self.param_rdbtn.get()

                                whole_information['visualization'] = self.information
                                try:
                                    os.startfile(self.file_path_img)
                                    self.Clicked_GetInteractiveVisualization()
                                except:
                                    self.Make_Window()
                                    self.image = Image.open(self.file_path_img)
                                    self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                                    self.image = ImageTk.PhotoImage(self.image)
                                    self.panel = Label(self.window1, image=self.image)
                                    self.panel.place(x=0, y=0)
                                    self.Clicked_GetInteractiveVisualization()

                                StateManagmentSubsystem.SaveWholeInformation(self)
                            except:
                                tkinter.messagebox.showerror("Input Error",
                                                             "The entered parameter does not match the column type. Try again.")
                    else:
                        temp_dataframe = None
                        try:
                            temp_dataframe = whole_information['data_recommenders'].copy()
                        except:
                            temp_dataframe = data
                        try:
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                float)
                            fig = px.scatter(temp_dataframe, x=self.combobox2.get(),
                                         y=self.combobox3.get())
                        except:
                            temp_dataframe = temp_dataframe.groupby(self.combobox2.get())[
                                self.combobox3.get()].count().reset_index()
                            temp_dataframe[self.combobox3.get()] = temp_dataframe[self.combobox3.get()].astype(
                                int)
                            fig = px.scatter(temp_dataframe, x=self.combobox2.get(),
                                         y=self.combobox3.get())
                            fig.update_layout(
                                yaxis_title=f'Count of {self.combobox3.get()}')

                        self.file_path_img, self.file_path_html = StateManagmentSubsystem().SaveVisualizationSubsystemImj(
                            fig)
                        self.information['type_visualization'] = 'scatter'
                        self.information['x_axis'] = self.combobox2.get()
                        self.information['y_axis'] = self.combobox3.get()
                        self.information['image'] = self.file_path_img
                        self.information['html'] = self.file_path_html
                        self.information['checkbutton'] = self.checkbutton.get()
                        self.information['entry'] = self.temp_entry.get()
                        self.information['rdbtn'] = self.param_rdbtn.get()

                        whole_information['visualization'] = self.information
                        try:
                            os.startfile(self.file_path_img)
                            self.Clicked_GetInteractiveVisualization()
                        except:
                            self.Make_Window()
                            self.image = Image.open(self.file_path_img)
                            self.image = self.image.resize((600, 300), Image.ANTIALIAS)
                            self.image = ImageTk.PhotoImage(self.image)
                            self.panel = Label(self.window1, image=self.image)
                            self.panel.place(x=0, y=0)
                            self.Clicked_GetInteractiveVisualization()


                        StateManagmentSubsystem.SaveWholeInformation(self)

    def Clicked_GetInteractiveVisualization(self):
        try:
            webbrowser.open(self.file_path_html)
        except:
            tkinter.messagebox.showerror("Open Error",
                                         "You have no browser to open interactive visualization.")

    def Clicked_GoToUserInterface(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToUserInterface()
    def Clicked_GoToDataLoadingSubsystem(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToDataLoadingSubsystem()
    def Clicked_GoToRecommendersSubsystem(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToRecommendersSubsystem()





class RecommendersSubsystem:
    def __init__(self):
        self.window = Tk()
        self.window.title('Recommendation system with data visualization. Recommendation Screen')
        self.window.geometry('600x400')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(width=False, height=False)
        self.ShowRecommendersScreen()
        self.window.mainloop()
    def ShowRecommendersScreen(self):
        global data
        self.list_of_parameters = list(data.columns.values)
        self.lbl1 = Label(self.window,
                          text='Select the parameters by which you can judge the advantage\n of one element over others and their behavior:',
                          font=('Times New Roman', 16))
        self.btn0 = Button(self.window, text='Select parameters', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_SelectParameters)
        self.btn0.place(x=205, y = 95)
        self.lbl1.place(x=25, y = 5)
        self.lbl2 = Label(self.window,
                          text=f'Enter the number of recommendations (max = {data.shape[0]-1}):',
                          font=('Times New Roman', 16))
        self.lbl2.place(x=25, y=175)
        self.spinbox1 = ttk.Spinbox(from_=1, to= data.shape[0])
        self.spinbox1.place(x=25, y = 215)
        self.btn1 = Button(self.window, text='Get recommendations', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GetRecommendations)
        self.btn1.place(x=205, y = 300)
        self.btn2 = Button(self.window, text='Go to Initial Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToUserInterface)
        self.btn2.place(x=5, y=340)
        self.btn3 = Button(self.window, text='Go to Data Loading Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToDataLoadingSubsystem)
        self.btn3.place(x=205, y=340)
        self.btn4 = Button(self.window, text='Go to Visualization Screen', font=('Times new Roman', 12), width=20,
                           command=self.Clicked_GoToVisualizationSubsystem)
        self.btn4.place(x=405, y=340)
        try:
            self.spinbox1.set(whole_information['count'])
        except:
            None

        try:
            self.max_priority = whole_information['max_priority']
            self.priority_vars = [IntVar(value=var) for var in whole_information['priority_vars']]
            self.sort_vars = [StringVar(value=var) for var in whole_information['sort_vars']]
            self.temp_max_priority = self.max_priority
            self.temp_priority_vars = [var.get() for var in self.priority_vars]
            self.temp_sort_vars = [var.get() for var in self.sort_vars]

            priorities = [self.priority_vars[i].get() for i in range(len(self.list_of_parameters))]
            sort_methods = [self.sort_vars[i].get() for i in range(len(self.list_of_parameters))]

            self.list_of_priority_parametrs = []
            i = 0
            for parameter in self.list_of_parameters:
                temp = []
                temp.append(parameter)
                temp.append(priorities[i])
                temp.append(sort_methods[i])
                i += 1
                self.list_of_priority_parametrs.append(temp)
        except:
            self.priority_vars = []
            self.sort_vars = []

    def Check_Float(self):
        try:
            float(self.spinbox1.get())
        except:
            return True
        return False

    def Check_Int(self):
        try:
            int(self.spinbox1.get())
        except:
            return True
        return False
    def Combine_Features(self, row):
        temp = ''
        for element in self.list_of_parameters:
            temp += str(row[element]) + ' '
        return temp

    def dismiss(self):
        self.window1.grab_release()
        self.window1.destroy()

    def dismiss1(self):
        self.window2.grab_release()
        self.window2.destroy()

    def Check_Type(self, data_temp):
        global data
        priorities = sorted(self.list_of_priority_parametrs, key=lambda x: x[1])
        elements = []
        ascend = []
        for el in priorities:
            if el[1] == 0:
                continue
            else:
                elements.append(el[0])
                if el[2] == 'ascending order':
                    ascend.append(True)
                else:
                    ascend.append(False)
            try:
                 data = data_temp.sort_values(by=elements, ascending=ascend)
            except:
                return False, el[0]
        return True, None


    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//100), "units")

    def combobox_wheel(self, event):
        return "break"

    def Clicked_SelectParameters(self):
        self.window2 = Toplevel()
        self.window2.title('Recommendation system with data visualization. Select Parameters Screen')
        self.window2.geometry('400x600')
        self.window2.iconbitmap('icon.ico')
        self.window2.resizable(width=False, height=False)
        self.window2.protocol("WM_DELETE_WINDOW", lambda: self.dismiss1())
        self.window2.grab_set()
        self.frame = Frame(self.window2)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame)
        self.canvas.pack(side='left',fill="both", expand=True)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame=Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0),window=self.scrollable_frame, anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        try:
           self.max_priority = self.temp_max_priority
           self.priority_vars = [IntVar(value=var) for var in self.temp_priority_vars]
           self.sort_vars = [StringVar(value=var) for var in self.temp_sort_vars]
        except:
            self.max_priority = len(self.list_of_parameters) - 1
            self.priority_vars = [IntVar(value=0) for i in range(self.max_priority + 1)]
            self.sort_vars = [StringVar(value="ascending order") for _ in range(len(self.list_of_parameters))]

        label_param = Label(self.scrollable_frame, text="Parameters:", font="bold")
        label_param.grid(row = 0, column = 0, padx=5, sticky="w")
        label_priority = Label(self.scrollable_frame, text="Priority:",font="bold")
        label_priority.grid(row=0, column=1, padx=5, sticky="w")
        label_behavior = Label(self.scrollable_frame, text="Behavior:",font="bold")
        label_behavior.grid(row=0, column=2, padx=5, sticky="w")
        for i, param in enumerate(self.list_of_parameters):
            param_label = Label(self.scrollable_frame, text=param)
            param_label.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")

            # Поле выбора приоритета для каждого параметра
            priority_combobox = ttk.Combobox(self.scrollable_frame, values=list(range(self.max_priority + 1)), textvariable=self.priority_vars[i],
                                             state="readonly", width=3)
            priority_combobox.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
            priority_combobox.bind("<MouseWheel>", self.combobox_wheel)
            # Поле выбора варианта сортировки для каждого параметра
            sort_combobox = ttk.Combobox(self.scrollable_frame, values=["descending order", "ascending order"], textvariable=self.sort_vars[i], state="readonly",
                                         width=17)
            sort_combobox.grid(row=i+1, column=2, padx=5, pady=5, sticky="w")
            sort_combobox.bind("<MouseWheel>", self.combobox_wheel)
 
        self.parameters_button = Button(self.scrollable_frame, text="Save parameters", width= 20, command=self.Save_parameters)
        self.parameters_button.grid(row=len(self.list_of_parameters) + 1, column=0, columnspan=4, pady=10)


    def Save_parameters(self):
        self.temp_max_priority = self.max_priority
        self.temp_priority_vars = [var.get() for var in self.priority_vars]
        self.temp_sort_vars = [var.get() for var in self.sort_vars]
        # Получение значений приоритетов и вариантов сортировки для каждого параметра
        priorities = [self.priority_vars[i].get() for i in range(len(self.list_of_parameters))]
        sort_methods = [self.sort_vars[i].get() for i in range(len(self.list_of_parameters))]

            # Проверка на уникальность приоритетов
        unique_priorities = set(priorities)
        unique_priorities.remove(0)
        temp_priorities = priorities.copy()
        temp_priorities=list(filter(lambda x: x != 0, temp_priorities))

        if len(unique_priorities) != len(temp_priorities):
            tkinter.messagebox.showerror("Parameters Error",
                                         "Priorities, with the exception of 0, must be unique.")
        elif len(unique_priorities) == 0:
            tkinter.messagebox.showerror("Parameters Error",
                                         "At least one parameter must be given a non-zero priority.")
        else:
            self.list_of_priority_parametrs = []
            i = 0
            for parameter in self.list_of_parameters:
                temp = []
                temp.append(parameter)
                temp.append(priorities[i])
                temp.append(sort_methods[i])
                i += 1
                self.list_of_priority_parametrs.append(temp)
            self.window2.destroy()





    def Clicked_GetRecommendations(self):
        global data
        global whole_information
        if self.Check_Float():
            tkinter.messagebox.showerror("Input Error",
                                         "The entered string is not a number. Try again.")
        elif self.Check_Int():
            tkinter.messagebox.showerror("Input Error",
                                         "The entered number is not an integer. Try again.")
        elif int(self.spinbox1.get()) < 1 or int(self.spinbox1.get()) > data.shape[0]-1:
            tkinter.messagebox.showerror("Input Error",
                                         "The entered number is not included in the row range. Try again.")
        elif len(self.priority_vars) == 0 or len(self.sort_vars) == 0:
            tkinter.messagebox.showerror("Parametera Error",
                                         "No parameters have been entered. Try again.")
        else:
            data_recommenders = pd.DataFrame()
            try:
                if whole_information['list_of_priority_parameters'] == self.list_of_priority_parametrs and \
                        whole_information['count'] == int(self.spinbox1.get()):
                    data_recommenders = whole_information['data_recommenders']
                    self.window1 = Toplevel()
                    self.window1.title('Recommendation system with data visualization. Recommendation Screen')
                    self.window1.geometry('600x300')
                    self.window1.iconbitmap('icon.ico')
                    self.window1.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())
                    self.window1.grab_set()
                    self.table1 = Table(self.window1, dataframe=data_recommenders,
                                        showtoolbar=False, showstatusbar=False)
                    self.table1.show()
                    self.table1.redraw()
                else:
                    raise Exception("Parameters not indentic.")
            except:
                self.check, self.error = self.Check_Type(data)
                if self.check:
                    features = self.list_of_parameters
                    for feature in features:
                        data[feature] = data[feature].fillna('')
                    data['combined_features'] = data.apply(self.Combine_Features,
                                                           axis=1)  
                    cv = CountVectorizer()  
                    count_matrix = cv.fit_transform(
                        data[
                            'combined_features'])  
                    cosine_sim = cosine_similarity(count_matrix)
                    index = 1
                    like = list(enumerate(cosine_sim[index]))
                    sorted_like = sorted(like, key=lambda x: x[1], reverse=True)[1:]

                    i = 0
                    indexes = []
                    indexes.append(index)
                    for element in sorted_like:
                        indexes.append(element[0])
                        i += 1
                        if i == int(self.spinbox1.get()):
                            break
                    data_recommenders = data.iloc[indexes]
                    whole_information['list_of_priority_parameters'] = self.list_of_priority_parametrs
                    whole_information['count'] = int(self.spinbox1.get())
                    whole_information['data_recommenders'] = data_recommenders
                    whole_information['max_priority'] = self.max_priority
                    whole_information['priority_vars'] = [var.get() for var in self.priority_vars]
                    whole_information['sort_vars'] = [var.get() for var in self.sort_vars]
                    StateManagmentSubsystem.SaveWholeInformation(self)


                    self.window1 = Toplevel()
                    self.window1.title('Recommendation system with data visualization. Recommendation Screen')
                    self.window1.geometry('600x300')
                    self.window1.iconbitmap('icon.ico')
                    self.window1.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())
                    self.window1.grab_set()
                    self.table1 = Table(self.window1, dataframe=data_recommenders,
                                            showtoolbar=False, showstatusbar=False)
                    self.table1.show()
                    self.table1.redraw()
                else:
                    tkinter.messagebox.showerror("Input Error",
                                                 f"The difference is in the type of data in the column with the specifier {self.error}. It needs to be fixed.")
                try:
                    whole_information['visualization'] = dict()
                except:
                    None



    def Clicked_GoToUserInterface(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToUserInterface()

    def Clicked_GoToDataLoadingSubsystem(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToDataLoadingSubsystem()

    def Clicked_GoToVisualizationSubsystem(self):
        self.window.destroy()
        StateTransitionSubsystem().GoToVisualizationSubsystem()




class StateTransitionSubsystem:
    def GoToDataLoadingSubsystem(self):
        DataLoadingSubsystem()
    def GoToUserInterface(self):
        UserInterface()
    def GoToVisualizationSubsystem(self):
        VisualizationSubsystem()
    def GoToRecommendersSubsystem(self):
        RecommendersSubsystem()



class StateManagmentSubsystem:
    def RegisterSave(self, persons_dict):
        global temp_login
        login = temp_login
        fout = open('Persons_information.bin', 'wb')
        pickle.dump(persons_dict, fout)
        fout.close()
        if not os.path.isdir('AccountInformation\\' + login):
            os.mkdir('AccountInformation\\' + login)
        if not os.path.isdir('AccountInformation\\' + login + '\\Datasets'):
            os.mkdir('AccountInformation\\' + login + '\\Datasets')
        if not os.path.isdir('AccountInformation\\' + login + '\\Models'):
            os.mkdir('AccountInformation\\' + login + '\\Models')
        if not os.path.isdir('AccountInformation\\' + login + '\\Visualizations'):
            os.mkdir('AccountInformation\\' + login + '\\Visualizations')

    def LoadLogInInformation(self):
        fin = open('Persons_information.bin', 'rb')
        persons_dict = pickle.load(fin)
        fin.close()
        return persons_dict

    def SaveWholeInformation(self):
        global temp_login
        global whole_information
        fout = open('AccountInformation\\' + temp_login + '\\information.bin', 'wb')
        pickle.dump(whole_information, fout)
        fout.close()


    def SaveDataLoadingSubsystemFile(self, filepath):
        global temp_login
        index = 1
        k = 0
        while True:
            if filepath[len(filepath) - k - 1:-k] == '.':
                break
            k += 1
        if os.path.isfile(
                'AccountInformation\\' + temp_login + '\\Datasets' + '\\data' + filepath[len(filepath) - k - 1:]):
            while True:
                if not os.path.isfile(
                        'AccountInformation\\' + temp_login + '\\Datasets' + '\\data' + str(index) + filepath[
                                                                                                     len(filepath) - k - 1:]):
                    shutil.copyfile(filepath, 'AccountInformation\\' + temp_login + '\\Datasets' + '\\data' + str(
                        index) + filepath[len(filepath) - k - 1:])
                    break
                index += 1
        else:
            shutil.copyfile(filepath, 'AccountInformation\\' + temp_login + '\\Datasets' + '\\data' + filepath[
                                                                                                      len(filepath) - k - 1:])

    def DownloadDataLoadingSubsystemWholeInformation(self):
        global temp_login
        fin = open('AccountInformation\\' + temp_login + '\\information.bin', 'rb')
        whole_information = pickle.load(fin)
        fin.close()
        return whole_information

    def SaveVisualizationSubsystemImj(self, fig):
        global temp_login
        index = 1
        file_path_img = ''
        file_path_html = ''
        if os.path.isfile(
                'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization.html'):
            while True:
                if not os.path.isfile(
                        'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + str(
                            index) + ".html"):
                    fig.write_html(
                        'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + str(
                            index) + ".html")
                    hti = Html2Image(
                        output_path='AccountInformation\\' + temp_login + '\\Visualizations')
                    hti.screenshot(
                        html_file='AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + str(
                            index) + ".html",
                        save_as='Visualization' + str(index) + ".jpg")
                    file_path_img = 'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + str(
                        index) + ".jpg"
                    file_path_html = 'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + str(
                        index) + ".html"
                    break
                index += 1
        else:
            fig.write_html(
                'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization.html')
            hti = Html2Image(output_path='AccountInformation\\' + temp_login + '\\Visualizations')
            hti.screenshot(
                html_file='AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization.html',
                save_as='Visualization.jpg')
            file_path_img = 'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + ".jpg"
            file_path_html = 'AccountInformation\\' + temp_login + '\\Visualizations' + '\\Visualization' + ".html"



        return file_path_img, file_path_html



if __name__ == '__main__':
    if not os.path.isfile('Persons_information.bin'):
        tempf = open('Persons_information.bin', 'wb')
        tempf.close()
    if os.stat('Persons_information.bin').st_size == 0:
        fout = open('Persons_information.bin', 'wb')
        persons_dict = dict()
        persons_dict['admin'] = 'admin'
        pickle.dump(persons_dict, fout)
        fout.close()
    if not os.path.isdir('AccountInformation'):
        os.mkdir('AccountInformation')
    UserInterface(

