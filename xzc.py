#burç was here
#from gayness import burc


import tkinter
from tkinter import ttk
import pandas as pd

class Program(ttk.Frame):
    accumulation = 1.1
    Kd = 0.97
    Kc = 1

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def on_quit(self):
        self.root.destroy()

    def fire(self):
        if (self.firevar.get() == 1):
            self.accumulation = 1.21
        elif (self.firevar.get() == 0 and self.instvar.get() == 1):
            self.accumulation = 1.16
        else:
            self.accumulation = 1.1

    def rupture(self):
        if (self.kdcoeffvar.get() ==1):
            self.Kd = 0.62
        else:
            self.Kd = 0.97

    def ruptureinst(self):
        if (self.kccoeffvar.get() ==1):
            self.Kc = 0.9
        else:
            self.Kc = 1

    def calculate(self):
        # Constant Values

        flow = int(self.flow_entry.get())
        pressure_first = int(self.pressure_entry.get())
        temperature_first = int(self.temperature_entry.get())
        press_unit = self.var_press.get()
        temp_unit = self.var_temp.get()

        def press_unit_conversion(press_unit, pressure_first):
            if press_unit == "bar":
                return pressure_first / 0.069
            elif press_unit == "kPa":
                return pressure_first / 6.895
            elif press_unit == "psig":
                return pressure_first

        def temp_unit_conversion(temp_unit, temperature_first):
            if temp_unit == "K":
                return 1.8 * (temperature_first - 273) + 32
            elif temp_unit == "°C":
                return temperature_first * 1.8 + 32
            elif temp_unit == "F":
                return temperature_first

        temperature = temp_unit_conversion(temp_unit, temperature_first)
        pressure = press_unit_conversion(press_unit, pressure_first)

#data pulling from table starts here
        def roundup_temp(temperature):
            return table_df.columns[table_df.columns >= temperature].min()

        def roundup_pres(pressure):
            return table_df.index[table_df.index >= pressure].min()

        def pull_data(pressure, temperature):
            return table_df.loc[roundup_pres(pressure), roundup_temp(temperature)]

        filename = "API Table 9.csv"
        table_df = pd.read_csv(filename).set_index("Unnamed: 0")
        table_df.index.name = None
        table_df.columns = table_df.columns.astype(int)
        self.Ksh=pull_data(pressure, temperature)
#data pulling ends here
        self.P1=pressure*self.accumulation+14.7

        self.Kn=(0.1906*self.P1-1000)/(0.2292*self.P1-1061)

        #self.Kb= -2.428*(14.7/pressure)**2+(14.7/pressure)*0.372+1.108
        self.Kb = 1

        A=flow/(51.5*self.P1*self.Kd*self.Kb*self.Kc*self.Kn*self.Ksh)

        self.answer_label['text'] = A
        print(flow)
        print(pressure)
        print(temperature)

    def init_gui(self):
        self.root.title('Sizing Pressure-Relieving Devices (API 520)')
        self.grid(column=0, row=0, sticky='nsew')

        self.firevar = tkinter.IntVar()
        self.firecase = ttk.Checkbutton(self, text='Fire Case', variable=self.firevar, command=self.fire)
        self.firecase.grid(column=0, row=11)

        self.instvar = tkinter.IntVar()
        self.firecase = ttk.Checkbutton(self, text='Valve Installation mode', variable=self.instvar, command=self.fire)
        self.firecase.grid(column=1, row=11)

        self.kdcoeffvar = tkinter.IntVar()
        self.ruptureonlycase = ttk.Checkbutton(self, text='No pressure relief valve only rupture disk', variable=self.kdcoeffvar, command=self.rupture)
        self.ruptureonlycase.grid(column=0, row=12)

        self.kccoeffvar = tkinter.IntVar()
        self.ruptureinstcase = ttk.Checkbutton(self, text='There is rupture disk in the upstream',
                                               variable=self.kccoeffvar, command=self.ruptureinst)
        self.ruptureinstcase.grid(column=0, row=13)

        self.flow_entry = ttk.Entry(self, width=10)
        self.flow_entry.grid(column=1, row=2)
        self.var_flow = tkinter.StringVar()
        self.flow_unit = tkinter.OptionMenu(self, self.var_flow, "kg/h", "kg/s", "lb/h", "lb/s")
        self.flow_unit.grid(column=2, row=2)
        self.var_flow.set("kg/h")

        self.pressure_entry = ttk.Entry(self, width=10)
        self.pressure_entry.grid(column=1, row=3)
        self.var_press = tkinter.StringVar()
        self.pressure_unit = tkinter.OptionMenu(self, self.var_press, "psig", "bar", "kPa")
        self.pressure_unit.grid(column=2, row=3)
        self.var_press.set("psig")

        self.temperature_entry = ttk.Entry(self, width=10)
        self.temperature_entry.grid(column=1, row=4)
        self.var_temp = tkinter.StringVar()
        self.temperature_unit = tkinter.OptionMenu(self, self.var_temp, "F", "K", "°C")
        self.temperature_unit.grid(column=2, row=4)
        self.var_temp.set("F")

        self.calc_button = ttk.Button(self, text='Calculate', command=self.calculate)
        self.calc_button.grid(column=0, row=5, columnspan=4)

        self.quit_button = ttk.Button(self, text='Quit', command=self.on_quit)
        self.quit_button.grid(column=3, row=5, columnspan=4)

        self.answer_frame = ttk.LabelFrame(self, text='Answer', height=100)
        self.answer_frame.grid(column=0, row=6, columnspan=4, sticky='nesw')

        self.answer_label = ttk.Label(self.answer_frame, text='')
        self.answer_label.grid(column=0, row=0)

        #constant labels
        ttk.Label(self, text='Sizing Pressure-Relieving Devices (API 520)').grid(column=0, row=0, columnspan=4)
        ttk.Label(self, text='Flow').grid(column=0, row=2, columnspan=4, sticky='w')
        ttk.Label(self, text='Pressure').grid(column=0, row=3, sticky='w')
        ttk.Label(self, text='Temperature').grid(column=0, row=4, sticky='w')

        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root =tkinter.Tk()
    Program(root)
    root.mainloop()