from customtkinter import *               # A modern and customizable python UI-library based on Tkinter
from PIL import Image                     # for image 
from tkinter import messagebox            # to guide user's input (showing errors)
import matplotlib.pyplot as plt           # for graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg    # to place the graphs in to the tk window

def change_mode():
    # changing the appearance_mode takes some time, so we added a loading effect
    loading_label = CTkLabel(window, text="Changing Mode...", font=("Arial", 10, "italic"))
    loading_label.place(relx=0.5, rely=0.5, anchor="center")
    
    if switch.get() == "on":
        window.after(1000, lambda: set_appearance_mode("dark"))
    else:
        window.after(1000, lambda: set_appearance_mode("light"))
    
    window.after(1000, loading_label.destroy)

def Entry_Slot():
    frame_slot = CTkFrame(frame2)  # An Inner frame that will hold the three widgets (Image, Entry_name, Entry_vote)
    frame_slot.pack()

    person_image = CTkImage(light_image=Image.open("person_logo_dark.png"), dark_image=Image.open("person_logo_light.png"),size=(30,30))
    person_logo = CTkLabel(frame_slot, image=person_image, text="")
    person_logo.pack(side="left")
    
    entry_name = CTkEntry(frame_slot, placeholder_text="Name", font=("Arial", 10, "italic"))
    entry_name.pack(side="left", pady=5, padx=10)
    entry_name_list.append(entry_name)      # Putting the memory address in a list 

    
    entry_vote = CTkEntry(frame_slot, placeholder_text="Votes", font=("Arial", 10, "italic"))
    entry_vote.pack(side="right", pady=5, padx=25)
    entry_vote_list.append(entry_vote)      # Putting the memory address in a list 
    
    return frame_slot   # returns the value of the frame_slot, so the three widgets could be easily removed by just removing their frame

def remove_entry():
    last_entry_frame = entry_frames.pop()      # remove the frame from the list
    last_entry_frame.pack_forget()             # removing it visually 
    
    entry_name_list.pop()                      # removing the last added memory address from the collected names in the entry_name_list
    entry_vote_list.pop()                      # removing the last added memory address from the collected votes in the entry_vote_list

def Clear_Entry():
    
    
    for entry_name in entry_name_list:
        entry_name.delete(0, "end")  # Clear the content of each entry_name
        entry_name.configure(placeholder_text="Name")


    for entry_vote in entry_vote_list:
        entry_vote.delete(0, "end")  # Clear the content of each entry_vote
        entry_vote.configure(placeholder_text="Vote")
        
    position.focus_set() # setting the cursor back to the ComboBox
    
    position.set("")  # Clear the selection in the ComboBox

def Extract_Data():
    global ranked_name_values, ranked_vote_values, ranking_list
    # Extracting the data from the Entry (user's input) into a new list
    name_values = [entry_name.get() for entry_name in entry_name_list]    # we do this because what on the entry_name and entry_vote is all memory address   
    vote_values = [entry_vote.get() for entry_vote in entry_vote_list]

######################################################################################################################################
    # Detecting errors for the user's input
    error_entry = False
    error_vote = False
    error_name = False
    
    if len(name_values) == 0:
        error_entry = True
        
    if "" in (name_values + vote_values):
        error_entry = True
    
    for vote in vote_values:
        if vote.isdigit():
            pass
        else:
            error_vote = True 
            break
        
    for name in name_values:
        if name.isalpha():
            pass
        else:                  
            error_name = True
            
    if error_entry:
        messagebox.showerror(title="Value Error", message="Please fill in all fields")
    elif error_vote:
        messagebox.showerror(title="Value Error", message="Votes must be only positive numbers")
    elif error_name:
        messagebox.showerror(title="Value Error", message="Names must not contain numbers or any special character")

######################################################################################################################################
    else:           # if there's no error inputs (which is what we want)
        
        # This is the part where the extraction of data comes

        ranked_vote_values = []      # sorted vote_values from highest to lowest
        
        for i in vote_values:
            ranked_vote_values.append(int(i))
        ranked_vote_values = sorted(ranked_vote_values, reverse=True)
        
        ranked_name_values = []      # sorted name_values from highest to lowest votes that they have
        
        for vote in ranked_vote_values:
            ranked_name_values.append(name_values[vote_values.index(str(vote))])       # the index of vote_values corresponds to the index of name_values
            name_values.remove(name_values[vote_values.index(str(vote))]) # removing the data from the name_values to avoid an error that occurs when there is a tie
            vote_values.remove(str(vote))                 # removing the data from the vote_values to avoid an error that occurs when there is a tie
            
        ranking_list = []           # added this to manipulate the presented ranking if there is a tie
        
        recent_vote = 'this is just to iniatiate the recent_vote'  
        rank_count = 1
        for num in ranked_vote_values:
            if num == recent_vote:
                ranking_list.append(ranking_list[-1])
            else:
                ranking_list.append(rank_count)
            recent_vote = num
            rank_count += 1

