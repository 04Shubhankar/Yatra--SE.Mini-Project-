import pandas as pd
import tkinter as tk
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DatasetSelect

file = DatasetSelect.open_file_dialog()
if file is None:
    print("No file selected. Exiting.")
    exit()  # Exit if no file is selected

# Load and prepare the training data
data = pd.read_csv(file)

# Format the date using pandas
data['date_time'] = pd.to_datetime(data['date_time'], format='%d-%m-%Y %H:%M')

# Drop rows with missing 'traffic_volume'
data = data.dropna(subset=['traffic_volume'])

# Extract features and target (excluding 'toll_collected')
X = data[['temp', 'clouds_all', 'rain_1h']]
y = data['traffic_volume']

# Handle missing values and create polynomial features
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_imputed)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Fit the polynomial regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Predict traffic volume on the testing data
y_test_pred = model.predict(X_test)

# Predict traffic volume on the entire dataset for plotting
y_pred = model.predict(X_poly)
data['predicted_traffic_volume'] = y_pred

# Convert datetime to numerical values for polynomial fitting
data['date_numeric'] = (data['date_time'] - data['date_time'].min()) / np.timedelta64(1, 'D')

# Prepare feature and target for polynomial fitting (excluding 'toll_collected')
X_date = data[['date_numeric']]
y_date = data['traffic_volume']

# Create polynomial features for dates
poly_date = PolynomialFeatures(degree=2)
X_date_poly = poly_date.fit_transform(X_date)

# Fit polynomial regression model for dates
model_date = LinearRegression()
model_date.fit(X_date_poly, y_date)

# Predict traffic volume based on dates
date_range = np.linspace(X_date.min(), X_date.max(), 500).reshape(-1, 1)
date_range_poly = poly_date.transform(date_range)
y_date_pred = model_date.predict(date_range_poly)

def trafficvsday():
    # Plot
    plt.figure(figsize=(14, 9))
    plt.scatter(data['date_numeric'], y_date, color='blue', label='Actual Traffic Volume', alpha=0.5)
    plt.plot(date_range, y_date_pred, color='red', linestyle='--', linewidth=2, label='Polynomial Regression Line')
    plt.xlabel('Days Since Start')
    plt.ylabel('Traffic Volume')
    plt.title('Traffic Volume vs. Days Since Start: Polynomial Regression')
    plt.legend()
    plt.grid(True)
    plt.show()

def actualvspredicted():
    # Plot 1: Actual vs. Predicted Traffic Volume Over Time
    plt.figure(figsize=(16, 8))
    plt.plot(data['date_time'], data['traffic_volume'], color='blue', label='Actual Traffic Volume', linewidth=1.5)
    plt.plot(data['date_time'], data['predicted_traffic_volume'], color='red', linestyle='--', label='Predicted Traffic Volume', linewidth=1.5)
    plt.xlabel('Date Time')
    plt.ylabel('Traffic Volume')
    plt.title('Traffic Volume Over Time: Actual vs. Predicted')
    plt.legend()
    plt.grid(True)

    # Adjust x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def tollcollected():
    # Plot 2: Toll Collected Over Time
    plt.figure(figsize=(16, 8))
    plt.plot(data['date_time'], data['toll_collected'], color='green', linestyle=':', label='Toll Collected', linewidth=1.5)
    plt.xlabel('Date Time')
    plt.ylabel('Toll Collected')
    plt.title('Toll Collected Over Time')
    plt.legend()
    plt.grid(True)

    # Adjust x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.show()

def historicalvsnew():
    # Combine historical and predicted data
    combined_df = data[['date_time', 'traffic_volume', 'predicted_traffic_volume']]
    combined_df = combined_df.rename(columns={'traffic_volume': 'Volume', 'predicted_traffic_volume': 'Predicted Volume'})
    combined_df['Type'] = 'Historical Data'

    # Plot Historical Traffic Volumes
    plt.figure(figsize=(16, 7))
    plt.plot(data['date_time'], data['traffic_volume'], color='blue', label='Historical Traffic Volume', linewidth=1.5)
    plt.plot(data['date_time'], data['predicted_traffic_volume'], color='red', linestyle='--', label='Predicted Traffic Volume', linewidth=1.5)
    plt.xlabel('Date Time')
    plt.ylabel('Traffic Volume')
    plt.title('Traffic Volume Over Time: Historical Data and Predictions')
    plt.legend()
    plt.grid(True)

    # Adjust x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def head():
    def get():
        # Get user input and convert to integer (assuming valid input)
        rows = int(entry.get())

        # Create a Text widget to display the output
        text_widget = tk.Text(root, height=rows)
        text_widget.pack(fill="both", expand=True)

        # Insert the output into the Text widget
        head_string = data.head(rows).to_string()
        text_widget.delete("1.0", tk.END)  # Clear existing text
        text_widget.insert(tk.END, head_string)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configure scrollbar and Text widget connection
        text_widget.config(yscrollcommand=scrollbar.set)

    # Create the Tkinter window
    root = tk.Tk()
    root.title("DataFrame Head")

    # Create an Entry widget
    entry = tk.Entry(root, bg="lightblue", fg="black", font=("Arial", 12), justify="center")
    entry.pack()
    button4 = tk.Button(root, text="Head", command=get)
    button4.pack()

    # Start the Tkinter event loop
    root.mainloop()

def predictnew():
    # Load new data for prediction
    new_data = pd.read_csv('PredictionSet.csv')

    # Format the date using pandas
    new_data['date_time'] = pd.to_datetime(new_data['date_time'], format='%d-%m-%Y %H:%M')

    # Extract features (excluding 'toll_collected' and 'traffic_volume')
    X_new = new_data[['temp', 'clouds_all', 'rain_1h']]
    
    # Handle missing values: Impute missing values in features
    X_new_imputed = imputer.transform(X_new)
    
    # Create polynomial features for new data (must match the training set)
    X_new_poly = poly.transform(X_new_imputed)

    # Predict traffic volume using the trained model
    new_data['predicted_traffic_volume'] = model.predict(X_new_poly)

    # Display the predictions in a new Tkinter window
    display_predictions(new_data)

def display_predictions(new_data):
    # Create a new Tkinter window
    pred_window = tk.Tk()
    pred_window.title("Predictions")

    # Create a Text widget to display the predicted values
    text_widget = tk.Text(pred_window, height=20, width=80)
    text_widget.pack(fill="both", expand=True)

    # Insert the predicted values into the Text widget
    pred_string = new_data[['date_time', 'predicted_traffic_volume']].to_string(index=False)
    text_widget.delete("1.0", tk.END)  # Clear existing text
    text_widget.insert(tk.END, pred_string)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(pred_window, orient=tk.VERTICAL, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Configure scrollbar and Text widget connection
    text_widget.config(yscrollcommand=scrollbar.set)

    # Create a Matplotlib figure for the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the predicted values
    ax.plot(new_data['date_time'], new_data['predicted_traffic_volume'], color='red', label='Predicted Traffic Volume', linewidth=1.5)
    ax.set_xlabel('Date Time')
    ax.set_ylabel('Predicted Traffic Volume')
    ax.set_title('Predicted Traffic Volume Over Time')
    ax.legend()
    ax.grid(True)

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=pred_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


