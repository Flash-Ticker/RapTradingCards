import random

class Dice:
    def __init__(self, sides=6):
        """Initialisiert einen Würfel mit der angegebenen Anzahl an Seiten (Standard: 6)."""
        self.sides = sides

    def roll(self):
        """Würfelt eine zufällige Zahl zwischen 1 und der Anzahl der Seiten."""
        return random.randint(1, self.sides)


class DiceGame:
    def __init__(self):
        """Initialisiert das Würfelspiel mit Ergebnissen für Bot und Spieler."""
        self.bot_roll = 0
        self.player_roll = 0
        self.dice = Dice()

    def bot_roll_dice(self):
        """Lässt den Bot würfeln."""
        self.bot_roll = self.dice.roll()
        return self.bot_roll

    def player_roll_dice(self):
        """Lässt den Spieler würfeln."""
        self.player_roll = self.dice.roll()
        return self.player_roll

    def determine_first_turn(self):
        """Vergleicht die Ergebnisse und entscheidet, wer beginnt."""
        if self.bot_roll > self.player_roll:
            return "Bot beginnt!"
        elif self.player_roll > self.bot_roll:
            return "Spieler beginnt!"
        else:
            return "Unentschieden! Würfelt erneut."
