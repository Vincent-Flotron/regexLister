import tkinter as tk
from ApproxScore    import ApproxScore
from DbConnection   import DbConnection
from RegexRecord    import RegexRecord, RegexRecordsList
from Configuration  import Configuration
from DefaultConfig  import DefaultConfig
import os

# Read settings from config file
config         = Configuration()
initial_width  = int(config.read_value('Window', 'width', DefaultConfig.get_width()))
initial_height = int(config.read_value('Window', 'height', DefaultConfig.get_hight()))

# Function to perform approximative search
def approximativeSearch(input_text):
    db_relative_path = 'regex_database.db'
    db_path          = os.path.join(os.path.dirname(__file__), db_relative_path)

    db_conn          = DbConnection(db_path)
    table_name       = 'regex'

    # Execute SQL query to fetch records
    records = db_conn.execute_query(f"SELECT id, short_description FROM {table_name} ORDER BY id")

    ids, short_descriptions = zip(*records)

    match_scores = ApproxScore.approx_score(short_descriptions, input_text)

    reg_rec_list = RegexRecordsList(fields_names=db_conn.get_table_fields(table_name))
    for id, m in zip(ids, match_scores):
        reg_rec_list.append(RegexRecord(id, m['item'], None, None, m['score']))

    reg_rec_match_list = reg_rec_list.get_match_only()
    ids = reg_rec_match_list.get_list_attribute_values('id')

    # Create a string with placeholders for the list of short descriptions
    placeholders = ', '.join(['?'] * len(ids))

    # Execute SQL query to fetch records
    records = db_conn.execute_query(f"SELECT * FROM {table_name} WHERE id IN ({placeholders}) ORDER BY id", ids)

    reg_rec_match_list.complete_fields(records)
    reg_rec_match_list.add_a_field_name('match_score')

    reg_rec_match_list.sort_by_match_score_desc()

    return reg_rec_match_list


# Function to display search results
def displayResults():
    input_text = entry.get()
    reg_rec_match_list = approximativeSearch(input_text)

    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Get field names and create header labels
    field_names = reg_rec_match_list.get_field_names()
    for j, field_name in enumerate(field_names):
        header_label = tk.Label(result_frame, text=field_name, padx=10, pady=5, relief=tk.SOLID, borderwidth=1)
        header_label.grid(row=0, column=j, sticky="nsew")

    # Display search results
    for i, reg_rec_match in enumerate(reg_rec_match_list.items(), start=1):
        fields = reg_rec_match.get_all_attributes()
        for j, field in enumerate(fields):
            result_label = tk.Label(result_frame, text=field, padx=10, pady=5, relief=tk.SOLID, borderwidth=1)
            result_label.grid(row=i, column=j, sticky="nsew")
            result_label.bind("<Button-1>", lambda event, text=field: copyToClipboard(text))


# Function to copy content to clipboard
def copyToClipboard(text):
    fill_clipboard(text)
    # tkinter.messagebox.showinfo("Clipboard", f"{text} copied to clipboard")

def fill_clipboard(text):
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(text)  # Append "Hello World" to the clipboard


# Create main window
root = tk.Tk()
root.title("Approximative Search")

# Set initial window size
root.geometry(f"{initial_width}x{initial_height}")

# Create input field
entry_label = tk.Label(root, text="Enter search text:")
entry_label.pack()
entry = tk.Entry(root)
entry.pack()

# Create search button
search_button = tk.Button(root, text="Search", command=displayResults)
search_button.pack()

# Create frame for displaying results
result_frame = tk.Frame(root)
result_frame.pack()

# Make the result frame expandable
for i in range(3):
    result_frame.columnconfigure(i, weight=1)
result_frame.rowconfigure(0, weight=1)

# Create status bar
status_bar = tk.Label(root, text="Window size: (0, 0)")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Update status bar with window size
def update_status_bar(event):
    size = f"Window size: ({root.winfo_width()}, {root.winfo_height()})"
    status_bar.config(text=size)

root.bind("<Configure>", update_status_bar)

root.mainloop()
