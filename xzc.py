#burç was here
#from lamenesslib import burc
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
        pressure_unit = self.var_pressure.get()
        temperature_unit = self.var_temperature.get()

        def pressure_unit_conversion(pressusre_unit, pressure_first):
            if pressure_unit == "bar":
                return pressure_first / 0.069
            elif pressure_unit == "kPa":
                return pressure_first / 6.895
            elif pressure_unit == "psig":
                return pressure_first

        def temperature_unit_conversion(temp_unit, temperature_first):
            if temperature_unit == "K":
                return 1.8 * (temperature_first - 273) + 32
            elif temperature_unit == "°C":
                return temperature_first * 1.8 + 32
            elif temperature_unit == "F":
                return temperature_first

        temperature = temperature_unit_conversion(temperature_unit, temperature_first)
        pressure = pressure_unit_conversion(pressure_unit, pressure_first)

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
        self.firecase.grid(column=0, row=11, sticky="W")

        self.instvar = tkinter.IntVar()
        self.firecase = ttk.Checkbutton(self, text='Valve Installation mode', variable=self.instvar, command=self.fire)
        self.firecase.grid(column=1, row=11, sticky="W")

        self.kdcoeffvar = tkinter.IntVar()
        self.ruptureonlycase = ttk.Checkbutton(self, text='No pressure relief valve only rupture disk', variable=self.kdcoeffvar, command=self.rupture)
        self.ruptureonlycase.grid(column=0, row=12)

        self.kccoeffvar = tkinter.IntVar()
        self.ruptureinstcase = ttk.Checkbutton(self, text='There is rupture disk in the upstream',
                                               variable=self.kccoeffvar, command=self.ruptureinst)
        self.ruptureinstcase.grid(column=0, row=13, sticky="W")

        self.flow_entry = ttk.Entry(self, width=10)
        self.flow_entry.grid(column=1, row=2, sticky="W")
        self.var_flow = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.var_flow,
                                state='readonly')
        self.box['values'] = ("kg/h", "kg/s", "lb/h", "lb/s")
        self.box.current(0)
        self.box.grid(column=2, row=2)

        self.pressure_entry = ttk.Entry(self, width=10)
        self.pressure_entry.grid(column=1, row=3, sticky="W")
        self.var_pressure = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.var_pressure,
                                state='readonly')
        self.box['values'] = ("psig", "bar", "kPa")
        self.box.current(0)
        self.box.grid(column=2, row=3)

        self.temperature_entry = ttk.Entry(self, width=10)
        self.temperature_entry.grid(column=1, row=4, sticky="W")
        self.var_temperature = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.var_temperature,
                                state="readonly")
        self.box["values"] = ("F", "K", "°C")
        self.box.current(0)
        self.box.grid(column=2, row=4)

        self.calc_button = ttk.Button(self, text='Calculate', command=self.calculate)
        self.calc_button.grid(column=2, row=5, columnspan=4, sticky="E")

        self.quit_button = ttk.Button(self, text='Quit', command=self.on_quit)
        self.quit_button.grid(column=2, row=13, columnspan=4, sticky="E")

        self.answer_frame = ttk.LabelFrame(self, text='Answer', height=100)
        self.answer_frame.grid(column=0, row=6, columnspan=4, sticky='nesw')

        self.answer_label = ttk.Label(self.answer_frame, text='')
        self.answer_label.grid(column=0, row=0)

        #constant labels
        ttk.Label(self, text='Sizing Pressure-Relieving Devices (API 520)').grid(column=0, row=0, columnspan=4)
        ttk.Label(self, text='Flow').grid(row=2, sticky='w')
        ttk.Label(self, text='Pressure').grid(row=3, sticky='w')
        ttk.Label(self, text='Temperature').grid(row=4, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root =tkinter.Tk()
    Program(root)
    root.mainloop()