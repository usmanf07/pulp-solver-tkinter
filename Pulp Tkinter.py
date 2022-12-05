import tkinter as tk
import tkinter.ttk as ttk
from pulp import *
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import time

toplevel2 = None     #Main Top Level
frame1 = None  #Main Frame

prob = None     #LP Problem Variable
probType = None     #Lp Problem Type
option1 = False     #Step1 Option Check
option2 = False     #Step2 Option Check
option3 = False     #Step3 Option Check
option4 = False     #Step4 Option Check
option5 = False     #Step5 Option Check

############## Decision Variable Config ###############
entries = []        #Decision Variable Text Field Entries
descVar = []        #Decision Variables in LP Variable
descVarCoff = []    ##Decision Variables Cofficients in LP Variable
numDescVarField = None  #Total No. of Decision Variables Text Field
numDecsVar = None   #Total No. of Decision Variables
dx = 80
dy = 135
############## Constraints Variable Config ###############
numConstField = None  #Total No. of Constraints Text Field
numConst = None   #Total No. of Constraints
constVarCoff = []   #Cofficients of constraints Array
# empty arrays for your Entrys and StringVars
text_var = []
entries2 = [] 
matrix = [] 
m = 0.05
n = dy + 0.15
setConstraintMatrix = None  #Find Solution Button
addConstraintBtn = None  #Add Constraint Button

############################################
toplevel2 = tk.Tk()     #Main Top Level
frame1 = ttk.Frame(toplevel2)   #Main Frame
    
def setConstraintMatrixFunc():
    setConstraintMatrix["state"] = "disabled"
    addConstraintBtn["state"] = "disabled"
    global option5
    if not option5:
        constraint = []
        for i in range(numConst):
            constName = "Const" + str(i + 1)
            for j in range(numDecsVar):
                constraint.append(float(text_var[i][j].get()))
            rhs = float(entries2[i][j + 2].get())
            symbol = entries2[i][j + 1].get()
            print(constraint)
            global prob
            if symbol == ">=":
                cons = lpSum([constraint[g]*descVar[g] for g in range(numDecsVar)]) >= rhs, constName
                print(cons)
                prob += cons
                constraint = []
            if symbol == "<=":
                cons = lpSum([constraint[g]*descVar[g] for g in range(numDecsVar)]) <= rhs, constName
                print(cons)
                prob += cons
                constraint = []
            if symbol == "=":
                cons = lpSum([constraint[g]*descVar[g] for g in range(numDecsVar)]) == rhs, constName
                print(cons)
                prob += cons
                constraint = []
        global n
        start = time.perf_counter()
        prob.solve()
        total = time.perf_counter() - start
        solution = ttk.Label(frame1)
        solution.configure(text='Status:' + LpStatus[prob.status],  font=('TkTextFont 15'))
        n+=50
        solution.place(anchor="nw", x = 10, y = n)
        
        optimalValue = ttk.Label(frame1)
        optimalValue.configure(text='Optimal Value:' + str(value(prob.objective)),  font=('TkTextFont 15'))
        optimalValue.place(anchor="nw", x = 10, y= n + 40)

        myx = 10
        for x in prob.variables():
            optimalvar = ttk.Label(frame1)
            optimalvar.configure(text=x.name + '=' + str(x.varValue),  font=('TkTextFont 15'))
            optimalvar.place(anchor="nw", x = myx, y = n + 80)
            print(len(str(x.varValue)))
            myx += 22*len(str(x.varValue))
            
        timetaken = str(total)
        cputime = ttk.Label(frame1)
        cputime.configure(text='Time Taken(S):' + timetaken[0:5],  font=('TkTextFont 15'))
        cputime.place(anchor="nw", x = 10, y = n+130)
        option5 = True
    return

