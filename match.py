import customtkinter as ctk
from PIL import Image, ImageTk

# File handling functions
def startXY(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    print(f"Start: ({start_x}, {start_y})")

def endXY(event):
    end_x, end_y = event.x, event.y
    print(f"End: ({end_x}, {end_y})")

def update_event_display():
    # Ensure that selected player, event, and team are all set before updating
    if selected_player and selected_event and selected_team:
        event_label.configure(text=f"{selected_team}, {selected_player}, {selected_event}")

def key_press(event):
    global key_bindings_paused  # Add this line to access the global variable
    if key_bindings_paused:
        return
    
    main_events = ["Perte de Ball", "Passe Precise", "Passe Perdue", "Longue Passe Precise", "Interception", "Dribble",
                    "Longue Passe Perdue", "Passe en Profondeur", "Tir Cadre", "Tir non Cadre"]
    key_event = event.char
    if key_event.isdigit():
        index = int(key_event)
        if 0 <= index < len(main_events):  # Ensure the index is within range
            selected_event = main_events[index]
            insertion_event(selected_event)

def insertion_player(team, player):
    global selected_player, selected_team
    selected_player = player
    selected_team = team
    
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{team},{player},")
    
    update_event_display()

def insertion_event(event):
    global selected_event
    selected_event = event
    
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{event}\n")
    
    update_event_display()

def subs_player(team, player_out_entry, player_in_entry):
    player_out = player_out_entry.get()
    player_in = player_in_entry.get()

    if team == "H":
        with open('match\\home_players.txt', 'r') as file:
            data = file.read()
        data = data.replace(player_out, player_in)

        with open('match\\home_players.txt', 'w') as file:
            file.write(data)

        # Update home players list
        global home_players
        home_players = read_players('match\\home_players.txt')

    else:
        with open('match\\away_players.txt', 'r') as file:
            data = file.read()
        data = data.replace(player_out, player_in)

        with open('match\\away_players.txt', 'w') as file:
            file.write(data)

        # Update away players list
        global away_players
        away_players = read_players('match\\away_players.txt')

    fenetre.bind("<Control_L>", resume_key_bindings)
    # Refresh ALL after substitution
    player_in = ctk.CTkEntry(fenetre, placeholder_text='IN')
    player_in.place(x=350, y=590)
    player_out = ctk.CTkEntry(fenetre, placeholder_text='OUT')
    player_out.place(x=350, y=550)
    players_lists()

# Function to read player lists
def read_players(file_name):
    with open(file_name, 'r') as file:
        players = [line.strip() for line in file.readlines()]
    return players

# Function to read events
def read_events(file_name):
    with open(file_name, "r") as file_events:
        events = [line.strip() for line in file_events.readlines()]
    return events

# Function to read teams
def read_team(file):
    with open(file, "r") as file:
        home_team = file.readline().strip()
        away_team = file.readline().strip()
    return home_team, away_team

def players_lists():
    global home_players, away_players

    # Clear existing player buttons for Home and Away teams
    for widget in fenetre.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget not in [home_subs, away_subs]:
            widget.destroy()

    # Create Home Team players' list
    y_position = 50
    for player in home_players:
        player_selection = ctk.CTkButton(fenetre, text=player, command=lambda p=player: insertion_player(home_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#557C56")
        player_selection.place(x=30, y=y_position)
        y_position += 50

    # Create Away Team players' list
    y_position = 50
    for player in away_players:
        player_selection = ctk.CTkButton(fenetre, text=player, command=lambda p=player: insertion_player(away_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#C96868")
        player_selection.place(x=700, y=y_position)
        y_position += 50

# Functions to pause and resume key bindings

def resume_key_bindings(event=None):  # Accept the event argument
    global key_bindings_paused
    key_bindings_paused = False
    subs_situation.configure(text="Les évenements: ON", text_color="#117554")
    fenetre.focus_set()

def disable_key_bindings(event=None):  # Accept event argument to be consistent
    global key_bindings_paused
    key_bindings_paused = True
    subs_situation.configure(text="Les évenements: OFF", text_color="#C7253E")


def enable_key_bindings(event=None):  # Accept event argument
    global key_bindings_paused
    key_bindings_paused = False
    fenetre.bind("<Key>", key_press)


# Main application creation function
def create_app():
    global fenetre, home_players, away_players, home_subs, away_subs, event_label, home_team, away_team
    global selected_event, selected_player, selected_team, events, subs_situation, player_in, player_out,key_bindings_paused

    selected_event = None
    selected_player = None
    selected_team = None
    key_bindings_paused = False

    # GUI
    fenetre = ctk.CTk()
    fenetre.title("HeroScore - Analyse du Match")
    fenetre.iconbitmap("logo_ico.ico")
    width = fenetre.winfo_screenwidth()
    height = fenetre.winfo_screenheight()
    fenetre.geometry(f"{width}x{height}+0+0")
    fenetre.bind("<Key>", key_press)
    
    # Get all players and teams
    home_players = read_players('match\\home_players.txt')
    away_players = read_players('match\\away_players.txt')
    home_team, away_team = read_team('match\\team_names.txt')

    # Create the pitch
    pitch_frame = ctk.CTkFrame(fenetre, width=630, height=430, corner_radius=10)
    pitch_frame.place(x=860, y=50)
    image = Image.open('football pitch.jpg')
    photo = ImageTk.PhotoImage(image)
    pitch_label = ctk.CTkLabel(pitch_frame, text="", image=photo)
    pitch_label.place(relx=0.5, rely=0.5, anchor="center")

    # The Mouse functions
    pitch_label.bind("<ButtonPress-1>", startXY)
    pitch_label.bind("<ButtonRelease-1>", endXY)

    # Create a frame for events
    events_frame = ctk.CTkFrame(fenetre, width=150, height=300, corner_radius=10)
    events_frame.place(x=180, y=50)
    events = read_events('régles\\events.txt')

    # Display event buttons
    for row in range(10):
        for col in range(3):
            index = row * 3 + col
            if index < len(events):
                event_text = events[index]
                button = ctk.CTkButton(events_frame, text=event_text, command=lambda event=event_text: insertion_event(event[3:]),
                                       fg_color="#D8A25E", text_color="black", hover_color="#B99470")
                button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

    # Substitution function
    player_in = ctk.CTkEntry(fenetre, placeholder_text='IN')
    player_in.place(x=350, y=590)
    player_in.bind("<FocusIn>", disable_key_bindings)
    player_in.bind("<FocusOut>", enable_key_bindings)
    
    player_out = ctk.CTkEntry(fenetre, placeholder_text='OUT')
    player_out.place(x=350, y=550)
    player_out.bind("<FocusIn>", disable_key_bindings)
    player_out.bind("<FocusOut>", enable_key_bindings)
    
    home_subs = ctk.CTkButton(fenetre, text=home_team, command=lambda: subs_player('H', player_out, player_in),
                              fg_color="#41B3A2", text_color="black", hover_color="#16423C", width=80, height=30)
    home_subs.place(x=320, y=630)
    away_subs = ctk.CTkButton(fenetre, text=away_team, command=lambda: subs_player('A', player_out, player_in),
                              fg_color="#C7253E", text_color="black", hover_color="#821131", width=80, height=30)
    away_subs.place(x=420, y=630)

    # Event display label at the top right
    event_label = ctk.CTkLabel(fenetre, text="", font=("Arial", 14))
    event_label.place(x=width - 450, y=480)

    subs_situation = ctk.CTkLabel(fenetre, text="situation", font=("Arial", 14))
    subs_situation.place(x=185, y=20)
    subs_situation.configure(text="Les évenements: ON", text_color="#117554")

    # To have a new list of players after subs
    players_lists()

    fenetre.mainloop()

# MAIN
create_app()