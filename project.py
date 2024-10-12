import tkinter as tk   #Importation du module tkinter pour la création d'interfaces graphiques
from tkinter import ttk  #Importation du module ttk pour des widgets avancés dans tkinter
from tkinter import messagebox #Importation du module messagebox pour afficher des messages pop-up
import mysql.connector #Importation du module mysql.connector pour interagir avec une base de données MySQL

#Fonction pour établir la connexion à la base de données MySQL
def connect_db():
    try:    #On tente de se connecter à la base de données 'gestion_notes' sur le serveur local avec les identifiants fournis
        conn = mysql.connector.connect( 
            host="localhost",
            user="root",
            password="M@estro99",
            database="gestion_notes"
        )
        return conn #Retourne l'objet connexion s'il n'y a pas d'erreurs
    except mysql.connector.Error as err:
         #En cas d'erreur de connexion, affiche l'erreur et retourne None
        print(f"Erreur de connexion: {err}")
        return None #Aucun objet de connexion n'est retourné si une erreur se produit

#Fonction ajouter note
def ajouter_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note):
    conn = connect_db() #Connexion à la base de données
    if conn:  #Si la connexion réussit
        cursor = conn.cursor()  #Création d'un curseur pour exécuter des requêtes SQL
        try:
            
            #On vérifie si l'identifiant est déjà utilisé par un autre étudiant
            query_verification_identifiant = "SELECT * FROM liste WHERE identifiant_etudiant = %s"
            cursor.execute(query_verification_identifiant, (identifiant_etudiant,))
            result = cursor.fetchone() #Récupère la première ligne de résultat

            if result:
                # Si l'identifiant existe déjà, afficher un message d'erreur
                messagebox.showerror("Erreur", f"L'identifiant {identifiant_etudiant} est déjà attribué à un autre étudiant.")
                return  # Sortir immédiatement de la fonction pour éviter toute exécution supplémentaire
            
            # Vérifier si l'étudiant a déjà une note pour cette matière
            query_verification = "SELECT * FROM liste WHERE identifiant_etudiant = %s AND matiere = %s"
            cursor.execute(query_verification, (identifiant_etudiant, matiere))
            result = cursor.fetchone()

            if result:
                # Si une note existe déjà pour cette matière, afficher un message d'erreur  
                messagebox.showerror("Erreur", f"L'étudiant avec l'identifiant {identifiant_etudiant} a déjà une note pour la matière {matiere}.")
                return # Sortir immédiatement de la fonction pour éviter toute exécution supplémentaire
                    
               
            else:
                # Sinon
                query = "INSERT INTO liste (identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note))
                conn.commit() # Enregistrement des données saisies dans la base de données
                print("Note ajoutée avec succès")
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Erreur", "Connexion à la base de données échouée.")        
            

def modifier_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:  
            query = "UPDATE liste SET prenom_etudiant = %s, nom_etudiant = %s, matiere = %s, note = %s WHERE identifiant_etudiant = %s"  #Requête SQL pour mettre à jour les informations de l'étudiant et sa note dans la base de données
            cursor.execute(query, (prenom_etudiant, nom_etudiant, matiere, note, identifiant_etudiant))  #Exécution de la requête avec les nouveaux paramètres (prénom, nom, matière, note) pour l'étudiant correspondant à l'identifiant
            conn.commit()  #Enregistrement des modifications dans la base de données
            print("Note modifiée avec succès")
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
        finally:
            cursor.close()
            conn.close()

def supprimer_note_db(identifiant_etudiant):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM liste WHERE identifiant_etudiant = %s"    #Requête SQL pour supprimer la note d'un étudiant en fonction de son identifiant
            cursor.execute(query, (identifiant_etudiant,))  #Exécution de la requête avec l'identifiant de l'étudiant à supprimer
            conn.commit()
            print("Note supprimée avec succès")
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
        finally:
            cursor.close()
            conn.close()

def charger_notes():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM liste"   #Requête SQL pour récupérer toutes les lignes de la table 'liste'
            cursor.execute(query)   #Exécution de la requête
            rows = cursor.fetchall()   # On récupère toutes les lignes résultant de la requête
            #On supprime toutes les lignes actuellement affichées dans le tableau (table)
            for row in table.get_children():
                table.delete(row)
            #On insère chaque ligne récupérée dans le tableau    
            for row in rows:
                table.insert('', tk.END, values=row)  #On ajoute les lignes dans le tableau
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
            return[]
        finally:
            cursor.close()
            conn.close()
            
    return[]     #En cas de problème de connexion, renvoyer également une liste vide       
            

  

