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

    #for the effective coefficient of discharge
    def rupture(self):
        if (self.kdcoeffvar.get() ==1):
            self.Kd = 0.62
        else:
            self.Kd = 0.975
            #self.combinationcorrection.state(state=DISABLED)

    #for combination correction factor for installation with a rupture
    #  disk upstream of the pressure relief valve
    def ruptureinst(self):
        if (self.kccoeffvar.get() ==1):
            self.Kc = 0.9
        else:
            self.Kc = 1

    def calculate(self):
        # Constant Values

        raw_flow = int(self.flow_entry.get())
        raw_pressure = int(self.pressure_entry.get())
        raw_temperature = int(self.temperature_entry.get())

        unit_flow = self.unit_index_flow.get()
        unit_pressure = self.unit_index_pressure.get()
        unit_temperature = self.unit_index_temperature.get()

        def flow_unit_conversion(unit_flow, raw_flow):
            if unit_flow == "kg/h":
                return raw_flow * 2.20462262185
            elif unit_flow == "kg/s":
                return raw_flow *2.20462262185 /3600
            elif unit_flow == "lb/h":
                return raw_flow
            elif unit_flow == "lb/s":
                return raw_flow /3600

        def pressure_unit_conversion(unit_pressure, raw_pressure):
            if unit_pressure == "barg":
                return raw_pressure / 0.069
            elif unit_pressure == "kPag":
                return raw_pressure / 6.895
            elif unit_pressure == "psig":
                return raw_pressure

        def temperature_unit_conversion(unit_temperature, raw_temperature):
            if unit_temperature == "K":
                return 1.8 * (raw_temperature - 273) + 32
            elif unit_temperature == "°C":
                return raw_temperature * 1.8 + 32
            elif unit_temperature == "F":
                return raw_temperature

        converted_flow = flow_unit_conversion(unit_flow, raw_flow)
        converted_temperature = temperature_unit_conversion(unit_temperature, raw_temperature)
        converted_pressure = pressure_unit_conversion(unit_pressure, raw_pressure)

#data pulling from table starts here
        def roundup_temp(converted_temperature):
            return table_df.columns[table_df.columns >= converted_temperature].min()

        def roundup_pres(converted_pressure):
            return table_df.index[table_df.index >= converted_pressure].min()

        def pull_data(converted_pressure, converted_temperature):
            return table_df.loc[roundup_pres(converted_pressure), roundup_temp(converted_temperature)]

        filename = "API Table 9.csv"
        table_df = pd.read_csv(filename).set_index("Unnamed: 0")
        table_df.index.name = None
        table_df.columns = table_df.columns.astype(int)
        self.Ksh=pull_data(converted_pressure, converted_temperature)
#data pulling ends here

        #P1= Relieving Pressure
        self.P1=converted_pressure*self.accumulation+14.7

        if self.P1 <= 1500:
            self.Kn=1
        elif self.P1 <= 3200 and self.P1 > 1500:
            self.Kn=(0.1906*self.P1-1000)/(0.2292*self.P1-1061)

        self.Kb1= -2.428*(14.7/converted_pressure)**2+(14.7/converted_pressure)*0.372+1.108
        self.Kb2 = 1

        A=converted_flow/(51.5*self.P1*self.Kd*self.Kb1*self.Kc*self.Kn*self.Ksh)
        A_rounded=round(A,2)

        self.answer_label['text'] = A_rounded

        #print(converted_flow)
        #print(self.unit_index_flow)
        #print(unit_flow)
        #print(converted_pressure)
        #print(self.unit_index_pressure)
        #print(unit_pressure)
        #print(converted_temperature)
        #print(self.unit_index_temperature)
        #print(unit_temperature)
        #print(self.Kb1)
        print(self.Kd)

    def init_gui(self):
        self.root.title('Sizing Pressure-Relieving Devices (API 520)')
        self.grid(column=0, row=0, sticky='nsew')

        self.firevar = tkinter.IntVar()
        self.firecase = ttk.Checkbutton(self, text='Fire Case', variable=self.firevar, command=self.fire)
        self.firecase.grid(column=0, row=11, sticky="W")

        self.instvar = tkinter.IntVar()
        self.firecase = ttk.Checkbutton(self, text='Valve Installation mode', variable=self.instvar, command=self.fire)
        self.firecase.grid(column=1, row=11, sticky="W")

#getting effective coefficient of discharge input starts here
        self.kdcoeffvar = tkinter.IntVar()
        self.effectivecoefdisc = ttk.Checkbutton(self, text='A pressure relief valve is not installed and '
                                                          'sizing is for a rupture disk',
                                               variable=self.kdcoeffvar, command=self.rupture)
        self.effectivecoefdisc.grid(column=0, row=12)
#getting effective coefficient of discharge input ends here

        self.kccoeffvar = tkinter.IntVar()
        self.combinationcorrection = ttk.Checkbutton(self, text='A rupture disk is installed in combination with'
                                                          ' a pressure relief valve',
                                               variable=self.kccoeffvar, command=self.ruptureinst)
        self.combinationcorrection.grid(column=0, row=13, sticky="W")

#GETTING FLOW AND UNIT STARTS HERE
        self.flow_entry = ttk.Entry(self, width=10)
        self.flow_entry.grid(column=1, row=2, sticky="W")
        self.unit_index_flow = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.unit_index_flow,
                                state='readonly')
        self.box['values'] = ("kg/h", "kg/s", "lb/h", "lb/s")
        self.box.current(0)
        self.box.grid(column=2, row=2)
# GETTING FLOW AND UNIT STARTS HERE

# GETTING PRESSURE AND UNIT STARTS HERE
        self.pressure_entry = ttk.Entry(self, width=10)
        self.pressure_entry.grid(column=1, row=3, sticky="W")
        self.unit_index_pressure = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.unit_index_pressure,
                                state='readonly')
        self.box['values'] = ("psig", "barg", "kPag")
        self.box.current(0)
        self.box.grid(column=2, row=3)
# GETTING PRESSURE AND UNIT ENDS HERE

# GETTING TEMPERATURE AND UNIT STARTS HERE
        self.temperature_entry = ttk.Entry(self, width=10)
        self.temperature_entry.grid(column=1, row=4, sticky="W")
        self.unit_index_temperature = tkinter.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.unit_index_temperature,
                                state="readonly")
        self.box["values"] = ("F", "K", "°C")
        self.box.current(0)
        self.box.grid(column=2, row=4)
# GETTING TEMPERATURE AND UNIT ENDS HERE

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