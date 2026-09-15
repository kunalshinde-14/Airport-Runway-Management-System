import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from airport import Plane, Queue, HashTable, Stack


# ============================================================
# COLORS
# ============================================================

BG = "#EEF2F5"
NAVY = "#172B3A"
DARK = "#243746"
WHITE = "#FFFFFF"
BORDER = "#C7D0D8"
BLUE = "#2364AA"
BLUE_DARK = "#1B4F87"
GREEN = "#278A5B"
GREEN_DARK = "#1F704A"
AMBER = "#D98B22"
RED = "#C74634"
TEXT = "#263746"
MUTED = "#6B7C89"


# ============================================================
# DATA STRUCTURES
# ============================================================

flight_table = HashTable()

landing_queue = Queue()
takeoff_queue = Queue()

history_stack = Stack()


# ============================================================
# REGISTER FLIGHT
# ============================================================

def register_flight_gui():

    flight_no = flight_no_entry.get().strip()
    airline = airline_entry.get().strip()
    source = source_entry.get().strip()
    destination = destination_entry.get().strip()
    aircraft = aircraft_entry.get().strip()

    if not flight_no or not airline or not source or not destination or not aircraft:
        status_label.config(
            text="  Please fill in all flight details.",
            fg=RED
        )
        return

    if flight_table.search(flight_no):
        status_label.config(
            text=f"  Flight {flight_no} already exists.",
            fg=RED
        )
        return

    plane = Plane(
        flight_no,
        airline,
        source,
        destination,
        aircraft
    )

    flight_table.insert(plane)

    flight_no_entry.delete(0, tk.END)
    airline_entry.delete(0, tk.END)
    source_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)
    aircraft_entry.delete(0, tk.END)

    update_registered_flights()
    update_dashboard_counts()

    status_label.config(
        text=f"  Flight {flight_no} registered successfully.",
        fg=GREEN
    )


# ============================================================
# SEARCH FLIGHT
# ============================================================

def search_flight_gui():

    flight_no = search_entry.get().strip()

    if not flight_no:
        search_result.config(
            text="Enter a flight number.",
            fg=RED
        )
        return

    plane = flight_table.search(flight_no)

    if plane:

        search_result.config(
            text=(
                f"Flight: {plane.flight_no}\n"
                f"Airline: {plane.airline}\n"
                f"Route: {plane.source} → {plane.destination}\n"
                f"Aircraft: {plane.aircraft}\n"
                f"Status: {plane.status}"
            ),
            fg=TEXT
        )

        status_label.config(
            text=f"  Flight {flight_no} found.",
            fg=GREEN
        )

    else:

        search_result.config(
            text="Flight not found.",
            fg=RED
        )

        status_label.config(
            text=f"  Flight {flight_no} not found.",
            fg=RED
        )


# ============================================================
# ADD TO LANDING QUEUE
# ============================================================

def add_landing_gui():

    flight_no = landing_entry.get().strip()

    if not flight_no:
        status_label.config(
            text="  Enter a flight number.",
            fg=RED
        )
        return

    plane = flight_table.search(flight_no)

    if plane:

        if plane.status == "Registered":

            plane.status = "Waiting for Landing"

            landing_queue.enqueue(plane)

            landing_entry.delete(0, tk.END)

            update_landing_queue()
            update_registered_flights()
            update_dashboard_counts()

            status_label.config(
                text=f"  {flight_no} added to landing queue.",
                fg=GREEN
            )

        else:

            status_label.config(
                text=f"  Flight status is already: {plane.status}",
                fg=AMBER
            )

    else:

        status_label.config(
            text="  Flight not found.",
            fg=RED
        )


# ============================================================
# PROCESS LANDING
# ============================================================

def process_landing_gui():

    plane = landing_queue.dequeue()

    if plane:

        plane.status = "Landed"

        update_landing_queue()
        update_registered_flights()
        update_dashboard_counts()

        status_label.config(
            text=f"  Landing processed for {plane.flight_no}.",
            fg=GREEN
        )

    else:

        status_label.config(
            text="  Landing queue is empty.",
            fg=AMBER
        )


# ============================================================
# ADD TO TAKEOFF QUEUE
# ============================================================

