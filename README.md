# Job Assistant

Projekt aplikacji opartej na modelach językowych, którego celem jest stworzenie asystenta AI wspierającego pracę z informacjami i realizację wybranych zadań.

Repozytorium udostępniono w celach dydaktycznych. Kod może stanowić punkt wyjścia do nauki, eksperymentowania oraz budowania własnych rozwiązań opartych na AI.

## Funkcjonalności

- Wykorzystanie modeli językowych do generowania odpowiedzi.
- Możliwość konfiguracji agentów AI.
- Personalizacja promptów i sposobu działania asystenta.
- Możliwość rozbudowy projektu o własne funkcjonalności.
- Struktura umożliwiająca dalszy rozwój aplikacji.

## Wymagania

Do uruchomienia projektu potrzebujesz:

- Python 3,
- Git,
- klucza API do wybranego modelu AI, zgodnie z konfiguracją projektu.

## Instalacja i uruchomienie

### 1. Pobranie repozytorium

```powershell
git clone https://github.com/SSJ0406/job_assistant.git
cd job_assistant
```

### 2. Utworzenie środowiska wirtualnego

```powershell
python -m venv .venv
```

Aktywacja środowiska w PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalacja zależności

```powershell
python -m pip install -r requirements.txt
```

### 4. Konfiguracja zmiennych środowiskowych

W repozytorium znajduje się plik `.env.example`, który zawiera przykładową konfigurację zmiennych środowiskowych.

Skopiuj go do pliku `.env`:

```powershell
Copy-Item .env.example .env
```

Następnie otwórz plik `.env` i uzupełnij wartości zgodnie z własną konfiguracją.

Przykład:

```env
OPENAI_API_KEY=twoj_wlasny_klucz_api
OPENAI_BASE_URL=odpowiedni_base_url
MODEL_NAME=nazwa_wybranego_modelu
```

Wartości należy dostosować do własnej konfiguracji i wykorzystywanego modelu AI.

`OPENAI_BASE_URL` jest opcjonalne. Możesz pozostawić je puste, jeśli korzystasz ze standardowego endpointu OpenAI. W przypadku innego dostawcy lub własnego endpointu wpisz odpowiedni adres.

Nie udostępniaj swojego klucza API ani nie umieszczaj go w repozytorium.

### 5. Uruchomienie aplikacji

```powershell
.\run_app.ps1
```

## Konfiguracja i personalizacja

Konfiguracja projektu znajduje się między innymi w katalogu `job_assistant/`.

W zależności od potrzeb możesz modyfikować:

- `job_assistant/agents/agent_config.py` — konfigurację agentów,
- `job_assistant/agents/prompts.py` — prompty i instrukcje dla agentów,
- `app_settings.py` — ustawienia aplikacji.

Przed wprowadzeniem zmian warto zapoznać się ze strukturą repozytorium oraz dokumentacją projektu.

## Dokumentacja architektury

W repozytorium znajduje się dokument opisujący architekturę aplikacji, jej strukturę oraz najważniejsze komponenty i sposób ich współpracy.

Zachęcam do zapoznania się z nim przed rozpoczęciem pracy z kodem, a szczególnie przed wprowadzaniem własnych modyfikacji i rozbudową projektu.

[Dokumentacja architektury projektu (ARCHITECTURE.md)](docs/ARCHITECTURE.md)

## Testy

Aby uruchomić testy, wykonaj:

```powershell
python -m pytest
```

## Struktura projektu

```text
job_assistant/
├── docs/                 # Dokumentacja, w tym opis architektury
├── job_assistant/        # Kod aplikacji
│   └── agents/           # Konfiguracja i logika agentów
├── tests/                # Testy
├── .env.example          # Przykładowa konfiguracja środowiska
├── .gitignore            # Pliki wykluczone z repozytorium
├── AGENTS.md             # Wytyczne dla agentów AI
├── README.md             # Dokumentacja projektu
├── REVIEW.md             # Wytyczne dotyczące code review
├── main.py               # Punkt wejścia aplikacji
├── requirements.txt      # Zależności
└── run_app.ps1           # Skrypt uruchamiający
```

## Rozwijanie projektu

Projekt został przygotowany z myślą o dalszym rozwoju, personalizacji i eksperymentowaniu. Zachęcam do dostosowania go do własnych potrzeb, założeń oraz preferowanych rozwiązań.

Możesz potraktować zastosowany w projekcie wzorzec jako punkt wyjścia do stworzenia własnego **osobistego asystenta AI**. W tym celu możesz modyfikować konfigurację, agentów, prompty, przepływy pracy oraz pozostałe elementy aplikacji, tak aby odpowiadały Twoim potrzebom i sposobowi pracy.

W przypadku rozwijania projektu warto:

- dostosować konfigurację i działanie agentów do własnego przypadku użycia,
- modyfikować prompty oraz sposób generowania odpowiedzi,
- rozwijać istniejące funkcjonalności lub dodawać nowe,
- uzupełniać testy,
- aktualizować dokumentację,
- zachowywać spójność architektury,
- nie umieszczać danych poufnych w repozytorium.

**Projekt stanowi punkt wyjścia do własnych eksperymentów, modyfikacji oraz budowy osobistego asystenta AI.**

## Licencja i zasady wykorzystania

Projekt został udostępniony na potrzeby dydaktyczne. Uprawnienie do jego wykorzystania dotyczy wyłącznie studentów autora.

Pozostałe osoby nie są uprawnione do wykorzystywania, kopiowania ani rozpowszechniania projektu bez uzyskania odrębnej zgody autora.

