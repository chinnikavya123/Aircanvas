
import cv2
import mediapipe as mp
import numpy as np
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox, colorchooser
from pathlib import Path
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AirCanvas:

    def __init__(self, root):
        self.root = root
        self.root.title("AirCanvas | Gesture Drawing Studio")
        self.root.geometry("1440x900")
        self.root.minsize(1100, 720)
        self.root.configure(fg_color="#0B1020")

        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )

        self.canvas = None
        self.canvas_alpha = None

        self.previous_point = None
        self.is_drawing = False
        self.active_action = None

        self.current_gesture = "NONE"
        self.candidate_gesture = "NONE"
        self.gesture_frames = 0
        self.required_gesture_frames = 3
        self.hand_detected = False

        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 20

        self.current_color = "#8B5CF6"
        self.current_color_name = "Purple"
        self.brush_size = 7
        self.eraser_size = 35
        self.brush_style = "Marker"
        self.eraser_mode = False

        self.palette_popup = None
        self.color_buttons = {}

        self.favorites = set()

        self.gallery_path = Path.cwd() / "AirCanvas_Gallery"
        self.gallery_path.mkdir(exist_ok=True)

        self.colors = {
            "Black": "#000000",
            "White": "#FFFFFF",
            "Gray": "#808080",
            "Silver": "#C0C0C0",
            "Light Gray": "#D3D3D3",
            "Dark Gray": "#404040",
            "Charcoal": "#36454F",

            "Navy": "#000080",
            "Midnight Blue": "#191970",
            "Royal Blue": "#4169E1",
            "Blue": "#0000FF",
            "Dodger Blue": "#1E90FF",
            "Steel Blue": "#4682B4",
            "Sky Blue": "#87CEEB",
            "Baby Blue": "#89CFF0",
            "Light Blue": "#ADD8E6",
            "Powder Blue": "#B0E0E6",
            "Cyan": "#00FFFF",
            "Turquoise": "#40E0D0",
            "Teal": "#008080",

            "Dark Green": "#006400",
            "Forest Green": "#228B22",
            "Green": "#008000",
            "Emerald": "#50C878",
            "Sea Green": "#2E8B57",
            "Mint": "#98FF98",
            "Pastel Mint": "#C1F0D0",
            "Lime": "#00FF00",
            "Olive": "#808000",
            "Sage": "#B2AC88",

            "Yellow": "#FFFF00",
            "Lemon": "#FFF44F",
            "Pastel Yellow": "#FDFD96",
            "Gold": "#FFD700",
            "Goldenrod": "#DAA520",
            "Mustard": "#FFDB58",
            "Orange": "#FFA500",
            "Dark Orange": "#FF8C00",
            "Coral": "#FF7F50",
            "Peach": "#FFCBA4",
            "Pastel Peach": "#FFE5B4",
            "Apricot": "#FBCEB1",

            "Red": "#FF0000",
            "Dark Red": "#8B0000",
            "Crimson": "#DC143C",
            "Scarlet": "#FF2400",
            "Maroon": "#800000",
            "Burgundy": "#800020",
            "Wine": "#722F37",
            "Salmon": "#FA8072",

            "Pink": "#FFC0CB",
            "Hot Pink": "#FF69B4",
            "Deep Pink": "#FF1493",
            "Pastel Pink": "#FFD1DC",
            "Baby Pink": "#F4C2C2",
            "Rose": "#F4C2C2",
            "Dusty Rose": "#DCAE96",
            "Blush": "#DE5D83",

            "Purple": "#8B5CF6",
            "Dark Purple": "#301934",
            "Violet": "#8F00FF",
            "Lavender": "#E6E6FA",
            "Lilac": "#C8A2C8",
            "Mauve": "#E0B0FF",
            "Orchid": "#DA70D6",
            "Plum": "#DDA0DD",
            "Indigo": "#4B0082",

            "Brown": "#8B4513",
            "Chocolate": "#D2691E",
            "Coffee": "#6F4E37",
            "Mocha": "#967969",
            "Tan": "#D2B48C",
            "Beige": "#F5F5DC",
            "Cream": "#FFFDD0",
            "Ivory": "#FFFFF0",
            "Khaki": "#C3B091",
            "Sand": "#C2B280",

            "Copper": "#B87333",
            "Bronze": "#CD7F32",
            "Rose Gold": "#B76E79",
            "Mint Cream": "#F5FFFA",
            "Alice Blue": "#F0F8FF",
            "Antique White": "#FAEBD7"
        }

        self.backgrounds = {
            "Transparent": None,
            "White": (255, 255, 255),
            "Black": (18, 18, 18),
            "Lavender": (230, 230, 250),
            "Lavender Mist": (245, 240, 255),
            "Cream": (255, 253, 208),
            "Beige": (245, 245, 220),
            "Pastel Pink": (255, 209, 220),
            "Peach": (255, 218, 185),
            "Mint": (189, 252, 201),
            "Sky Blue": (176, 224, 230),
            "Light Gray": (245, 245, 245),
            "Dark Slate": (30, 41, 59),
            "Pale Yellow": (255, 255, 180),
            "Soft Rose": (255, 228, 225)
        }

        self.background_name = "Transparent"

        self.build_ui()
        self.setup_shortcuts()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.after(20, self.update_frame)

    # --------------------------------------------------
    # MAIN UI
    # --------------------------------------------------

    def build_ui(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            self.root,
            height=76,
            corner_radius=0,
            fg_color="#111A2E"
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text="✦  AIR CANVAS",
            font=("Segoe UI", 25, "bold"),
            text_color="#A78BFA"
        ).pack(side="left", padx=30, pady=18)

        ctk.CTkLabel(
            header,
            text="GESTURE DRAWING STUDIO",
            font=("Segoe UI", 11, "bold"),
            text_color="#8492AA"
        ).pack(side="left", padx=12)

        self.header_status = ctk.CTkLabel(
            header,
            text="● INITIALIZING CAMERA",
            font=("Segoe UI", 12, "bold"),
            text_color="#FACC15"
        )
        self.header_status.pack(side="right", padx=30)

        sidebar = ctk.CTkScrollableFrame(
            self.root,
            width=265,
            corner_radius=0,
            fg_color="#111A2E",
            scrollbar_button_color="#475569"
        )
        sidebar.grid(row=1, column=0, sticky="nsew", padx=(0, 2))

        def section(text, top=22):
            ctk.CTkLabel(
                sidebar,
                text=text,
                font=("Segoe UI", 12, "bold"),
                text_color="#8492AA"
            ).pack(anchor="w", padx=18, pady=(top, 10))

        # Gesture controls
        section("GESTURE CONTROLS", 18)

        ctk.CTkButton(
            sidebar,
            text="✋  View Gesture Guide",
            height=40,
            fg_color="#49327E",
            hover_color="#6244A5",
            command=self.show_gesture_guide
        ).pack(fill="x", padx=14, pady=4)

        # Drawing tools
        section("DRAWING TOOLS", 20)

        self.draw_button = ctk.CTkButton(
            sidebar,
            text="✎   Brush Mode",
            height=40,
            anchor="w",
            fg_color="#49327E",
            hover_color="#49327E",
            command=self.select_brush
        )
        self.draw_button.pack(fill="x", padx=14, pady=4)

        self.eraser_button = ctk.CTkButton(
            sidebar,
            text="⌫   Eraser Mode",
            height=40,
            anchor="w",
            fg_color="#1D2940",
            hover_color="#33415C",
            command=self.select_eraser
        )
        self.eraser_button.pack(fill="x", padx=14, pady=4)

        # Brush style
        section("BRUSH STYLE", 20)

        self.style_menu = ctk.CTkOptionMenu(
            sidebar,
            values=["Marker", "Pencil", "Neon"],
            command=self.change_brush_style,
            fg_color="#31245C",
            button_color="#49327E",
            button_hover_color="#6244A5",
            dropdown_fg_color="#1D2940"
        )
        self.style_menu.set("Marker")
        self.style_menu.pack(fill="x", padx=14, pady=4)

        # Colour settings
        section("COLOUR SETTINGS", 20)

        self.color_label = ctk.CTkLabel(
            sidebar,
            text="Selected: Purple",
            font=("Segoe UI", 12, "bold"),
            text_color="#C4B5FD"
        )
        self.color_label.pack(anchor="w", padx=17, pady=(2, 8))

        self.palette_button = ctk.CTkButton(
            sidebar,
            text="🎨  Select Colour  ＋",
            height=42,
            fg_color="#49327E",
            hover_color="#6244A5",
            command=self.toggle_palette
        )
        self.palette_button.pack(fill="x", padx=14, pady=4)

        # Favourite colours - reduced spacing
        section("FAVORITE COLORS", 10)

        self.favorite_frame = ctk.CTkFrame(
            sidebar,
            fg_color="transparent",
            height=1
        )
        self.favorite_frame.pack(
            fill="x",
            padx=12,
            pady=0
        )

        self.favorite_button = ctk.CTkButton(
            sidebar,
            text="☆  Add to Favorites",
            height=35,
            fg_color="#1D2940",
            hover_color="#33415C",
            command=self.toggle_favorite
        )
        self.favorite_button.pack(
            fill="x",
            padx=14,
            pady=(3, 0)
        )

        # Brush size - reduced top spacing
        section("BRUSH SIZE", 10)

        self.brush_value = ctk.CTkLabel(
            sidebar,
            text="7 px",
            text_color="#A78BFA"
        )
        self.brush_value.pack(anchor="e", padx=18)

        self.brush_slider = ctk.CTkSlider(
            sidebar,
            from_=2,
            to=30,
            number_of_steps=28,
            command=self.change_brush_size,
            progress_color="#8B5CF6",
            button_color="#A78BFA"
        )
        self.brush_slider.set(7)
        self.brush_slider.pack(
            fill="x",
            padx=17,
            pady=(3, 10)
        )

        # Eraser size
        section("ERASER SIZE", 14)

        self.eraser_value = ctk.CTkLabel(
            sidebar,
            text="35 px",
            text_color="#FCA5A5"
        )
        self.eraser_value.pack(anchor="e", padx=18)

        self.eraser_slider = ctk.CTkSlider(
            sidebar,
            from_=10,
            to=80,
            number_of_steps=70,
            command=self.change_eraser_size,
            progress_color="#EF4444",
            button_color="#FCA5A5"
        )
        self.eraser_slider.set(35)
        self.eraser_slider.pack(
            fill="x",
            padx=17,
            pady=(3, 10)
        )

        # Artwork background
        section("ARTWORK BACKGROUND", 18)

        self.background_menu = ctk.CTkOptionMenu(
            sidebar,
            values=list(self.backgrounds.keys()),
            command=self.change_background,
            fg_color="#31245C",
            button_color="#49327E",
            button_hover_color="#6244A5",
            dropdown_fg_color="#1D2940"
        )
        self.background_menu.set("Transparent")
        self.background_menu.pack(fill="x", padx=14, pady=4)

        ctk.CTkLabel(
            sidebar,
            text="Background is applied when exporting.",
            font=("Segoe UI", 9),
            text_color="#64748B",
            wraplength=220
        ).pack(anchor="w", padx=17, pady=4)

        # Canvas actions
        section("CANVAS ACTIONS", 20)

        ctk.CTkButton(
            sidebar,
            text="↶   Undo",
            height=37,
            fg_color="#1D2940",
            hover_color="#33415C",
            command=self.undo
        ).pack(fill="x", padx=14, pady=3)

        ctk.CTkButton(
            sidebar,
            text="↷   Redo",
            height=37,
            fg_color="#1D2940",
            hover_color="#33415C",
            command=self.redo
        ).pack(fill="x", padx=14, pady=3)

        ctk.CTkButton(
            sidebar,
            text="✕   Clear Canvas",
            height=37,
            fg_color="#7F2639",
            hover_color="#A8324B",
            command=self.clear_canvas
        ).pack(fill="x", padx=14, pady=3)

        ctk.CTkButton(
            sidebar,
            text="↓   Save Artwork",
            height=40,
            fg_color="#6D4AFF",
            hover_color="#805FFF",
            command=self.save_artwork
        ).pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkButton(
            sidebar,
            text="▣   Open Gallery Folder",
            height=37,
            fg_color="#1D2940",
            hover_color="#33415C",
            command=self.open_gallery
        ).pack(fill="x", padx=14, pady=4)

        ctk.CTkLabel(
            sidebar,
            text="AIR CANVAS v4.0\nDraw naturally. Create freely.",
            font=("Segoe UI", 10),
            text_color="#64748B",
            justify="left"
        ).pack(anchor="w", padx=17, pady=22)

        # Main workspace
        workspace = ctk.CTkFrame(
            self.root,
            fg_color="#0B1020",
            corner_radius=0
        )
        workspace.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=22,
            pady=20
        )

        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(
            workspace,
            fg_color="transparent"
        )
        top.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            top,
            text="Creative Workspace",
            font=("Segoe UI", 23, "bold"),
            text_color="#F1F5F9"
        ).pack(side="left")

        self.mode_label = ctk.CTkLabel(
            top,
            text="BRUSH ACTIVE",
            font=("Segoe UI", 11, "bold"),
            text_color="#A78BFA",
            fg_color="#241C42",
            corner_radius=10
        )
        self.mode_label.pack(side="right", padx=5, pady=5)

        video_card = ctk.CTkFrame(
            workspace,
            fg_color="#111A2E",
            corner_radius=18,
            border_width=1,
            border_color="#263650"
        )
        video_card.grid(row=1, column=0, sticky="nsew")
        video_card.grid_columnconfigure(0, weight=1)
        video_card.grid_rowconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(
            video_card,
            text="Starting webcam...",
            text_color="#94A3B8",
            font=("Segoe UI", 16)
        )
        self.video_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # Status bar
        bottom = ctk.CTkFrame(
            workspace,
            fg_color="#111A2E",
            corner_radius=12,
            height=72
        )
        bottom.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        bottom.grid_propagate(False)

        self.hand_status = ctk.CTkLabel(
            bottom,
            text="● Hand not detected",
            font=("Segoe UI", 12),
            text_color="#F87171"
        )
        self.hand_status.pack(side="left", padx=17, pady=20)

        self.gesture_status = ctk.CTkLabel(
            bottom,
            text="Gesture: Waiting",
            font=("Segoe UI", 12),
            text_color="#A5B4FC"
        )
        self.gesture_status.pack(side="left", padx=18)

        ctk.CTkLabel(
            bottom,
            text="Index: Draw  |  Fist: Erase  |  Palm: Pause",
            font=("Segoe UI", 10),
            text_color="#8492AA"
        ).pack(side="right", padx=17)

    # --------------------------------------------------
    # POPUP COLOUR PALETTE
    # --------------------------------------------------

    def toggle_palette(self):

        if self.palette_popup is not None:
            try:
                if self.palette_popup.winfo_exists():
                    self.hide_palette()
                    return
            except Exception:
                self.palette_popup = None

        self.show_palette_popup()

    def show_palette_popup(self):

        popup = ctk.CTkToplevel(self.root)
        self.palette_popup = popup

        popup.withdraw()
        popup.title("Choose a Colour")
        popup.configure(fg_color="#111A2E")
        popup.resizable(False, False)
        popup.transient(self.root)

        popup_width = 350
        popup_height = 465

        self.root.update_idletasks()
        self.palette_button.update_idletasks()

        x = self.palette_button.winfo_rootx()
        y = (
            self.palette_button.winfo_rooty()
            + self.palette_button.winfo_height()
            + 6
        )

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if x + popup_width > screen_width:
            x = screen_width - popup_width - 10

        if y + popup_height > screen_height:
            y = self.palette_button.winfo_rooty() - popup_height - 6

        x = max(5, x)
        y = max(5, y)

        popup.geometry(
            f"{popup_width}x{popup_height}+{x}+{y}"
        )

        heading = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )
        heading.pack(fill="x", padx=14, pady=(12, 6))

        ctk.CTkLabel(
            heading,
            text="Choose a Colour",
            font=("Segoe UI", 17, "bold"),
            text_color="#C4B5FD"
        ).pack(side="left")

        ctk.CTkButton(
            heading,
            text="✕",
            width=30,
            height=28,
            fg_color="#7F2639",
            hover_color="#A8324B",
            command=self.hide_palette
        ).pack(side="right")

        ctk.CTkLabel(
            popup,
            text="Select from the available shades",
            font=("Segoe UI", 10),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        palette_scroll = ctk.CTkScrollableFrame(
            popup,
            fg_color="#172238",
            corner_radius=12,
            width=310,
            height=330,
            scrollbar_button_color="#475569"
        )
        palette_scroll.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        self.color_buttons = {}

        for i, (name, color) in enumerate(self.colors.items()):

            button = ctk.CTkButton(
                palette_scroll,
                text="",
                width=32,
                height=32,
                corner_radius=7,
                fg_color=color,
                hover_color=color,
                border_width=3 if name == self.current_color_name else 1,
                border_color="#FFFFFF" if name == self.current_color_name else "#334155",
                command=lambda c=color, n=name: self.select_color(c, n)
            )

            button.grid(
                row=i // 7,
                column=i % 7,
                padx=5,
                pady=5
            )

            self.color_buttons[name] = button

        ctk.CTkButton(
            popup,
            text="＋  Choose Custom Colour",
            height=38,
            fg_color="#49327E",
            hover_color="#6244A5",
            command=self.choose_custom_color
        ).pack(fill="x", padx=12, pady=(8, 12))

        popup.bind("<Escape>", lambda event: self.hide_palette())

        popup.deiconify()
        popup.lift()
        popup.focus_force()

    def hide_palette(self):

        if self.palette_popup is not None:

            try:
                if self.palette_popup.winfo_exists():
                    self.palette_popup.destroy()
            except Exception:
                pass

            self.palette_popup = None

    # --------------------------------------------------
    # GESTURE GUIDE
    # --------------------------------------------------

 
    def show_gesture_guide(self):

        window = ctk.CTkToplevel(self.root)
        window.title("AirCanvas | Gesture Guide")
        window.geometry("520x620")
        window.resizable(False, False)
        window.configure(fg_color="#111A2E")
        window.transient(self.root)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="✋ AirCanvas Gesture Guide",
            font=("Segoe UI", 22, "bold"),
            text_color="#A78BFA"
        ).pack(pady=(22, 8))

        ctk.CTkLabel(
            window,
            text="Use these hand gestures to control your artwork.",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(pady=(0, 15))

        gestures = [
            (
                "☝",
                "INDEX FINGER — DRAW",
                "Raise your index finger and fold your middle, ring and little fingers. Move your index finger to draw."
            ),
            (
                "✊",
                "CLOSED FIST — ERASE",
                "Close your four fingers into a fist. Move your hand over the drawing to erase."
            ),
            (
                "✋",
                "OPEN PALM — PAUSE",
                "Extend all four fingers. Drawing pauses while your palm remains open."
            ),
            (
                "✌",
                "PEACE SIGN — REPOSITION",
                "Raise your index and middle fingers. No drawing or erasing happens."
            )
        ]

        for symbol, heading, description in gestures:

            card = ctk.CTkFrame(
                window,
                fg_color="#1D2940",
                corner_radius=12
            )
            card.pack(fill="x", padx=20, pady=6)

            ctk.CTkLabel(
                card,
                text=symbol,
                font=("Segoe UI Emoji", 27),
                text_color="#A78BFA",
                width=55
            ).pack(side="left", padx=8)

            content = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            content.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5,
                pady=10
            )

            ctk.CTkLabel(
                content,
                text=heading,
                font=("Segoe UI", 12, "bold"),
                text_color="#E2E8F0"
            ).pack(anchor="w")

            ctk.CTkLabel(
                content,
                text=description,
                font=("Segoe UI", 10),
                text_color="#94A3B8",
                wraplength=340,
                justify="left"
            ).pack(anchor="w", pady=(3, 0))

        ctk.CTkLabel(
            window,
            text="Tip: Keep your hand clearly visible inside the camera frame.",
            font=("Segoe UI", 10),
            text_color="#A78BFA"
        ).pack(pady=(12, 5))

        # Prominent Got it button
        ctk.CTkButton(
            window,
            text="Got it  ✓",
            width=300,
            height=60,
            font=("Segoe UI", 19, "bold"),
            corner_radius=15,
            command=window.destroy,
            fg_color="#7655FF",
            hover_color="#9278FF",
            text_color="#FFFFFF",
            border_width=2,
            border_color="#A997FF"
        ).pack(
            fill="x",
            padx=35,
            pady=(10, 20)
        )


    # --------------------------------------------------
    # SHORTCUTS
    # --------------------------------------------------

    def setup_shortcuts(self):

        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-s>", lambda event: self.save_artwork())
        self.root.bind("<Escape>", lambda event: self.select_brush())

    # --------------------------------------------------
    # DRAWING CONTROLS
    # --------------------------------------------------

    def select_brush(self):

        self.eraser_mode = False

        self.draw_button.configure(fg_color="#49327E")
        self.eraser_button.configure(fg_color="#1D2940")

        self.mode_label.configure(
            text=f"{self.brush_style.upper()} ACTIVE",
            text_color="#A78BFA",
            fg_color="#241C42"
        )

        self.reset_drawing_state()

    def select_eraser(self):

        self.eraser_mode = True

        self.draw_button.configure(fg_color="#1D2940")
        self.eraser_button.configure(fg_color="#49327E")

        self.mode_label.configure(
            text="ERASER ACTIVE",
            text_color="#FCA5A5",
            fg_color="#46212C"
        )

        self.reset_drawing_state()

    def reset_drawing_state(self):

        self.previous_point = None
        self.is_drawing = False
        self.active_action = None

    def change_brush_style(self, style):

        self.brush_style = style

        if not self.eraser_mode:
            self.select_brush()

    def select_color(self, color, name="Custom"):

        self.current_color = color
        self.current_color_name = name

        self.eraser_mode = False
        self.select_brush()

        self.color_label.configure(
            text=f"Selected: {name}"
        )

        self.update_favorite_button()
        self.hide_palette()

    def choose_custom_color(self):

        selected = colorchooser.askcolor(
            color=self.current_color,
            title="Choose Your AirCanvas Color"
        )

        if selected and selected[1]:
            self.select_color(selected[1], "Custom")

    # --------------------------------------------------
    # FAVOURITES
    # --------------------------------------------------

    def toggle_favorite(self):

        color = self.current_color

        if color in self.favorites:
            self.favorites.remove(color)
        else:
            self.favorites.add(color)

        self.update_favorites()
        self.update_favorite_button()

    def update_favorite_button(self):

        if self.current_color in self.favorites:
            self.favorite_button.configure(
                text="★  Remove Favorite"
            )
        else:
            self.favorite_button.configure(
                text="☆  Add to Favorites"
            )

    def update_favorites(self):

        for widget in self.favorite_frame.winfo_children():
            widget.destroy()

        for i, color in enumerate(sorted(self.favorites)):

            button = ctk.CTkButton(
                self.favorite_frame,
                text="",
                width=39,
                height=31,
                fg_color=color,
                hover_color=color,
                border_width=2,
                border_color="#FFFFFF",
                command=lambda c=color: self.select_color(c, "Favorite")
            )

            button.grid(
                row=i // 4,
                column=i % 4,
                padx=4,
                pady=4
            )

    # --------------------------------------------------
    # SIZE AND BACKGROUND
    # --------------------------------------------------

    def change_brush_size(self, value):

        self.brush_size = int(float(value))
        self.brush_value.configure(
            text=f"{self.brush_size} px"
        )

    def change_eraser_size(self, value):

        self.eraser_size = int(float(value))
        self.eraser_value.configure(
            text=f"{self.eraser_size} px"
        )

    def change_background(self, name):

        self.background_name = name

    # --------------------------------------------------
    # UNDO AND REDO
    # --------------------------------------------------

    def get_snapshot(self):

        return (
            self.canvas.copy(),
            self.canvas_alpha.copy()
        )

    def restore_snapshot(self, snapshot):

        self.canvas = snapshot[0].copy()
        self.canvas_alpha = snapshot[1].copy()

    def add_undo(self):

        if self.canvas is not None:

            self.undo_stack.append(self.get_snapshot())

            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)

            self.redo_stack.clear()

    def undo(self):

        if self.canvas is not None and self.undo_stack:

            self.redo_stack.append(self.get_snapshot())

            self.restore_snapshot(
                self.undo_stack.pop()
            )

            self.reset_drawing_state()

    def redo(self):

        if self.canvas is not None and self.redo_stack:

            self.undo_stack.append(self.get_snapshot())

            self.restore_snapshot(
                self.redo_stack.pop()
            )

            self.reset_drawing_state()

    def clear_canvas(self):

        if self.canvas is not None and np.any(self.canvas_alpha):

            self.add_undo()

            self.canvas[:] = 0
            self.canvas_alpha[:] = 0

            self.reset_drawing_state()

    # --------------------------------------------------
    # DRAWING ENGINE
    # --------------------------------------------------

    def get_bgr_color(self):

        r = int(self.current_color[1:3], 16)
        g = int(self.current_color[3:5], 16)
        b = int(self.current_color[5:7], 16)

        return b, g, r

    def draw_stroke(self, point1, point2, erase=None):

        if erase is None:
            erase = self.eraser_mode

        if erase:

            cv2.line(
                self.canvas_alpha,
                point1,
                point2,
                0,
                self.eraser_size,
                cv2.LINE_8
            )

            return

        color = self.get_bgr_color()

        if self.brush_style == "Pencil":
            thickness = max(1, self.brush_size // 2)
            alpha_value = 190

        elif self.brush_style == "Neon":
            thickness = self.brush_size + 7
            alpha_value = 255

        else:
            thickness = self.brush_size
            alpha_value = 255

        cv2.line(
            self.canvas,
            point1,
            point2,
            color,
            thickness,
            cv2.LINE_AA
        )

        cv2.line(
            self.canvas_alpha,
            point1,
            point2,
            alpha_value,
            thickness,
            cv2.LINE_AA
        )

    def create_display_frame(self, frame):

        if not np.any(self.canvas_alpha):
            return frame.copy()

        output = frame.astype(np.float32)
        alpha = self.canvas_alpha.astype(np.float32) / 255.0

        if self.brush_style == "Neon" and not self.eraser_mode:

            glow_color = cv2.GaussianBlur(
                self.canvas.astype(np.float32),
                (0, 0),
                12
            )

            glow_alpha = cv2.GaussianBlur(
                alpha,
                (0, 0),
                12
            )

            glow_alpha = np.clip(
                glow_alpha * 0.75,
                0,
                0.75
            )

            output = (
                output * (1 - glow_alpha[:, :, None])
                + glow_color * glow_alpha[:, :, None]
            )

        color_layer = self.canvas.astype(np.float32)

        if self.brush_style == "Pencil" and not self.eraser_mode:
            alpha = alpha * 0.75

        output = (
            output * (1 - alpha[:, :, None])
            + color_layer * alpha[:, :, None]
        )

        return np.clip(output, 0, 255).astype(np.uint8)

    # --------------------------------------------------
    # SAVE AND GALLERY
    # --------------------------------------------------

    def save_artwork(self):

        if self.canvas is None or not np.any(self.canvas_alpha):

            messagebox.showinfo(
                "AirCanvas",
                "Draw something before saving!"
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialdir=str(self.gallery_path),
            initialfile="AirCanvas_Artwork.png",
            filetypes=[("PNG Image", "*.png")]
        )

        if not file_path:
            return

        alpha = self.canvas_alpha.astype(np.float32) / 255.0

        if self.background_name == "Transparent":

            bgra = cv2.merge([
                self.canvas[:, :, 0],
                self.canvas[:, :, 1],
                self.canvas[:, :, 2],
                self.canvas_alpha
            ])

            success = cv2.imwrite(file_path, bgra)

        else:

            rgb = self.backgrounds[self.background_name]
            background_bgr = tuple(reversed(rgb))

            background = np.full(
                self.canvas.shape,
                background_bgr,
                dtype=np.uint8
            )

            result = (
                self.canvas.astype(np.float32) * alpha[:, :, None]
                + background.astype(np.float32) * (1 - alpha[:, :, None])
            )

            result = np.clip(
                result,
                0,
                255
            ).astype(np.uint8)

            success = cv2.imwrite(file_path, result)

        if success:

            messagebox.showinfo(
                "AirCanvas",
                f"Artwork saved successfully!\n\n{file_path}"
            )

        else:

            messagebox.showerror(
                "AirCanvas",
                "Unable to save artwork."
            )

    def open_gallery(self):

        self.gallery_path.mkdir(exist_ok=True)

        try:
            os.startfile(str(self.gallery_path))

        except Exception as error:

            messagebox.showerror(
                "AirCanvas",
                f"Unable to open gallery:\n{error}"
            )

    # --------------------------------------------------
    # GESTURE RECOGNITION
    # --------------------------------------------------

    def classify_gesture(self, hand):

        landmarks = hand.landmark

        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y
        ring_up = landmarks[16].y < landmarks[14].y
        pinky_up = landmarks[20].y < landmarks[18].y

        if index_up and not middle_up and not ring_up and not pinky_up:
            return "DRAW"

        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "ERASE"

        if index_up and middle_up and ring_up and pinky_up:
            return "PAUSE"

        if index_up and middle_up and not ring_up and not pinky_up:
            return "READY"

        return "NONE"

    def stabilize_gesture(self, gesture):

        if gesture == self.candidate_gesture:
            self.gesture_frames += 1

        else:
            self.candidate_gesture = gesture
            self.gesture_frames = 1

        if self.gesture_frames >= self.required_gesture_frames:
            self.current_gesture = gesture

        return self.current_gesture

    def process_gesture(self, gesture, point):

        if gesture == "DRAW":

            if self.eraser_mode:
                self.select_brush()

            self.gesture_status.configure(
                text="Gesture: Drawing",
                text_color="#4ADE80"
            )

            self.mode_label.configure(
                text="DRAWING",
                text_color="#4ADE80",
                fg_color="#173B32"
            )

            if not self.is_drawing or self.active_action != "DRAW":

                self.add_undo()

                self.is_drawing = True
                self.active_action = "DRAW"
                self.previous_point = point

            else:

                if self.previous_point is not None:
                    self.draw_stroke(
                        self.previous_point,
                        point
                    )

                self.previous_point = point

        elif gesture == "ERASE":

            self.gesture_status.configure(
                text="Gesture: Erasing",
                text_color="#FCA5A5"
            )

            self.mode_label.configure(
                text="GESTURE ERASER",
                text_color="#FCA5A5",
                fg_color="#46212C"
            )

            if not self.is_drawing or self.active_action != "ERASE":

                self.add_undo()

                self.is_drawing = True
                self.active_action = "ERASE"
                self.previous_point = point

            else:

                if self.previous_point is not None:
                    self.draw_stroke(
                        self.previous_point,
                        point,
                        erase=True
                    )

                self.previous_point = point

        elif gesture == "PAUSE":

            self.gesture_status.configure(
                text="Gesture: Paused",
                text_color="#FACC15"
            )

            self.mode_label.configure(
                text="DRAWING PAUSED",
                text_color="#FACC15",
                fg_color="#45391D"
            )

            self.reset_drawing_state()

        elif gesture == "READY":

            self.gesture_status.configure(
                text="Gesture: Ready / Reposition",
                text_color="#A5B4FC"
            )

            self.mode_label.configure(
                text="READY",
                text_color="#A5B4FC",
                fg_color="#241C42"
            )

            self.reset_drawing_state()

        else:

            self.gesture_status.configure(
                text="Gesture: Waiting",
                text_color="#A5B4FC"
            )

            self.reset_drawing_state()

    # --------------------------------------------------
    # WEBCAM
    # --------------------------------------------------

    def update_frame(self):

        if not self.camera.isOpened():

            self.header_status.configure(
                text="● CAMERA NOT AVAILABLE",
                text_color="#F87171"
            )

            self.video_label.configure(
                text="Camera not available. Check your webcam connection."
            )

            return

        success, frame = self.camera.read()

        if not success:
            self.root.after(30, self.update_frame)
            return

        self.header_status.configure(
            text="● CAMERA CONNECTED",
            text_color="#4ADE80"
        )

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        if self.canvas is None:

            self.canvas = np.zeros(
                (height, width, 3),
                dtype=np.uint8
            )

            self.canvas_alpha = np.zeros(
                (height, width),
                dtype=np.uint8
            )

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        self.hand_detected = bool(
            results.multi_hand_landmarks
        )

        if self.hand_detected:

            for hand in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

                index = hand.landmark[8]

                x = int(index.x * width)
                y = int(index.y * height)

                x = max(0, min(width - 1, x))
                y = max(0, min(height - 1, y))

                detected = self.classify_gesture(hand)
                gesture = self.stabilize_gesture(detected)

                self.hand_status.configure(
                    text="● Hand detected",
                    text_color="#4ADE80"
                )

                self.process_gesture(
                    gesture,
                    (x, y)
                )

                if gesture == "DRAW":
                    cursor_color = (0, 255, 0)

                elif gesture == "ERASE":
                    cursor_color = (0, 0, 255)

                elif gesture == "PAUSE":
                    cursor_color = (0, 255, 255)

                else:
                    cursor_color = (255, 255, 255)

                cv2.circle(
                    frame,
                    (x, y),
                    12,
                    cursor_color,
                    2
                )

        else:

            self.hand_status.configure(
                text="● Hand not detected",
                text_color="#F87171"
            )

            self.gesture_status.configure(
                text="Gesture: Waiting",
                text_color="#A5B4FC"
            )

            self.candidate_gesture = "NONE"
            self.gesture_frames = 0
            self.current_gesture = "NONE"

            self.reset_drawing_state()

        output = self.create_display_frame(frame)

        cv2.putText(
            output,
            "AIR CANVAS",
            (22, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        output = cv2.cvtColor(
            output,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(output)

        self.video_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(960, 540)
        )

        self.video_label.configure(
            image=self.video_image,
            text=""
        )

        self.root.after(15, self.update_frame)

    # --------------------------------------------------
    # CLOSE
    # --------------------------------------------------

    def close_app(self):

        self.hide_palette()

        if self.camera is not None:
            self.camera.release()

        if self.hands is not None:
            self.hands.close()

        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":

    root = ctk.CTk()
    app = AirCanvas(root)
    root.mainloop()
