import tkinter as tk
from tkinter import ttk, messagebox
from collections import OrderedDict
import winsound

class LRUCache:
    """LRU Cache implementation with O(1) operations using OrderedDict"""
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity must be non-negative")
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity and self.capacity > 0:
                self.cache.popitem(last=False)
        self.cache[key] = value

    def clear(self) -> None:
        self.cache.clear()
        self.hits = 0
        self.misses = 0

class CacheVisualizer(tk.Tk):
    """Modern Tkinter GUI for LRU Cache visualization"""
    def __init__(self):
        super().__init__()
        self.title("LRU Cache Visualizer")
        self.geometry("1200x800")
        self.configure(bg="#2d2d2d")
        self.cache = None
        self.dark_mode = True
        self.sound_enabled = True
        self._create_widgets()
        self._setup_styles()
        
    def _create_widgets(self):
        # Control Panel
        control_frame = ttk.Frame(self, padding=20)
        control_frame.pack(fill=tk.X)
        
        ttk.Label(control_frame, text="Capacity:").grid(row=0, column=0)
        self.capacity_entry = ttk.Entry(control_frame, width=10)
        self.capacity_entry.grid(row=0, column=1)
        
        ttk.Button(control_frame, text="Initialize Cache", 
                  command=self.initialize_cache).grid(row=0, column=2, padx=10)
        
        ttk.Label(control_frame, text="Key:").grid(row=1, column=0)
        self.key_entry = ttk.Entry(control_frame, width=10)
        self.key_entry.grid(row=1, column=1)
        
        ttk.Label(control_frame, text="Value:").grid(row=1, column=2)
        self.value_entry = ttk.Entry(control_frame, width=10)
        self.value_entry.grid(row=1, column=3)
        
        ttk.Button(control_frame, text="Put", command=self.put_item).grid(row=1, column=4, padx=5)
        ttk.Button(control_frame, text="Get", command=self.get_item).grid(row=1, column=5, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_cache).grid(row=1, column=6, padx=5)
        
        # Visualization Canvas
        self.canvas = tk.Canvas(self, bg="#1e1e1e", height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Statistics Panel
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill=tk.X, padx=20)
        
        self.stats_labels = {
            'hits': ttk.Label(stats_frame, text="Hits: 0"),
            'misses': ttk.Label(stats_frame, text="Misses: 0"),
            'size': ttk.Label(stats_frame, text="Current Size: 0"),
            'capacity': ttk.Label(stats_frame, text="Capacity: 0")
        }
        for i, label in enumerate(self.stats_labels.values()):
            label.grid(row=0, column=i, padx=10)
            
        # Theme Toggle
        self.theme_btn = ttk.Button(stats_frame, text="☀️", 
                                  command=self.toggle_theme, width=3)
        self.theme_btn.grid(row=0, column=4, padx=10)
        
        # Operation Log
        self.log = tk.Text(self, height=8, bg="#252526", fg="white")
        self.log.pack(fill=tk.X, padx=20, pady=10)
        
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TButton', background='#3c3c3c', foreground='white')
        style.map('TButton', background=[('active', '#4c4c4c')])
        
    def initialize_cache(self):
        try:
            capacity = self.capacity_entry.get()
            if not capacity:
                raise ValueError("Capacity cannot be empty")
            
            capacity = int(capacity)
            if capacity < 0:
                raise ValueError("Capacity must be non-negative")
                
            self.cache = LRUCache(capacity)
            self._update_stats()
            self._log_operation(f"Initialized cache with capacity {capacity}")
            self._visualize_cache()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def put_item(self):
        if not self._validate_inputs(need_value=True):
            return
            
        try:
            key = int(self.key_entry.get())
            value = self.value_entry.get()  # Keep as string
            
            # Optional: Convert to actual Python objects
            try:
                value = eval(value)  # Be careful with eval!
            except:
                pass  # Keep as string if conversion fails
                
            self.cache.put(key, value)
            self._log_operation(f"PUT ({key}, {value})")
            self._play_sound(1000)
            self._update_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def get_item(self):
        if not self._validate_inputs():
            return
            
        try:
            key = int(self.key_entry.get())
            value = self.cache.get(key)
            result = f"GET {key} → {'Found' if value != -1 else 'Not Found'}"
            self._log_operation(result)
            self._play_sound(500 if value == -1 else 800)
            self._update_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def clear_cache(self):
        if self.cache:
            self.cache.clear()
            self._log_operation("Cache cleared")
            self._update_display()
            
    def _validate_inputs(self, need_value=False):
        if not self.cache:
            messagebox.showwarning("Warning", "Initialize cache first")
            return False
            
        errors = []
        # Validate key
        key = self.key_entry.get()
        if not key:
            errors.append("Key cannot be empty")
        elif not key.isdigit():
            errors.append("Key must be an integer")
            
        # Validate value if needed
            if need_value:
                value = self.value_entry.get()
                if not value:
                    errors.append("Value cannot be empty")
                
        if errors:
            messagebox.showerror("Input Error", "\n".join(errors))
            return False
            
        return True
            
    def _update_display(self):
        self._update_stats()
        self._visualize_cache()
        
    def _update_stats(self):
        if self.cache:
            self.stats_labels['hits'].config(text=f"Hits: {self.cache.hits}")
            self.stats_labels['misses'].config(text=f"Misses: {self.cache.misses}")
            self.stats_labels['size'].config(text=f"Size: {len(self.cache.cache)}")
            self.stats_labels['capacity'].config(text=f"Capacity: {self.cache.capacity}")
            
    def _visualize_cache(self):
        self.canvas.delete("all")
        if not self.cache or self.cache.capacity == 0:
            return
            
        x = 150
        y = 250
        node_size = 60
        
        for i, (key, value) in enumerate(self.cache.cache.items()):
            color = "#4CAF50" if i == 0 else "#2196F3"
            self._draw_node(x, y, key, value, color)
            if i > 0:
                self._draw_arrow(x-node_size-20, y, x-node_size, y)
            x += node_size + 50
            
        self._draw_legend()
            
    def _draw_node(self, x, y, key, value, color):
        self.canvas.create_oval(x, y, x+60, y+60, fill=color, outline="white")
        self.canvas.create_text(x+30, y+30, text=f"{key}:{value}", 
                              fill="white", font=('Arial', 10, 'bold'))
        
    def _draw_arrow(self, x1, y1, x2, y2):
        self.canvas.create_line(x1+30, y1+30, x2, y2+30, 
                              arrow=tk.LAST, fill="white", width=2)
        
    def _draw_legend(self):
        self.canvas.create_text(100, 100, text="LRU", fill="white", 
                              font=('Arial', 12, 'bold'))
        self.canvas.create_text(1100, 100, text="MRU", fill="white", 
                              font=('Arial', 12, 'bold'))
        
    def _log_operation(self, message):
        self.log.insert(tk.END, f"[{self._timestamp()}] {message}\n")
        self.log.see(tk.END)
        
    def _timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#2d2d2d" if self.dark_mode else "#f0f0f0"
        fg = "white" if self.dark_mode else "black"
        self.configure(bg=bg)
        self.theme_btn.config(text="🌙" if self.dark_mode else "☀️")
        self.log.config(bg=bg, fg=fg)
        self._setup_styles()
        
    def _play_sound(self, freq):
        if self.sound_enabled:
            winsound.Beep(freq, 200)

if __name__ == "__main__":
    app = CacheVisualizer()
    app.mainloop()
