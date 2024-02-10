"""
Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
"""
from tkinter import Tk, Frame, Button, messagebox, Toplevel, Label, Entry
from tkinter.colorchooser import askcolor


from case import Case
from tableau import Tableau
from bouton_case import BoutonCase
from chrono import Chronometre
from niveau import Niveau
import pygame


class InterfacePartie(Tk):
    def __init__(self):
        """
        Constructeur de la classe InterfacePartie.
        Crée tous les boutons existants dans l'interface, dont ceux qui
        correspondent à des cases
        """
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0, 0)

        self.bind("<Control-q>", self.quitter )
        self.bind("<Control-s>", self.sauvegarder )
        self.bind("<Control-l>", self.charger )
        self.bind("<Control-n>", self.nouvelle_partie )

        self.dimension_rangee = 5
        self.dimension_colonne = 5
        self.nombre_mines = 5

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_niveaux = Button(bouton_frame, text="Niveaux", command=self.conception_niveaux)
        bouton_niveaux.grid(row=0, column=0)
        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie',command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=1)
        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid(row=0, column=2)

        bouton_configuration = Button(bouton_frame, text="Configurer", command=self.configurer)
        bouton_configuration.grid(row=1, column=0)
        bouton_sauvegarder = Button(bouton_frame, text="Sauvegarder", command=self.sauvegarder)
        bouton_sauvegarder.grid(row=1, column=1)
        bouton_charger = Button(bouton_frame, text="Charger", command=self.charger)
        bouton_charger.grid(row=1, column=2)



        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)


        chrono_frame = Frame(self)
        chrono_frame.grid()
        self.chrono = Chronometre(chrono_frame)
        self.chrono.button.invoke()


        self.max_temps = 60
        self.after(1000, self.verifier_temps)


        shorts_label = Label(self, text="Ctrl+Q:quitter Ctrl+s:sauvegarder \n Ctrl+C:charger Ctrl+N:nouvelle partie")
        shorts_label.grid()
        self.ouvrir_partie()

    def verifier_temps(self):
        """
        vérifie le temps maximum s'il est écoulé ou non
        """
        if self.max_temps-1 >= self.chrono.time :
            self.after(1000, self.verifier_temps)
        else:
            self.chrono.toggle()
            for coords in self.tableau_mines.dictionnaire_cases:
                self.tableau_mines.devoilement_en_cascade(coords[0], coords[1])
            self.desactiver_jeu()
            messagebox.showinfo("Fin de la partie", "Temps écoulé")


    def ouvrir_partie(self, dictionnaire_cases=None, activer_jeu=True):
        """
        Redémarre le tableau avec de nouveaux emplacements de mines
        """
        pygame.mixer.init()
        pygame.mixer.music.load("start.mp3")
        pygame.mixer.music.play()

        self.chrono.time = 0
        #print(self.cadre.winfo_children())
        for bouton in self.cadre.winfo_children():
            bouton.destroy()
        self.dictionnaire_boutons = {}
        for i in range(self.dimension_rangee):
            for j in range(self.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton
        self.tableau_mines = Tableau(self.dimension_rangee, self.dimension_colonne, self.nombre_mines)
        if dictionnaire_cases is not None:
            self.tableau_mines.dictionnaire_cases = dictionnaire_cases
            for case in self.tableau_mines.dictionnaire_cases.values():
                if case.est_devoilee:
                    self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1

        try:
            self.max_time_label.destroy()
        except:
            pass
        self.max_time_label = Label(self, text="Temps maximum: "+ str(self.max_temps)+" secondes" )
        self.max_time_label.grid()

        try:
            self.levels_frame.destroy()
        except:
            pass
        self.levels_frame = Frame(self)
        f = open("niveaux.txt", "r")
        for ligne in f.readlines()[1:]:
            niveau = ligne.replace('\n','').split(',')
            params = [int(niveau[1]),int(niveau[2]),int(niveau[3]),int(niveau[4])]
            bouton_niveau = Button(self.levels_frame, text=niveau[0], command = lambda params = params :self.lancer_niveau(params) )
            bouton_niveau.grid()
        self.levels_frame.grid()

        if activer_jeu:
            self.activer_jeu()
        else:
            self.desactiver_jeu()
        self.redessiner()


    def redessiner(self):
        """
        Affiche l'apparence de tous les boutons en fonction de si ils
        ont été dévoilés. Cette méthode doit être appelée chaque fois que l'état
        du jeu a été modifié.
        """
        for i in range(1, self.tableau_mines.dimension_rangee + 1):
            for j in range(1, self.tableau_mines.dimension_colonne + 1):
                case = self.tableau_mines.obtenir_case(i, j)
                # self.dictionnaire_boutons[(i, j)]['text'] = case.obtenir_apparence()
                apparence = case.obtenir_apparence()
                bouton = self.dictionnaire_boutons[(i, j)]
                bouton['text'] = apparence

                # Change la couleur du bouton en fonction de la valeur du texte
                if apparence == "1":
                    bouton.config(bg="yellow")
                elif apparence == "2":
                    bouton.config(bg="orange")
                elif apparence.isdigit() and int(apparence) >= 3:
                    bouton.config(bg="red")
                else:
                    bouton.config(bg="SystemButtonFace")  # Couleur par défaut

    def personnaliser_couleurs(self):
        # Demander à l'utilisateur de choisir une couleur pour le fond
        couleur_fond = askcolor()[1]
        if couleur_fond:
            self.config(bg=couleur_fond)
            self.cadre.config(bg=couleur_fond)

        # Demander à l'utilisateur de choisir une couleur pour le texte
        couleur_texte = askcolor()[1]
        if couleur_texte:
            for bouton in self.dictionnaire_boutons.values():
                bouton.config(fg=couleur_texte)


    def activer_jeu(self):
        """
        Rend tous les boutons de case cliquables.
        """
        for bouton in self.dictionnaire_boutons.values():
            bouton.activer(self.devoiler_case, self.afficher_drapeau)

    def afficher_drapeau(self,event):
        print("bouton droit cliqué")
        bouton = event.widget
        rangee_x, colonne_y = bouton.rangee_x, bouton.colonne_y
        case = self.tableau_mines.obtenir_case(rangee_x, colonne_y)
        case.marquer()
        self.redessiner()

    def desactiver_jeu(self):
        """
        Rend tous les boutons de case non-cliquables.
        """
        for bouton in self.dictionnaire_boutons.values():
            bouton.desactiver()

    def devoiler_case(self, event):
        """
        Déclenche un dévoilement en cascade à partir de la case cliquée

        Args:
            event (Tkinter.event): L'événement de clic, qui contient le bouton cliqué
                en attribut
        """
        bouton = event.widget
        rangee_x, colonne_y = bouton.rangee_x, bouton.colonne_y
        # TO DO: effectuer un dévoilement en cascade là où se situe le bouton
        self.tableau_mines.devoilement_en_cascade(rangee_x, colonne_y)

        self.detecter_fin(rangee_x, colonne_y)
        self.redessiner()

    def detecter_fin(self, rangee_x, colonne_y):
        """
        Détecte la fin de la partie. Si la partie est terminée,
        un message indiquant s'il s'agit d'une victoire ou d'une défaite est affiché,
        puis les cases sont toutes révélées, et le jeu est désactivé.

        Note: vous pouvez vous inspirer de la classe Partie du TP3 pour savoir
        comment détecter la fin de la partie

        Args:
            rangee_x (int): Numéro de la rangée
            colonne_y (int): Numéro de la colonne
        """
        # TO DO: à compléter
        nombre_cases = 0
        for coords in self.tableau_mines.dictionnaire_cases:
            case = self.tableau_mines.obtenir_case(coords[0], coords[1])
            if case.est_devoilee == False:
                nombre_cases += 1
        #print(nombre_cases)
        case_est_minee = self.tableau_mines.obtenir_case(rangee_x, colonne_y).est_minee
        #print(case_est_minee)
        if nombre_cases == 0 or nombre_cases == self.nombre_mines :
            message = "Félicitations vous avez gagné !!"
            sound_file = "win.mp3"
        elif case_est_minee :
            message = "Désolé vous avez perdu :("
            sound_file = "lose.mp3"
        else:
            message = "???"
        if nombre_cases == 0 or nombre_cases == self.nombre_mines or case_est_minee :
            self.chrono.toggle()
            for coords in self.tableau_mines.dictionnaire_cases:
                self.tableau_mines.devoilement_en_cascade(coords[0], coords[1])
            self.desactiver_jeu()
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            messagebox.showinfo("Fin de la partie", message)


    def nouvelle_partie(self,event=None):
        """
        Ouvre une partie en utilisant la méthode ouvrir_partie avec les arguments par défaut.
        """
        # TO DO: à compléter
        self.ouvrir_partie()

    def configurer(self):
        self.fenetre_configuration = Toplevel(self)
        self.fenetre_configuration.title("Configuration")
        # TO DO: contenu de la fenêtre
        global rangee_entry
        global colonne_entry
        global mines_entry
        global temps_entry

        bouton_personnaliser_couleurs = Button(self.fenetre_configuration, text="Personnaliser les couleurs",command=self.personnaliser_couleurs)
        bouton_personnaliser_couleurs.grid(row=4, column=0)

        rangee_label = Label(self.fenetre_configuration, text="Rangées", pady=1)
        rangee_label.grid(row=1, column=0)

        rangee_entry = Entry(self.fenetre_configuration, width=3)
        rangee_entry.grid(row=1, column=1)

        colonne_label = Label(self.fenetre_configuration, text="Colonnes", pady=10)
        colonne_label.grid(row=1, column=3)

        colonne_entry = Entry(self.fenetre_configuration, width=3)
        colonne_entry.grid(row=1, column=4)

        mines_label = Label(self.fenetre_configuration, text="Mines", pady=10)
        mines_label.grid(row=2, column=0)

        mines_entry = Entry(self.fenetre_configuration, width=3)
        mines_entry.grid(row=2, column=1)

        temps_label = Label(self.fenetre_configuration, text="Temps Max", pady=10)
        temps_label.grid(row=2, column=3)

        temps_entry = Entry(self.fenetre_configuration, width=3)
        temps_entry.grid(row=2, column=4)

        #   Créez des labels, des entrys, et n'oubliez pas de
        #   les placer dans self.fenetre_configuration et de les "grider"
        bouton_ok = Button(self.fenetre_configuration, text="Lancer la nouvelle partie",
                           command=self.lancer_partie_configuree)
        bouton_ok.grid(row=3, column=0)


    def conception_niveaux(self):
        self.fenetre_configuration = Toplevel(self)
        self.fenetre_configuration.title("Conception Niveaux")
        # TO DO: contenu de la fenêtre
        global titre_entry_niveaux
        global rangee_entry_niveaux
        global colonne_entry_niveaux
        global mines_entry_niveaux
        global temps_entry_niveaux

        titre_label_niveaux = Label(self.fenetre_configuration, text="Titre", pady=1)
        titre_label_niveaux.grid(row=1, column=0)

        titre_entry_niveaux = Entry(self.fenetre_configuration, width=20)
        titre_entry_niveaux.grid(row=1, column=1)

        rangee_label_niveaux = Label(self.fenetre_configuration, text="Rangées", pady=1)
        rangee_label_niveaux.grid(row=2, column=0)

        rangee_entry_niveaux = Entry(self.fenetre_configuration, width=3)
        rangee_entry_niveaux.grid(row=2, column=1)

        colonne_label_niveaux = Label(self.fenetre_configuration, text="Colonnes", pady=10)
        colonne_label_niveaux.grid(row=2, column=3)

        colonne_entry_niveaux = Entry(self.fenetre_configuration, width=3)
        colonne_entry_niveaux.grid(row=2, column=4)

        mines_label_niveaux = Label(self.fenetre_configuration, text="Mines", pady=10)
        mines_label_niveaux.grid(row=3, column=0)

        mines_entry_niveaux = Entry(self.fenetre_configuration, width=3)
        mines_entry_niveaux.grid(row=3, column=1)

        temps_label_niveaux = Label(self.fenetre_configuration, text="Temps Max", pady=10)
        temps_label_niveaux.grid(row=3, column=3)

        temps_entry_niveaux = Entry(self.fenetre_configuration, width=3)
        temps_entry_niveaux.grid(row=3, column=4)


        bouton_save = Button(self.fenetre_configuration, text="Sauvegarder",
                           command=self.sauvegarder_niveau)
        bouton_save.grid(row=4, column=0)


        bouton_ok = Button(self.fenetre_configuration, text="Lancer la nouvelle partie",
                           command=self.lancer_niveau )
        bouton_ok.grid(row=4, column=1)

    def lancer_niveau(self,params=None):
        print(params)
        try:
            self.dimension_rangee = params[0]
            self.dimension_colonne = params[1]
            self.nombre_mines = params[2]
            self.max_temps = params[3]
        except:
            self.dimension_rangee = int(rangee_entry_niveaux.get())
            self.dimension_colonne = int(colonne_entry_niveaux.get())
            self.nombre_mines = int(mines_entry_niveaux.get())
            self.max_temps = int(temps_entry_niveaux.get())
        self.redessiner()
        self.ouvrir_partie()
        #self.fenetre_configuration.destroy()

    def lancer_partie_configuree(self):
        # TO DO: obtenir les valeurs dans les Entry
        try:
            self.dimension_rangee = int(rangee_entry.get())
            self.dimension_colonne = int(colonne_entry.get())
            self.nombre_mines = int(mines_entry.get())
            self.max_temps = int(temps_entry.get())

            #   Il faut affecter de nouveaux entiers aux
            #   attributs dimension_rangee, dimension_colonne, nombre_mines
            #   de la classe InterfacePartie.
            #   Note: il n'est pas obligatoire de faire la validation des entrys,
            #   c'est une fonctionnalité facultative.
            self.redessiner()
            self.ouvrir_partie()
            self.fenetre_configuration.destroy()
        except:
            messagebox.showinfo("","Svp entrez des numéros valides")

    def sauvegarder_niveau(self, event=None):
        """
        Sauvegarde le niveau dans un fichier texte nommé 'niveaux.txt'.
        """
        niveau_text =str(titre_entry_niveaux.get()) +","+str(rangee_entry_niveaux.get()) +","+ str(colonne_entry_niveaux.get())+","+ str(mines_entry_niveaux.get())+","+ str(temps_entry_niveaux.get())
        f = open("niveaux.txt", "r")
        niveaux_texte = str(f.read())+"\n"+niveau_text
        print(niveaux_texte)
        text_file = open("niveaux.txt", "w")
        text_file.write(niveaux_texte)
        text_file.close()
        messagebox.showinfo("","Niveau sauvegardé")

    def sauvegarder(self, event=None):
        """
        Sauvegarde la partie en cours dans un fichier texte nommé 'sauvegarde.txt'.
        Se référer à la méthode charger pour connaître le format attendu.
        """
        # TODO: À compléter
        partie_text = ""
        for i in range(1, self.tableau_mines.dimension_rangee + 1):
            for j in range(1, self.tableau_mines.dimension_colonne + 1):
                case_text = ""
                case = self.tableau_mines.obtenir_case(i, j)
                if case.est_devoilee:
                    case_text += "o"
                else:
                    case_text += "n"
                if case.est_minee:
                    case_text += "M"
                else:
                    case_text += str(case.nombre_mines_voisines)
                partie_text += case_text + " "
            partie_text += "\n"

        print(partie_text)

        text_file = open("sauvegarde.txt", "w")
        text_file.write(partie_text)
        text_file.close()



    def charger(self,event=None):
        """
        Charge une partie sauvegardée. Celle-ci doit être stockée dans un fichier nommé
        'sauvegarde.txt' et doit correspondre au format suivant:

        Dans ce fichier, chaque case doit être représentée par deux caractères,
            - un 'o' si la case est dévoilée, un 'n' sinon
            - un 'M' si la case est minée, sinon un entier de 0 à 8
            représentant le nombre de mines voisines

        Les cases d'une même rangée sont séparées par un espace,
        celles sur des rangées différentes par un retour de ligne.

        Exemple (partie 5x5 où l'on a cliqué aux coordonnées 1,3):
        nM o1 o0 o1 n1
        n2 o2 o1 o2 nM
        nM n2 n1 nM n2
        nM n2 n1 n1 n1
        n1 n1 n0 n0 n0
        """
        f = open("sauvegarde.txt", "r")
        x, y_max, n_mines = 0, 1, 0
        dictionnaire_cases = {}
        jeu_en_cours = False
        for ligne in f.readlines():
            x += 1
            y = 0
            rangee = ligne.rstrip().split(" ")
            for str_case in rangee:
                y += 1
                y_max = max(y, y_max)
                case = Case()
                if str_case[0] == "o":
                    case.devoiler()
                else:
                    jeu_en_cours = True
                if str_case[1] == "M":
                    case.ajouter_mine()
                    n_mines += 1
                else:
                    mines_voisines = int(str_case[1])
                    for i in range(mines_voisines):
                        case.ajouter_une_mine_voisine()
                dictionnaire_cases[(x, y)] = case
        f.close()
        self.dimension_rangee = x
        self.dimension_colonne = y_max
        self.nombre_mines = n_mines
        self.ouvrir_partie(dictionnaire_cases, jeu_en_cours)

    def quitter(self,event=None):
        """
        Affiche un message de confirmation, et dans l'affirmative,
        quitte l'interface.

        Vous aurez besoin de messagebox.askyesno et de self.quit.
        """
        # TO DO: à compléter
        reponse = messagebox.askyesno("Validation", "Voulez-vous finir la partie ?")
        if reponse:
            self.destroy()
        else:
            pass
