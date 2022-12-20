from tkinter import *
from tkinter.ttk import *

class TicketGui(Tk):
    def __init__(self):
        super().__init__()
        self.title("主窗体")
        self.geometry("900x640+180+80")
        self["bg"] = "skyblue"

        self.loding_gui()

    def loding_gui(self):
        # 设定Style
        self.Style01 = Style()
        self.Style01.configure("left.TPanedwindow", background = "navy")
        self.Style01.configure("right.TPanedwindow", background="skyblue")
        self.Style01.configure("TButton", width=10, font=("华文黑体", 15, "bold"))

        # 选项区
        self.top_left = PanedWindow(width=880, height=100)
        self.top_left.place(x=10, y=10)
        self.label_add = Label(self.top_left, text="出发").place(x=0, y=0)
        self.select_add = Combobox(self.top_left, width=4).place(x=30, y=0)
        self.label_add = Label(self.top_left, text="目的").place(x=90, y=0)
        self.select_add = Combobox(self.top_left, width=4).place(x=120, y=0)

        # 列车信息区
        self.body_left = PanedWindow(width=880, height=100)
        self.body_left.place(x=10, y=120)
        Label(self.body_left, text="出发").place(x=0, y=0)

        # 功能区
        self.bottom = PanedWindow(width=880, height=100)
        self.bottom.place(x=10, y=230)

        # 日志区
        self.foot = PanedWindow(width=880, height=100)
        self.foot.place(x=10, y=340)

        # ## left banner
        # self.Pane_left = PanedWindow(width = 200,height = 540,style = "left.TPanedwindow")
        # self.Pane_left.place(x = 4,y = 94)
        # self.Pane_right = PanedWindow(width=685, height=540,style = "right.TPanedwindow")
        # self.Pane_right.place(x = 210,y = 94)
        # # 添加左边按钮
        # self.Button_add = Button(self.Pane_left,text = "添加学生",style = "TButton")
        # self.Button_add.place(x = 40,y = 20)
        # self.Button_update = Button(self.Pane_left, text="修改学生", style="TButton")
        # self.Button_update.place(x=40, y=45)
        # self.Button_delete = Button(self.Pane_left, text="删除学生", style="TButton")
        # self.Button_delete.place(x=40, y=70)
        # self.Button_modify = Button(self.Pane_left, text="更改密码", style="TButton")
        # self.Button_modify.place(x=40, y=120)
        #
        # ## right banner
        # self.Pane_right = PanedWindow(width=725, height=540, style="right.TPanedwindow")
        # self.Pane_right.place(x=170, y=94)
        # self.LabelFrame_query = LabelFrame(self.Pane_right,text = "学生信息查询",width = 700,height = 70)
        # self.LabelFrame_query.place(x = 10 , y = 10)
        # # 添加控件
        # self.Label_sno = Label(self.LabelFrame_query,text = "学号：")
        # self.Label_sno.place(x = 5,y = 13)
        # self.Entry_sno = Entry(self.LabelFrame_query,width = 8)
        # self.Entry_sno.place(x = 40,y = 10)
        #
        # self.Label_name = Label(self.LabelFrame_query, text="姓名：")
        # self.Label_name.place(x=125, y=13)
        # self.Entry_name = Entry(self.LabelFrame_query, width=8)
        # self.Entry_name.place(x=160, y=10)
        #
        # self.Label_mobile = Label(self.LabelFrame_query, text="电话：")
        # self.Label_mobile.place(x=245, y=13)
        # self.Entry_mobile = Entry(self.LabelFrame_query, width=8)
        # self.Entry_mobile.place(x=280, y=10)
        #
        # self.Label_id = Label(self.LabelFrame_query, text="身份证：")
        # self.Label_id.place(x=365, y=13)
        # self.Entry_id = Entry(self.LabelFrame_query, width=10)
        # self.Entry_id.place(x=420, y=10)
        #
        # self.Button_query = Button(self.LabelFrame_query, text="查询",width = 4)
        # self.Button_query.place(x=520, y=10)
        # self.Button_all = Button(self.LabelFrame_query, text="显示全部",width = 8)
        # self.Button_all.place(x=590, y=10)
        #
        # # 添加TreeView控件
        # self.Tree = Treeview(self.Pane_right,columns=("sno","names",
        #                                               "gender","birthday","mobile","email","address"),show="headings",height=20)
        #
        # # 设置每一个列的宽度和对齐的方式
        # self.Tree.column("sno",width=100,anchor="center")
        # self.Tree.column("names",width=80,anchor="center")
        # self.Tree.column("gender",width=80,anchor="center")
        # self.Tree.column("birthday",width=100,anchor="center")
        # self.Tree.column("mobile",width=100,anchor="center")
        # self.Tree.column("email", width=100, anchor="center")
        # self.Tree.column("address",width=120,anchor="center")
        #
        # # 设置每个列的标题
        # self.Tree.heading("sno",text="学号")
        # self.Tree.heading("names", text="姓名")
        # self.Tree.heading("gender", text="性别")
        # self.Tree.heading("birthday", text="生日")
        # self.Tree.heading("mobile", text="手机号码")
        # self.Tree.heading("email", text="邮箱地址")
        # self.Tree.heading("address", text="家庭住址")
        #
        # self.Tree.place(x=10,y=80)

if __name__ == '__main__':
    app = TicketGui()
    app.mainloop()