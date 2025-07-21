"""
Professional Number System Converter
A comprehensive number base conversion tool with advanced features
Author: Praveen Yadav
Version: 2.0.0
"""

import csv
import json
import os
import struct
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from datetime import datetime
from tkinter import ttk, messagebox, filedialog
from typing import Union


class NumberSystemConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.load_settings()
        self.setup_styles()
        # Initialize base systems
        self.init_base_systems()

        self.setup_ui()
        self.setup_menu()
        self.load_history()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("Professional Number System Converter v2.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#f0f0f0")

        # Set icon if available
        try:
            self.root.iconbitmap("assets/icon/conversion.ico")
        except:
            pass  # Icon not found, continue without it

        # Center window on screen
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_variables(self):
        """Initialize variables"""
        self.input_number = tk.StringVar()
        self.from_base = tk.StringVar(value="10")
        self.to_base = tk.StringVar(value="2")
        self.result_var = tk.StringVar()

        # Calculator variables
        self.calc_display = tk.StringVar(value="0")
        self.calc_base = tk.StringVar(value="10")
        self.calc_memory = 0
        self.calc_operation = None
        self.calc_operand = None

        # IEEE 754 variables
        self.ieee_input = tk.StringVar()
        self.ieee_format = tk.StringVar(value="single")

        self.history = []
        self.settings = {
            "auto_save_history": True,
            "max_history_entries": 100,
            "default_from_base": "10",
            "default_to_base": "2",
            "show_process": True,
            "group_digits": True
        }

    def init_base_systems(self):
        """Initialize number base systems"""
        self.base_systems = {
            "2": {"name": "Binary", "digits": "01", "max_digit": 1},
            "3": {"name": "Ternary", "digits": "012", "max_digit": 2},
            "4": {"name": "Quaternary", "digits": "0123", "max_digit": 3},
            "5": {"name": "Quinary", "digits": "01234", "max_digit": 4},
            "6": {"name": "Senary", "digits": "012345", "max_digit": 5},
            "7": {"name": "Septenary", "digits": "0123456", "max_digit": 6},
            "8": {"name": "Octal", "digits": "01234567", "max_digit": 7},
            "9": {"name": "Nonary", "digits": "012345678", "max_digit": 8},
            "10": {"name": "Decimal", "digits": "0123456789", "max_digit": 9},
            "11": {"name": "Undecimal", "digits": "0123456789A", "max_digit": 10},
            "12": {"name": "Duodecimal", "digits": "0123456789AB", "max_digit": 11},
            "13": {"name": "Tridecimal", "digits": "0123456789ABC", "max_digit": 12},
            "14": {"name": "Tetradecimal", "digits": "0123456789ABCD", "max_digit": 13},
            "15": {"name": "Pentadecimal", "digits": "0123456789ABCDE", "max_digit": 14},
            "16": {"name": "Hexadecimal", "digits": "0123456789ABCDEF", "max_digit": 15},
            "20": {"name": "Vigesimal", "digits": "0123456789ABCDEFGHIJ", "max_digit": 19},
            "36": {"name": "Base36", "digits": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", "max_digit": 35}
        }

    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("converter_settings.json"):
                with open("converter_settings.json", "r") as f:
                    self.settings.update(json.load(f))
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to file"""
        try:
            with open("converter_settings.json", "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def load_history(self):
        """Load conversion history from file"""
        try:
            if os.path.exists("converter_history.json"):
                with open("converter_history.json", "r") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")

    def save_history(self):
        """Save conversion history to file"""
        try:
            # Keep only the last N entries based on settings
            max_entries = self.settings.get("max_history_entries", 100)
            with open("converter_history.json", "w") as f:
                json.dump(self.history[-max_entries:], f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def setup_styles(self):
        """Setup custom styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom button styles
        self.style.configure(
            "Convert.TButton",
            font=("Arial", 12, "bold"),
            padding=(20, 10)
        )

        self.style.configure(
            "Calc.TButton",
            font=("Arial", 10, "bold"),
            padding=(5, 5)
        )

    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Main Converter Tab
        self.converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.converter_frame, text="Number Converter")
        self.setup_converter_tab()

        # Batch Converter Tab
        self.batch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.batch_frame, text="Batch Converter")
        self.setup_batch_tab()

        # Calculator Tab
        self.calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calculator_frame, text="Multi-Base Calculator")
        self.setup_calculator_tab()

        # IEEE 754 Tab
        self.ieee_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ieee_frame, text="IEEE 754 Converter")
        self.setup_ieee_tab()

        # Programming Tab
        self.programming_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.programming_frame, text="Programming Tools")
        self.setup_programming_tab()

        # Educational Tab
        self.education_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.education_frame, text="Number Systems Guide")
        self.setup_education_tab()

        # History Tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="History")
        self.setup_history_tab()

    def setup_converter_tab(self):
        """Setup the main converter tab"""
        main_container = ttk.Frame(self.converter_frame, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_container,
            text="Professional Number System Converter",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))

        # Input Section
        input_frame = ttk.LabelFrame(main_container, text="Input", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # From Base Selection
        from_frame = ttk.Frame(input_frame)
        from_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(from_frame, text="From Base:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        from_combo = ttk.Combobox(
            from_frame,
            textvariable=self.from_base,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=15
        )
        from_combo.pack(side=tk.LEFT, padx=(10, 20))
        from_combo.bind("<<ComboboxSelected>>", self.on_from_base_change)

        # Display base name
        self.from_base_label = tk.Label(from_frame, text="(Decimal)", font=("Arial", 10))
        self.from_base_label.pack(side=tk.LEFT)

        # Input Number
        input_number_frame = ttk.Frame(input_frame)
        input_number_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(input_number_frame, text="Number:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        self.input_entry = tk.Entry(
            input_number_frame,
            textvariable=self.input_number,
            font=("Courier", 14),
            width=30,
            validate="key",
            validatecommand=(self.root.register(self.validate_input), '%P')
        )
        self.input_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # To Base Selection
        to_frame = ttk.Frame(input_frame)
        to_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(to_frame, text="To Base:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        to_combo = ttk.Combobox(
            to_frame,
            textvariable=self.to_base,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=15
        )
        to_combo.pack(side=tk.LEFT, padx=(10, 20))
        to_combo.bind("<<ComboboxSelected>>", self.on_to_base_change)

        # Display base name
        self.to_base_label = tk.Label(to_frame, text="(Binary)", font=("Arial", 10))
        self.to_base_label.pack(side=tk.LEFT)

        # Control Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)

        convert_button = tk.Button(
            button_frame,
            text="Convert",
            command=self.convert_number,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        convert_button.pack(side=tk.LEFT, padx=(0, 10))

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_conversion,
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))

        swap_button = tk.Button(
            button_frame,
            text="Swap Bases",
            command=self.swap_bases,
            font=("Arial", 12),
            bg="#9b59b6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        swap_button.pack(side=tk.LEFT)

        # Results Section
        results_frame = ttk.LabelFrame(main_container, text="Results", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Quick Results Grid
        quick_frame = ttk.Frame(results_frame)
        quick_frame.pack(fill=tk.X, pady=(0, 10))

        # Common base results
        self.quick_results = {}
        common_bases = ["2", "8", "10", "16"]

        for i, base in enumerate(common_bases):
            row = i // 2
            col = i % 2

            base_name = self.base_systems[base]["name"]

            label = tk.Label(quick_frame, text=f"{base_name} ({base}):", font=("Arial", 11, "bold"))
            label.grid(row=row, column=col * 2, sticky=tk.W, padx=(0, 10), pady=2)

            result_var = tk.StringVar()
            result_entry = tk.Entry(
                quick_frame,
                textvariable=result_var,
                font=("Courier", 11),
                state="readonly",
                width=20
            )
            result_entry.grid(row=row, column=col * 2 + 1, sticky=tk.W, padx=(0, 20), pady=2)

            self.quick_results[base] = result_var

        # Detailed Results
        detail_frame = ttk.LabelFrame(results_frame, text="Detailed Conversion", padding="10")
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.result_text = scrolledtext.ScrolledText(
            detail_frame,
            font=("Courier", 10),
            height=12,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def setup_batch_tab(self):
        """Setup the batch converter tab"""
        batch_container = ttk.Frame(self.batch_frame, padding="20")
        batch_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            batch_container,
            text="Batch Number Converter",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Controls
        controls_frame = ttk.Frame(batch_container)
        controls_frame.pack(fill=tk.X, pady=(0, 20))

        # From/To Base Selection
        base_frame = ttk.Frame(controls_frame)
        base_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(base_frame, text="From Base:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.batch_from_base = tk.StringVar(value="10")
        ttk.Combobox(
            base_frame,
            textvariable=self.batch_from_base,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=10
        ).grid(row=0, column=1, padx=(0, 20))

        tk.Label(base_frame, text="To Base:", font=("Arial", 11)).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.batch_to_base = tk.StringVar(value="2")
        ttk.Combobox(
            base_frame,
            textvariable=self.batch_to_base,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=10
        ).grid(row=0, column=3)

        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            button_frame,
            text="Load from File",
            command=self.load_batch_file,
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="Convert All",
            command=self.convert_batch,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="Export Results",
            command=self.export_batch_results,
            font=("Arial", 10),
            bg="#e67e22",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_batch,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.LEFT)

        # Input/Output Area
        io_frame = ttk.Frame(batch_container)
        io_frame.pack(fill=tk.BOTH, expand=True)

        # Input
        input_batch_frame = ttk.LabelFrame(io_frame, text="Input Numbers (one per line)", padding="10")
        input_batch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.batch_input = scrolledtext.ScrolledText(
            input_batch_frame,
            font=("Courier", 10),
            height=20,
            wrap=tk.WORD
        )
        self.batch_input.pack(fill=tk.BOTH, expand=True)

        # Output
        output_batch_frame = ttk.LabelFrame(io_frame, text="Conversion Results", padding="10")
        output_batch_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.batch_output = scrolledtext.ScrolledText(
            output_batch_frame,
            font=("Courier", 10),
            height=20,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.batch_output.pack(fill=tk.BOTH, expand=True)

    def setup_calculator_tab(self):
        """Setup the multi-base calculator tab"""
        calc_container = ttk.Frame(self.calculator_frame, padding="20")
        calc_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            calc_container,
            text="Multi-Base Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Calculator Controls
        calc_controls = ttk.Frame(calc_container)
        calc_controls.pack(fill=tk.X, pady=(0, 20))

        tk.Label(calc_controls, text="Base:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        base_calc_combo = ttk.Combobox(
            calc_controls,
            textvariable=self.calc_base,
            values=["2", "8", "10", "16"],
            state="readonly",
            width=10
        )
        base_calc_combo.pack(side=tk.LEFT, padx=(10, 20))
        base_calc_combo.bind("<<ComboboxSelected>>", self.on_calc_base_change)

        # Calculator Display
        display_frame = ttk.Frame(calc_container)
        display_frame.pack(fill=tk.X, pady=(0, 20))

        self.calc_display_entry = tk.Entry(
            display_frame,
            textvariable=self.calc_display,
            font=("Courier", 20),
            justify=tk.RIGHT,
            state="readonly",
            bg="black",
            fg="lime"
        )
        self.calc_display_entry.pack(fill=tk.X)

        # Calculator Buttons
        buttons_frame = ttk.Frame(calc_container)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_calculator_buttons(buttons_frame)

    def setup_calculator_buttons(self, parent):
        """Setup calculator button layout"""
        # Button layout based on current base
        button_layout = [
            ['C', 'CE', '⌫', '/'],
            ['A', 'B', 'C', '*'],
            ['D', 'E', 'F', '-'],
            ['7', '8', '9', '+'],
            ['4', '5', '6', '='],
            ['1', '2', '3'],
            ['0', '.']
        ]

        self.calc_buttons = {}

        for i, row in enumerate(button_layout):
            for j, btn_text in enumerate(row):
                if btn_text in ['C', 'CE', '⌫', '/', '*', '-', '+', '=', '.']:
                    # Operation buttons
                    btn = tk.Button(
                        parent,
                        text=btn_text,
                        font=("Arial", 14, "bold"),
                        bg="#34495e",
                        fg="white",
                        relief=tk.FLAT,
                        command=lambda t=btn_text: self.calc_button_click(t)
                    )
                else:
                    # Number buttons
                    btn = tk.Button(
                        parent,
                        text=btn_text,
                        font=("Arial", 14),
                        bg="#7f8c8d",
                        fg="white",
                        relief=tk.FLAT,
                        command=lambda t=btn_text: self.calc_button_click(t)
                    )

                btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                self.calc_buttons[btn_text] = btn

        # Configure grid weights
        for i in range(len(button_layout)):
            parent.grid_rowconfigure(i, weight=1)
        for j in range(4):
            parent.grid_columnconfigure(j, weight=1)

        self.update_calculator_buttons()

    def setup_ieee_tab(self):
        """Setup the IEEE 754 converter tab"""
        ieee_container = ttk.Frame(self.ieee_frame, padding="20")
        ieee_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            ieee_container,
            text="IEEE 754 Floating Point Converter",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Format Selection
        format_frame = ttk.Frame(ieee_container)
        format_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(format_frame, text="Format:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.ieee_format,
            values=["single", "double"],
            state="readonly",
            width=15
        )
        format_combo.pack(side=tk.LEFT, padx=(10, 0))

        # Input
        input_ieee_frame = ttk.LabelFrame(ieee_container, text="Input", padding="15")
        input_ieee_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(input_ieee_frame, text="Decimal Number:", font=("Arial", 11)).pack(anchor=tk.W)

        ieee_entry = tk.Entry(
            input_ieee_frame,
            textvariable=self.ieee_input,
            font=("Courier", 12),
            width=30
        )
        ieee_entry.pack(fill=tk.X, pady=(5, 10))

        tk.Button(
            input_ieee_frame,
            text="Convert to IEEE 754",
            command=self.convert_to_ieee,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT
        ).pack()

        # Results
        ieee_results_frame = ttk.LabelFrame(ieee_container, text="IEEE 754 Representation", padding="15")
        ieee_results_frame.pack(fill=tk.BOTH, expand=True)

        self.ieee_results = scrolledtext.ScrolledText(
            ieee_results_frame,
            font=("Courier", 10),
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.ieee_results.pack(fill=tk.BOTH, expand=True)

    def setup_programming_tab(self):
        """Setup the programming tools tab"""
        prog_container = ttk.Frame(self.programming_frame, padding="20")
        prog_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            prog_container,
            text="Programming Number Tools",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Two's Complement Section
        twos_frame = ttk.LabelFrame(prog_container, text="Two's Complement", padding="15")
        twos_frame.pack(fill=tk.X, pady=(0, 20))

        twos_input_frame = ttk.Frame(twos_frame)
        twos_input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(twos_input_frame, text="Decimal Number:", font=("Arial", 11)).pack(side=tk.LEFT)

        self.twos_input = tk.StringVar()
        tk.Entry(
            twos_input_frame,
            textvariable=self.twos_input,
            font=("Courier", 11),
            width=20
        ).pack(side=tk.LEFT, padx=(10, 20))

        tk.Label(twos_input_frame, text="Bits:", font=("Arial", 11)).pack(side=tk.LEFT)

        self.twos_bits = tk.StringVar(value="8")
        ttk.Combobox(
            twos_input_frame,
            textvariable=self.twos_bits,
            values=["8", "16", "32", "64"],
            state="readonly",
            width=5
        ).pack(side=tk.LEFT, padx=(10, 20))

        tk.Button(
            twos_input_frame,
            text="Calculate",
            command=self.calculate_twos_complement,
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Bit Operations Section
        bit_ops_frame = ttk.LabelFrame(prog_container, text="Bitwise Operations", padding="15")
        bit_ops_frame.pack(fill=tk.X, pady=(0, 20))

        bit_input_frame = ttk.Frame(bit_ops_frame)
        bit_input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(bit_input_frame, text="Number A:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.bit_a = tk.StringVar()
        tk.Entry(bit_input_frame, textvariable=self.bit_a, font=("Courier", 11), width=15).grid(row=0, column=1,
                                                                                                padx=(0, 20))

        tk.Label(bit_input_frame, text="Number B:", font=("Arial", 11)).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.bit_b = tk.StringVar()
        tk.Entry(bit_input_frame, textvariable=self.bit_b, font=("Courier", 11), width=15).grid(row=0, column=3,
                                                                                                padx=(0, 20))

        tk.Button(
            bit_input_frame,
            text="Calculate All",
            command=self.calculate_bit_operations,
            font=("Arial", 10),
            bg="#e67e22",
            fg="white",
            relief=tk.FLAT
        ).grid(row=0, column=4)

        # Results Area
        prog_results_frame = ttk.LabelFrame(prog_container, text="Results", padding="15")
        prog_results_frame.pack(fill=tk.BOTH, expand=True)

        self.prog_results = scrolledtext.ScrolledText(
            prog_results_frame,
            font=("Courier", 10),
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.prog_results.pack(fill=tk.BOTH, expand=True)

    def setup_education_tab(self):
        """Setup the educational content tab"""
        edu_container = ttk.Frame(self.education_frame, padding="20")
        edu_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            edu_container,
            text="Number Systems Educational Guide",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Topic Selection
        topic_frame = ttk.Frame(edu_container)
        topic_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(topic_frame, text="Select Topic:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        self.edu_topic = tk.StringVar(value="Number Systems Overview")
        topic_combo = ttk.Combobox(
            topic_frame,
            textvariable=self.edu_topic,
            values=[
                "Number Systems Overview",
                "Binary System",
                "Octal System",
                "Hexadecimal System",
                "Conversion Methods",
                "Computer Number Representation",
                "IEEE 754 Standard",
                "Two's Complement",
                "Bitwise Operations"
            ],
            state="readonly",
            width=30
        )
        topic_combo.pack(side=tk.LEFT, padx=(10, 20))
        topic_combo.bind("<<ComboboxSelected>>", self.show_educational_content)

        # Content Area
        self.edu_content = scrolledtext.ScrolledText(
            edu_container,
            font=("Arial", 11),
            height=25,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.edu_content.pack(fill=tk.BOTH, expand=True)

        # Load initial content
        self.show_educational_content()

    def setup_history_tab(self):
        """Setup the history tab"""
        history_container = ttk.Frame(self.history_frame, padding="10")
        history_container.pack(fill=tk.BOTH, expand=True)

        # History controls
        controls_frame = ttk.Frame(history_container)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(controls_frame, text="Conversion History", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

        tk.Button(
            controls_frame,
            text="Clear History",
            command=self.clear_history,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.RIGHT, padx=(10, 0))

        tk.Button(
            controls_frame,
            text="Export History",
            command=self.export_history,
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT
        ).pack(side=tk.RIGHT)

        # History treeview
        history_tree_frame = ttk.Frame(history_container)
        history_tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Time", "Input", "From Base", "To Base", "Result")
        self.history_tree = ttk.Treeview(history_tree_frame, columns=columns, show="headings")

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)

        # Scrollbar for history
        history_scrollbar = ttk.Scrollbar(history_tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_menu(self):
        """Setup application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Conversion", command=self.clear_conversion)
        file_menu.add_command(label="Load Numbers from File", command=self.load_numbers_file)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Export History", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Base Converter", command=lambda: self.notebook.select(0))
        tools_menu.add_command(label="Batch Converter", command=lambda: self.notebook.select(1))
        tools_menu.add_command(label="Multi-Base Calculator", command=lambda: self.notebook.select(2))
        tools_menu.add_command(label="IEEE 754 Converter", command=lambda: self.notebook.select(3))
        tools_menu.add_command(label="Programming Tools", command=lambda: self.notebook.select(4))

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences", command=self.show_preferences)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=lambda: self.notebook.select(5))
        help_menu.add_command(label="About", command=self.show_about)

    def validate_input(self, value):
        """Validate input based on selected base"""
        if value == "":
            return True

        try:
            from_base = int(self.from_base.get())
            valid_chars = self.base_systems[str(from_base)]["digits"]

            for char in value.upper():
                if char not in valid_chars:
                    return False
            return True
        except:
            return True  # Allow input if validation fails

    def on_from_base_change(self, event=None):
        """Handle from base change"""
        base = self.from_base.get()
        if base in self.base_systems:
            name = self.base_systems[base]["name"]
            self.from_base_label.config(text=f"({name})")

            # Clear input if it's invalid for new base
            current_input = self.input_number.get()
            if current_input and not self.validate_input(current_input):
                self.input_number.set("")

    def on_to_base_change(self, event=None):
        """Handle to base change"""
        base = self.to_base.get()
        if base in self.base_systems:
            name = self.base_systems[base]["name"]
            self.to_base_label.config(text=f"({name})")

    def on_calc_base_change(self, event=None):
        """Handle calculator base change"""
        self.calc_display.set("0")
        self.calc_memory = 0
        self.calc_operation = None
        self.calc_operand = None
        self.update_calculator_buttons()

    def update_calculator_buttons(self):
        """Update calculator button states based on current base"""
        base = int(self.calc_base.get())
        valid_digits = self.base_systems[str(base)]["digits"]

        for btn_text, btn in self.calc_buttons.items():
            if btn_text in "0123456789ABCDEF":
                if btn_text in valid_digits:
                    btn.config(state=tk.NORMAL, bg="#7f8c8d")
                else:
                    btn.config(state=tk.DISABLED, bg="#2c3e50")

    def convert_number(self):
        """Convert number between bases"""
        try:
            input_num = self.input_number.get().strip()
            if not input_num:
                messagebox.showwarning("Warning", "Please enter a number to convert")
                return

            from_base = int(self.from_base.get())
            to_base = int(self.to_base.get())

            # Convert to decimal first
            decimal_value = self.to_decimal(input_num, from_base)

            if decimal_value is False:
                messagebox.showerror("Error", "Invalid number for the selected base")
                return

            # Convert from decimal to target base
            result = self.from_decimal(decimal_value, to_base)

            # Update quick results
            self.update_quick_results(decimal_value)

            # Show detailed conversion process
            self.show_conversion_details(input_num, from_base, to_base, decimal_value, result)

            # Add to history
            if self.settings.get("auto_save_history", True):
                self.add_to_history(input_num, from_base, to_base, result)

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def to_decimal(self, number: str, base: int) -> Union[int, bool]:
        """Convert number from any base to decimal"""
        try:
            decimal = 0
            number = number.upper()
            power = len(number) - 1

            for digit in number:
                if digit in "0123456789":
                    digit_value = int(digit)
                else:
                    digit_value = ord(digit) - ord('A') + 10

                if digit_value >= base:
                    return False

                decimal += digit_value * (base ** power)
                power -= 1

            return decimal
        except:
            return False

    def from_decimal(self, decimal: int, base: int) -> str:
        """Convert decimal number to any base"""
        if decimal == 0:
            return "0"

        result = ""
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        while decimal > 0:
            remainder = decimal % base
            result = digits[remainder] + result
            decimal = decimal // base

        return result

    def update_quick_results(self, decimal_value: int):
        """Update quick conversion results"""
        for base, result_var in self.quick_results.items():
            try:
                converted = self.from_decimal(decimal_value, int(base))
                # Format large numbers with grouping if enabled
                if self.settings.get("group_digits", True) and base == "10":
                    converted = f"{int(converted):,}"
                result_var.set(converted)
            except:
                result_var.set("Error")

    def show_conversion_details(self, input_num: str, from_base: int, to_base: int, decimal_value: int, result: str):
        """Show detailed conversion process"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        details = f"""
Number Base Conversion Details
{'=' * 50}

Input: {input_num} (Base {from_base})
Output: {result} (Base {to_base})
Decimal Value: {decimal_value:,}

Conversion Process:
{'=' * 30}

Step 1: Convert {input_num} (Base {from_base}) to Decimal
"""

        if from_base != 10:
            details += self.get_to_decimal_process(input_num, from_base)
        else:
            details += f"Already in decimal: {decimal_value}\n"

        if to_base != 10:
            details += f"\nStep 2: Convert {decimal_value} (Decimal) to Base {to_base}\n"
            details += self.get_from_decimal_process(decimal_value, to_base)

        details += f"""

Summary:
--------
{input_num} (Base {from_base}) = {decimal_value} (Decimal) = {result} (Base {to_base})

Additional Information:
----------------------
- Base {from_base} uses digits: {self.base_systems[str(from_base)]["digits"]}
- Base {to_base} uses digits: {self.base_systems[str(to_base)]["digits"]}
- Conversion completed at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        self.result_text.insert(1.0, details)
        self.result_text.config(state=tk.DISABLED)

    def get_to_decimal_process(self, number: str, base: int) -> str:
        """Get step-by-step process for converting to decimal"""
        process = ""
        number = number.upper()
        power = len(number) - 1
        total = 0

        for i, digit in enumerate(number):
            if digit in "0123456789":
                digit_value = int(digit)
            else:
                digit_value = ord(digit) - ord('A') + 10

            term_value = digit_value * (base ** power)
            total += term_value

            process += f"Position {i + 1}: {digit} × {base}^{power} = {digit_value} × {base ** power} = {term_value}\n"
            power -= 1

        process += f"\nSum: {total}\n"
        return process

    def get_from_decimal_process(self, decimal: int, base: int) -> str:
        """Get step-by-step process for converting from decimal"""
        process = ""
        original_decimal = decimal
        digits = []
        step = 1

        while decimal > 0:
            remainder = decimal % base
            quotient = decimal // base

            digit_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[remainder]
            digits.append(digit_char)

            process += f"Step {step}: {decimal} ÷ {base} = {quotient} remainder {remainder} ({digit_char})\n"
            decimal = quotient
            step += 1

        process += f"\nReading remainders from bottom to top: {''.join(reversed(digits))}\n"
        return process

    def swap_bases(self):
        """Swap from and to bases"""
        from_base = self.from_base.get()
        to_base = self.to_base.get()

        self.from_base.set(to_base)
        self.to_base.set(from_base)

        self.on_from_base_change()
        self.on_to_base_change()

        # Clear input as it might not be valid for the new base
        self.input_number.set("")

        # Clear results
        for result_var in self.quick_results.values():
            result_var.set("")

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    def clear_conversion(self):
        """Clear all conversion fields"""
        self.input_number.set("")

        for result_var in self.quick_results.values():
            result_var.set("")

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    def calc_button_click(self, button_text: str):
        """Handle calculator button clicks"""
        current = self.calc_display.get()
        base = int(self.calc_base.get())

        if button_text == 'C':
            self.calc_display.set("0")
            self.calc_memory = 0
            self.calc_operation = None
            self.calc_operand = None
        elif button_text == 'CE':
            self.calc_display.set("0")
        elif button_text == '⌫':
            if len(current) > 1:
                self.calc_display.set(current[:-1])
            else:
                self.calc_display.set("0")
        elif button_text in "0123456789ABCDEF":
            if current == "0":
                self.calc_display.set(button_text)
            else:
                self.calc_display.set(current + button_text)
        elif button_text in "+-*/":
            try:
                current_value = self.to_decimal(current, base)
                if self.calc_operation and self.calc_operand is not None:
                    result = self.perform_calculation(self.calc_operand, current_value, self.calc_operation, base)
                    self.calc_display.set(result)
                    self.calc_operand = self.to_decimal(result, base)
                else:
                    self.calc_operand = current_value
                self.calc_operation = button_text
            except:
                self.calc_display.set("Error")
        elif button_text == '=':
            try:
                current_value = self.to_decimal(current, base)
                if self.calc_operation and self.calc_operand is not None:
                    result = self.perform_calculation(self.calc_operand, current_value, self.calc_operation, base)
                    self.calc_display.set(result)
                    self.calc_operation = None
                    self.calc_operand = None
            except:
                self.calc_display.set("Error")

    def perform_calculation(self, operand1: int, operand2: int, operation: str, base: int) -> str:
        """Perform calculation and return result in current base"""
        if operation == '+':
            result = operand1 + operand2
        elif operation == '-':
            result = operand1 - operand2
        elif operation == '*':
            result = operand1 * operand2
        elif operation == '/':
            if operand2 == 0:
                return "Error"
            result = operand1 // operand2  # Integer division for simplicity
        else:
            return "Error"

        return self.from_decimal(result, base) if result >= 0 else "Error"

    def convert_to_ieee(self):
        """Convert decimal to IEEE 754 format"""
        try:
            value = float(self.ieee_input.get())
            format_type = self.ieee_format.get()

            if format_type == "single":
                # 32-bit IEEE 754
                packed = struct.pack('>f', value)
                bits = ''.join(f'{byte:08b}' for byte in packed)

                sign = bits[0]
                exponent = bits[1:9]
                mantissa = bits[9:32]

                result = f"""
IEEE 754 Single Precision (32-bit) Representation
{'=' * 50}

Decimal Value: {value}
Binary Representation: {bits}

Breakdown:
----------
Sign bit (1 bit):      {sign} ({'Positive' if sign == '0' else 'Negative'})
Exponent (8 bits):     {exponent} (Decimal: {int(exponent, 2)})
Mantissa (23 bits):    {mantissa}

Detailed Analysis:
-----------------
- Sign: {'+' if sign == '0' else '-'}
- Biased Exponent: {int(exponent, 2)}
- Unbiased Exponent: {int(exponent, 2) - 127}
- Mantissa (with implicit 1): 1.{mantissa}

Hexadecimal: 0x{packed.hex().upper()}

Formula: (-1)^{sign} × 1.{mantissa} × 2^({int(exponent, 2)} - 127)
"""
            else:
                # 64-bit IEEE 754
                packed = struct.pack('>d', value)
                bits = ''.join(f'{byte:08b}' for byte in packed)

                sign = bits[0]
                exponent = bits[1:12]
                mantissa = bits[12:64]

                result = f"""
IEEE 754 Double Precision (64-bit) Representation
{'=' * 50}

Decimal Value: {value}
Binary Representation: {bits}

Breakdown:
----------
Sign bit (1 bit):      {sign} ({'Positive' if sign == '0' else 'Negative'})
Exponent (11 bits):    {exponent} (Decimal: {int(exponent, 2)})
Mantissa (52 bits):    {mantissa}

Detailed Analysis:
-----------------
- Sign: {'+' if sign == '0' else '-'}
- Biased Exponent: {int(exponent, 2)}
- Unbiased Exponent: {int(exponent, 2) - 1023}
- Mantissa (with implicit 1): 1.{mantissa}

Hexadecimal: 0x{packed.hex().upper()}

Formula: (-1)^{sign} × 1.{mantissa} × 2^({int(exponent, 2)} - 1023)
"""

            self.ieee_results.config(state=tk.NORMAL)
            self.ieee_results.delete(1.0, tk.END)
            self.ieee_results.insert(1.0, result)
            self.ieee_results.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"IEEE 754 conversion failed: {str(e)}")

    def calculate_twos_complement(self):
        """Calculate two's complement representation"""
        try:
            value = int(self.twos_input.get())
            bits = int(self.twos_bits.get())

            # Calculate various representations
            if value >= 0:
                binary = format(value, f'0{bits}b')
                twos_comp = binary
            else:
                # For negative numbers, calculate two's complement
                max_val = 2 ** bits
                twos_comp_val = max_val + value
                twos_comp = format(twos_comp_val, f'0{bits}b')
                binary = format(abs(value), f'0{bits}b')

            result = f"""
Two's Complement Representation
{'=' * 40}

Decimal Value: {value}
Bit Width: {bits} bits
Range: {-(2 ** (bits - 1))} to {2 ** (bits - 1) - 1}

Representations:
---------------
Unsigned Binary:     {format(abs(value), f'0{bits}b')}
Two's Complement:    {twos_comp}
Hexadecimal:         0x{int(twos_comp, 2):0{bits // 4}X}

Binary Analysis:
---------------
Sign bit: {twos_comp[0]} ({'Positive/Zero' if twos_comp[0] == '0' else 'Negative'})
Magnitude: {twos_comp[1:]}

"""

            if value < 0:
                result += f"""
Two's Complement Calculation Process:
------------------------------------
1. Binary of |{value}|:  {binary}
2. One's complement:     {''.join('1' if bit == '0' else '0' for bit in binary)}
3. Add 1:                {twos_comp}
"""

            self.prog_results.config(state=tk.NORMAL)
            self.prog_results.delete(1.0, tk.END)
            self.prog_results.insert(1.0, result)
            self.prog_results.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Two's complement calculation failed: {str(e)}")

    def calculate_bit_operations(self):
        """Calculate bitwise operations"""
        try:
            a = int(self.bit_a.get())
            b = int(self.bit_b.get())

            # Calculate operations
            and_result = a & b
            or_result = a | b
            xor_result = a ^ b
            not_a = ~a & 0xFFFFFFFF  # 32-bit mask
            not_b = ~b & 0xFFFFFFFF

            result = f"""
Bitwise Operations
{'=' * 30}

Input Values:
A = {a} (Decimal) = {bin(a)} (Binary) = 0x{a:X} (Hex)
B = {b} (Decimal) = {bin(b)} (Binary) = 0x{b:X} (Hex)

Operations:
----------
A AND B  = {and_result:10} (Decimal) = {bin(and_result):>15} (Binary) = 0x{and_result:X} (Hex)
A OR B   = {or_result:10} (Decimal) = {bin(or_result):>15} (Binary) = 0x{or_result:X} (Hex)
A XOR B  = {xor_result:10} (Decimal) = {bin(xor_result):>15} (Binary) = 0x{xor_result:X} (Hex)
NOT A    = {not_a:10} (Decimal) = {bin(not_a):>15} (Binary) = 0x{not_a:X} (Hex)
NOT B    = {not_b:10} (Decimal) = {bin(not_b):>15} (Binary) = 0x{not_b:X} (Hex)

Shift Operations (A):
--------------------
A << 1   = {a << 1:10} (Decimal) = {bin(a << 1):>15} (Binary) = 0x{(a << 1):X} (Hex)
A >> 1   = {a >> 1:10} (Decimal) = {bin(a >> 1):>15} (Binary) = 0x{(a >> 1):X} (Hex)
A << 2   = {a << 2:10} (Decimal) = {bin(a << 2):>15} (Binary) = 0x{(a << 2):X} (Hex)
A >> 2   = {a >> 2:10} (Decimal) = {bin(a >> 2):>15} (Binary) = 0x{(a >> 2):X} (Hex)
"""

            self.prog_results.config(state=tk.NORMAL)
            self.prog_results.delete(1.0, tk.END)
            self.prog_results.insert(1.0, result)
            self.prog_results.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Bit operations calculation failed: {str(e)}")

    def show_educational_content(self, event=None):
        """Show educational content based on selected topic"""
        topic = self.edu_topic.get()

        content = {
            "Number Systems Overview": """
Number Systems Overview
======================

A number system is a mathematical notation for representing numbers using a consistent set of digits or symbols. The most common number systems used in computing and mathematics are:

1. Binary (Base 2)
   - Uses digits: 0, 1
   - Used by computers for internal representation
   - Each position represents a power of 2

2. Octal (Base 8)
   - Uses digits: 0, 1, 2, 3, 4, 5, 6, 7
   - Often used in computer programming
   - Each position represents a power of 8

3. Decimal (Base 10)
   - Uses digits: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
   - Standard number system for everyday use
   - Each position represents a power of 10

4. Hexadecimal (Base 16)
   - Uses digits: 0-9 and letters A-F (representing 10-15)
   - Commonly used in computer science and programming
   - Each position represents a power of 16

Key Concepts:
- Base/Radix: The number of unique digits in the system
- Place Value: Each position has a value based on the base raised to a power
- Conversion: Numbers can be converted between different bases

Understanding number systems is fundamental to computer science, digital electronics, and programming.
""",

            "Binary System": """
Binary Number System (Base 2)
============================

The binary number system uses only two digits: 0 and 1. It's the fundamental number system used by all digital computers and electronic devices.

Characteristics:
- Base: 2
- Digits: 0, 1
- Place values: ..., 8, 4, 2, 1 (powers of 2)

Place Value Chart:
Position:  4   3   2   1   0
Power:    2⁴  2³  2²  2¹  2⁰
Value:    16   8   4   2   1

Example: 1101₂
= 1×2³ + 1×2² + 0×2¹ + 1×2⁰
= 1×8 + 1×4 + 0×2 + 1×1
= 8 + 4 + 0 + 1
= 13₁₀

Applications:
1. Computer Memory: All data is stored in binary
2. Digital Circuits: Represent ON/OFF states
3. Boolean Logic: True/False operations
4. Network Protocols: Data transmission

Binary Arithmetic:
Addition Rules:
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10 (0 with carry 1)

Common Binary Numbers:
0₂ = 0₁₀    1000₂ = 8₁₀
1₂ = 1₁₀    1001₂ = 9₁₀
10₂ = 2₁₀   1010₂ = 10₁₀
11₂ = 3₁₀   1011₂ = 11₁₀
100₂ = 4₁₀  1100₂ = 12₁₀
101₂ = 5₁₀  1101₂ = 13₁₀
110₂ = 6₁₀  1110₂ = 14₁₀
111₂ = 7₁₀  1111₂ = 15₁₀
""",

            "Conversion Methods": """
Number Base Conversion Methods
=============================

Converting between number bases is a fundamental skill in computer science. Here are the main methods:

1. CONVERTING TO DECIMAL (Any Base → Base 10)
   Method: Positional Value

   Steps:
   a) Identify the base of the source number
   b) Multiply each digit by its positional value
   c) Sum all the products

   Example: 1A3₁₆ to decimal
   = 1×16² + A×16¹ + 3×16⁰
   = 1×256 + 10×16 + 3×1
   = 256 + 160 + 3 = 419₁₀

2. CONVERTING FROM DECIMAL (Base 10 → Any Base)
   Method: Repeated Division

   Steps:
   a) Divide the decimal number by the target base
   b) Record the remainder
   c) Repeat with the quotient until it becomes 0
   d) Read remainders from bottom to top

   Example: 419₁₀ to hexadecimal
   419 ÷ 16 = 26 remainder 3
   26 ÷ 16 = 1 remainder 10 (A)
   1 ÷ 16 = 0 remainder 1
   Result: 1A3₁₆

3. DIRECT CONVERSION (Non-Decimal to Non-Decimal)
   Method: Via Decimal (Two-step process)

   Step 1: Convert source to decimal
   Step 2: Convert decimal to target base

   Alternative for Binary/Octal/Hex:
   - Binary ↔ Octal: Group by 3 bits
   - Binary ↔ Hex: Group by 4 bits
   - Octal ↔ Hex: Via binary

4. SHORTCUT METHODS

   Binary ↔ Hexadecimal:
   Each hex digit = 4 binary digits

   Binary: 1101 1010 0011
   Hex:      D    A    3

   Binary ↔ Octal:
   Each octal digit = 3 binary digits

   Binary: 001 101 010 011
   Octal:    1   5   2   3

Tips for Success:
- Practice with small numbers first
- Always verify your conversions
- Use the converter tool to check your work
- Remember the digit values for each base
"""
        }

        selected_content = content.get(topic, "Content not available for this topic.")

        self.edu_content.config(state=tk.NORMAL)
        self.edu_content.delete(1.0, tk.END)
        self.edu_content.insert(1.0, selected_content)
        self.edu_content.config(state=tk.DISABLED)

    def add_to_history(self, input_num: str, from_base: int, to_base: int, result: str):
        """Add conversion to history"""
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input": input_num,
            "from_base": from_base,
            "to_base": to_base,
            "result": result
        }

        self.history.append(history_entry)
        self.save_history()
        self.update_history_display()

    def update_history_display(self):
        """Update history treeview"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Add history items (most recent first)
        for entry in reversed(self.history[-50:]):  # Show last 50 entries
            values = (
                entry["timestamp"],
                entry["input"],
                f"Base {entry['from_base']}",
                f"Base {entry['to_base']}",
                entry["result"]
            )
            self.history_tree.insert("", 0, values=values)

    def load_batch_file(self):
        """Load numbers from file for batch conversion"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Numbers from File",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'r') as f:
                    content = f.read()

                self.batch_input.delete(1.0, tk.END)
                self.batch_input.insert(1.0, content)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def convert_batch(self):
        """Convert all numbers in batch input"""
        try:
            input_text = self.batch_input.get(1.0, tk.END).strip()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter numbers to convert")
                return

            lines = input_text.split('\n')
            from_base = int(self.batch_from_base.get())
            to_base = int(self.batch_to_base.get())

            results = []
            results.append(f"Batch Conversion Results")
            results.append(f"From Base {from_base} to Base {to_base}")
            results.append("=" * 40)
            results.append("")

            success_count = 0
            error_count = 0

            for i, line in enumerate(lines, 1):
                number = line.strip()
                if not number:
                    continue

                try:
                    decimal_value = self.to_decimal(number, from_base)
                    if decimal_value is False:
                        results.append(f"{i:3d}. {number:>15} → Error: Invalid number")
                        error_count += 1
                    else:
                        converted = self.from_decimal(decimal_value, to_base)
                        results.append(f"{i:3d}. {number:>15} → {converted}")
                        success_count += 1
                except Exception as e:
                    results.append(f"{i:3d}. {number:>15} → Error: {str(e)}")
                    error_count += 1

            results.append("")
            results.append(f"Summary: {success_count} successful, {error_count} errors")

            self.batch_output.config(state=tk.NORMAL)
            self.batch_output.delete(1.0, tk.END)
            self.batch_output.insert(1.0, '\n'.join(results))
            self.batch_output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Batch conversion failed: {e}")

    def export_batch_results(self):
        """Export batch conversion results"""
        try:
            content = self.batch_output.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Warning", "No results to export")
                return

            filename = filedialog.asksaveasfilename(
                title="Export Batch Results",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'w') as f:
                    f.write(content)

                messagebox.showinfo("Success", f"Results exported to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {e}")

    def clear_batch(self):
        """Clear batch conversion data"""
        self.batch_input.delete(1.0, tk.END)
        self.batch_output.config(state=tk.NORMAL)
        self.batch_output.delete(1.0, tk.END)
        self.batch_output.config(state=tk.DISABLED)

    def clear_history(self):
        """Clear conversion history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.history.clear()
            self.update_history_display()
            self.save_history()
            messagebox.showinfo("Success", "History cleared successfully!")

    def export_history(self):
        """Export history to CSV"""
        try:
            if not self.history:
                messagebox.showwarning("Warning", "No history to export")
                return

            filename = filedialog.asksaveasfilename(
                title="Export History",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write headers
                    writer.writerow(["Timestamp", "Input", "From Base", "To Base", "Result"])

                    # Write data
                    for entry in self.history:
                        writer.writerow([
                            entry["timestamp"],
                            entry["input"],
                            entry["from_base"],
                            entry["to_base"],
                            entry["result"]
                        ])

                messagebox.showinfo("Success", f"History exported to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export history: {e}")

    def load_numbers_file(self):
        """Load numbers from file"""
        self.load_batch_file()

    def save_results(self):
        """Save current conversion results"""
        try:
            content = self.result_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Warning", "No results to save")
                return

            filename = filedialog.asksaveasfilename(
                title="Save Results",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'w') as f:
                    f.write(content)

                messagebox.showinfo("Success", f"Results saved to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")

    def show_preferences(self):
        """Show preferences dialog"""
        pref_window = tk.Toplevel(self.root)
        pref_window.title("Preferences")
        pref_window.geometry("400x350")
        pref_window.resizable(False, False)
        pref_window.transient(self.root)
        pref_window.grab_set()

        # Center the preference window
        pref_window.update_idletasks()
        x = (pref_window.winfo_screenwidth() // 2) - 200
        y = (pref_window.winfo_screenheight() // 2) - 175
        pref_window.geometry(f"400x350+{x}+{y}")

        frame = ttk.Frame(pref_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Auto-save history
        auto_save_var = tk.BooleanVar(value=self.settings.get("auto_save_history", True))
        auto_save_cb = tk.Checkbutton(
            frame,
            text="Automatically save conversions to history",
            variable=auto_save_var
        )
        auto_save_cb.pack(anchor=tk.W, pady=(0, 10))

        # Max history entries
        tk.Label(frame, text="Maximum history entries:", font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        max_entries_var = tk.StringVar(value=str(self.settings.get("max_history_entries", 100)))
        tk.Entry(frame, textvariable=max_entries_var, width=10).pack(anchor=tk.W, pady=(0, 15))

        # Default bases
        tk.Label(frame, text="Default From Base:", font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        default_from_var = tk.StringVar(value=self.settings.get("default_from_base", "10"))
        ttk.Combobox(
            frame,
            textvariable=default_from_var,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=10
        ).pack(anchor=tk.W, pady=(0, 10))

        tk.Label(frame, text="Default To Base:", font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        default_to_var = tk.StringVar(value=self.settings.get("default_to_base", "2"))
        ttk.Combobox(
            frame,
            textvariable=default_to_var,
            values=list(self.base_systems.keys()),
            state="readonly",
            width=10
        ).pack(anchor=tk.W, pady=(0, 15))

        # Show conversion process
        show_process_var = tk.BooleanVar(value=self.settings.get("show_process", True))
        show_process_cb = tk.Checkbutton(
            frame,
            text="Show detailed conversion process",
            variable=show_process_var
        )
        show_process_cb.pack(anchor=tk.W, pady=(0, 10))

        # Group digits
        group_digits_var = tk.BooleanVar(value=self.settings.get("group_digits", True))
        group_digits_cb = tk.Checkbutton(
            frame,
            text="Group digits in large numbers (1,234)",
            variable=group_digits_var
        )
        group_digits_cb.pack(anchor=tk.W, pady=(0, 20))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        def save_preferences():
            try:
                self.settings["auto_save_history"] = auto_save_var.get()
                self.settings["max_history_entries"] = int(max_entries_var.get())
                self.settings["default_from_base"] = default_from_var.get()
                self.settings["default_to_base"] = default_to_var.get()
                self.settings["show_process"] = show_process_var.get()
                self.settings["group_digits"] = group_digits_var.get()

                self.save_settings()

                # Apply new defaults
                self.from_base.set(default_from_var.get())
                self.to_base.set(default_to_var.get())
                self.on_from_base_change()
                self.on_to_base_change()

                pref_window.destroy()
                messagebox.showinfo("Success", "Preferences saved successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")

        tk.Button(
            btn_frame,
            text="Save",
            command=save_preferences,
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 10)
        ).pack(side=tk.RIGHT, padx=(10, 0))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=pref_window.destroy,
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            font=("Arial", 10)
        ).pack(side=tk.RIGHT)

    def show_about(self):
        """Show about dialog"""
        about_text = """Professional Number System Converter v2.0

A comprehensive number base conversion tool with advanced features.

Features:
• Multi-base number conversion (2-36 bases)
• Batch conversion capabilities
• Multi-base calculator
• IEEE 754 floating point converter
• Programming tools (Two's complement, bitwise operations)
• Educational content about number systems
• Conversion history tracking
• Professional user interface

Author: Your Name
© 2025 All Rights Reserved

Built with Python and tkinter
Advanced mathematical algorithms included

Version: 2.0.0
Build Date: January 2025"""

        messagebox.showinfo("About Professional Number System Converter", about_text)

    def run(self):
        """Start the application"""
        # Set default bases from settings
        self.from_base.set(self.settings.get("default_from_base", "10"))
        self.to_base.set(self.settings.get("default_to_base", "2"))

        # Update UI
        self.on_from_base_change()
        self.on_to_base_change()
        self.update_history_display()
        self.show_educational_content()

        # Start the main loop
        self.root.mainloop()


if __name__ == "__main__":
    app = NumberSystemConverter()
    app.run()
