# QuarGen CLI

QuarGen è un tool da linea di comando sviluppato per il progetto QuarTrend. Il suo scopo è quello di automatizzare la generazione della struttura di moduli (repository) per il progetto, gestendo:
- La creazione automatica di un'architettura modulare completa (con directory predefinite e file come `main.py`, `webpack.config.js` e `package.json`).
- La configurazione dei blueprint per API, UI e sockets (con supporto per file statici e template).
- L'integrazione di un logger a colori per un output di log chiaro e immediato.
- Comandi per avviare l'applicazione in modalità sviluppo (dev), eseguire la build per la produzione (build) e aggiungere nuove classi o template (add) con endpoint personalizzati.

---

## Caratteristiche implementate

- **Generazione modulo completo**  
  - Creazione delle seguenti directory e file:  
    - `config/` (con `default.py`)
    - `docs/` (con `installation.md` e `usage.md`)
    - `models/`, `controllers/`, `services/`
    - `utils/` (con la classe `ColoredLogger`)
    - `tests/` (con file di test di base)
    - `api/` (con il modulo API)
    - `ui/` che include:
      - `templates/` con le cartelle `base/` (contenente `base.html`) ed `index/` (contenente `index.html`)
      - `static/` (con sottocartelle `css/`, `js/`, `images/`)
      - `endpoints/` per eventuali endpoint aggiuntivi
    - `sockets/` per il modulo di gestione delle connessioni (rinominato per evitare conflitti)
    - `main.py` per l'avvio dell'app in modalità sviluppo
    - `webpack.config.js` e `package.json` per la build in produzione tramite webpack
  - Configurazione del blueprint UI per servire i template e i file statici correttamente (usando `template_folder` e `static_folder`).

- **Comandi CLI**
  - `generate`: genera la struttura completa di un nuovo modulo.
  - `dev`: avvia il server Flask in modalità sviluppo (eseguendo `main.py`).
  - `build`: esegue la build in modalità produzione tramite webpack (minimizzazione dei file JS).
  - `add`: permette di aggiungere nuove classi o template; per i template, con l'opzione `--url_prefix` viene generato anche un endpoint extra che estende la UI.

- **Logger a colori**  
  La classe `ColoredLogger` fornisce un output di log con colori in base al livello (DEBUG, INFO, WARNING, ERROR, CRITICAL) e viene utilizzata in API, UI e sockets.

---

## Cosa fa il software

- **Automatizzazione della struttura modulare**:  
  Permette di generare, in modo standardizzato, la struttura di un modulo (repository) per il progetto QuarTrend, includendo tutti i componenti necessari (config, docs, modelli, API, UI, sockets, file statici, ecc.).

- **Avvio e build**:  
  Consente di avviare l’app in modalità sviluppo e di eseguire la build per la produzione tramite webpack, semplificando il flusso di lavoro.

- **Estendibilità**:  
  Permette di aggiungere facilmente nuove classi o template, inclusa la possibilità di creare endpoint personalizzati che si integrano con la UI già generata.

---

## TODO / Prossimi sviluppi

- **Testing e CI/CD**:
  - Implementare ulteriori test unitari e di integrazione per tutti i componenti.
  - Integrare un sistema di Continuous Integration (CI) per l'esecuzione automatica dei test.

- **Documentazione e Messaggi di Log**:
  - Migliorare la documentazione interna e esterna.
  - Aggiornare e dettagliare ulteriormente i messaggi di log per facilitare il debug.

- **Estendibilità**:
  - Aggiungere nuove opzioni per personalizzare ulteriormente la generazione della struttura (ad esempio, supporto per nuovi linguaggi o framework).
  - Consentire l'integrazione di ulteriori strumenti per la build e il deploy.

- **Ottimizzazione del processo di build**:
  - Integrare strumenti di minificazione e bundle (oltre a webpack) per ottimizzare la produzione.
  - Automatizzare il deploy su ambienti di staging e produzione.

---

## Aggiornamenti

Questo file README.md viene aggiornato ad ogni modifica significativa del progetto.  
*TODO: Mantieni questo file aggiornato ogni volta che viene implementata una nuova funzionalità o che viene risolto un bug.*

---

## Come contribuire

Se desideri contribuire al progetto, sentiti libero di fare un fork del repository, apportare le modifiche e aprire una pull request.  
Consulta il file `CONTRIBUTING.md` (se disponibile) per le linee guida sul contributo.

---

