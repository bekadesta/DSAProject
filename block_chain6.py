import hashlib
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_pool = []  # Transaction pool
        self.create_block(data="Genesis Block", previous_hash='-1')  # Genesis block with previous hash as -1

    def create_block(self, data, previous_hash=None):
        index = len(self.chain)  # Start index from 0
        timestamp = time.time()
        hash = self.hash_block(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(block)
        return block

    def hash_block(self, index, previous_hash, timestamp, data):
        value = f"{index}{previous_hash}{timestamp}{data}".encode()
        return hashlib.sha256(value).hexdigest()

    def display_chain(self):
        # Create a formatted string for the blockchain
        blockchain_str = f"{'Index':<6} | {'Previous Hash':<66} | {'Timestamp':<25} | {'Data':<40} | {'Hash'}\n"
        blockchain_str += "-" * 200 + "\n"

        for block in self.chain:
            blockchain_str += f"{block.index:<6} | {block.previous_hash:<66} | {block.timestamp:<25} | {block.data:<40} | {block.hash}\n"

        return blockchain_str

    def add_transaction(self, data):
        self.transaction_pool.append(data)  # Add transaction to the pool

    def display_transaction_pool(self):
        return "\n".join(self.transaction_pool) if self.transaction_pool else "No transactions in the pool."

class BlockchainApp:
    def __init__(self, root):
        self.blockchain = Blockchain()
        self.root = root
        self.root.title("Simple Blockchain with Transaction Pool")
        self.root.geometry("1100x700")  # Set window size
        self.root.configure(bg="#f0f0f0")  # Set background color

        # Title Label with different colors for each word
        title_frame = tk.Frame(root, bg="#f0f0f0")
        title_frame.pack(pady=20)

        self.title_label1 = tk.Label(title_frame, text="Simple", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.title_label1.pack(side=tk.LEFT)

        self.title_label2 = tk.Label(title_frame, text="Blockchain", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#FF9800")
        self.title_label2.pack(side=tk.LEFT)

        self.title_label3 = tk.Label(title_frame, text="Application", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#2196F3")
        self.title_label3.pack(side=tk.LEFT)

        # Create a frame for input
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        self.label = tk.Label(self.input_frame, text="Enter transaction data:", bg="#f0f0f0")
        self.label.pack(side=tk.LEFT, padx=5)

        self.data_entry = tk.Entry(self.input_frame, width=60)  # Increased width
        self.data_entry.pack(side=tk.LEFT, padx=5)

        self.add_transaction_button = tk.Button(self.input_frame, text="Add Transaction", command=self.add_transaction, bg="#4CAF50",
                                                 fg="white")
        self.add_transaction_button.pack(side=tk.LEFT, padx=5)

        self.add_block_button = tk.Button(root, text="Add Block", command=self.add_block, bg="#FF9800", fg="white")
        self.add_block_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View Blockchain", command=self.view_blockchain, bg="#2196F3",
                                     fg="white")
        self.view_button.pack(pady=10)

        # Output area for blockchain
        self.output_area = scrolledtext.ScrolledText(root, width=120, height=15, font=("Courier New", 10))
        self.output_area.pack(pady=10)

        # Output area for transaction pool
        self.transaction_area = scrolledtext.ScrolledText(root, width=120, height=10, font=("Courier New", 10))
        self.transaction_area.pack(pady=10)

        # Bind the Enter key to the add_transaction method
        self.data_entry.bind("<Return>", self.add_transaction_with_enter)

    def add_transaction(self):
        data = self.data_entry.get()
        if data:
            self.blockchain.add_transaction(data)  # Add transaction to the pool
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.data_entry.delete(0, tk.END)  # Clear the entry field
            self.update_transaction_area()  # Update the transaction pool display
        else:
            messagebox.showwarning("Input Error", "Please enter some data.")

    def add_transaction_with_enter(self, event):
        self.add_transaction()  # Call the add_transaction method when Enter is pressed

    def add_block(self):
        if not self.blockchain.transaction_pool:
            messagebox.showwarning("Input Error", "No transactions in the pool to add a block.")
            return

        previous_hash = self.blockchain.chain[-1].hash if self.blockchain.chain else '-1'
        data = ', '.join(self.blockchain.transaction_pool)  # Combine all transactions into one block
        self.blockchain.create_block(data, previous_hash)
        messagebox.showinfo("Success", "Block added successfully!")
        self.blockchain.transaction_pool.clear()  # Clear the transaction pool after adding the block
        self.update_transaction_area()  # Update the transaction pool display

    def view_blockchain(self):
        blockchain_str = self.blockchain.display_chain()
        self.output_area.delete(1.0, tk.END)  # Clear the output area
        self.output_area.insert(tk.END, blockchain_str)  # Display the blockchain

    def update_transaction_area(self):
        self.transaction_area.delete(1.0, tk.END)  # Clear the transaction area
        transactions_str = "Current Transactions in Pool:\n" + self.blockchain.display_transaction_pool()
        self.transaction_area.insert(tk.END, transactions_str)  # Display current transactions

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()