def add_takeoff_gui():

    flight_no = takeoff_entry.get().strip()

    if not flight_no:
        status_label.config(
            text="  Enter a flight number.",
            fg=RED
        )
        return

    plane = flight_table.search(flight_no)

    if plane:

        if plane.status == "Landed":

            plane.status = "Waiting for Takeoff"

            takeoff_queue.enqueue(plane)

            takeoff_entry.delete(0, tk.END)

            update_takeoff_queue()
            update_registered_flights()
            update_dashboard_counts()

            status_label.config(
                text=f"  {flight_no} added to takeoff queue.",
                fg=GREEN
            )

        else:

            status_label.config(
                text=f"  Flight cannot be added for takeoff. Current status: {plane.status}",
                fg=AMBER
            )

    else:

        status_label.config(
            text="  Flight not found.",
            fg=RED
        )


# ============================================================
# PROCESS TAKEOFF
# ============================================================

def process_takeoff_gui():

    plane = takeoff_queue.dequeue()

    if plane:

        plane.status = "Departed"

        # Store completed flight in Stack
        history_stack.push(plane)

        # Remove departed flight from active Hash Table
        flight_table.delete(plane.flight_no)

        update_takeoff_queue()
        update_registered_flights()
        update_history()
        update_dashboard_counts()

        if search_entry.get().strip() == plane.flight_no:

            search_result.config(
                text="Flight has departed and is now in history.",
                fg=GREEN
            )

        status_label.config(
            text=f"  {plane.flight_no} departed successfully.",
            fg=GREEN
        )

    else:

        status_label.config(
            text="  Takeoff queue is empty.",
            fg=AMBER
        )


# ============================================================
# UPDATE LANDING QUEUE
# ============================================================

def update_landing_queue():

    landing_list.delete(0, tk.END)

    if len(landing_queue.items) == 0:

        landing_list.insert(
            tk.END,
            "  QUEUE EMPTY"
        )

    else:

        for position, plane in enumerate(
            landing_queue.items,
            start=1
        ):

            landing_list.insert(
                tk.END,
                f"  {position:02d}   {plane.flight_no}   |   {plane.airline}"
            )


# ============================================================
# UPDATE TAKEOFF QUEUE
# ============================================================

def update_takeoff_queue():

    takeoff_list.delete(0, tk.END)

    if len(takeoff_queue.items) == 0:

        takeoff_list.insert(
            tk.END,
            "  QUEUE EMPTY"
        )

    else:

        for position, plane in enumerate(
            takeoff_queue.items,
            start=1
        ):

            takeoff_list.insert(
                tk.END,
                f"  {position:02d}   {plane.flight_no}   |   {plane.airline}"
            )


# ============================================================
# UPDATE FLIGHT HISTORY
# ============================================================

def update_history():

    history_list.delete(0, tk.END)

    if len(history_stack.items) == 0:

        history_list.insert(
            tk.END,
            "  NO DEPARTED FLIGHTS"
        )

    else:

        for position, plane in enumerate(
            reversed(history_stack.items),
            start=1
        ):

            history_list.insert(
                tk.END,
                f"  {position:02d}   {plane.flight_no}   |   {plane.airline}"
            )


# ============================================================
# UPDATE ACTIVE FLIGHTS TABLE
# ============================================================

def update_registered_flights():

    for item in registered_table.get_children():
        registered_table.delete(item)

    for plane in flight_table.table:

        if plane is not None:

            if plane.status == "Registered":
                tag = "registered"

            elif plane.status in (
                "Waiting for Landing",
                "Waiting for Takeoff"
            ):
                tag = "waiting"

            elif plane.status == "Landed":
                tag = "landed"

            else:
                tag = ""

            registered_table.insert(
                "",
                tk.END,
                values=(
                    plane.flight_no,
                    plane.airline,
                    plane.source,
                    plane.destination,
                    plane.aircraft,
                    plane.status
                ),
                tags=(tag,)
            )


# ============================================================
# UPDATE DASHBOARD COUNTS
# ============================================================

def update_dashboard_counts():

    active_count = 0

    for plane in flight_table.table:

        if plane is not None:
            active_count += 1

    total_value.config(
        text=str(active_count)
    )

    landing_value.config(
        text=str(len(landing_queue.items))
    )

    takeoff_value.config(
        text=str(len(takeoff_queue.items))
    )


# ============================================================
# BUTTON HOVER
# ============================================================

def button_hover(button, normal_color, hover_color):

    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=normal_color
        )
    )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Airport Operations - Runway Management System")

root.geometry("1100x700")

root.resizable(True, True)

