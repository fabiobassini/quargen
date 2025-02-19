# QuarGen CLI

QuarGen è un tool da linea di comando sviluppato per il progetto QuarTrend. Il suo scopo è automatizzare la generazione della struttura di moduli (repository) per il progetto, creando un'architettura modulare standardizzata e facilmente integrabile in sistemi più grandi.

---

## Funzionalità Principali

- **Generazione della Struttura Modulare Completa**
  - **Directory e File di Base:**
    - `config/`: contiene il file `default.py` con le configurazioni (es. porta API, tema UI, abilitazione sockets).
    - `docs/`: include documentazione, con file `installation.md` e `usage.md`.
    - `models/`: suddiviso in:
      - `domain/`: per i modelli di business.
      - `dto/`: per i Data Transfer Object.
    - `controllers/`: suddivisi in:
      - `rest/`: per i controller delle API REST.
      - `web/`: per i controller web (se necessario).
    - `services/`: divisi in:
      - `business/`: per la logica di business.
      - `data/`: per l’accesso ai dati.
    - `utils/`: contiene utility come la classe `ColoredLogger` per il logging a colori.
    - `tests/`: per test unitari e di integrazione.
    - `api/`: implementa il modulo API con blueprint Flask.
    - `ui/`: include:
      - `templates/`: con cartelle `base/` (contenente `base.html`) ed `index/` (contenente `index.html`).
      - `static/`: con sottocartelle `css/`, `js/`, `images/`.
      - `endpoints/`: cartella separata (fuori da `templates/`) per endpoint extra della UI.
    - `sockets/`: per la gestione delle connessioni socket.
    - `interfaces/`: definisce le interfacce base (core, data, config, business) che devono essere implementate da tutti i componenti.
    - `main.py`: punto di ingresso dell'applicazione che registra automaticamente API, UI, sockets e tutti i controller presenti.
    - `webpack.config.js` e `package.json`: per la build della parte front-end tramite webpack.
    - File aggiuntivi: `.env`, `README.md`, `requirements.txt`.

- **Comandi CLI**
  - **generate:** Genera l’intera struttura di un nuovo modulo.
  - **dev:** Avvia l’applicazione in modalità sviluppo eseguendo `main.py` come modulo (con import relativi corretti).
  - **build:** Esegue la build per la produzione usando webpack, minimizzando i file JavaScript.
  - **add:** Permette di aggiungere nuove classi o template.  
    - Per i **controller**, è possibile specificare un sottotipo (`rest` o `web`).
    - Per i **service**, il sottotipo può essere `business` o `data`.
    - Per i **model**, il sottotipo può essere `domain` o `dto`.
    - Per i **template**, se viene fornita l’opzione `--url_prefix`, viene generato anche un endpoint extra nella cartella `ui/endpoints`.

- **Logger a Colori**
  - La classe `ColoredLogger` fornisce log colorati in base al livello (DEBUG, INFO, WARNING, ERROR, CRITICAL), facilitando il debugging.

- **Registrazione Automatica dei Componenti**
  - Il file `main.py` generato:
    - Importa e inizializza i moduli API, UI e Sockets.
    - Registra automaticamente tutti i controller presenti nella cartella `controllers` (scansione ricorsiva), rendendo il modulo autonomo e facilmente integrabile.

---

## Come Funziona QuarGen

1. **Generazione del Modulo**
   - Esegui il comando:
     ```bash
     python quargen.py generate --name MyApp --base <percorso>
     ```
   - Verrà creata una struttura modulare completa con tutte le directory e i file necessari, inclusi i file `__init__.py` per rendere ogni cartella un package Python.

2. **Avvio in Modalità Sviluppo**
   - Avvia l’applicazione con:
     ```bash
     python quargen.py dev --module MyApp
     ```
   - Il DevServer cambia il working directory al livello superiore di `MyApp` e lancia l’app come modulo (`python -m MyApp.main`), garantendo che gli import relativi siano risolti correttamente.
   - Il file `main.py` registra automaticamente API, UI, Sockets e tutti i controller presenti.

