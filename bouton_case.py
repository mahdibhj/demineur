"""
Bouton représentant une case. Le fait de cliquer sur le bouton remplace
les inputs de coordonnées au TP3.
"""

from tkinter import Button


class BoutonCase(Button):
    def __init__(self, parent, rangee_x, colonne_y):
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        super().__init__(parent, text=' ', padx=1, pady=3, height=1, width=2)

    def activer(self, commande, commande_click_droit):
        self["state"] = "normal"
        self.bind('<Button-1>', commande)
        self.bind('<Button-3>', commande_click_droit)

    def desactiver(self):
        self["state"] = "disabled"
        self.unbind("<Button-1>")