root.configure(
    bg=BG
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=NAVY,
    height=82
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title_frame = tk.Frame(
    header,
    bg=NAVY
)

title_frame.pack(
    side="left",
    padx=28,
    pady=13
)


title_label = tk.Label(
    title_frame,
    text="AIRPORT OPERATIONS",
    font=("Arial", 18, "bold"),
    bg=NAVY,
    fg=WHITE
)

title_label.pack(
    anchor="w"
)


subtitle_label = tk.Label(
    title_frame,
    text="RUNWAY MANAGEMENT SYSTEM",
    font=("Arial", 8, "bold"),
    bg=NAVY,
    fg="#AFC0CC"
)

subtitle_label.pack(
    anchor="w",
    pady=(2, 0)
)


online_frame = tk.Frame(
    header,
    bg=NAVY
)

online_frame.pack(
    side="right",
    padx=28
)


online_dot = tk.Label(
    online_frame,
    text="●",
    font=("Arial", 11),
    bg=NAVY,
    fg=GREEN
)

online_dot.pack(
    side="left"
)


online_label = tk.Label(
    online_frame,
    text=" SYSTEM ONLINE",
    font=("Arial", 9, "bold"),
    bg=NAVY,
    fg=WHITE
)

online_label.pack(
    side="left"
)


# ============================================================
# CONTENT AREA
# ============================================================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=22,
    pady=14
)


# ============================================================
# TOP LABEL
# ============================================================

control_label = tk.Label(
    content,
    text="RUNWAY CONTROL",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=MUTED
)

control_label.pack(
    anchor="w",
    pady=(0, 8)
)


# ============================================================
# STATISTICS
# ============================================================

stats_frame = tk.Frame(
    content,
    bg=BG
)

stats_frame.pack(
    fill="x",
    pady=(0, 10)
)


def create_stat_box(parent, title):

    frame = tk.Frame(
        parent,
        bg=WHITE,
        bd=1,
        relief="solid",
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 8)
    )

    label = tk.Label(
        frame,
        text=title,
        font=("Arial", 8, "bold"),
        bg=WHITE,
        fg=MUTED
    )

    label.pack(
        anchor="w",
        padx=12,
        pady=(8, 1)
    )

    value = tk.Label(
        frame,
        text="0",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=NAVY
    )

    value.pack(
        anchor="w",
        padx=12,
        pady=(0, 7)
    )

    return value


total_value = create_stat_box(
    stats_frame,
    "TOTAL ACTIVE FLIGHTS"
)

landing_value = create_stat_box(
    stats_frame,
    "WAITING FOR LANDING"
)

takeoff_value = create_stat_box(
    stats_frame,
    "WAITING FOR TAKEOFF"
)
# ============================================================
# OPERATION AREA
# ============================================================

operation_frame = tk.Frame(
    content,
    bg=BG
)

operation_frame.pack(
    fill="x",
    pady=(0, 10)
)


# ============================================================
# FLIGHT REGISTRATION PANEL
# ============================================================

registration_frame = tk.LabelFrame(
    operation_frame,
    text=" FLIGHT REGISTRATION ",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=1,
    relief="solid",
    padx=10,
    pady=8
)

registration_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


# -------------------------
# Flight Number
# -------------------------

tk.Label(
    registration_frame,
    text="Flight Number",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=5,
    pady=(0, 3)
)

flight_no_entry = tk.Entry(
    registration_frame,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

flight_no_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=5,
    pady=(0, 7)
)


# -------------------------
# Airline
# -------------------------

tk.Label(
    registration_frame,
    text="Airline",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=5,
    pady=(0, 3)
)

airline_entry = tk.Entry(
    registration_frame,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

airline_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=5,
    pady=(0, 7)
)


# -------------------------
# Source
# -------------------------

tk.Label(
    registration_frame,
    text="Source",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=5,
    pady=(0, 3)
)

source_entry = tk.Entry(
    registration_frame,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

source_entry.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=5,
    pady=(0, 7)
)


# -------------------------
# Destination
# -------------------------

