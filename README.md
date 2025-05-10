Stick-Figure Simulation i Pygame – Udviklet af Jimmi Phan

For at køre programmet skal følgende Python-pakker være installeret:
  - PyGame (hvilket kan installeres med denne kommand: pip install pygame)

Start og Brug
1. Start programmet ved at kører Python filen:
  - python eksamensprojekt.py
2. Programmet kører i fuldskærm.
3. Brug musen for at interagere med programmet f.eks. tandstikfiguren eller knapperne.
  - Klik "Start" for at starte spillet.
  - Klik "Reset" for at genstarte tandstikfiguren position.
  - Klik "Options" for at skifte sværhedgrad.
  - Tryk på tasten "3" for at få koordinaterne af tandstikfiguren.
  - Tryk på tasten "j" og "i" og "m" (på samme tid) for at placere tandstikfiguren på hullets koordinater.
  
4. Tryk på tasten "ESC" for at afslutte programmet.

Test med PyTest
For at sikre, at programmets kernefunktioner fungerer korrekt, bruges PyTest til automatiserede tests. 
For at testene skal følende Python-pakker være installeret:
  - PyTest (hvilket kan installeres med denne kommand: pip install pytest)

Brug of Resultater
1. Skriv i terminalen følgende kommandoprompt (eller 2. for at køre en eneste test):
  - pytest eksamensprojekt.py
  - pytest eksamensprojekt.py-k "test_fit_check_success()"-v
2. Resultaterne skriv i terminalen, når kommandoen udføres.