def addNewConstraint():
    global numConst
    i = numConst
    numConst += 1
    text_var.append([])
    entries2.append([])

    global m
    global n
    for j in range(numDecsVar):
        # append your StringVar and Entry
        text_var[i].append(StringVar())
        entries2[i].append(Entry(frame1, textvariable=text_var[i][j], width = 4))
        descx1 = ttk.Label(frame1)
        descx1.configure(text="X" + str(j + 1), font=('TkTextFont 10'))
        descx1.place(anchor="nw", x = m + 40, y = n)

        if j != numDecsVar - 1:
            plus_sign = ttk.Label(frame1)
            plus_sign.configure(text="+", font=('TkTextFont 10'))
            plus_sign.place(anchor="nw", x=m + 60, y=n)
        entries2[i][j].place(x = m, y = n)
        m += 80

    symbol = ttk.Combobox(frame1)
    symbol.configure(values='<= = >=', width=3, state="readonly")
    symbol.current(0)
    symbol.place(anchor="nw", x = m - 10, y = n)
    entries2[i].append(symbol)

    en = Entry(toplevel2)
    en.configure(width = 5)
    en.place(anchor="nw", x = m + 50, y = n + 10)
    entries2[i].append(en)

    n += 30
    m = 10
    global addConstraintBtn
    addConstraintBtn.place(anchor="nw", x = 100, y = n + 5)

    global setConstraintMatrix
    setConstraintMatrix.place(anchor="nw", x = 10, y = n + 5)
    return

def genConstraintsFunc():
    global option4
    if not option4:
        global numConst
        global dy
        dy+=45
        numConst = int(numConstField.get())
        if numConst > 0:
            step5 = ttk.Label(frame1)
            step5.configure(text='Step 5. Fill the Constraints Matrix', font="TkTextFont 10")
            step5.place(anchor="nw", x = 10, y = dy)
            
            x2 = 0
            y2 = 0
            global n
            global m
            m = 10
            n = dy + 20
            rows, cols = (numConst, numDecsVar)
            for i in range(rows):
                # append an empty list to your two arrays
                # so you can append to those later
                text_var.append([])
                entries2.append([])
                
                for j in range(cols):
                    # append your StringVar and Entry
                    text_var[i].append(StringVar())
                    entries2[i].append(Entry(frame1, textvariable=text_var[i][j], width = 4))
                    descx1 = ttk.Label(frame1)
                    descx1.configure(text="X" + str(j + 1), font=('TkTextFont 10'))
                    descx1.place(anchor="nw", x = m + 40, y = n)

                    if j != numDecsVar - 1:
                        plus_sign = ttk.Label(frame1)
                        plus_sign.configure(text="+", font=('TkTextFont 10'))
                        plus_sign.place(anchor="nw", x=m + 60, y=n)
                    entries2[i][j].place(x = m, y = n)
                    m += 80

                symbol = ttk.Combobox(frame1)
                symbol.configure(values='<= = >=', width=3, state="readonly")
                symbol.current(0)
                symbol.place(anchor="nw", x = m - 10, y = n)
                entries2[i].append(symbol)

                en = Entry(toplevel2)
                en.configure(width = 5)
                en.place(anchor="nw", x = m + 50, y = n + 10)
                entries2[i].append(en)

                n += 30
                m = 10
            
            global setConstraintMatrix
            setConstraintMatrix = ttk.Button(frame1)
            setConstraintMatrix.configure(text='Find Solution!')
            setConstraintMatrix.place(
            anchor="nw", x = 10, y = n + 5)
            setConstraintMatrix.configure(command=lambda :setConstraintMatrixFunc())

            global addConstraintBtn
            addConstraintBtn = ttk.Button(frame1)
            addConstraintBtn.configure(text='Add Constraint')
            addConstraintBtn.place(
            anchor="nw", x = 100, y = n + 5)
            addConstraintBtn.configure(command=lambda :addNewConstraint())

            option4 = True
    return

def setObjectiveFunc():
    global option3
    if not option3:
        for x in range(numDecsVar):     #Make Array of LP Variables
            var_ = 'x' + str(x + 1)
            descVar.append(LpVariable(var_, 0))
        
        for x in range(numDecsVar):     #Make Array of Constraints
            var_ = 'x' + str(x + 1)
            n = float(entries[x].get())
            descVarCoff.append(n)

        global prob
        prob += lpSum([descVarCoff[i]*descVar[i] for i in range(numDecsVar)])       #Assign to the global function
        global dy
        dy += 45
        totConst = ttk.Label(frame1)
        totConst.configure(text='Step 4. Enter Total Constraints:', font="TkTextFont 10")
        totConst.place(anchor="nw", x=10, y=dy)

        global numConstField
        numConstField = ttk.Entry(frame1)
        numConstField.place(anchor="nw", x=10, y=dy+20, width=35)

        genConstraintMatrix = ttk.Button(frame1)
        genConstraintMatrix.configure(text='Make Constraints Matrix')
        genConstraintMatrix.place(
        anchor="nw", x = 50, y = dy + 20)
        genConstraintMatrix.configure(command=lambda :genConstraintsFunc())
        option3 = True
    return

