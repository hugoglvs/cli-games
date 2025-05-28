# -*- coding: utf-8 -*-
"""
Created on Tue May 27 16:45:40 2025

@author: user
add :
 - Added player balance
"""

import random

def creer_paquet():
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    couleurs = ['♠', '♥', '♦', '♣']
    paquet = [val + couleur for val in valeurs for couleur in couleurs]
    random.shuffle(paquet)
    return paquet

def valeur_carte(carte):
    val = carte[:-1]  # e.g., '10♠' → '10'
    if val in ['J', 'Q', 'K']:
        return 10
    elif val == 'A':
        return 11
    else:
        return int(val)

def calculer_score(main):
    score = 0
    nb_as = 0
    for carte in main:
        v = valeur_carte(carte)
        score += v
        if carte[:-1] == 'A':
            nb_as += 1
    while score > 21 and nb_as > 0:
        score -= 10
        nb_as -= 1
    return score

def afficher_main(joueur, main):
    print(f"{joueur} has: {', '.join(main)} (score: {calculer_score(main)})\n")

def tour_banque(paquet):
    main_banque = [tirer_carte(paquet), tirer_carte(paquet)]
    while calculer_score(main_banque) < 17:
        main_banque.append(tirer_carte(paquet))
    return main_banque

def tirer_carte(paquet):
    return paquet.pop()

def demander_mise(solde):
    while True:
        try:
            mise = int(input(f"Your balance is ${solde}.\nEnter your bet: "))
            if 1 <= mise <= solde:
                print()
                return mise
            else:
                print("❌ Invalid bet. It must be between 1 and your current balance.\n")
        except ValueError:
            print("❌ Please enter a valid integer.\n")

def jouer(solde):
    paquet = creer_paquet()
    mise = demander_mise(solde)

    main_joueur = [tirer_carte(paquet), tirer_carte(paquet)]
    afficher_main("You", main_joueur)

    while calculer_score(main_joueur) < 21:
        choix = input("Draw another card? (y/n): ").lower()
        while choix not in ['y', 'n']:
            choix = input("❌ Please enter a valid action (y/n): ").lower()

        if choix == 'y':
            main_joueur.append(tirer_carte(paquet))
            afficher_main("You", main_joueur)
        else:
            break

    score_joueur = calculer_score(main_joueur)
    if score_joueur > 21:
        print("💥 You busted! You lose your bet.\n")
        return solde - mise

    print("Dealer's turn...\n")
    main_banque = tour_banque(paquet)
    afficher_main("Dealer", main_banque)

    score_banque = calculer_score(main_banque)

    if score_banque > 21 or score_joueur > score_banque:
        print("🎉 You win! You double your bet.\n")
        return solde + mise
    elif score_joueur == score_banque:
        print("🤝 It's a tie. Your bet is returned.\n")
        return solde
    else:
        print("❌ Dealer wins. You lose your bet.\n")
        return solde - mise

# Main game loop
def main():
    solde = 100  # Starting balance
    print("=== Welcome to Blackjack 💵 ===\n")
    while solde > 0:
        solde = jouer(solde)
        print(f"💰 Current balance: ${solde}\n")
        if solde <= 0:
            print("🪦 You're broke. Game over.\n")
            break

        while True:
            rejouer = input("Do you want to play again? (y/n): ").lower()
            if rejouer in ['y', 'n']:
                break
            print("❌ Please enter a valid action (y/n).\n")

        if rejouer != 'y':
            print("\nThanks for playing! 👋\n")
            break

if __name__ == "__main__":
    main()
