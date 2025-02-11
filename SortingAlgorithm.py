import tkinter as tk
import time
from tkinter import messagebox

# Create a window using Tkinter
window = tk.Tk()
window.title("Sorting Algorithm Visualizer")
window.geometry("1000x1000")

# List to store the data
data = []

# Canvas to draw bars
canvas = tk.Canvas(window, width=800, height=500, bg="#A0A0A0")
canvas.pack()


# Draw the bars based on the current data
def draw_data(highlight_indices=None):
    canvas.delete("all")  # Clear canvas
    bar_width = 15
    for i, val in enumerate(data):
        x1 = i * (bar_width + 2)  # X coordinate for each bar
        y1 = 500 - val  # Y coordinate for each bar (flip for correct visual representation)
        x2 = x1 + bar_width
        y2 = 500
        color = "red" if highlight_indices and i in highlight_indices else "black"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    window.update()


# Insertion Sort Algorithm
def insertion_sort():
    global data
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]  # Shift element
            j -= 1
            draw_data(highlight_indices=[j + 1])
            time.sleep(1.0)
        data[j + 1] = key  # Insert key at correct position
        draw_data(highlight_indices=[j + 1])
        time.sleep(0.05)
    draw_data()


# Bubble Sort Algorithm
def bubble_sort():
    global data
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]  # Swap
                draw_data(highlight_indices=[j, j + 1])  # Update the visualization
                time.sleep(1.0)  # Pause for animation effect
    draw_data()  # Final draw after sorting


# Selection Sort Algorithm
def selection_sort():
    global data
    n = len(data)
    for i in range(n):
        min_index = i  # Assume the current element is the minimum
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                min_index = j  # Update the index of the minimum value
        # Swap the found minimum element with the first element
        data[i], data[min_index] = data[min_index], data[i]
        draw_data(highlight_indices=[i, min_index])  # Update the visualization
        time.sleep(1.0)  # Pause for animation effect
    draw_data()  # Final draw after sorting


# Heap Sort Algorithm
def heapify(n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child index
    right = 2 * i + 2  # Right child index

    if left < n and data[left] > data[largest]:
        largest = left

    if right < n and data[right] > data[largest]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]  # Swap
        draw_data(highlight_indices=[i, largest])  # Update the visualization
        time.sleep(1.0)  # Pause for animation effect
        heapify(n, largest)


def heap_sort():
    global data
    n = len(data)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]  # Swap the root (largest element) with the last element
        draw_data(highlight_indices=[i, 0])  # Update the visualization
        time.sleep(1.0)  # Pause for animation effect
        heapify(i, 0)  # Heapify the root

    draw_data()  # Final draw after sorting


# Function to process user input data
def process_input_data():
    global data
    input_data = entry_data.get()  # Get input from the entry widget
    try:
        # Convert the input string to a list of integers
        data = [int(x.strip()) for x in input_data.split(',')]

        print(data)
        if len(data) == 0:
            raise ValueError
        draw_data()  # Draw the data after input
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid input! Please enter numbers separated by commas.")


def clear_data():
    global data
    data = []  # Reset the data
    entry_data.delete(0, tk.END)  # Clear the input field
    error_label.config(text="")  # Clear the error message
    canvas.delete("all")  # Clear the canvas


# Setup GUI controls
frame = tk.Frame(window)
frame.pack()

# Input field and button for user data
entry_label = tk.Label(window, text="Enter numbers separated by commas or spaces:")
entry_label.pack(pady=10)

entry_data = tk.Entry(window, width=40)
entry_data.pack(pady=10)

process_button = tk.Button(window, text="Submit Input", command=process_input_data)
process_button.pack(pady=10)

# Create a frame to hold the sorting and clear buttons side by side
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Buttons for sorting algorithms and clear button inside button_frame
bubble_button = tk.Button(button_frame, text="Bubble Sort", command=bubble_sort)
bubble_button.grid(row=0, column=0, padx=5)

selection_button = tk.Button(button_frame, text="Selection Sort", command=selection_sort)
selection_button.grid(row=0, column=1, padx=5)

heap_button = tk.Button(button_frame, text="Heap Sort", command=heap_sort)
heap_button.grid(row=0, column=2, padx=5)

insertion_button = tk.Button(button_frame, text="Insertion Sort", command=insertion_sort)
insertion_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.grid(row=0, column=4, padx=5)

# Error label to display invalid input message
error_label = tk.Label(window, text="", fg="black")
error_label.pack()

# Run the application
window.mainloop()
