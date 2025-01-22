# RapTradingCard Game

Ein innovatives und spannendes Kartenspiel, bei dem Künstler, ihre Musik und kreative Strategien im Mittelpunkt stehen. Tritt gegen Freunde, Bots oder zufällige Gegner an und stelle dein Können unter Beweis.

## Features

- **Deck-Erstellung**: Stelle dein eigenes Deck aus 5 Artist-Karten zusammen.
- **Dynamische Spieloptionen**:
  - Tritt gegen zufällige Gegner an.
  - Lade Freunde über einen geteilten Link ein.
  - Trainiere gegen einen Bot.
- **Realistische Spielmechanik**: Würfelbasierte Spielzüge, strategischer Einsatz von Spezialkarten und variabler Schaden.
- **Kartenvielfalt**: Jede Karte enthält Attribute wie Style, Flow, Lyric, Beat und Video sowie einzigartige Lebenspunkte.
- **Verzeichnisfunktion**: Durchstöbere Karten deines Lieblingskünstlers und informiere dich über die Attribute.

## Spielbeschreibung und Anforderungen

### Der Anfang

#### Deck-Erstellung
- Spieler wählen ein Deck aus 5 verschiedenen Artist-Karten.
- Falls keine eigenen Karten vorhanden sind, erhält der Spieler 10 zufällige Karten.
- Daraus werden 5 Karten ausgewählt, die ins Spiel mitgenommen werden.

### Die Warteschlange

#### Optionen nach „Spielen“:
1. **Gegner suchen**: Tritt in die Warteschlange ein, um einen zufälligen Gegner zu finden.
2. **Freund einladen**: Erhalte einen Link (teilbar über WhatsApp, Telegram, Discord etc.), um Freunde einzuladen.
3. **Gegen einen Bot spielen**: Perfekt für ein Training.

#### Automatische Umschaltung:
- Wird innerhalb von 3 Minuten kein Gegner gefunden, erscheint die Option: 
  „Genug gewartet? Spiele jetzt gegen einen Bot.“

### Das Spiel

#### Deck und Karten
- Jeder Spieler hat 5 Karten, die nur ihm sichtbar sind.
- Ein Würfel bestimmt den Spielverlauf.

#### Spielstart
1. Beide Spieler würfeln.
2. Die niedrigste Zahl startet.
3. Würfeln eines 6:
   - Der Spieler zieht eine Spezialkarte vom verdeckten Stapel.
4. Beide Spieler wählen eine Startkarte.

#### Spielverlauf
- Spieler würfeln abwechselnd. 
- Würfelzahl aktiviert eine Kartenfähigkeit:
  - **1**: Style
  - **2**: Flow
  - **3**: Lyric
  - **4**: Beat
  - **5**: Video
  - **6**: Spezialkarte ziehen
- Beide Spieler reduziert mit den Fähigkeitspunkten die Lebenspunkte (LP) der gegnerischen Karte.

#### Spezialkarten
- Können gespielt werden, wenn der Spieler am Zug ist (vor odem Würfeln).
- Der Zug endet nach dem Würfeln.

#### Kartenfähigkeiten und Punkte
- Attribute: Style, Flow, Lyric, Beat, Video (KP = Killpunkte).
- Lebenspunkte (LP): Summe aller KP × 2.

### Beispielspiel
- Spieler A: Karte mit 10 KP (LP = 100).
- Spieler B: Karte mit 20 KP (LP = 200).
- Spieler A würfelt eine **2**:
  - B verliert 10 KP (B: 190 LP).
  - A verliert 20 KP (A: 80 LP).

### Kartendetails
- **Name des Künstlers** (Artist).
- **Titel des Songs** (Title).
- **Lebenspunkte (LP)** und **Killpunkte (KP)**: Style, Flow, Lyric, Beat, Video.
- **QR-Codes**:
  - Großer QR-Code: YouTube-Musikvideo.
  - Kleiner QR-Code: Kartenverzeichnis.
- **Seriennummern**:
  - NK: Normale Karte
  - SK: Spezialkarte
  - GK: Glitzerkarte (Holo)
  - BK: Besondere Karte
- **Datum & Vortlaufende Karten Nummer**:

Beispiel: NK-101918<br>
```Normale Karte im Oktober 2019 erstellt. War die 18te karte``` 

## Das Verzeichnis
Im Verzeichnis kannst du nach Karten deines Lieblingskünstlers suchen. Informiere dich über Attribute, Lebenspunkte und Fähigkeiten. Das Verzeichnis bietet zudem Steckbriefe zu allen Karten.

## Installation

### Voraussetzungen
- **Python**: Version 3.7 oder höher
- **MySQL**: Datenbankserver (z. B. via XAMPP)
- **Pip**: Paketmanager für Python

### Schritte

1. **Repository klonen**:
    git clone <repository-url>

2. **Datenbank einrichten:**
Starte XAMPP und Appache. 
Lege die Datenbank an: 
```
INSERT INTO rapcards (artistname, title, style, flow, lyric, beat, video, seriennummer, veroeffentlichung, url)
VALUES ('Artistname', 'Title', '00', '00', '00', '00', '00', '12345', '10/19', 'static/img/rapcards/1.jpg');
CREATE TABLE rapcards (
    id SERIAL PRIMARY KEY,
    artistname VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    style VARCHAR(2) NOT NULL,
    flow VARCHAR(2) NOT NULL,
    lyric VARCHAR(2) NOT NULL,
    beat VARCHAR(2) NOT NULL,
    video VARCHAR(2) NOT NULL,
    seriennummer VARCHAR(20) NOT NULL,
    veroeffentlichung VARCHAR(10) NOT NULL,
    url VARCHAR(255) NOT NULL
);
```

- Fülle außerdem die Config.py aus! Wenn du kein Passwort hast lasse diese Leer

3. **Starte das Projekt**
- Run App.py 

4. **Owner Account**
- Run create_admin.py lege einen admin fest

5. **Datenbank erzeugen**
- Run db_init.py 

## Projekt starten:
- python app.py
- Die Anwendung läuft auf http://127.0.0.1:5000.

## Verwendete Technologien
Python Flask: Backend-Framework
MySQL: Datenbankmanagement
HTML/CSS/JavaScript: Frontend-Design