########################################################################################################################################    
                        
        if radbtn_choice.get() == "Here":            # if the user selected the For Here Button (radbtn_here)
            Result()
        elif radbtn_choice.get() == "File":          # if the player chose the For File Button (radbtn_file)
            Save_File()         
        else:                                        # if the user chose "For file & Here"
            Save_File()
            Result()

def Result():
                result = CTk()
                result.title("Result")
                result.geometry("840x400")
                
                # Frame 5 (Displaying the results in a tabular style using grid)
                frame5 = CTkScrollableFrame(result, width=340, height=350)
                frame5.pack(side="left", padx=10, pady=10, expand=True, fill="both")
                
                lbl_frame5_rank = CTkLabel(frame5, text="Rank", font=("courier", 12, "bold"))
                lbl_frame5_rank.grid(row=0, column=0, padx=10)
                lbl_frame5_name = CTkLabel(frame5, text="Name", font=("courier", 12, "bold"))
                lbl_frame5_name.grid(row=0, column=1, padx=10)
                lbl_frame5_vote = CTkLabel(frame5, text="Vote", font=("courier", 12, "bold"))
                lbl_frame5_vote.grid(row=0, column=2, padx=10)
                lbl_frame5_percent = CTkLabel(frame5, text="Percent", font=("courier", 12, "bold"))
                lbl_frame5_percent.grid(row=0, column=3, padx=10)
                frame5.grid_columnconfigure(0, weight=1)    
                
                iteration_count = 0
                row_count = 1
                for vote in ranked_vote_values:
                    lbl_frame5_rank_info = CTkLabel(frame5, text=ranking_list[iteration_count], font=("courier", 12, "bold"))
                    lbl_frame5_rank_info.grid(row=row_count, column=0, padx=10, pady=5)
                    frame5.grid_columnconfigure(row_count, weight=1)
                    lbl_frame5_name_info = CTkLabel(frame5, text=ranked_name_values[iteration_count], font=("courier", 12, "bold"))
                    lbl_frame5_name_info.grid(row=row_count, column=1, padx=10, pady=5)
                    frame5.grid_columnconfigure(row_count, weight=1)
                    lbl_frame5_vote_info = CTkLabel(frame5, text=vote, font=("courier", 12, "bold"))
                    lbl_frame5_vote_info.grid(row=row_count, column=2, padx=10, pady=5)
                    frame5.grid_columnconfigure(row_count, weight=1)
                    lbl_frame5_percent_info = CTkLabel(frame5, text=f"{(vote/sum(ranked_vote_values))*100:.2f}%", font=("courier", 12, "bold"))
                    lbl_frame5_percent_info.grid(row=row_count, column=3, padx=10, pady=5)
                    frame5.grid_columnconfigure(row_count, weight=1)
                    
                    row_count += 1
                    iteration_count += 1
    ######################################################################################################################################
                # charts
                def plot_pie_chart():
                    # creating the pie graph using the imported matplotlib
                    fig, ax = plt.subplots()
                    
                    # The pie Graph
                    ax.pie(ranked_vote_values, labels=ranked_name_values, autopct='%1.1f%%', startangle=90)  # autopct(percentage formatting) startangle (size for the pie chart)
                        # value                  # label
                    
                    ax.set_title(position.get()) # based on what is on the ComboBox
                    
                    return fig # returns the figure of the graph

                def plot_bar_graph():
                    # creating the bar graph using the imported matplotlib 
                    fig, ax = plt.subplots()
                    # The bar Graph
                    ax.bar(ranked_name_values, ranked_vote_values)
                        #(values for each bar, the height of each bar) --> list
                        
                    ax.set_xlabel('Candidates')
                    ax.set_ylabel('Votes')
                    ax.set_title(position.get()) # based on what is on the ComboBox

                    return fig # returns the figure of the graph

                def embed_matplotlib_figure(frame, fig):
                    # embed the Matplotlib figure into the Tkinter GUI, allowing us to display Matplotlib plots within the tab.
                    
                    canvas = FigureCanvasTkAgg(fig, master=frame)          # creates a Tkinter canvas that is specifically designed to embed Matplotlib figures.
                    canvas.draw()                                           #  triggers the drawing of the Matplotlib figure on the canvas.
                    canvas.get_tk_widget().pack(fill="both", expand=True)   #retrieves the Tkinter widget associated with the canvas
                    
    ######################################################################################################################################
                # Frame 6 (Displaying the results in a tabular style using charts)
                frame6 = CTkTabview(result, anchor="nw", width=400, height=370)
                frame6.pack(side="left", padx=10, pady=20, expand=True, fill="both")
                
                tab_pie = frame6.add("Pie Graph")   # tab1
                tab_bar = frame6.add("Bar Graph")   # tab2
                
                frame_pie = CTkFrame(tab_pie)               # Putting the frame into the tab_pie
                frame_pie.pack(expand=True, fill="both")

                frame_bar = CTkFrame(tab_bar)               # Putting the frame into the tab_bar
                frame_bar.pack(expand=True, fill="both")

                fig_pie = plot_pie_chart()                  # Getting the figures of the Graphs
                fig_bar = plot_bar_graph()
                
                # calling the function to put the graphs to the frames (which is on the tab_pie and tab_bar)
                embed_matplotlib_figure(frame_pie, fig_pie)   
                embed_matplotlib_figure(frame_bar, fig_bar)
    
                result.mainloop()

