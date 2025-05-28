# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:52:40 2025

@author: user
add :
    - Added split option
    - Added double down option
    - Added natural blackjack detection
    - Improved user prompts and error handling
    - Added shoe management to shuffle when low
    - Improved scoring 
    - Added multiple hands support (6 hands)
 
"""

import random

def creer_paquet(nb_paquets=6):
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    couleurs = ['♠', '♥', '♦', '♣']
    paquet = [val + couleur for val in valeurs for couleur in couleurs] * nb_paquets
    random.shuffle(paquet)
    return paquet

def valeur_carte(carte):
    val = carte[:-1]
    if val in ['J', 'Q', 'K']:
        return 10
    elif val == 'A':
        return 11
    return int(val)

def nom_carte(carte):
    return carte[:-1]

def calculer_score(main):
    score = 0
    nb_as = 0
    for carte in main:
        v = valeur_carte(carte)
        score += v
        if nom_carte(carte) == 'A':
            nb_as += 1
    while score > 21 and nb_as > 0:
        score -= 10
        nb_as -= 1
    return score

def est_blackjack_naturel(main):
    return len(main) == 2 and calculer_score(main) == 21

def afficher_main(joueur, main):
    print(f"{joueur} has: {', '.join(main)} (score: {calculer_score(main)})\n")

def tirer_carte(paquet):
    if not paquet:
        raise Exception("The shoe is empty!")
    return paquet.pop()

def demander_mise(solde):
    while True:
        try:
            mise = int(input(f"Your balance is ${solde}.\nEnter your bet: "))
            if 1 <= mise <= solde:
                print()
                return mise
            print("❌ Invalid bet.\n")
        except ValueError:
            print("❌ Please enter a valid integer.\n")

def proposer_split(main, solde, mise):
    if nom_carte(main[0]) == nom_carte(main[1]) and solde >= mise * 2:
        while True:
            choix = input(f"🃏 You have a pair of {nom_carte(main[0])}. Do you want to split? (y/n): ").lower()
            if choix in ['y', 'n']:
                return choix == 'y'
            print("❌ Please enter y or n.\n")
    return False

def proposer_action_initiale(main, solde, mise):
    if len(main) == 2:
        options = ['h', 's']
        if solde >= mise:
            options.insert(0, 'd')
        while True:
            choix = input("Choose an action - (d) Double, (h) Hit, (s) Stand: ").lower()
            if choix in options:
                return choix
            print("❌ Invalid choice.\n")
    return 'h'

def jouer_main_avec_options(paquet, main, solde, mise):
    mise_initiale = mise
    choix = proposer_action_initiale(main, solde, mise)
    if choix == 'd':
        solde -= mise
        mise *= 2
        main.append(tirer_carte(paquet))
        afficher_main("You", main)
    elif choix == 'h':
        while calculer_score(main) < 21:
            main.append(tirer_carte(paquet))
            afficher_main("You", main)
            if calculer_score(main) >= 21:
                break
            if input("Draw another card? (y/n): ").lower() != 'y':
                break
    return main, mise, solde

def resoudre_mains_multiples(mains_mises, score_banque):
    total = 0
    for i, (main, mise) in enumerate(mains_mises):
        score = calculer_score(main)
        print(f"🧾 Result for hand {i+1}: {score}")
        if score > 21:
            print("💥 You lost this hand.")
            total -= mise
        elif score_banque > 21 or score > score_banque:
            print("🎉 You win this hand!")
            total += mise
        elif score == score_banque:
            print("🤝 It's a tie on this hand.")
        else:
            print("❌ You lose this hand.")
            total -= mise
        print()
    print(f"💰 Result this round: {total:+} $\n")
    return total

def jouer(solde, paquet):
    if len(paquet) < 60:
        print("🔄 Shoe is low. Shuffling a new one...\n")
        paquet.clear()
        paquet.extend(creer_paquet())

    mise = demander_mise(solde)
    mise_initiale = mise
    solde -= mise

    main_joueur = [tirer_carte(paquet), tirer_carte(paquet)]
    main_banque = [tirer_carte(paquet), tirer_carte(paquet)]

    afficher_main("You", main_joueur)
    print(f"Dealer has: {main_banque[0]}, [hidden card]\n")

    if proposer_split(main_joueur, solde, mise):
        solde -= mise
        main1 = [main_joueur[0], tirer_carte(paquet)]
        main2 = [main_joueur[1], tirer_carte(paquet)]

        print("\n▶️ Hand 1:")
        afficher_main("You", main1)
        main1, mise1, solde = jouer_main_avec_options(paquet, main1, solde, mise)

        print("\n▶️ Hand 2:")
        afficher_main("You", main2)
        main2, mise2, solde = jouer_main_avec_options(paquet, main2, solde, mise)

        print("Dealer's turn...\n")
        while calculer_score(main_banque) < 17:
            main_banque.append(tirer_carte(paquet))
        afficher_main("Dealer", main_banque)

        score_banque = calculer_score(main_banque)
        gain = resoudre_mains_multiples([(main1, mise1), (main2, mise2)], score_banque)
        return max(0, solde + gain)

    if est_blackjack_naturel(main_joueur):
        gain = int(mise * 1.5)
        print("🎯 BLACKJACK! You win 1.5× your bet 🎉\n")
        print(f"💰 Result this round: +{gain} $\n")
        return max(0, solde + mise + gain)

    main_joueur, mise, solde = jouer_main_avec_options(paquet, main_joueur, solde, mise)
    score_joueur = calculer_score(main_joueur)

    print("Dealer's turn...\n")
    while calculer_score(main_banque) < 17:
        main_banque.append(tirer_carte(paquet))
    afficher_main("Dealer", main_banque)
    score_banque = calculer_score(main_banque)

    if score_joueur > 21:
        print("💥 You busted! You lose your bet.\n")
        print(f"💰 Result this round: -{mise} $\n")
        return max(0, solde)
    elif score_banque > 21 or score_joueur > score_banque:
        print("🎉 You win!\n")
        print(f"💰 Result this round: +{mise} $\n")
        return max(0, solde + mise * 2)
    elif score_joueur == score_banque:
        print("🤝 It's a tie. Your bet is returned.\n")
        print("💰 Result this round: +0 $\n")
        return max(0, solde + mise)
    else:
        print("❌ Dealer wins. You lose your bet.\n")
        print(f"💰 Result this round: -{mise} $\n")
        return max(0, solde)

def main():
    solde = 100
    paquet = creer_paquet()
    print("==== Welcome to Blackjack 💰 ====")
    print("- Dealer must stand on all 17s - \n")
    while solde > 0:
        solde = jouer(solde, paquet)
        print(f"💰 Current balance: {solde} $\n")
        if solde <= 0:
            print("🪦 You're broke. Game over.\n")
            break
        if input("Do you want to play again? (y/n): ").lower() != 'y':
            print("\nThanks for playing! 👋\n")
            break

if __name__ == "__main__":
    main()
