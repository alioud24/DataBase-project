import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect( 
            host="localhost",
            user="root",
            password="M@estro99",
            database="gestion_notes"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion: {err}")
        return None

def ajouter_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            
            # Vérifier si l'identifiant est déjà utilisé par un autre étudiant
            query_verification_identifiant = "SELECT * FROM liste WHERE identifiant_etudiant = %s"
            cursor.execute(query_verification_identifiant, (identifiant_etudiant,))
            result = cursor.fetchone()

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
                conn.commit()
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
            query = "UPDATE liste SET prenom_etudiant = %s, nom_etudiant = %s, matiere = %s, note = %s WHERE identifiant_etudiant = %s"
            cursor.execute(query, (prenom_etudiant, nom_etudiant, matiere, note, identifiant_etudiant))
            conn.commit()
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
            query = "DELETE FROM liste WHERE identifiant_etudiant = %s"
            cursor.execute(query, (identifiant_etudiant,))
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
            query = "SELECT * FROM liste"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert('', tk.END, values=row)
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
            return[]
        finally:
            cursor.close()
            conn.close()
            
    return[]            
            

  

def ajouter_note():
    identifiant_etudiant = identifiant_entry.get().strip()
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
    if note < 0 or note > 20:
        messagebox.showerror("Erreur", "La note doit être inférieure ou égale à 20.")
        return
      

    ajouter_note_db(identifiant_etudiant, prenom_etudiant, nom_etudiant, matiere, note)
    
    identifiant_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    nom_entry.delete(0, tk.END)
    matiere_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

    messagebox.showinfo("Succès", "Note ajoutée avec succès.")
    charger_notes()

def modifier_note():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Alerte", "Veuillez sélectionner une note à modifier.")
        return
    
    identifiant_etudiant = table.item(selected_item, 'values')[0]
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
    supprimer_note_db(identifiant_etudiant)

    messagebox.showinfo("Succès", "Note supprimée avec succès.")
    charger_notes()

def afficher_toutes_notes():
    charger_notes()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion des Notes des Étudiants")
root.geometry("800x600")
root.config(bg="#f5f5f5")
root.iconbitmap("icone.ico")

label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

title_label = tk.Label(root, text="Gestion des Notes", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10)
title_label.pack(fill="x")

form_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
form_frame.pack(pady=20)

tk.Label(form_frame, text="Identifiant de l'étudiant:", font=label_font, bg="#f5f5f5").grid(row=0, column=0, pady=5, sticky="w")
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

ajouter_button = tk.Button(form_frame, text="Ajouter", font=button_font, bg="#4CAF50", fg="white", padx=10, pady=5, command=ajouter_note)
ajouter_button.grid(row=5, column=0, pady=20)

modifier_button = tk.Button(form_frame, text="Modifier", font=button_font, bg="#FFC107", fg="black", padx=10, pady=5, command=modifier_note)
modifier_button.grid(row=5, column=1, pady=20)

supprimer_button = tk.Button(form_frame, text="Supprimer", font=button_font, bg="#F44336", fg="white", padx=10, pady=5, command=supprimer_note)
supprimer_button.grid(row=5, column=2, pady=20)

#afficher_button = tk.Button(form_frame, text="Afficher Toutes les Notes", font=button_font, bg="#2196F3", fg="white", padx=10, pady=5, command=charger_notes)
# afficher_button.grid(row=5, column=3, pady=20)

table_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
table_frame.pack(fill="both", expand=True)

table = ttk.Treeview(table_frame, columns=("id", "prenom", "nom", "matiere", "note"), show='headings')
table.heading("id", text="Identifiant")
table.heading("prenom", text="Prénom de l'étudiant")
table.heading("nom", text="Nom de l'étudiant")
table.heading("matiere", text="Matière")
table.heading("note", text="Note")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4CAF50", foreground="white")
style.configure("Treeview", font=("Arial", 10), background="#e1e1e1", foreground="black", fieldbackground="#e1e1e1")

table.pack(fill="both", expand=True)

charger_notes()

root.mainloop()
