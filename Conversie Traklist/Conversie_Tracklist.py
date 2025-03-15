import re
import tkinter as tk

# Fereastra principală
root = tk.Tk()
root.title("Conversie Tracklist © Hodis Florin")
root.geometry("1200x700")
root.configure(bg="black")  # Fundal negru

# Două frame-uri pentru a împărți fereastra în două
frame_left = tk.Frame(root, bg="black", highlightbackground="#FFD700", highlightthickness=5)
frame_left.place(relx=0.05, rely=0.01, relwidth=0.4, relheight=0.9)

frame_right = tk.Frame(root, bg="black", highlightbackground="#FFD700", highlightthickness=5)
frame_right.place(relx=0.55, rely=0.01, relwidth=0.4, relheight=0.9)

# Zona de intrare text (Text n)
text_input = tk.Text(frame_left, wrap="word", font=("Arial", 12), bg="#A9A9A9", fg="black", selectbackground="black", insertbackground="black")
text_input.pack(expand=True, fill="both", padx=5, pady=5)

# Zona de ieșire text (Text p)
text_output = tk.Text(frame_right, wrap="word", font=("Arial", 12), bg="#A9A9A9", fg="black", selectbackground="black", insertbackground="black")
text_output.pack(expand=True, fill="both", padx=5, pady=5)

# Frame pentru buton (mijloc)
frame_middle = tk.Frame(root, bg="black")
frame_middle.place(relx=0.45, rely=0.45, relwidth=0.1, relheight=0.1)

# Funcția care procesează textul
def process_text():
    input_text = text_input.get("1.0", tk.END).strip()
    processed_value = transform_text(input_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, processed_value)

# Funcția de conversie a textului
def transform_text(input_text):
    output_lines = []
    lines = input_text.split("\n")
    current_track = ""
    featuring_part = ""

    for line in lines:
        line = line.strip()
        
        if re.match(r"^[A-H]\d{1,2}\s", line):
            if current_track:
                if featuring_part:  
                    featuring_artists = re.sub(r"\s*\(\d+\)", "", featuring_part).split(",")
                    featuring_artists = [artist.strip() for artist in featuring_artists]

                    if len(featuring_artists) == 2:
                        formatted_artists = f"{featuring_artists[0]} & {featuring_artists[1]}"
                    elif len(featuring_artists) > 2:
                        formatted_artists = ", ".join(featuring_artists[:-1]) + f" & {featuring_artists[-1]}"
                    else:
                        formatted_artists = featuring_artists[0]

                    current_track = f"{current_track.strip()} (Feat. {formatted_artists})"
                
                current_track = re.sub(r"\s\d{1,2}:\d{2}$", "", current_track)
                output_lines.append(current_track.strip())
            
            current_track = line
            featuring_part = ""

        elif re.search(r"\b[Ff]eaturing\s*[-–]*", line):
            featuring_part = re.split(r"\b[Ff]eaturing\s*[-–]*", line, maxsplit=1)[-1].strip()

        elif re.match(r".*\d{1,2}:\d{2}$", line):
            continue

        else:
            continue

    if current_track:
        if featuring_part:
            featuring_artists = re.sub(r"\s*\(\d+\)", "", featuring_part).split(",")
            featuring_artists = [artist.strip() for artist in featuring_artists]

            if len(featuring_artists) == 2:
                formatted_artists = f"{featuring_artists[0]} & {featuring_artists[1]}"
            elif len(featuring_artists) > 2:
                formatted_artists = ", ".join(featuring_artists[:-1]) + f" & {featuring_artists[-1]}"
            else:
                formatted_artists = featuring_artists[0]

            current_track = f"{current_track.strip()} (Feat. {formatted_artists})"
        
        current_track = re.sub(r"\s\d{1,2}:\d{2}$", "", current_track)
        output_lines.append(current_track.strip())

    return "\n".join(output_lines)

# Buton pentru procesare
button_process = tk.Button(frame_middle, text="Procesează \n >>>", font=("Arial", 12, "bold"), bg="#FFD700", fg="black", command=process_text, borderwidth=3, relief="raised")
button_process.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

root.mainloop()
