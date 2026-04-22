# 🛡️ Utilizzo dell'intelligenza artificiale per contrastare il phishing

Il progetto è un insieme di script python che indentificano e rilevano automaticamente i domini di phishing utilizzando il **machine learning**.

---

## 📌 Descrizione

Il progetto implementa un classificatore binario in grado di distinguere domini di **phishing** da domini **legittimi**, analizzando esclusivamente le caratteristiche intrinseche dei nomi di dominio, senza ricorrere a servizi o strumenti esterni.

Il sistema sfrutta tecniche di **feature engineering** su URL e nomi di dominio, addestra e confronta diversi algoritmi di machine learning, e identifica il modello più performante per il rilevamento in tempo reale.

---

## 🗂️ Struttura del progetto

```
├── data/
│   ├── phishing_domains.txt      # Lista domini di phishing (Phishing.Database Project)
│   └── legitimate_domains.txt    # Lista domini legittimi (Tranco Top 1M)
│
├── principale.py                 # Entry point: orchestrazione dell'intero sistema
├── db_builder.py                 # Costruzione e bilanciamento del dataframe
├── phishing_cleaner.py           # Caricamento e pulizia dei domini di phishing
├── legitimate_cleaner.py         # Caricamento e pulizia dei domini legittimi
├── machine_learning.py           # Addestramento e valutazione dei modelli ML
└── data_visualization.py         # Visualizzazione della matrice di correlazione
```

---

### Dipendenze principali

| Libreria | Utilizzo |
|---|---|
| `pandas` | Manipolazione e gestione dei dataframe |
| `scikit-learn` | Modelli ML (Random Forest, Extra Trees, Logistic Regression) e metriche |
| `xgboost` | Classificatore XGBoost |
| `lightgbm` | Classificatore LightGBM |
| `catboost` | Classificatore CatBoost |
| `tldextract` | Estrazione di dominio, sottodominio e TLD |
| `seaborn` / `matplotlib` | Visualizzazione della matrice di correlazione |
| `ipaddress` | Rilevamento di indirizzi IP |

---

## 🚀 Utilizzo

```bash
python principale.py
```

Lo script esegue in sequenza:
1. Caricamento e pulizia dei dataset di phishing e legittimi
2. Costruzione del dataframe con rimozione dei duplicati e bilanciamento
3. Estrazione delle feature descrittive
4. Visualizzazione della matrice di correlazione
5. Addestramento e valutazione di tutti i modelli
6. Test su esempi specifici non presenti nel dataset di addestramento

---

## 🔬 Feature estratte

Le feature sono costruite esclusivamente dalle informazioni interne dei domini:

| Feature | Tipo | Descrizione |
|---|---|---|
| `domain_length` | int | Lunghezza in caratteri del dominio principale |
| `count_digits` | int | Numero di cifre numeriche nel dominio |
| `is_ip` | binary | 1 se il dominio è un indirizzo IP |
| `has_at_symbol` | binary | Presenza del simbolo `@` nel dominio |
| `count_special_chars` | int | Numero di caratteri non alfanumerici |
| `free_hosting_keyword` | int | Corrispondenze con nomi di hosting gratuiti (es. GitHub, Weebly) |
| `count_sensitive_keyword` | int | Parole chiave sospette nel dominio (es. "login", "bank", "secure") |
| `has_explicit_port` | binary | Presenza di una porta esplicita (es. `:8080`) |
| `entropy` | float | Entropia di Shannon del dominio (misura di casualità) |
| `tld_phishing_ratio` | float | Percentuale di phishing associata al TLD nel dataset |

---

## 📊 Dataset

- **Phishing:** [Phishing.Database Project](https://github.com/mitchellkrogza/Phishing.Database) — lista open-source aggiornata regolarmente, scaricata il 14 luglio 2025 (812.635 domini attivi)
- **Legittimi:** [Tranco Top List](https://tranco-list.eu/) — il milione di domini più visitati a livello globale, scaricata il 14 luglio 2025

Dopo la rimozione dei duplicati e il bilanciamento tramite **undersampling**, il dataset finale contiene **423.690 record bilanciati** (211.845 per classe).

---

## 🤖 Modelli confrontati

Sono stati addestrati e confrontati i seguenti algoritmi di classificazione supervisionata:

| Modello | Accuracy | Precision (phishing) | Recall (phishing) | F1 (phishing) |
|---|---|---|---|---|
| Random Forest | 0.73 | 0.77 | 0.64 | 0.70 |
| **LightGBM** ✅ | **0.73** | **0.77** | **0.65** | **0.70** |
| XGBoost | 0.73 | 0.77 | 0.64 | 0.70 |
| CatBoost | 0.73 | 0.77 | 0.64 | 0.70 |
| Extra Trees | 0.71 | 0.80 | 0.57 | 0.67 |
| Logistic Regression | 0.72 | 0.75 | 0.65 | 0.70 |

**LightGBM** è il modello selezionato come migliore per la combinazione ottimale di accuracy e metriche di classificazione.

---

## 📈 Risultati

Il miglior modello (LightGBM) raggiunge:
- **Accuracy: 73%**
- **Precision (phishing): 0.77**
- **Recall (phishing): 0.65**
- **F1-score (phishing): 0.70**

---

## 📚 Riferimenti

- Phishing.Database Project: https://github.com/mitchellkrogza/Phishing.Database
- Tranco List: https://tranco-list.eu/
- Verizon DBIR 2025
- Scikit-learn documentation: https://scikit-learn.org
- LightGBM documentation: https://lightgbm.readthedocs.io

---

## 👤 Autore

**Marco Caldarola** — Tesi Triennale in Ingegneria Informatica, A.A. 2024/2025  
Relatore: Prof. Rocco Pietrini
