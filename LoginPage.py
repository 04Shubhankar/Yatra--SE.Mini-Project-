import tkinter as tk
from PIL import Image, ImageTk
import cv2
from datetime import datetime
import SQLcheck

def main():
    global login_success
    login_success = False

    def show_camera_feed():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (200, 150))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)

            camera_label.img_tk = img_tk
            camera_label.config(image=img_tk)

        camera_label.after(1, show_camera_feed)

    def get_values():
        pan_value = pan.get()
        login_name_value = login.get()
        password_value = password.get()
        
        if len(pan_value) == 0 or len(login_name_value) == 0 or len(password_value) == 0:
            return False, None, None, None
        else:
            return True, pan_value, login_name_value, password_value

    def hide_invalid_label():
        invalid.place_forget()

    def show_success_message():
        global login_success
        login_success = True
        success_label = tk.Label(root, text="Login Successful", font=("Arial", 24), fg="green", bg="white")
        success_label.place(relx=0.5, rely=0.5, anchor='center')
        root.after(2000, root.destroy)  # Wait for 2 seconds before closing

    def validate_and_capture_image():
        is_valid, pan_value, login_name_value, password_value = get_values()

        if not is_valid:
            invalid.place(relx=0.5, rely=0.8, anchor='center')
            print("Invalid input, cannot save image.")
            root.after(3000, hide_invalid_label)
            return False
        else:
            if SQLcheck.validate_login(pan_value, login_name_value, password_value):
                invalid.place_forget()
                capture_image()
                show_success_message()
                return True
            else:
                invalid.place(relx=0.5, rely=0.8, anchor='center')
                print("Invalid credentials.")
                root.after(3000, hide_invalid_label)
                return False

    def capture_image():
        ret, frame = cap.read()
        if ret:
            current_time = datetime.now()
            time_string = current_time.strftime("%H-%M-%S")
            is_valid, pan_value, login_name_value, password_value = get_values()

            if is_valid:
                filename = f"{pan_value}_{time_string}.png"
                cv2.imwrite(filename, frame)
                print(f"Image saved as {filename}")
            else:
                print("Invalid input, cannot save image.")
        else:
            print("Failed to capture image")

    root = tk.Tk()
    root.title("Yatra")
    root.geometry("770x480")
    root.configure(bg="white")

    def update_date():
        current_date = datetime.now().strftime("%Y-%m-%d\n %H:%M:%S")
        date_label.config(text=current_date, font=(12), bg="white")
        date_label.after(1000, update_date)

    date_label = tk.Label(root, font=("Arial", 20))
    date_label.pack(side="bottom", pady=(40, 20))
    update_date()

    icon_image = Image.open("logo.png")
    resized_icon_image = icon_image.resize((100, 100))
    logo = ImageTk.PhotoImage(resized_icon_image)
    root.wm_iconphoto(False, logo)

    center_frame = tk.Frame(root, bg="white")
    center_frame.pack(expand=True, fill="both")

    app_name_label = tk.Label(center_frame, text="  Yielding Advanced Research and \n Traffic Analytics",
                              font=("Arial", 24, "bold"), bg="white", image=logo, compound="left")
    app_name_label.place(relx=0.41, rely=0.1, anchor='center')

    login_label = tk.Label(center_frame, text="  LOGIN  🔐", font=("Arial Bold", 20), bg="white")
    login_label.place(relx=0.5, rely=0.29, anchor='center')

    login_govtid = tk.Label(center_frame, text="P.A.N Number ", font=("Arial Bold", 18), bg="white")
    login_govtid.place(relx=0.3, rely=0.4, anchor='e')

    pan = tk.Entry(center_frame, width=20)
    pan.place(relx=0.4, rely=0.4, anchor='w')

    login_name_label = tk.Label(center_frame, text="Name (As On ID)", font=("Arial Bold", 18), bg="white")
    login_name_label.place(relx=0.3, rely=0.55, anchor='e')

    login = tk.Entry(center_frame, width=20)
    login.place(relx=0.4, rely=0.55, anchor='w')

    login_pass = tk.Label(center_frame, text="Password", font=("Arial Bold", 18), bg="white")
    login_pass.place(relx=0.3, rely=0.7, anchor='e')

    password = tk.Entry(center_frame, width=20, show='*')
    password.place(relx=0.4, rely=0.7, anchor='w')

    loginbutton = tk.Button(center_frame, text="Login 🔐", bg="skyblue", font=(13), command=validate_and_capture_image)
    loginbutton.place(relx=0.48, rely=0.85, anchor='center')

    disclaimer = tk.Label(center_frame, text="Disclaimer - A real-time photo of the user will be captured and used for authentication", bg="white", font=("Arial Bold", 10))
    disclaimer.place(relx=0.5, rely=0.95, anchor='center')

    camera_label = tk.Label(center_frame, bg="white")
    camera_label.place(relx=0.8, rely=0.5, anchor='center')

    invalid = tk.Label(center_frame, text="Invalid Input", font=("Arial", 18, "bold"), fg="red", bg="white")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    show_camera_feed()

    root.mainloop()

    cap.release()
    cv2.destroyAllWindows()
    
    print(login_success)  # Print the value of login_success to verify

    return login_success
