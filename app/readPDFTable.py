import pdfplumber
import os
import tkinter as tk
import tkinter.filedialog as tkfd

errorMessageList = {
    FileNotFoundError : "ファイルが見つかりませんでした。ファイル名、拡張子、ファイルの保存場所を確認してください。",
    TypeError : "指定したページに「表」が存在することを確認してください。",
    ValueError : "ページ数は半角および全角の数字で指定してください。", 
    IndexError : "pdfファイルのページが存在しないようです。ページ数を確認してください。"
    }

dir = os.getcwd()
root = tk.Tk()
root.geometry("600x400")
root.title("SampleText")


fnameLabel = tk.Label(root, text = "表を出力したいPDFファイルを選択してください", font = ("Courier", 12))
fnameLabel.pack(pady = 10)
fTyp = [("",".pdf")]
iDir = os.path.abspath(os.path.dirname(__file__))

def choiceFile():
    fnameLabel["text"] = f"{os.path.splitext(tk.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir))[0]}.pdf"
button = tk.Button(root, text = "ファイルを選択", command = choiceFile)
button.pack()

fpageLabel = tk.Label(root, text = "ファイル内の目的の表があるページを入力してください（数字）", font = ("Courier", 12))
fpageLabel.pack(pady = 10)
fpageEntry = tk.Entry(root, width = 20)
fpageEntry.pack(pady = 10)
ftitleLabel = tk.Label(root, text = "ファイル名を設定してください", font = ("Courier", 12))
ftitleLabel.pack(pady = 10)
ftitleEntry = tk.Entry(root, width = 20)
ftitleEntry.pack()
fextLabel = tk.Label(root, text = "拡張子を指定してください。指定がなければtxtが設定されます。")
fextLabel.pack()
fextEntry = tk.Entry(root, width = 7)
fextEntry.pack()
message = tk.Message(root, text = "サンプルテキスト", font = ("Courier", 12), aspect = 800)
message.pack()

def readImage():
    try:
        getName = ftitleEntry.get()
        getPage = fpageEntry.get()
        getExt = fextEntry.get()
        path = fnameLabel["text"]
        pdf = pdfplumber.open(path)
        page = pdf.pages[int(getPage) - 1]
        table = page.extract_table()
        if getExt == "":
            getExt = "txt"
        else:
            getExt = fextEntry.get()

        print(table)
        with open(tkfd.asksaveasfilename(initialfile = f"{getName}_page{getPage}", defaultextension = f".{getExt}"), "w+") as o:
            for row in table:
                print(*row, sep = "\t", file = o)
        message["text"] = "ファイルが生成されました。" 

    except tuple(errorMessageList.keys()) as e:
        message["text"] = f"{errorMessageList[type(e)]}\n{e}"

button = tk.Button(text="保存する", command = readImage)
button.pack()
root.mainloop()

