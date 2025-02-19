# QuarGen CLI

QuarGen è un tool da linea di comando sviluppato per il progetto QuarTrend.
Il suo scopo è automatizzare la generazione della struttura di moduli (repository)
per il progetto, creando un'architettura modulare standardizzata e facilmente integrabile in sistemi più grandi.

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
      - `templates/`: con la nuova struttura:
        - `html_templates/`: contiene la cartella `base/` (con `ui_base_template.html`) e il file `ui_index_template.html`.
      - `static/`: con sottocartelle `css/`, `js/`, `images/`.
      - `endpoints/`: cartella separata (fuori da `templates/`) per endpoint extra della UI.
    - `sockets/`: per la gestione delle connessioni socket.
    - `interfaces/`: definisce le interfacce base (core, data, config, business) che devono essere implementate da tutti i componenti.
    - `main.py`: punto di ingresso dell'applicazione che registra automaticamente API, UI, sockets e tutti i controller presenti.
    - `webpack.config.js` e `package.json`: per la build della parte front-end tramite webpack.
    - File aggiuntivi: `.env`, `README.md`, `requirements.txt`, e il file di manifest `module_manifest.json` che descrive il modulo.

- **Comandi CLI**
  - **generate:** Genera l’intera struttura di un nuovo modulo.  
    Aggiungendo il flag `--main` si indica che il modulo sarà quello principale (con endpoint `/`).
  - **dev:** Avvia l’applicazione in modalità sviluppo eseguendo `main.py` come modulo (con import relativi corretti).
  - **build:** Esegue la build per la produzione usando webpack, minimizzando i file JavaScript.
  - **add:** Permette di aggiungere nuove classi o template.  
    - Per i **controller**, è possibile specificare un sottotipo (`rest` o `web`).
    - Per i **service**, il sottotipo può essere `business` o `data`.
    - Per i **model**, il sottotipo può essere `domain` o `dto`.
    - Per i **template**, se viene fornita l’opzione `--url_prefix`, viene generato anche un endpoint extra nella cartella `ui/endpoints`.
    - È possibile anche aggiungere nuovi **endpoint API** tramite il flag `--prefix`.

- **Logger a Colori**
  - La classe `ColoredLogger` fornisce log colorati in base al livello (DEBUG, INFO, WARNING, ERROR, CRITICAL), facilitando il debugging.

- **Registrazione Automatica dei Componenti**
  - Il file `main.py` generato:
    - Importa e inizializza i moduli API, UI e Sockets.
    - Registra automaticamente tutti i controller presenti nella cartella `controllers` (scansione ricorsiva), rendendo il modulo autonomo e facilmente integrabile.

- **Organizzazione dei Template**
  - I template HTML per la UI sono ora gestiti nella cartella `templates/html_templates/`:
    - `base/ui_base_template.html`: template base.
    - `ui_index_template.html`: template per la pagina index.
  - Il template Python per il main si trova in `templates/py_templates/main_template.py`.

- **Manifest del Modulo**
  - Ogni modulo generato include un file `module_manifest.json` contenente le informazioni sul modulo,
    utile per future operazioni di aggregazione tra repository.

---

## Come Funziona QuarGen

1. **Generazione del Modulo**
   - Esegui il comando:
     ```bash
     python quargen.py generate --name MyApp --base <percorso>
     ```
   - Verrà creata una struttura modulare completa con tutte le directory e i file necessari,
     inclusi i file `__init__.py` per rendere ogni cartella un package Python e il file manifest.

2. **Avvio in Modalità Sviluppo**
   - Avvia l’applicazione con:
     ```bash
     python quargen.py dev --module MyApp
     ```
   - Il DevServer cambia il working directory al livello superiore di `MyApp` e lancia l’app come modulo
     (`python -m MyApp.main`), garantendo che gli import relativi siano risolti correttamente.
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
     - **Endpoint API Extra:** Usa il flag `--prefix` per definire il prefisso dell’endpoint.

5. **Logger a Colori**
   - Durante l’esecuzione, la classe `ColoredLogger` produce log colorati in console, facilitando il monitoraggio e il debug.

---

## Cosa Fa il Software

- **Automatizza la generazione della struttura modulare:**  
  Permette di creare in modo standardizzato un modulo completo per QuarTrend,
  includendo tutti i componenti necessari per API, UI, sockets e logica di business.

- **Gestione semplificata dell’avvio e della build:**  
  Fornisce comandi per avviare l’app in modalità sviluppo e per eseguire la build per la produzione tramite webpack.

- **Estendibilità e aggregazione:**  
  Tutti i componenti implementano interfacce standard, rendendo possibile l’aggregazione automatica della logica da moduli differenti in un progetto organico.

- **Output di log a colori:**  
  Grazie alla classe `ColoredLogger`, i log vengono visualizzati in modo chiaro e colorato, facilitando il debug.

- **Gestione centralizzata dei template:**  
  I template per la UI e il main sono gestiti in cartelle specifiche (html_templates e py_templates) per una manutenzione più semplice.

- **Manifest del modulo:**  
  Ogni modulo genera un file `module_manifest.json` con le informazioni sul modulo, utile per future operazioni di aggregazione.

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

Se desideri contribuire a QuarGen, fai un fork del repository, apporta le modifiche e apri una pull request.
Consulta il file `CONTRIBUTING.md` (se disponibile) per le linee guida sul contributo.

---

Con QuarGen potrai generare rapidamente una struttura modulare standardizzata e scalabile,
facilitando lo sviluppo e l'integrazione di applicazioni per il progetto QuarTrend.
