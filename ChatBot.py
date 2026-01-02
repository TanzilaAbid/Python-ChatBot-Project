import tkinter as tk
from tkinter import scrolledtext
import re
from datetime import datetime

class DatabaseBot:
    def __init__(self, root):
        self.root = root
        self.root.title("🗄️ Database Assistant")
        self.root.geometry("700x850")
        self.root.configure(bg="#1e1e1e")

        # --- AAPKA COMPLETE KNOWLEDGE BASE ---
        self.knowledge_base = {
            # GREETINGS
            "hello": {"response": "Hello! I can answer questions related to DBMS.", "category": "Greeting"},
            "hi|hey": {"response": "Hello! I am a DBMS Expert Chatbot. You can ask me about Database design or SQL.", "category": "Greeting"},
            "assalam o alaikum|salam|aoa": {"response": "Walaikum Assalam! I am your DBMS assistant. Please ask any question related to Databases.", "category": "Greeting"},

            # BASIC DBMS
            "dbms": {"response": "DBMS (Database Management System) is software that handles the storage, retrieval, and updating of data in a computer system.", "category": "Basics"},
            "rdbms": {"response": "Relational DBMS organizes data into tables. Examples: MySQL, Oracle, SQL Server.", "category": "Basics"},
            "acid": {"response": "ACID stands for Atomicity, Consistency, Isolation, and Durability. These ensure reliable transactions.", "category": "Transactions"},
            "data redundancy": {"response": "It means storing the same data multiple times, which wastes space. Normalization solves this.", "category": "Basics"},
            "data integrity": {"response": "It refers to the accuracy and consistency of data over its entire lifecycle.", "category": "Basics"},
            "cia|confidentiality|integrity|availability": {
                "response": "The CIA Triad is a model designed to guide policies for information security:\n1. Confidentiality: Authorized access only.\n2. Integrity: Accuracy and consistency.\n3. Availability: Ready for users.",
                "category": "Security"
            },

            # ERD
            "erd": {"response": "An ERD is a visual representation of entities and their relationships. It is the blueprint of a database.", "category": "Design"},
            "entity": {"response": "An Entity is a 'thing' or 'object' (e.g., Student, Car). Represented by a Rectangle.", "category": "ERD Symbols"},
            "attribute": {"response": "Attributes are properties of an entity (e.g., Student Name). Represented by an Ellipse.", "category": "ERD Symbols"},
            "primary key": {"response": "A unique identifier for a record. It cannot be null. (Underlined in ERD).", "category": "Design"},
            "foreign key": {"response": "A field that points to a primary key in another table to create a relationship.", "category": "Design"},
            "weak entity": {"response": "An entity that depends on another entity. Represented by a Double Rectangle.", "category": "ERD Symbols"},
            "cardinality": {"response": "It shows the number of instances of one entity related to another (1:1, 1:M, M:N).", "category": "Design"},

            # ADVANCED ERD/EERD
            "recursive relationship": {"response": "A relationship where the same entity type participates more than once (e.g., Employee 'manages' other Employees).", "category": "Advanced ERD"},
            "ternary relationship": {"response": "A relationship between three different entities.", "category": "Advanced ERD"},
            "participation constraint": {"response": "Specifies whether the existence of an entity depends on its being related to another entity.", "category": "Constraints"},
            "disjointness constraint": {"response": "Specifies that subclasses must be disjoint (an entity belongs to at most one subclass).", "category": "EERD"},
            "specialization": {"response": "Top-down approach: Breaking a high-level entity into subclasses.", "category": "EERD"},
            "generalization": {"response": "Bottom-up approach: Combining common entities into a higher-level superclass.", "category": "EERD"},

            # SQL
            "sql injection": {"response": "A type of attack where malicious SQL statements are inserted into an entry field for execution to steal data.", "category": "Security"},
            "sql": {"response": "Structured Query Language is used to communicate with databases.", "category": "SQL"},
            "ddl": {"response": "Data Definition Language: CREATE, ALTER, DROP, TRUNCATE. It defines the structure.", "category": "SQL"},
            "dml": {"response": "Data Manipulation Language: SELECT, INSERT, UPDATE, DELETE. It handles the data.", "category": "SQL"},
            "inner join": {"response": "Returns records that have matching values in both tables.", "category": "Joins"},
            "left join": {"response": "Returns all records from the left table and matched records from the right.", "category": "Joins"},

            # NORMALIZATION
            "normalization": {"response": "Process of organizing data to reduce redundancy and dependency.", "category": "Normalization"},
            "1nf": {"response": "First Normal Form: Data must be atomic (no groups), and each record must be unique.", "category": "Normalization"},
            "2nf": {"response": "Second Normal Form: Must be in 1NF and no partial functional dependency exists.", "category": "Normalization"},
            "3nf": {"response": "Third Normal Form: Must be in 2NF and no transitive dependency exists.", "category": "Normalization"},

            # RECOVERY & DATA MODELS
            "checkpoint": {"response": "A mechanism where previous logs are stored permanently in a storage disk to save time in recovery.", "category": "Recovery"},
            "shadow paging": {"response": "An alternative to log-based recovery where the database uses fixed-size logical units called pages.", "category": "Recovery"},
            "data models": {"response": "Major models: Hierarchical, Network, Relational, and Object-Oriented Models.", "category": "Data Models"},
            "transaction states": {"response": "Active, Partially Committed, Committed, Failed, and Aborted.", "category": "Transactions"},
        }

        self.create_widgets()
        self.display_welcome_message()

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#2d2d2d", height=70)
        header.pack(fill=tk.X)
        tk.Label(header, text="🗄️ Database Assistant", font=("Segoe UI", 16, "bold"), bg="#2d2d2d", fg="#4CAF50").pack(pady=20)

        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11), bg="#252526", fg="#D4D4D4", borderwidth=0)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.chat_display.config(state=tk.DISABLED)

        self.chat_display.tag_config("user", foreground="#569CD6", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("bot", foreground="#4EC9B0", font=("Consolas", 11, "bold"))

        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, padx=20, pady=20)

        self.user_input = tk.Entry(input_frame, font=("Consolas", 12), bg="#3C3C3C", fg="#D4D4D4", insertbackground="white", relief=tk.FLAT)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(input_frame, text="Send", command=self.send_message, bg="#4CAF50", fg="white", width=12, font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        send_btn.pack(side=tk.RIGHT)

    def display_welcome_message(self):
        self.display_message("BOT", "Welcome! I can help you with DBMS, SQL, ERD, and Normalization.", "System")

    def display_message(self, sender, message, category=None):
        self.chat_display.config(state=tk.NORMAL)
        current_time = datetime.now().strftime("%H:%M")
        if sender == "USER":
            self.chat_display.insert(tk.END, f"[{current_time}] YOU: {message}\n", "user")
        else:
            cat_text = f" [{category}]" if category else ""
            self.chat_display.insert(tk.END, f"[{current_time}] BOT{cat_text}: {message}\n", "bot")
        self.chat_display.insert(tk.END, "-"*60 + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def get_response(self, user_msg):
        # Cleaning the input
        clean = re.sub(r'[^\w\s]', '', user_msg.lower()).strip()
        
        # Sort keys by length so "sql injection" is checked before "sql"
        sorted_keys = sorted(self.knowledge_base.keys(), key=len, reverse=True)
        
        for keys in sorted_keys:
            patterns = keys.split("|")
            for pattern in patterns:
                # Word boundary check taake "sql" poora word match ho
                if re.search(r'\b' + re.escape(pattern) + r'\b', clean):
                    data = self.knowledge_base[keys]
                    return data["response"], data["category"]
        
        return "I'm not sure about that. Try asking about SQL Injection, Joins, or ERD.", "Unknown"

    def send_message(self):
        msg = self.user_input.get().strip()
        if msg:
            self.display_message("USER", msg)
            resp, cat = self.get_response(msg)
            self.display_message("BOT", resp, cat)
            self.user_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseBot(root)
    root.mainloop()