def generateObjectiveFunc():
    global option2
    if not option2:
        global numDecsVar
        global numDescVarField
        numDecsVar = int(numDescVarField.get())
        if numDecsVar > 0:
            step3Lbl = ttk.Label(frame1)
            step3Lbl.configure(text='Step 3. Fill the Objective Function:', font="TkTextFont 10")
            step3Lbl.place(anchor="nw", x=10, y=105)
            probTypeLbl = ttk.Label(frame1)
            if probType == "max":
                probTypeLbl.configure(text='Max Z = ', font="TkTextFont 10")
            else:
                probTypeLbl.configure(text='Min Z = ', font="TkTextFont 10")

            probTypeLbl.place(anchor="nw", x = 10, y=125)
            global entries
            global dx
            global dy

            buttony = 0.23
            for i in range(numDecsVar):
                en = Entry(toplevel2)
                en.configure(width=5)
                en.place(anchor="nw", x = dx, y = dy)
                descx1 = ttk.Label(frame1)
                descx1.configure(text="X" + str(i + 1), font=('TkTextFont 10'))
                descx1.place(anchor="nw", x = dx + 30, y = dy - 10)
                if i != numDecsVar - 1:
                    plus_sign = ttk.Label(frame1)
                    plus_sign.configure(text="+", font=('Arial 10'))
                    plus_sign.place(anchor="nw", x = dx + 55, y = dy - 10)
                dx += 85
                # if dx > 0.97:
                #     dx = 0.22
                #     dy += 0.06
                    
                entries.append(en)
            
            setObjFuncBtn = ttk.Button(frame1)
            setObjFuncBtn.configure(text='Done')
            setObjFuncBtn.place(anchor="nw", x = 8, y = dy + 15)
            setObjFuncBtn.configure(command=lambda :setObjectiveFunc())
            option2 = True
    return

def problemType(type):
    global option1
    if not option1:
        if type == "max":
            global prob
            prob = LpProblem("Question", LpMaximize)
        if type == "min":
            prob = LpProblem("Question", LpMinimize)
        #print(type)
        global probType
        probType = type
        descLbl = ttk.Label(frame1)
        descLbl.configure(text='Step 2. Enter Total Decision Variables:', font="TkTextFont 10")
        descLbl.place(anchor="nw", x=10, y=50)
        global numDescVarField
        numDescVarField = ttk.Entry(frame1)
        numDescVarField.place(anchor="nw", x=10, y=75, width=35)

        genObjFunc = ttk.Button(frame1)
        genObjFunc.configure(text='Make Objective Equation')
        genObjFunc.place(anchor="nw", x=50, y=75)
        genObjFunc.configure(command=lambda :generateObjectiveFunc())
        option1 = True
    return

def main():
    # build ui
    toplevel2.configure(height=900, width=700)
    toplevel2.geometry("500x700")
    toplevel2.maxsize(1920, 1080)
    toplevel2.minsize(900, 720)
    toplevel2.title("Pulp Solver By Usman (20L-1385)")

    frame1.configure(height=1080, padding=10, width=1920)
    
    titleLbl = ttk.Label(frame1)
    titleLbl.configure(
        font="TkTextFont 20",
        text='Pulp Solver By Usman (20L-1385)')
    titleLbl.pack(side="top")
    probLbl = ttk.Label(frame1)
    probLbl.configure(text='Step 1. Choose Problem Type:', font="TkTextFont 10")
    probLbl.place(anchor="nw", x=10, y=0)
    

    #Maximization Button
    maxBtn = ttk.Button(frame1)
    maxBtn.configure(text='Maximization')
    maxBtn.place(anchor="nw", x=10, y=20)
    maxBtn.configure(command=lambda m="max":problemType(m))

    #Minimization Button
    minBtn = ttk.Button(frame1)
    minBtn.configure(text='Minimization')
    minBtn.place(anchor="nw", x=100, y=20)
    minBtn.configure(command=lambda m="min":problemType(m))

    frame1.place(anchor="nw", relheight=1.0, relwidth=1.0, x=0, y=0)

    # Main widget
    mainwindow = toplevel2

    mainwindow.mainloop()


if __name__ == '__main__':
    main()



