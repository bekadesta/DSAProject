import tkinter as tk
import time
from tkinter import messagebox
from tkinter import font

window = tk.Tk()
window.title("Sorting Algorithm Visualizer")
window.geometry("1000x800")
window.configure(bg="#E0F7FA")

data = []

canvas = tk.Canvas(window, width=800, height=500, bg="#B2EBF2", highlightthickness=0)
canvas.pack(pady=20)

times_new_roman = font.Font(family="Times New Roman", size=12)
def draw_data(highlight_indices=None):
    canvas.delete("all")
    bar_width = 25
    spacing = 2
    total_width = len(data) * (bar_width + spacing)
    start_x = (800 - total_width) / 2

    for i, val in enumerate(data):
        x1 = start_x + i * (bar_width + spacing)
        y1 = 400 - val * 3
        x2 = x1 + bar_width
        y2 = 400
        color = "#FF5252" if highlight_indices and i in highlight_indices else "#00796B"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        canvas.create_text((x1 + x2) / 2, y2 + 15, text=str(val), fill="#004D40", font=times_new_roman)
    window.update()

def insertion_sort():
    global data
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            draw_data(highlight_indices=[j + 1])
            time.sleep(0.5)
        data[j + 1] = key
        draw_data(highlight_indices=[j + 1])
        time.sleep(0.05)
    draw_data()

def bubble_sort():
    global data
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_data(highlight_indices=[j, j + 1])
                time.sleep(0.5)
    draw_data()

def selection_sort():
    global data
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        draw_data(highlight_indices=[i, min_index])
        time.sleep(0.5)
    draw_data()


def heapify(n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[left] > data[largest]:
        largest = left

    if right < n and data[right] > data[largest]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        draw_data(highlight_indices=[i, largest])
        time.sleep(0.5)
        heapify(n, largest)


def heap_sort():
    global data
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_data(highlight_indices=[i, 0])
        time.sleep(0.5)
        heapify(i, 0)

    draw_data()


def process_input_data():
    global data
    input_data = entry_data.get()
    try:
        data = [int(x.strip()) for x in input_data.split(',')]
        if len(data) == 0:
            raise ValueError
        draw_data()
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid input! Please enter numbers separated by commas.")


def clear_data():
    global data
    data = []
    entry_data.delete(0, tk.END)
    error_label.config(text="")
    canvas.delete("all")


frame = tk.Frame(window, bg="#E0F7FA")
frame.pack(pady=10)

entry_label = tk.Label(frame, text="Enter numbers separated by commas:", bg="#E0F7FA", font=times_new_roman)
entry_label.grid(row=0, column=0, padx=10, pady=10)

entry_data = tk.Entry(frame, width=40, font=times_new_roman, bg="#FFFFFF", fg="#004D40", relief="flat")
entry_data.grid(row=0, column=1, padx=10, pady=10)

process_button = tk.Button(frame, text="Submit Input", command=process_input_data, bg="#00796B", fg="#FFFFFF",
                           font=times_new_roman, relief="flat")
process_button.grid(row=0, column=2, padx=10, pady=10)

button_frame = tk.Frame(window, bg="#E0F7FA")
button_frame.pack(pady=10)

bubble_button = tk.Button(button_frame, text="Bubble Sort", command=bubble_sort, bg="#00796B", fg="#FFFFFF",
                          font=times_new_roman, relief="flat")
bubble_button.grid(row=0, column=0, padx=5, pady=5)

selection_button = tk.Button(button_frame, text="Selection Sort", command=selection_sort, bg="#00796B", fg="#FFFFFF",
                             font=times_new_roman, relief="flat")
selection_button.grid(row=0, column=1, padx=5, pady=5)

heap_button = tk.Button(button_frame, text="Heap Sort", command=heap_sort, bg="#00796B", fg="#FFFFFF",
                        font=times_new_roman, relief="flat")
heap_button.grid(row=0, column=2, padx=5, pady=5)

insertion_button = tk.Button(button_frame, text="Insertion Sort", command=insertion_sort, bg="#00796B", fg="#FFFFFF",
                             font=times_new_roman, relief="flat")
insertion_button.grid(row=0, column=3, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data, bg="#FF5252", fg="#FFFFFF",
                         font=times_new_roman, relief="flat")
clear_button.grid(row=0, column=4, padx=5, pady=5)

error_label = tk.Label(window, text="", fg="#FF5252", bg="#E0F7FA", font=times_new_roman)
error_label.pack()

window.mainloop()
