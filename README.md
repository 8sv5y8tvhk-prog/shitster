# Shitster

Timeline-Musikspiel im Stil von Hitster – als Web-App (PWA) fürs Handy.
Songs laufen als 30-Sekunden-Previews über die Deezer-API, ganz ohne Login und ohne Server.

## Lokal starten

```bash
python3 -m http.server 8765
```

Dann http://localhost:8765 öffnen.

## Aufbau

- `index.html`, `css/app.css`: Oberfläche im iOS-Stil
- `js/game.js`: reine Spiellogik (serialisierbarer State, später für Multiplayer synchronisierbar)
- `js/app.js`: Bildschirme und Ablauf
- `js/deezer.js`: Deezer-API per JSONP; Preview-Links werden bei jedem Abspielen frisch geholt
- `data/*.json`: Kategorien mit geprüften Originaljahren
- `tools/`: Skripte zum Erstellen von Kategorien (Deezer-Suche und Jahresabgleich mit MusicBrainz)

## Neue Kategorie

1. Songs als `Interpret|Titel` in eine Textdatei schreiben.
2. `tools/resolve.py` ausführen. Das Skript sucht die Deezer-IDs und die frühesten Veröffentlichungsjahre.
3. Die Jahre in `tools/build.py` prüfen und dann `data/<kategorie>.json` erzeugen.
