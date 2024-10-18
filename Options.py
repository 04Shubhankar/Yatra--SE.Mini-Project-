import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL

def main():
    import RegressionModel

    def update_date():
        current_date = datetime.now().strftime("%Y-%m-%d\n %H:%M:%S")
        date_label.config(text=current_date, font=("Arial", 20), bg="white")
        date_label.after(1000, update_date)

    # Define functions for each toll collection option
    def toll_collection():
        RegressionModel.tollcollected()  # Call the function with parentheses

    def toll_head():
        RegressionModel.head()  # Call the function with parentheses

    # Define functions for each traffic analysis option
    def traffic_vs_day():
        RegressionModel.trafficvsday()  # Call the function with parentheses

    def traffic_head():
        RegressionModel.head()  # Call the function with parentheses

    def model_accuracy():
        RegressionModel.actualvspredicted()  # Call the function with parentheses

    def projection():
        RegressionModel.predictnew()  # Call the function with parentheses

    def toll_selection(selected_option):
        print(f"Toll Collection Statistics selected: {selected_option}")
        if selected_option == "Collection":
            toll_collection()
        elif selected_option == "Head":
            toll_head()
        # Clear the 'Head' option from the Traffic Analysis Report dropdown
        traffic_var.set("")  # Set the traffic variable to empty after selection

    def traffic_selection(selected_option):
        print(f"Traffic Analysis Report selected: {selected_option}")
        if selected_option == "Traffic vs Day":
            traffic_vs_day()
        elif selected_option == "Head":
            traffic_head()
        elif selected_option == "Model Accuracy":
            model_accuracy()
        elif selected_option == "Projection":
            projection()
        # Clear the 'Head' option from the Toll Collection Statistics dropdown
        toll_var.set("")  # Set the toll variable to empty after selection

    def clear_heads():
        # Clear the 'Head' option from both dropdowns after 3 seconds
        toll_var.set("")    # Clear toll variable
        traffic_var.set("") # Clear traffic variable

    # Main application window
    root = tk.Tk()
    root.title("Yatra")
    root.geometry("770x480")
    root.configure(bg="white")


    # Create a date label for the main window
    date_label = tk.Label(root, font=("Arial", 20))
    date_label.pack(side="bottom", pady=(40, 20))
    update_date()

    # Application name label
    app_label = tk.Label(root, text="Y.A.T.R.A\n\tYielding Advanced Research and Traffic Analysis", font=("Arial Bold", 20, "bold"), bg="white")
    app_label.place(relx=0.5, rely=0.1, anchor='center')

    # Dropdown for Toll Collection Statistics
    toll_label = tk.Label(root, text="Toll Collection Statistics", font=("Arial", 14), bg="white")
    toll_label.place(relx=0.4, rely=0.4, anchor='e')

    toll_options = ["Collection", "Head"]
    toll_var = tk.StringVar(value="Head")  # Set default value to 'Head'

    # Create OptionMenu with command to call toll_selection function
    toll_menu = tk.OptionMenu(root, toll_var, *toll_options, command=toll_selection)
    toll_menu.place(relx=0.6, rely=0.4, anchor='w')

    # Dropdown for Traffic Analysis Report
    traffic_label = tk.Label(root, text="Traffic Analysis Report", font=("Arial", 14), bg="white")
    traffic_label.place(relx=0.4, rely=0.6, anchor='e')

    traffic_options = ["Traffic vs Day", "Head", "Model Accuracy", "Projection"]
    traffic_var = tk.StringVar(value="Head")  # Set default value to 'Head'

    # Create OptionMenu with command to call traffic_selection function
    traffic_menu = tk.OptionMenu(root, traffic_var, *traffic_options, command=traffic_selection)
    traffic_menu.place(relx=0.6, rely=0.6, anchor='w')

    # Clear both 'Head' options after 3 seconds
    root.after(3000, clear_heads)

    # Run the main loop
    root.mainloop()

