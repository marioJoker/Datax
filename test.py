import tkinter as tk
from PIL import ImageTk, Image
# from tabulate import tabulate
from tkinter import filedialog, messagebox
import os
import pandas as pd
import missingno as msno
import numpy as np
import matplotlib.pyplot as plt


HEIGHT = 1080
WIDTH = 1920

# def test_function(entry):
# 	print("This is the entry:", entry)
#
# # api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
# # a4aa5e3d83ffefaba8c00284de6ef7c3
#
# def format_response(weather):
# 	try:
# 		name = weather['name']
# 		desc = weather['weather'][0]['description']
# 		temp = weather['main']['temp']
#

# 	except:
# 		final_str = 'There was a problem retrieving that information'
#
# 	return final_str

def get_report(entry):
    df = pd.read_csv(entry, na_values=["#"])
    pd.set_option('display.max_columns', None)
    outputFrame2.insert(tk.INSERT, "       DISPLAYING THE FIRST 5 ROWS OF THE DATASET" + "\n\n")
    outputFrame2.tag_add('DISPLAYING THE FIRST 10 ROWS OF THE DATASET', '1.0', '1.end')
    outputFrame2.tag_config('DISPLAYING THE FIRST 10 ROWS OF THE DATASET', font='arial 16 bold')  # Set font, size and style
    outputFrame2.insert(tk.INSERT, df.head(5))
    outputFrame2.config(state=tk.DISABLED)
    get_report2(df)
    onClick()

def get_report2(df):
    pd.set_option('display.max_columns', None)
    outputFrame.insert(tk.INSERT, "          STATISTCAL ANALYSIS OF THE DATASET" + "\n\n")
    outputFrame.tag_add('      STATISTCAL ANALYSIS OF THE DATASET', '1.0', '1.end')
    outputFrame.tag_config('      STATISTCAL ANALYSIS OF THE DATASET',
                            font='arial 16 bold')  # Set font, size and style
    outputFrame.insert(tk.INSERT, 'Total number of missing value per column')
    outputFrame.insert(tk.INSERT, '\n')
    outputFrame.insert(tk.INSERT, df.isnull().sum())
    outputFrame.insert(tk.INSERT, '\n\n')
    outputFrame.insert(tk.INSERT, 'Percentage of missing data per column')
    outputFrame.insert(tk.INSERT, '\n')
    outputFrame.insert(tk.INSERT, df.isna().mean().round(4) * 100)
    outputFrame.insert(tk.INSERT, '\n\n')
    outputFrame.insert(tk.INSERT, 'Aggregation into table format')
    outputFrame.insert(tk.INSERT, '\n')
    outputFrame.insert(tk.INSERT, missing_zero_values_table(df))
    outputFrame.config(state=tk.DISABLED)

def missing_zero_values_table(df):
    zero_val = (df == 0.00).astype(int).sum(axis=0)
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mz_table = pd.concat([zero_val, mis_val, mis_val_percent], axis=1)
    mz_table = mz_table.rename(
        columns={0: 'Zero Values', 1: 'Missing Values', 2: '% of Total Values'})
    mz_table = mz_table[
        mz_table.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print("Your selected dataframe has " + str(df.shape[1]) + " columns and " + str(df.shape[0]) + " Rows.\n"
                                                                                                   "There are " + str(
        mz_table.shape[0]) +
          " columns that have missing values.")
    #         mz_table.to_excel('D:/sampledata/missing_and_zero_values.xlsx', freeze_panes=(1,0), index = False)
    return mz_table

def get_matrix(entry):
    df = pd.read_csv(entry, na_values=["#"])
    msno.matrix(df, figsize=(11, 5))
    plt.show()


def get_bar(entry):
    df = pd.read_csv(entry, na_values=['#'])
    headers = list(df)
    y_pos = np.arange(len(headers))
    missing_data_per_column = list(df.isnull().sum(axis=0))
    plt.bar(y_pos, missing_data_per_column, align='center', alpha=0.5)
    plt.xticks(y_pos, headers)
    plt.xlabel('The Dataset Columns')
    plt.ylabel('Missing Data Count')
    plt.title('The missing data visualized')
    plt.show()

def get_heatmap(entry):
    df = pd.read_csv(entry, na_values=['#'])
    headers = list(df)
    temp_container = []
    container_num = []
    for i in np.arange(len(headers)):
        result = list((pd.isnull(df[headers[i]]).to_numpy().nonzero()[0]) + 2)
        temp_container.append(result)

    for i in temp_container:
        container_num.append(len(i))

    def recurse(container):
        for i in np.arange(len(container)):
            if len(container[i]) < max(container_num):
                container[i].append('NIL')
                recurse(container)

    recurse(temp_container)

    X = []
    for i in range(max(container_num)):
        X.append(i)

    Y = headers

    m = len(Y)
    n = len(X)

    plt.figure(figsize=(n + 1, m + 1))
    for krow, row in enumerate(temp_container):
        plt.text(5, 10 * krow + 15, Y[krow],
                 horizontalalignment='center',
                 verticalalignment='center')
        for kcol, num in enumerate(row):
            if krow == 0:
                plt.text(10 * kcol + 15, 5, X[kcol],
                         horizontalalignment='center',
                         verticalalignment='center')
            plt.text(10 * kcol + 15, 10 * krow + 15, num,
                     horizontalalignment='center',
                     verticalalignment='center')

    plt.axis([0, 10 * (n + 1), 10 * (m + 1), 0])
    plt.xticks(np.linspace(0, 10 * (n + 1), n + 2), [])
    plt.yticks(np.linspace(0, 10 * (m + 1), m + 2), [])
    plt.grid(which='major', axis='both', linestyle="dashed", linewidth=1)
    plt.savefig("Table.png", dpi=300)
    plt.show()

    # diction = []
    #
    # i = 0
    # for val in np.arange(len(temp_container)):
    #     diction.append(temp_container[val])
    #     i = i + 1
    #
    # missing_data_rows = pd.DataFrame(diction, index=headers)
    # pdtabulate = lambda missing_data_rows:tabulate(missing_data_rows, headers='keys', showindex='always', tablefmt='psql')



def get_dendogram(entry):
    # df = pd.read_csv(entry)
    data = {'0': ['Tom', 'Jack', 'nick', 'juli'], '1': [99, 98, 95, 90]}

    # Creates pandas DataFrame.
    df = pd.DataFrame(data, index=['rank1', 'rank2', 'rank3', 'rank4'])

    # print the data
    print(df)

def handleReturn(event, entry):
    entry.delete(0, 'end')
    answer = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title="Choose your CSV Dataset", filetypes=my_filetypes)
    entry.insert(0, answer)
    outputFrame.config(state=tk.NORMAL)
    outputFrame.delete('1.0', tk.END)
    outputFrame2.config(state=tk.NORMAL)
    outputFrame2.delete('1.0', tk.END)