tk.Label(
    registration_frame,
    text="Destination",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(
    row=2,
    column=1,
    sticky="w",
    padx=5,
    pady=(0, 3)
)

destination_entry = tk.Entry(
    registration_frame,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

destination_entry.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=5,
    pady=(0, 7)
)


# -------------------------
# Aircraft
# -------------------------

tk.Label(
    registration_frame,
    text="Aircraft",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(
    row=4,
    column=0,
    sticky="w",
    padx=5,
    pady=(0, 3)
)

aircraft_entry = tk.Entry(
    registration_frame,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

aircraft_entry.grid(
    row=5,
    column=0,
    sticky="ew",
    padx=5
)


# -------------------------
# Register Button
# -------------------------

register_button = tk.Button(
    registration_frame,
    text="REGISTER FLIGHT",
    command=register_flight_gui,
    font=("Arial", 9, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=10,
    pady=7,
    cursor="hand2"
)

register_button.grid(
    row=5,
    column=1,
    sticky="ew",
    padx=5
)

button_hover(
    register_button,
    BLUE,
    BLUE_DARK
)


registration_frame.columnconfigure(
    0,
    weight=1
)

registration_frame.columnconfigure(
    1,
    weight=1
)


# ============================================================
# FLIGHT LOOKUP PANEL
# ============================================================

lookup_frame = tk.LabelFrame(
    operation_frame,
    text=" FLIGHT LOOKUP ",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=1,
    relief="solid",
    padx=10,
    pady=8
)

lookup_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


tk.Label(
    lookup_frame,
    text="Flight Number",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=5
)


lookup_top = tk.Frame(
    lookup_frame,
    bg=WHITE
)

lookup_top.pack(
    fill="x",
    padx=5,
    pady=(3, 7)
)


search_entry = tk.Entry(
    lookup_top,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True
)


search_button = tk.Button(
    lookup_top,
    text="SEARCH",
    command=search_flight_gui,
    font=("Arial", 8, "bold"),
    bg=DARK,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=12,
    pady=5,
    cursor="hand2"
)

search_button.pack(
    side="left",
    padx=(6, 0)
)

button_hover(
    search_button,
    DARK,
    NAVY
)


search_result = tk.Label(
    lookup_frame,
    text="Enter a flight number to view details.",
    font=("Arial", 8),
    bg=WHITE,
    fg=MUTED,
    justify="left",
    anchor="w"
)

search_result.pack(
    fill="both",
    expand=True,
    padx=5
)


# ============================================================
# RUNWAY OPERATIONS
# ============================================================

queue_frame = tk.LabelFrame(
    operation_frame,
    text=" RUNWAY OPERATIONS ",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=1,
    relief="solid",
    padx=10,
    pady=8
)

queue_frame.pack(
    side="left",
    fill="y"
)


# ============================================================
# LANDING QUEUE
# ============================================================

landing_section = tk.Frame(
    queue_frame,
    bg=WHITE
)

landing_section.pack(
    side="left",
    padx=(0, 8)
)


tk.Label(
    landing_section,
    text="LANDING QUEUE",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(
    anchor="w"
)


landing_list = tk.Listbox(
    landing_section,
    width=24,
    height=4,
    font=("Courier New", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1,
    highlightthickness=0
)

landing_list.pack(
    pady=(4, 5)
)


landing_entry = tk.Entry(
    landing_section,
    width=24,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

landing_entry.pack(
    pady=(0, 5)
)


landing_add_button = tk.Button(
    landing_section,
    text="ADD TO QUEUE",
    command=add_landing_gui,
    font=("Arial", 8, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    cursor="hand2"
)

landing_add_button.pack(
    fill="x"
)

button_hover(
    landing_add_button,
    BLUE,
    BLUE_DARK
)


landing_process_button = tk.Button(
    landing_section,
    text="PROCESS LANDING",
    command=process_landing_gui,
    font=("Arial", 8, "bold"),
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    cursor="hand2"
)

landing_process_button.pack(
    fill="x",
    pady=(5, 0)
)

button_hover(
    landing_process_button,
    GREEN,
    GREEN_DARK
)


# ============================================================
# TAKEOFF QUEUE
# ============================================================

takeoff_section = tk.Frame(
    queue_frame,
    bg=WHITE
)

takeoff_section.pack(
    side="left"
)


tk.Label(
    takeoff_section,
    text="TAKEOFF QUEUE",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(
    anchor="w"
)


takeoff_list = tk.Listbox(
    takeoff_section,
    width=24,
    height=4,
    font=("Courier New", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1,
    highlightthickness=0
)

takeoff_list.pack(
    pady=(4, 5)
)


takeoff_entry = tk.Entry(
    takeoff_section,
    width=24,
    font=("Arial", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1
)

takeoff_entry.pack(
    pady=(0, 5)
)


takeoff_add_button = tk.Button(
    takeoff_section,
    text="ADD TO QUEUE",
    command=add_takeoff_gui,
    font=("Arial", 8, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    cursor="hand2"
)

takeoff_add_button.pack(
    fill="x"
)

button_hover(
    takeoff_add_button,
    BLUE,
    BLUE_DARK
)


takeoff_process_button = tk.Button(
    takeoff_section,
    text="PROCESS TAKEOFF",
    command=process_takeoff_gui,
    font=("Arial", 8, "bold"),
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    cursor="hand2"
)

takeoff_process_button.pack(
    fill="x",
    pady=(5, 0)
)

button_hover(
    takeoff_process_button,
    GREEN,
    GREEN_DARK
)


# ============================================================
# BOTTOM INFORMATION AREA
# ============================================================

bottom_area = tk.Frame(
    content,
    bg=BG
)

bottom_area.pack(
    fill="x",
    pady=(0, 3)
)


# ============================================================
# ACTIVE FLIGHTS
# ============================================================

registered_frame = tk.LabelFrame(
    bottom_area,
    text=" ACTIVE FLIGHTS ",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=1,
    relief="solid",
    padx=8,
    pady=6
)

registered_frame.pack(
    side="left",
    fill="both",
    expand=True
)


columns = (
    "flight",
    "airline",
    "source",
    "destination",
    "aircraft",
    "status"
)


registered_table = ttk.Treeview(
    registered_frame,
    columns=columns,
    show="headings",
    height=4
)

registered_table.heading("flight", text="FLIGHT NO.")
registered_table.heading("airline", text="AIRLINE")
registered_table.heading("source", text="FROM")
registered_table.heading("destination", text="TO")
registered_table.heading("aircraft", text="AIRCRAFT")
registered_table.heading("status", text="STATUS")

registered_table.column(
    "flight",
    width=85,
    anchor="center",
    stretch=False
)

registered_table.column(
    "airline",
    width=125,
    anchor="w",
    stretch=False
)

registered_table.column(
    "source",
    width=95,
    anchor="center",
    stretch=False
)

registered_table.column(
    "destination",
    width=105,
    anchor="center",
    stretch=False
)

registered_table.column(
    "aircraft",
    width=110,
    anchor="center",
    stretch=False
)

registered_table.column(
    "status",
    width=165,
    anchor="w",
    stretch=False
)

registered_table.tag_configure(
    "registered",
    foreground=BLUE
)

registered_table.tag_configure(
    "waiting",
    foreground=AMBER
)

registered_table.tag_configure(
    "landed",
    foreground=GREEN
)

registered_table.pack(
    fill="both",
    expand=True
)


# ============================================================
# FLIGHT HISTORY
# ============================================================

history_frame = tk.LabelFrame(
    bottom_area,
    text=" FLIGHT HISTORY ",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=1,
    relief="solid",
    padx=8,
    pady=6
)

history_frame.pack(
    side="right",
    fill="y",
    padx=(8, 0)
)


tk.Label(
    history_frame,
    text="MOST RECENT DEPARTURES",
    font=("Arial", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=3
)


history_list = tk.Listbox(
    history_frame,
    width=28,
    height=4,
    font=("Courier New", 9),
    bg="#F8FAFB",
    fg=TEXT,
    relief="solid",
    bd=1,
    highlightthickness=0
)

history_list.pack(
    pady=(5, 0)
)


# ============================================================
# FOOTER - DSA INFORMATION
# ============================================================

footer = tk.Label(
    content,
    text="QUEUE: FIFO   |   HASH TABLE: LINEAR PROBING   |   STACK: LIFO",
    font=("Arial", 8, "bold"),
    bg=BG,
    fg=MUTED
)

footer.pack(
    pady=(5, 2)
)


# ============================================================
# CURRENT SYSTEM STATUS
# ============================================================

bottom_frame = tk.Frame(
    content,
    bg=BG
)

bottom_frame.pack(
    fill="x"
)


status_indicator = tk.Label(
    bottom_frame,
    text="●",
    font=("Arial", 10),
    bg=BG,
    fg=GREEN
)

status_indicator.pack(
    side="left"
)


status_label = tk.Label(
    bottom_frame,
    text="  System Ready",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
)

status_label.pack(
    side="left"
)


# ============================================================
# INITIAL DISPLAY
# ============================================================

update_landing_queue()
update_takeoff_queue()
update_history()
update_registered_flights()
update_dashboard_counts()


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

flight_no_entry.focus()


root.bind(
    "<Return>",
    lambda event: register_flight_gui()
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()