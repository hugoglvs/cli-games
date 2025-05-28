# -*- coding: utf-8 -*-
"""
Created on Tue May 27 15:51:57 2025

@author: thomasdmg
"""

import random

def creer_paquet():
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    couleurs = ['?', '?', '?', '?']
    paquet = [val + couleur for val in valeurs for couleur in couleurs]
    random.shuffle(paquet)
    return paquet

def valeur_carte(carte):
    val = carte[:-1]  # remove the suit symbol (e.g., '10?' ? '10')
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
        val = carte[:-1]
        if val in ['J', 'Q', 'K']:
            score += 10
        elif val == 'A':
            score += 11
            nb_as += 1
        else:
            score += int(val)

    # Adjust Aces from 11 to 1 if score exceeds 21
    while score > 21 and nb_as > 0:
        score -= 10
        nb_as -= 1

    return score

def afficher_main(joueur, main):
    print(f"{joueur} has: {', '.join(main)} (score: {calculer_score(main)})")

def tour_banque(paquet):
    main_banque = [tirer_carte(paquet), tirer_carte(paquet)]
    while calculer_score(main_banque) < 17:
        main_banque.append(tirer_carte(paquet))
    return main_banque

def tirer_carte(paquet):
    return paquet.pop()

def jouer():
    print(" ")
    print("=== Blackjack ===")
    print("- Dealer Must Stand on all 17's - ")
    print(" ")
    paquet = creer_paquet()

    main_joueur = [tirer_carte(paquet), tirer_carte(paquet)]
    afficher_main("You", main_joueur)

    while calculer_score(main_joueur) < 21:
        choix = input("Draw another card? (y/n): ").lower()
        if choix == 'y':
            main_joueur.append(tirer_carte(paquet))
            afficher_main("You", main_joueur)
        else:
            break

    score_joueur = calculer_score(main_joueur)
    if score_joueur > 21:
        print("?? You busted! You lose.")
        return

    print("\nDealer's turn...")
    main_banque = tour_banque(paquet)
    afficher_main("Dealer", main_banque)

    score_banque = calculer_score(main_banque)
    if score_banque > 21 or score_joueur > score_banque:
        print("?? You win!")
    elif score_joueur == score_banque:
        print("?? It's a tie.")
    else:
        print("? Dealer wins.")

# Start a new game
if __name__ == "__main__":
    while True:
        jouer()
        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            break
