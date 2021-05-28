import numpy as np
import os

import pandas

proc_path = "/proc"
global df
class pro_info():
    name = ""
    status = ""
    pid = 0
    ppid = 0
    VM_peak = 0  # memory peak size
    VM_size = 0  # current memory size
    VM_HWM = 0  # physical memory peak size
    VM_RSS = 0  # current physical memory

    def tos(self):
        print("{}\t\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(self.name, self.status, self.pid, self.ppid, self.VM_peak,
                                                          self.VM_size, self.VM_HWM, self.VM_RSS))

class mem_info():
    MemTotal = 0
    MemFree = 0
    MemAvailable = 0
    Buffers = 0
    Cached = 0
    SwapCached = 0
    Active = 0
    Inactive = 0

    def tos(self):
        print("Total\tFree\tAvailable\tBuffer\tCache\tSwapCache\tActive\tInactive\t")
        print(
            "{}\t{}\t{}\t\t{}\t{}\t{}\t\t{}\t{}\t".format(self.MemTotal, self.MemFree, self.MemAvailable, self.Buffers,
                                                          self.Cached, self.SwapCached, self.Active, self.Inactive))

def clear():
    os.system("clear")

def get_mem_info():
    mem_path = os.path.join(proc_path, "meminfo")
    mem = mem_info()
    with open(mem_path, "r") as f:
        all_data = f.readlines()
        mem.MemTotal = all_data[0].split()[-2]
        mem.MemFree = all_data[1].split()[-2]
        mem.MemAvailable = all_data[2].split()[-2]
        mem.Buffers = all_data[3].split()[-2]
        mem.Cached = all_data[4].split()[-2]
        mem.SwapCached = all_data[5].split()[-2]
        mem.Active = all_data[6].split()[-2]
        mem.Inactive = all_data[7].split()[-2]
    return mem
    # print(all_data)
    # print(mem.MemTotal)
    # mem.MemFree=

def get_process_info(pid):
    status_path = os.path.join(proc_path, str(pid), "status")
    process = pro_info()
    flag = True
    with open(status_path, "r") as status:
        name = status.readline().split()[1]
        process.name = name
        for i in range(40):
            temp = status.readline()
            st = temp.split()
            if i == 1:
                process.status = st[-1][1:-1]
            elif i == 4:
                process.pid = st[-1]
            elif i == 5:
                process.ppid = temp.split()[-1]
            elif i == 20 and st[0] == "VmRSS:":
                process.VM_RSS = st[1]
            elif i == 15:
                if st[0] == "VmPeak:":
                    process.VM_peak = st[1]
                else:
                    flag = False
                    break
            elif i == 19 and st[0] == "VmHWM:":
                process.VM_HWM = st[1]

            elif i == 16 and st[0] == "VmSize:":
                process.VM_size = st[1]

    # print(status)
    return process, flag

def show_mem_usage():
    # print("PID\tMemory (KiB)\tName")
    all_pro = os.listdir(proc_path)
    pro_list = []
    count = 0
    for pid in os.listdir(proc_path):
        if not pid.isdigit():
            continue
        # if count>5:
        #    break
        count += 1
        pid = int(pid)
        # get_process_name(pid)
        # mem_usage = "{} KiB".format(get_RSS(pid))
        pro, flag = get_process_info(pid)
        if flag:
            pro_list.append(pro)
        # if len(mem_usage) < 8:
        #    mem_usage += "\t"

        # print("{}\t{}\t{}".format(pid, mem_usage, get_process_name(pid)))
    #
    mem = get_mem_info()
    pro = pro_info()
    pro.name = "Mem info:"+str(mem.MemTotal)
    pro.status = mem.MemFree
    pro.pid = mem.MemAvailable
    pro.ppid = mem.Buffers
    pro.VM_peak = mem.Cached
    pro.VM_size = mem.SwapCached
    pro.VM_HWM = mem.Active
    pro.VM_RSS = mem.Inactive
    pro_list.append(pro)
    np.save("./pro_info.npy",pro_list)
    for pro in pro_list:
        pro.tos()