def Save_File():
                file_name1 = CTkInputDialog(text="Input the File Name", title="File")
                # loading effect
                
                with open(f"{file_name1.get_input()}.txt", "w") as file:
                    if position.get() == "":
                        file.write(f"Voting for the position of unknown\n\n")
                    else:
                        file.write(f"Voting for the position of {position.get()}\n\n")
                    
                    
                    ranked_vote_values_count1 = 0          # iteration count on ranked_vote_values
                    for name in ranked_name_values:
                        file.write(f"{name} got {ranked_vote_values[ranked_vote_values_count1]} votes ({ranked_vote_values[ranked_vote_values_count1]/sum(ranked_vote_values)*100:.2f}%) \n")
                        ranked_vote_values_count1 += 1
                
                loading_file = CTkLabel(window, text="  Saving...  ", font=("Arial", 10, "italic"))
                loading_file.place(relx=0.5, rely=0.5, anchor="center")
                window.after(1000, loading_file.destroy) 

                       
######################################################################################################################################
# Creating the Master Window
window = CTk()
window.title("PyVote")
window.geometry("400x540")       # 400x500
set_appearance_mode("light")     # default appearance_mode is "dark", so we have to initialize it as "light"
######################################################################################################################################
# Switch
switch = CTkSwitch(window, command=change_mode, onvalue="on", offvalue="off", text="Dark Mode")
switch.pack(anchor="e", padx=10, pady=5)

######################################################################################################################################
# Frame 1 (Getting the position using ComboBox which would provide both of the property of OptionMenu and Entry)
frame1 = CTkFrame(window, width=375, height=50) 
frame1.pack(pady=5, padx=10, fill="x")

lbl_frame1_position = CTkLabel(frame1, text="Position:")
lbl_frame1_position.pack(side="left", pady=10, padx=40, expand=True, fill="x")

position_choices = ["","President", "Vice-President", "Secretary", "Auditor", "P.I.O.", "Srgt & Arms", "Muse", "Escort"]
position = CTkComboBox(frame1, values=position_choices)
position.set(position_choices[0])  # setting the empty string from the position_choices to be the default on the ComboBox
position.pack(side="left", pady=10, padx=40, expand=True)

######################################################################################################################################
# Frame 2 (Getting the user's Entry of names and votes respectively also to add and remove Entry Slots)
frame2 = CTkScrollableFrame(window, width=350, height=250)
frame2.pack(pady=5, padx=10, expand=True, fill="both")

entry_frames = []       # List to store added entry frames
entry_name_list = []    # List to store the memory address that corresponds to the entry_name
entry_vote_list = []    # List to store the memory address that corresponds to the entry_vote

for i in range(5):                            # default counts of entry
    entry_frames.append(Entry_Slot())         # added the frames to the entry_frames
    

Iframe_frame2 = CTkFrame(frame2, width=350, height=50)  # Frame that holds the add and remove button
Iframe_frame2.pack(side="bottom")

btn_Iframe_addslot = CTkButton(Iframe_frame2, text="Add", command=lambda: entry_frames.append(Entry_Slot()))   # added the frames to the entry_frames
btn_Iframe_addslot.place(x=35, y=10)
btn_Iframe_remove = CTkButton(Iframe_frame2, text="Remove", command=remove_entry)
btn_Iframe_remove.place(x=200, y=10)

######################################################################################################################################
# Frame 3 (Choosing where to present the output)
frame3 = CTkFrame(window, width=187, height=120) # 375/2 = width (375=width of window)
frame3.pack(pady=(5,10), padx=(10,0), fill="x", side="left", expand=True)

radbtn_choice = StringVar(value="Here")
radbtn_here = CTkRadioButton(frame3, text="For Here", variable=radbtn_choice, value="Here")
radbtn_here.pack(anchor="w", pady=(15,0), padx=10)
radbtn_file = CTkRadioButton(frame3, text="For File", variable=radbtn_choice, value="File")
radbtn_file.pack(anchor="w", pady=(15,0), padx=10)
radbtn_both = CTkRadioButton(frame3, text="For Here & File", variable=radbtn_choice, value="Both")
radbtn_both.pack(anchor="w", pady=(15,0), padx=10)

######################################################################################################################################
# Frame 4 (Holds the Clear and Submit Button)
frame4 = CTkFrame(window, width=187, height=120)
frame4.pack(pady=(5,10), padx=10, fill="x", side="left", expand=True)

btn_frame4_clear = CTkButton(frame4, text="Clear Entry", command=Clear_Entry, height=45, width=177)
btn_frame4_clear.pack(anchor="e", pady=(10,0), padx=10)

btn_frame4_submit = CTkButton(frame4, text="Submit", command=Extract_Data, height=45, width=177)
btn_frame4_submit.pack(anchor="e", pady=(0,10), padx=10, side="bottom")

window.mainloop()
