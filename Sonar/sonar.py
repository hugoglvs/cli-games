import random

LARGEUR = 60
HAUTEUR = 15
NB_COFFRES = 3
NB_SONARS = 20

def afficher_instructions():
    print("""
=== 📡 SONAR GAME INSTRUCTIONS ===
Three treasure chests are hidden under the ocean.
The ocean is a 60-column by 15-row grid.
You have 20 sonar devices to find them.

On each turn, enter coordinates (x y).
You’ll get a signal:
- 🔊 Strong: a chest is within 1–2 tiles (Manhattan distance)
- 🔉 Normal: a chest is 3 tiles away
- 🔈 Weak: a chest is 4 tiles away
- 🔇 None: no chest nearby

Type 'help' or 'instructions' at any time to see this message again.
Good luck!
""")

def creer_grille():
    return [['~' for _ in range(LARGEUR)] for _ in range(HAUTEUR)]

def afficher_grille(grille):
    print("   " + "".join([str(x // 10) if x % 10 == 0 else " " for x in range(LARGEUR)]))
    print("   " + "".join([str(x % 10) for x in range(LARGEUR)]))
    for y in range(HAUTEUR):
        ligne = "".join(grille[y])
        print(f"{y:2} {ligne}")

def generer_coffres():
    return random.sample([(x, y) for x in range(LARGEUR) for y in range(HAUTEUR)], NB_COFFRES)

def distance_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def evaluer_signal(x, y, coffres_restants):
    distances = [distance_manhattan(x, y, cx, cy) for cx, cy in coffres_restants]
    if not distances:
        return "🔇 No signal"
    min_dist = min(distances)
    if min_dist <= 2:
        return "🔊 Strong signal"
    elif min_dist == 3:
        return "🔉 Normal signal"
    elif min_dist == 4:
        return "🔈 Weak signal"
    else:
        return "🔇 No signal"

def jouer():
    grille = creer_grille()
    coffres = generer_coffres()
    # print(f"🔍 [DEBUG] Chests located at: {coffres}")  # Ligne de test
    coffres_trouves = []
    essais_restants = NB_SONARS
    deja_joues = set()

    afficher_instructions()
    while essais_restants > 0 and len(coffres_trouves) < NB_COFFRES:
        afficher_grille(grille)
        print(f"\n📡 Sonars left: {essais_restants} | Chests found: {len(coffres_trouves)}/{NB_COFFRES}")

        saisie = input("Enter coordinates x y (or 'help'): ").strip()
        if saisie.lower() in ['help', 'instructions']:
            afficher_instructions()
            continue

        try:
            x, y = map(int, saisie.split())
            if not (0 <= x < LARGEUR and 0 <= y < HAUTEUR):
                print("❌ Coordinates out of bounds.")
                continue
        except ValueError:
            print("❌ Invalid input. Format: x y")
            continue

        if (x, y) in deja_joues:
            print("📍 You've already placed a sonar here. Choose another spot.")
            continue

        deja_joues.add((x, y))

        if (x, y) in coffres:
            print("🎉 You found a treasure chest!")
            coffres_trouves.append((x, y))
            coffres.remove((x, y))
            grille[y][x] = 'X'
        else:
            signal = evaluer_signal(x, y, coffres)
            print(f"📍 At ({x}, {y}): {signal}")
            grille[y][x] = signal[2]

        essais_restants -= 1

    afficher_grille(grille)
    if len(coffres_trouves) == NB_COFFRES:
        print("\n🏆 Congratulations! You found all the treasure chests!")
    else:
        print("\n⛔ Game over. You missed the remaining chests.")
        print("📍 They were at: " + ", ".join(f"({x},{y})" for x, y in coffres))

if __name__ == "__main__":
    jouer()