3. **Build per la Produzione**
   - Esegui il comando:
     ```bash
     python quargen.py build --module MyApp
     ```
   - Questo comando esegue `npm install` e `npx webpack` per creare la versione minimizzata dei file JS, pronta per la produzione.

4. **Aggiunta di Nuovi Componenti**
   - Usa il comando `add` per aggiungere nuove classi o template. Ad esempio:
     - **Template UI con Endpoint Extra:**
       ```bash
       python quargen.py add --type template --class_name CustomTemplate --module MyApp/ --url_prefix custom
       ```
     - **Controller, Service e Model:** È possibile specificare il sottotipo (es. `rest`, `business`, `domain`, ecc.) per posizionarli nelle cartelle appropriate.

5. **Logger a Colori**
   - Durante l’esecuzione, la classe `ColoredLogger` produce log colorati in console, facilitando il monitoraggio e il debug.

---

## Struttura del Progetto Generato

Esempio di struttura di un modulo generato (MyApp):

MyApp/
├── .env
├── README.md
├── requirements.txt
├── config/
│   └── default.py
├── docs/
│   ├── installation.md
│   └── usage.md
├── models/
│   ├── domain/
│   │   └── sample_model.py
│   └── dto/
├── controllers/
│   ├── rest/
│   │   └── sample_controller.py
│   └── web/
├── services/
│   ├── business/
│   │   └── sample_service.py
│   └── data/
├── utils/
│   └── logger.py
├── tests/
│   └── test_module.py
├── api/
│   └── api_module.py
├── ui/
│   ├── ui_module.py
│   ├── templates/
│   │   ├── base/
│   │   │   └── base.html
│   │   └── index/
│   │       └── index.html
│   ├── endpoints/   <-- Endpoint extra per la UI
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
├── sockets/
│   └── socket_module.py
├── interfaces/
│   ├── core.py
│   ├── data.py
│   ├── config.py
│   └── business.py
└── main.py

---

## Cosa Fa il Software

- **Automatizza la generazione della struttura modulare:**  
  Permette di creare in modo standardizzato un modulo completo per QuarTrend, includendo tutti i componenti necessari per API, UI, sockets e logica di business.

- **Gestione semplificata dell’avvio e della build:**  
  Fornisce comandi per avviare l’app in modalità sviluppo e per eseguire la build per la produzione tramite webpack.

- **Estendibilità e aggregazione:**  
  Tutti i componenti implementano interfacce standard, rendendo possibile l’aggregazione automatica della logica da moduli differenti in un progetto organico.

- **Output di log a colori:**  
  Grazie alla classe `ColoredLogger`, i log vengono visualizzati in modo chiaro e colorato, facilitando il debug.

---

## Prossimi Sviluppi

- **Testing e CI/CD:**
  - Aggiungere ulteriori test unitari e di integrazione.
  - Integrare un sistema di Continuous Integration per l’esecuzione automatica dei test.

- **Documentazione e Miglioramenti Log:**
  - Migliorare la documentazione interna ed esterna.
  - Aggiornare i messaggi di log per rendere il debug ancora più intuitivo.

- **Estendibilità:**
  - Aggiungere nuovi tipi di componenti e opzioni di personalizzazione.
  - Supportare altri linguaggi o framework nella generazione della struttura.

- **Ottimizzazione della Build e del Deploy:**
  - Integrare strumenti aggiuntivi per la minificazione e il bundling.
  - Automatizzare il deploy su ambienti di staging e produzione.

---

## Aggiornamenti

Questo README viene aggiornato ad ogni modifica significativa del progetto.  
*TODO: Mantieni questo file aggiornato con nuove funzionalità o modifiche.*

---

## Come Contribuire

Se desideri contribuire a QuarGen, fai un fork del repository, apporta le modifiche e apri una pull request. Consulta il file `CONTRIBUTING.md` (se disponibile) per le linee guida sul contributo.

---

Con QuarGen potrai generare rapidamente una struttura modulare standardizzata e scalabile, facilitando lo sviluppo e l'integrazione di applicazioni per il progetto QuarTrend.
