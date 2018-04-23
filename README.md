# FakeReviewsProject #

## ToDo List ##
- [x] Scraping dettagli prodotto
- [x] Scraping di tutte le recensioni per un prodotto
- [x] Scraping dei customer
- - [x] rank, voti utili, totale recensioni fatte, ultime 50 recensioni

- [x] Analisi feature della recensione:
- - [x] recensioni per date
- - [x] recensioni per utente
- - [x] discostamento dalla media delle recensioni
- - [x] acquisto verificato o meno
- - [x] voti di utilità per la recensione
- - [x] analisi trigrammi del testo delle recensioni
- - [x] se "Recensione Vine"
- - [x] conteggio parole delle review
- - - [x] analisi sulla media delle parole usate sulla base del fatto che per unafake reviews (si immagina) non ci si perda molto tempo
- - - [x] analisi congiunta del numero di parole superiore alla media su recensioni che contengono trigrammi ripetuti. potrebbero essere copie di altre recensioni, e quindi probabili fake
- - [x] affidabilità del recensore basata su:
- - - [x] posizione in classifica (rank) - score valutato sulla base dei voti utili e totale recensioni scritte
- - - [x] analisi dei trigrammi delle ultime recensioni pubblicate (ultime 10 ad esempio) per controllare se contengono tutte testo simile
- - - [x] se risulta essere un "easy grader", ovvero se per le sue ultime recensioni pubblicate almeno una percentuale (ad esempio il 50%) sono a 5 stelle
- - - [x] se risulta essere un "one time reviewer", ovvero se per le sue ultime recensioni pubblicate una percentuale (ad esempio il 50%) sono state realizzate tutte nello stesso giorno

- [x] Analisi di eventuali correlazioni tra le feature (coefficiente di Pearson)
- - [x] risultati su file ".xls" per analisi. osservazioni studiate e trascritte

- [x] Anomaly detection
- - [x] clustering
- - [x] isolation forest
- - [x] svm

