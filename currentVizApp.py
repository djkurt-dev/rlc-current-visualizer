import tkinter as tk 
from tkinter import messagebox
from PIL import ImageTk, Image, ImageSequence
import matplotlib.animation as anime
import matplotlib.pyplot as plt
import numpy as np
from math import *
import sympy as sp
import time

# Timajo, Kurt Vincent 
# Callo, Denzel D. 
# CpE_2b

class RLCViz:
    t = sp.symbols('t')
    q = sp.Function('q')
    master = tk.Tk()
    
    def __init__(self):
        self.master.geometry("1368x734")
        self.master.title("RLC Current Visualizer by Kurt Timajo & Denzel Callo")
        
        self.imageBg = Image.open('current-bg2.png')
        self.bckEnd = ImageTk.PhotoImage(self.imageBg)
        self.bg = tk.Label(self.master, image=self.bckEnd)
        self.bg.place(x=0,y=0)
        
        self.btnSolveImg = Image.open('solve-btn.png')
        self.btnEnd = ImageTk.PhotoImage(self.btnSolveImg)
        
        # RESISTANCE
        global ohms
        ohms = tk.StringVar()
        self.resistance = tk.Entry(self.master, textvariable=ohms, font=('Arial bold', 16), width=12, bg=None)
        self.resistance.place(x=94,y=104)
        
        self.Rlabel  = tk.Label(self.master, textvariable=ohms, font=('Arial bold', 20))
        self.Rlabel.config( bg= "white", fg= "red", justify="center")
        self.Rlabel.place(x=127,y=353)
        
        # INDUCTANCE
        global henry 
        henry = tk.StringVar()
        self.inductance = tk.Entry(self.master, textvariable=henry, font=('Arial bold', 16), width=12, bg=None)
        self.inductance.place(x=94,y=162)
        
        self.Llabel  = tk.Label(self.master, textvariable=henry, font=('Arial bold', 20))
        self.Llabel.config( bg= "white", fg= "red", justify="center")
        self.Llabel.place(x=320,y=353)
        
        # CAPACITANCE      
        global farad  
        farad = tk.StringVar()
        self.capacitance = tk.Entry(self.master, textvariable=farad, font=('Arial bold', 16), width=12, bg=None)
        self.capacitance.place(x=94,y=220)
        
        self.Clabel  = tk.Label(self.master, textvariable=farad, font=('Arial bold', 20))
        self.Clabel.config( bg= "white", fg= "red", justify="center")
        self.Clabel.place(x=460,y=353)
        
        # SINE COSINE
        global sineState
        sineState = tk.IntVar()
        self.sinusoid = tk.Checkbutton(self.master, command=self.sineClicked, relief='flat', font=('Arial', 12),  variable=sineState, onvalue=1, offvalue=0)
        self.sinusoid.place(x=340,y=206)
        
        global amp
        amp = tk.StringVar()
        self.amplitude = tk.Entry(self.master, textvariable=amp, font=('Arial', 14), width=5, fg="#242422")
        self.amplitude.place(x=357,y=266)
        
        global freq
        freq = tk.StringVar()
        self.angFrequency = tk.Entry(self.master, textvariable=freq, font=('Arial', 14), width=5, fg="#242422")
        self.angFrequency.place(x=487,y=266)
        
        global volts
        volts = tk.StringVar()
        self.voltage = tk.Entry(self.master, textvariable=volts, font=('Arial bold', 16), width=12, bg=None)
        self.voltage.place(x=94,y=278)
        
        self.Vlabel  = tk.Label(self.master, textvariable=volts, font=('Arial bold', 20))
        self.Vlabel.config( bg= "white", fg= "red", justify="center")
        self.Vlabel.place(x=355,y=585)
        
        # INITIAL CONDITIONS
        initialCharge = tk.StringVar()
        self.initCharge = tk.Entry(self.master, textvariable=initialCharge, font=('Arial bold', 18), width=5, bg=None, fg="#E46000", justify="center")
        self.initCharge.insert(0,0)
        self.initCharge.place(x=410,y=90)
        
        initialCurrent = tk.StringVar()
        self.initCurrent = tk.Entry(self.master, textvariable=initialCurrent, font=('Arial bold', 18), width=5, bg=None, fg="#E46000", justify="center")
        self.initCurrent.insert(0,0)
        self.initCurrent.place(x=410,y=150)
        
        # SOLVE
        self.solveBtn = tk.Button(self.master, text="Solve", font=('Arial bold', 18), image=self.btnEnd, relief="flat", command=self.solveClicked)
        self.solveBtn.place(x=39,y=664)
        
        self.exitBtn = tk.Button(self.master, text="EXIT", bg="red", fg="white", font=('Arial Bold',14), command=self.exitApp)
        self.exitBtn.place(x=200,y=665)
        
        # USE SLIDER
        self.sliderState = tk.IntVar()
        self.useSlider = tk.Checkbutton(self.master, command=self.useSlider, relief='flat', font=('Arial', 12),  variable=self.sliderState, onvalue=1, offvalue=0)
        self.useSlider.place(x=350,y=670)
        
        # ANSWER
        self.func = tk.Text(self.master, font=('Arial', 12), height=2, padx=10, pady=10, width=68)
        self.func.place(x=686,y=590)   
        
        self.master.mainloop()
    
    def useSlider(self):
        slideState = self.sliderState.get()
        
        if slideState == 1:
            self.resistance.destroy()
            self.inductance.destroy()
            self.capacitance.destroy()
            self.voltage.destroy()
            
            self.resistance = tk.Scale(self.master, showvalue=0, cursor="dot", variable=ohms, font=('Arial', 15), from_=0, to=20, orient='horizontal', length=180, digits = 3, resolution = 0.1)
            self.resistance.place(x=94,y=104)
            
            self.inductance = tk.Scale(self.master, showvalue=0, cursor="dot", variable=henry, font=('Arial', 15), from_=0, to=15, orient='horizontal', length=180, digits = 3, resolution = 0.1)
            self.inductance.place(x=94,y=162)
            
            self.capacitance = tk.Scale(self.master, showvalue=0, cursor="dot", variable=farad, font=('Arial', 15), from_=0, to=10, orient='horizontal', length=180, digits = 3, resolution = 0.1)
            self.capacitance.place(x=94,y=220)
            
            self.voltage = tk.Scale(self.master, showvalue=0, cursor="dot", variable=volts, font=('Arial', 15), from_=0, to=100, orient='horizontal', length=180)
            self.voltage.place(x=94,y=278)
            if sineState.get() == 1:
                self.voltage.config(state='disabled')
            
        else:
            self.resistance.destroy()
            self.inductance.destroy()
            self.capacitance.destroy()
            self.voltage.destroy()
            
            self.resistance = tk.Entry(self.master, textvariable=ohms, font=('Arial bold', 16), width=12, bg=None)
            self.resistance.place(x=94,y=102)
            
            self.inductance = tk.Entry(self.master, textvariable=henry, font=('Arial bold', 16), width=12, bg=None)
            self.inductance.place(x=94,y=160)
            
            self.capacitance = tk.Entry(self.master, textvariable=farad, font=('Arial bold', 16), width=12, bg=None)
            self.capacitance.place(x=94,y=218)
            
            self.voltage = tk.Entry(self.master, textvariable=volts, font=('Arial bold', 16), width=12, bg=None)
            self.voltage.place(x=94,y=276)
            if sineState.get() == 1:
                self.voltage.config(state='disabled')
    
    
    def sineClicked(self):
        sinState = sineState.get()
        if(sinState == 1):
            self.Vlabel.config(textvariable=amp)
            self.voltage.config(state='disabled')
        else:
            self.Vlabel.config(textvariable=volts)
            self.voltage.config(state='normal')
        
        
    def solveClicked(self):          
        E = float(self.voltage.get()) if sineState.get() == 0 else float(self.amplitude.get())*sp.sin(float(self.angFrequency.get())*self.t)
        R = float(self.resistance.get())
        L = float(self.inductance.get())
        C = float(self.capacitance.get())
        q0 = float(self.initCharge.get())
        i0 = float(self.initCurrent.get())

        it = self.solveDiffEqn(E, R, L, C, q0, i0)
        print("Done solving...")
        
        self.func.config(state="normal")
        self.func.delete('1.0', tk.END)
        self.func.insert(tk.END, f"i(t) = {str(it)}")
        self.func.config(state="disabled")
        
        solveInfo = tk.Label(self.master, text="Generating animation . . .", font=('Arial', 12), bg="red", fg="white")       
        solveInfo.place(x=680,y=104)
        
        self.generateAnimation(it)
        
        self.play_gif()
        
        
    def solveDiffEqn(self, voltage, resistance, inductance, capacitance, initQ, initI):
        diff_eq = sp.Eq( (inductance*self.q(self.t).diff(self.t,self.t)) + (resistance*self.q(self.t).diff(self.t)) + ((1/capacitance)*self.q(self.t)), voltage)
        ivp = sp.dsolve(diff_eq, ics={self.q(0): initQ, sp.diff(self.q(self.t),self.t).subs(self.t,0): initI})     
        return ivp.rhs.diff(self.t).simplify()
    
    
    def getCurrent(self, currentFunc, x):
        return currentFunc.subs(self.t,x)
    
    
    def generateAnimation(self, currentEqn):
        messagebox.showinfo("RLC Current Visualizer", "Solving the differential equation...")
            
        fig=plt.figure()
        l, =plt.plot([],[], color="red")
        p1, = plt.plot([], [], 'ko')
        plt.xlabel('Time')
        plt.ylabel('Current')
        plt.title('Current x Time')
        
        ylim = int(self.voltage.get()) + 3
        plt.xlim(0,30)
        plt.ylim(-ylim,ylim)
            
        metadata=dict(title="Current i",artist="kurt")
        writer= anime.PillowWriter(fps=15,metadata=metadata)
            
        time=[]
        currentI=[]
        with writer.saving(fig,"Current.gif",100):
            print("Generating animation...")
            for timeVal in np.linspace(0,50,250):
                time.append(timeVal)
                currentI.append(self.getCurrent(currentEqn,timeVal))
                l.set_data(time,currentI)
                p1.set_data(timeVal,self.getCurrent(currentEqn,timeVal))
                writer.grab_frame()
                    
        print("Done.")
        plt.clf()
        plt.close()
        
        
    def play_gif(self):
        Image.MAX_IMAGE_PIXELS = 933120000000
        global img
        img= Image.open('Current.gif')
        
        gifLbl = tk.Label(self.master)       
        gifLbl.place(x=680,y=104)
        
        for img in ImageSequence.Iterator(img):
            img = ImageTk.PhotoImage(img)
            gifLbl.config(image=img)
            self.master.update()
            time.sleep(0.01)
        
        self.master.after(200, self.play_gif)
    
    
    def exitApp(self):
        self.master.destroy()
        
        
gui = RLCViz() 