def ajouter_note():
    #Récupération des données entrées par l'utilisateur dans les champs de saisie et les supprimer des espaces inutiles
    identifiant_etudiant = identifiant_entry.get().strip()
    prenom_etudiant = prenom_entry.get().strip()
    nom_etudiant = nom_entry.get().strip()
    matiere = matiere_entry.get().strip()
    note = note_entry.get().strip()

    if not prenom_etudiant or not nom_etudiant or not matiere or not note:      #On vérifie si tous les champs (prénom, nom, matière, et note) sont remplis
        #Si un champ est vide, on affiche un message d'erreur et on sort de la fonction
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    
    try:
        identifiant_etudiant = int(identifiant_etudiant)
    except ValueError:
        messagebox.showerror("Erreur", "L'identifiant doit être un nombre entier.")
        return
    if not prenom_etudiant.isalpha():
        messagebox.showerror("Erreur", "Le prénom doit être une chaîne de caractères.")
        return  
    if not nom_etudiant.isalpha():
        messagebox.showerror("Erreur", "Le nom doit être une chaîne de caractères.")
        return    
    if not matiere.isalpha():
        messagebox.showerror("Erreur", "La matière doit être une chaîne de caractères.")
        return    
    try:
        note = float(note)
    except ValueError:
        messagebox.showerror("Erreur", "La note doit être un nombre.")
        return
    if note < 0 or note > 20:
        messagebox.showerror("Erreur", "La note doit être inférieure ou égale à 20.")
        return
      

    ajouter_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note)  #Appel de la fonction ajouter_note_db pour ajouter les informations de l'étudiant dans la base de données
    
    #On efface le contenu de chaque champ d'entrée après ajout
    identifiant_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    nom_entry.delete(0, tk.END)
    matiere_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

    messagebox.showinfo("Succès", "Note ajoutée avec succès.")  #On affiche une boîte de dialogue indiquant que la note a été ajoutée avec succès
    charger_notes()  #On recharge et affiche les données dans la table après l'ajout de la nouvelle note

def modifier_note():
    selected_item = table.selection()  #On récupère l'élément sélectionné dans la table
    #Si aucun élément n'est sélectionné, on affiche un message d'alerte et arrête l'exécution
    if not selected_item:
        messagebox.showwarning("Alerte", "Veuillez sélectionner une note à modifier.")
        return
    
    identifiant_etudiant = table.item(selected_item, 'values')[0]  #On récupère les valeurs de l'étudiant sélectionné depuis la table
    #On récupère et nettoie les valeurs des champs d'entrée pour le prénom, le nom, la matière et la note
    prenom_etudiant = prenom_entry.get().strip()
    nom_etudiant = nom_entry.get().strip()
    matiere = matiere_entry.get().strip()
    note = note_entry.get().strip()

    if not prenom_etudiant or not nom_etudiant or not matiere or not note:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    
    try:
        identifiant_etudiant = int(identifiant_etudiant)
    except ValueError:
        messagebox.showerror("Erreur", "L'identifiant doit être un nombre entier.")
        return  
    if not prenom_etudiant.isalpha():
        messagebox.showerror("Erreur", "Le prénom doit être une chaîne de caractères.")
        return
    if not nom_etudiant.isalpha():
        messagebox.showerror("Erreur", "Le nom doit être une chaîne de caractères.")
        return    
    if not matiere.isalpha():
        messagebox.showerror("Erreur", "La matière doit être une chaîne de caractères.")
        return 
    try:
        note = float(note)
    except ValueError:
        messagebox.showerror("Erreur", "La note doit être un nombre.")
        return

    modifier_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note)
    
    identifiant_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    nom_entry.delete(0, tk.END)
    matiere_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

    messagebox.showinfo("Succès", "Note modifiée avec succès.")
    charger_notes()

def supprimer_note():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Alerte", "Veuillez sélectionner une note à supprimer.")
        return

    identifiant_etudiant = table.item(selected_item, 'values')[0]
    supprimer_note_db(identifiant_etudiant)   #Appelle la fonction pour supprimer la note de la base de données en utilisant l'identifiant de l'étudiant

    messagebox.showinfo("Succès", "Note supprimée avec succès.")
    charger_notes()

