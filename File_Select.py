import DatasetSelect

def file_select():
        file = DatasetSelect.open_file_dialog()
        if file is None:
            print("No file selected. Exiting.")
            exit()  # Exit if no file is selected

        return file