def onClick():
    tk.messagebox.showinfo("File Process Dialog", "Your CSV Data has been Prepared")


root = tk.Tk()
my_filetypes = [('all files', '.csv')]


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack(side="left")
#
# photo=tk.PhotoImage(file="i.gif")
# l=tk.Label(canvas, image=photo)
# l.image=photo       #just keeping a reference
# l.place(relwidth=1, relheight=1)

# IMAGE_PATH = '//Users/macbookair//Documents//projectcode//Pattern.gif'
#
# background_image = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGHT), Image.ANTIALIAS))
# canvas.background = background_image
# bg = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
#
# # background_label = tk.Label(root, image=background_image)
# # background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=3)
frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

textFrame = tk.Frame(root)
textFrame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.1, anchor='s')

buttonFrame = tk.Frame(root)
buttonFrame.place(relx=0.5, rely=0.24, relwidth=0.75, relheight=0.05, anchor='n')

outputFrame = tk.Text(width=50, bg='#80c1ff', bd=4)
outputFrame.place(relx=0.7, rely=0.3, relwidth=0.365, relheight=0.6, anchor='n')

outputFrame2 = tk.Text(width=50, bg='#80c1ff', bd=4)
outputFrame2.place(relx=0.3, rely=0.3, relwidth=0.38, relheight=0.6, anchor='n')



entry = tk.Entry(frame, font=40)
entry.insert(0, "Choose your CSV Dataset")
entry.place(relwidth=0.65, relheight=1)
entry.bind('<Button-1>', lambda event: handleReturn(event, entry))

button = tk.Button(frame, text="Evaluate Dataset", font=40, command=lambda: get_report(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

# saveButton = tk.Button(frame, text="Save Dataset", font=40, command=lambda: get_report(entry.get()))
# saveButton.place(relx=0.82, rely=0.01, relheight=0.5, relwidth=0.1)
#
# retrieveButton = tk.Button(frame, text="Load Saved Dataset", font=40, command=lambda: get_report(entry.get()))
# retrieveButton.place(relx=0.82, rely=0.5, relheight=0.5, relwidth=0.1)

buttonMatrix = tk.Button(buttonFrame, text="MATRIX PLOT", font=40, command=lambda: get_matrix(entry.get()))
buttonMatrix.place(relx=0.18, relheight=1, relwidth=0.1)

buttonBar = tk.Button(buttonFrame, text="BAR PLOT", font=40, command=lambda: get_bar(entry.get()))
buttonBar.place(relx=0.35, relheight=1, relwidth=0.1)

buttonHeatmap = tk.Button(buttonFrame, text="VIEW ROWS WITH MISSING DATA", font=40, command=lambda: get_heatmap(entry.get()))
buttonHeatmap.place(relx=0.52, relheight=1, relwidth=0.3)

# buttonDendogram = tk.Button(buttonFrame, text="DENDOGRAM", font=40, command=lambda: get_dendogram(entry.get()))
# buttonDendogram.place(relx=0.69, relheight=1, relwidth=0.1)

textLabel = tk.Label(textFrame, text="Select a visualization style that soothes you", font=("Courier", 20)).pack()

# textLabel.place(relwidth=5, relheight=5)

# outputLabel = tk.Label(outputFrame, anchor="nw")
# outputLabel.place(relwidth=1, relheight=1)


root.mainloop()