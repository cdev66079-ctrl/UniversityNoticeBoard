# ============================================================
# UNIVERSITY NOTICE BOARD - THEME
# ============================================================

import customtkinter as ctk


class Theme:

    # ========================================================
    # LIGHT MODE COLORS
    # ========================================================

    LIGHT = {
        "app_bg": "#E8D5B7",
        "header": "#3B2415",
        "header_text": "#FFF4D6",

        "board": "#A66D3F",
        "board_outer": "#8A5A32",
        "board_border": "#4A2C19",

        "card": "#FFF8DC",
        "card_border": "#D2B98B",

        "text": "#332215",
        "text_secondary": "#765432",
        "text_muted": "#777777",

        "input_bg": "#FFFDF5",

        "button": "#6B4226",
        "button_hover": "#8A5A32",

        "danger": "#B22222",
        "danger_hover": "#8B0000",

        "comment_bg": "#F5EBD0",
        "comment_card": "#FFFDF5"
    }

    # ========================================================
    # DARK MODE COLORS
    # ========================================================

    DARK = {
        "app_bg": "#181512",
        "header": "#0F0D0B",
        "header_text": "#F5E6C8",

        "board": "#2A211B",
        "board_outer": "#211A15",
        "board_border": "#3D3026",

        "card": "#29231E",
        "card_border": "#4A3B2F",

        "text": "#F5F0E8",
        "text_secondary": "#D1BFA5",
        "text_muted": "#A9A29A",

        "input_bg": "#241F1A",

        "button": "#6B4226",
        "button_hover": "#8A5A32",

        "danger": "#9E3028",
        "danger_hover": "#C0392B",

        "comment_bg": "#211C18",
        "comment_card": "#2B2520"
    }

    # ========================================================
    # CURRENT MODE
    # ========================================================

    @staticmethod
    def get():

        if ctk.get_appearance_mode() == "Dark":
            return Theme.DARK

        return Theme.LIGHT

    # ========================================================
    # SET DARK MODE
    # ========================================================

    @staticmethod
    def set_dark():

        ctk.set_appearance_mode("Dark")

    # ========================================================
    # SET LIGHT MODE
    # ========================================================

    @staticmethod
    def set_light():

        ctk.set_appearance_mode("Light")

    # ========================================================
    # TOGGLE
    # ========================================================

    @staticmethod
    def toggle():

        if ctk.get_appearance_mode() == "Dark":

            ctk.set_appearance_mode("Light")

            return "Light"

        else:

            ctk.set_appearance_mode("Dark")

            return "Dark"

    # ========================================================
    # IS DARK?
    # ========================================================

    @staticmethod
    def is_dark():

        return ctk.get_appearance_mode() == "Dark"

    # ========================================================
    # GET COLOR
    # ========================================================

    @staticmethod
    def color(name):

        theme = Theme.get()

        return theme.get(
            name,
            "#FFFFFF"
        )