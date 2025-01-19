import sqlite3

def get_cards():
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cards")  # Beispiel-SQL-Abfrage
    cards = cursor.fetchall()
    connection.close()
    
    # Karten in ein Dictionary umwandeln, falls notwendig
    card_list = []
    for card in cards:
        card_list.append({
            'name': card[0],
            'image': card[1],  # Image URL oder Pfad
            'rarity': card[2],
            'strength': card[3],
            'speed': card[4]
        })
    return card_list