import wx
import time
import wx.grid
import pandas as pd
class ButtonFrame(wx.Frame):
    def __init__(self):
        global df
        wx.Frame.__init__(self, None, -1, 'Button Example',
                          size=(1500, 700))
        self.SetMaxSize((1700,700))
        df = self.todf()
        self.panel = wx.grid.Grid(self, pos=(1,1))
        self.button = wx.Button(self.panel, -1, "Hello", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        self.gridWin = self.panel.GetGridColLabelWindow()
        self.gridWin.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.all_pro=all_pro
        self.panel.CreateGrid(len(all_pro), 8)
        self.panel.SetColSize(0,250)
        self.panel.SetColSize(1,120)
        self.panel.SetColSize(2,100)
        self.panel.SetColSize(3,100)
        self.panel.SetColSize(4,200)
        self.panel.SetColSize(5,200)
        self.panel.SetColSize(6,200)
        self.panel.SetColSize(7,200)
        self.panel.SetColLabelValue(0, "name")
        self.panel.SetColLabelValue(1, "status")
        self.panel.SetColLabelValue(2, "pid")
        self.panel.SetColLabelValue(3, "ppid")
        self.panel.SetColLabelValue(4, "VM_peak/KB")
        self.panel.SetColLabelValue(5, "VM_size/KB")
        self.panel.SetColLabelValue(6, "VM_HWM/KB")
        self.panel.SetColLabelValue(7, "VM_RSS/KB")
        self.panel.SetColLabelSize(30)
        self.set_ele()

    def set_ele(self):
        global df
        for row in df.iterrows():
            # print(row[1]['name'])
            self.panel.SetCellValue(row[0], 0, row[1]['name'])
            self.panel.SetCellValue(row[0], 1, row[1]['status'])
            self.panel.SetCellValue(row[0], 2, str(row[1]['pid']))
            self.panel.SetCellValue(row[0], 3, str(row[1]['ppid']))
            self.panel.SetCellValue(row[0], 4, str(row[1]['VM_peak']))
            self.panel.SetCellValue(row[0], 5, str(row[1]['VM_size']))
            self.panel.SetCellValue(row[0], 6, str(row[1]['VM_HWM']))
            self.panel.SetCellValue(row[0], 7, str(row[1]['VM_RSS']))
    def todf(self):
        nl = []
        sl = []
        pl = []
        ppl = []
        vp = []
        vs = []
        vh = []
        vr = []

        df = pd.DataFrame()
        for pro in all_pro:
            nl.append(pro.name)
            sl.append(pro.status)
            pl.append(int(pro.pid))
            ppl.append(int(pro.ppid))
            vp.append(int(pro.VM_peak))
            vs.append(int(pro.VM_size))
            vh.append(int(pro.VM_HWM))
            vr.append(int(pro.VM_RSS))
        df["name"] = nl
        df["status"] = sl
        df["pid"] = pl
        df["ppid"] = ppl
        df["VM_peak"] = vp
        df["VM_size"] = vs
        df["VM_HWM"] = vh
        df["VM_RSS"] = vr
        return df
    def click(self,e):
        global df
        # print(e.x)
        x=e.x
        if x<250:
            df=df.sort_values(by=["name"] , ascending=[True])
        elif x<370:
            df=df.sort_values(by=["status"] , ascending=[True])
        elif x<470:
            df=df.sort_values(by=["pid"] , ascending=[True])
        elif x<570:
            df=df.sort_values(by=["ppid"] , ascending=[True])
        elif x<770:
            df=df.sort_values(by=["VM_peak"] , ascending=[True])
        elif x < 970:
            df=df.sort_values(by=["VM_size"] , ascending=[True])
        elif x<1170:
            df=df.sort_values(by=["VM_HWM"] , ascending=[True])
        elif x<1370:
            df=df.sort_values(by=["VM_RSS"] , ascending=[True])
        self.panel.ClearGrid()
        df.reset_index(drop=True, inplace=True)

        self.set_ele()

        self.gridWin.Update()
        self.gridWin.Refresh()
        self.panel.Refresh()
        self.panel.Update()

        self.panel.Refresh()
    def OnRadio(self, event):  # 事件处理器
        radioSelected = event.GetEventObject()
        print(event.GetEventObject())
    def OnClick(self, event):
            self.button.SetLabel("Clicked")
    def onChecked(self, e):
        cb = e.GetEventObject()
        print(cb.GetLabel(), ' is clicked', cb.GetValue())
from multiprocessing import  Process
import threading
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, df,frame):
        threading.Thread.__init__(self)
        self.df=df
        self.frame=frame
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print_time(self.df,self.frame)
def print_time(df,frame):
    while True:
        time.sleep(1)
        show_mem_usage()
        frame.set_ele()
        frame.gridWin.Update()
        frame.gridWin.Refresh()
        frame.panel.Refresh()
        frame.panel.Update()
        frame.panel.Refresh()


if __name__ == '__main__':
    show_mem_usage()
    all_pro = np.load("./pro_info.npy", allow_pickle=True)
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    app.MainLoop()

