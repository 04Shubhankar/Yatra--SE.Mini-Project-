import tkinter as tk
import pandas as pd  # Import pandas for potential DataFrame usage
import RegressionModel
import LoginPage



root = tk.Tk()
root.title("Yatra")



button1 = tk.Button(root, text="Traffic VS Day",command = RegressionModel.trafficvsday)
button1.pack()

button2 = tk.Button(root, text="Actual VS Predicted",command = RegressionModel.actualvspredicted)
button2.pack()

button3 = tk.Button(root, text="Collected Toll",command = RegressionModel.tollcollected)
button3.pack()

button4 = tk.Button(root, text="Head",command = RegressionModel.head)
button4.pack()

button5 = tk.Button(root, text="Predict",command = RegressionModel.predictnew)
button5.pack()


root.mainloop()