#def afficher_toutes_notes():
    #charger_notes()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion des Notes des Étudiants")  #Définit le titre de la fenêtre
root.geometry("800x600")  #Définit la taille de la fenêtre
root.config(bg="#f5f5f5") #Définit la couleur de fond de la fenêtre
root.iconbitmap("icone.ico")  #Définit l'icône de la fenêtre à partir d'un fichier .ico

label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

title_label = tk.Label(root, text="Gestion des Notes", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10)
title_label.pack(fill="x")

form_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
form_frame.pack(pady=20)

tk.Label(form_frame, text="Identifiant de l'étudiant:", font=label_font, bg="#f5f5f5").grid(row=0, column=0, pady=5, sticky="w")  #Crée une étiquette pour le champ "Identifiant de l'étudiant" avec un style défini
#Crée un champ de saisie pour l'identifiant de l'étudiant
identifiant_entry = tk.Entry(form_frame, font=entry_font, width=25)
identifiant_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Prenom de l'étudiant:", font=label_font, bg="#f5f5f5").grid(row=1, column=0, pady=5, sticky="w")
prenom_entry = tk.Entry(form_frame, font=entry_font, width=25)
prenom_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Nom de l'étudiant:", font=label_font, bg="#f5f5f5").grid(row=2, column=0, pady=5, sticky="w")
nom_entry = tk.Entry(form_frame, font=entry_font, width=25)
nom_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Matière:", font=label_font, bg="#f5f5f5").grid(row=3, column=0, pady=5, sticky="w")
matiere_entry = tk.Entry(form_frame, font=entry_font, width=25)
matiere_entry.grid(row=3, column=1, pady=5)

tk.Label(form_frame, text="Note:", font=label_font, bg="#f5f5f5").grid(row=4, column=0, pady=5, sticky="w")
note_entry = tk.Entry(form_frame, font=entry_font, width=25)
note_entry.grid(row=4, column=1, pady=5)

#Crée un bouton "Ajouter" qui appelle la fonction ajouter_note lorsque cliqué
ajouter_button = tk.Button(form_frame, text="Ajouter", font=button_font, bg="#4CAF50", fg="white", padx=10, pady=5, command=ajouter_note)
ajouter_button.grid(row=5, column=0, pady=20)

modifier_button = tk.Button(form_frame, text="Modifier", font=button_font, bg="#FFC107", fg="black", padx=10, pady=5, command=modifier_note)
modifier_button.grid(row=5, column=1, pady=20)

supprimer_button = tk.Button(form_frame, text="Supprimer", font=button_font, bg="#F44336", fg="white", padx=10, pady=5, command=supprimer_note)
supprimer_button.grid(row=5, column=2, pady=20)

#afficher_button = tk.Button(form_frame, text="Afficher Toutes les Notes", font=button_font, bg="#2196F3", fg="white", padx=10, pady=5, command=charger_notes)
# afficher_button.grid(row=5, column=3, pady=20)

table_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20) #Crée un cadre pour contenir la table avec un fond gris clair et des marges intérieures
table_frame.pack(fill="both", expand=True)  #Place le cadre dans la fenêtre principale, le remplit et l'agrandit si nécessaire
table = ttk.Treeview(table_frame, columns=("id", "prenom", "nom", "matiere", "note"), show='headings') #Crée une table (Treeview) avec des colonnes spécifiées pour afficher les données des étudiants
#Définit les en-têtes des colonnes de la table
table.heading("id", text="Identifiant")
table.heading("prenom", text="Prénom de l'étudiant")
table.heading("nom", text="Nom de l'étudiant")
table.heading("matiere", text="Matière")
table.heading("note", text="Note")

style = ttk.Style()  #Configure le style de la table pour les en-têtes et les lignes
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4CAF50", foreground="white")
style.configure("Treeview", font=("Arial", 10), background="#e1e1e1", foreground="black", fieldbackground="#e1e1e1")

table.pack(fill="both", expand=True)  #Place la table dans le cadre, la remplit et l'agrandit si nécessaire

charger_notes()  #Appelle la fonction pour charger et afficher les notes dans la table

root.mainloop()  #Démarre la boucle principale de l'interface graphique pour afficher la fenêtre
