# Answer Agent PoC

Prosta aplikacja Streamlit z jednym Answer Agentem. Każde pytanie trafia bezpośrednio do modelu skonfigurowanego przez OpenAI Responses API, razem z historią bieżącej rozmowy.

## Przewodnik po architekturze

Materiały do omówienia struktury projektu, przepływu zapytania i odpowiedzialności modułów znajdują się w [notatkach architektonicznych dla studentów](docs/ARCHITECTURE.md).

## Uruchomienie na Windows

Projekt wymaga Pythona 3.11 lub nowszego. W katalogu projektu utwórz środowisko i zainstaluj zależności:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Uruchom aplikację:

```powershell
.\run_app.ps1
```

Otwórz `http://localhost:8501`. Skrypt nasłuchuje tylko na `127.0.0.1`. Inny port można podać parametrem, np. `.\run_app.ps1 -Port 8502`.

## Konfiguracja

Skopiuj `.env.example` do `.env` i wpisz własny klucz w `OPENAI_API_KEY`. Klient OpenAI korzysta z tego klucza; plik `.env` jest ignorowany przez Git.

```dotenv
OPENAI_API_KEY=tu_wklej_swoj_klucz
OPENAI_MODEL=gpt-6-luna
OPENAI_BASE_URL=https://api.openai.com/v1
```

Ustawienia Answer Agenta (domyślnie: model `gpt-6-luna`, temperatura `0`, `max_output_tokens=2000`, `context_tokens=8000`, `reasoning_effort=none`) są w `job_assistant/agents/agent_config.py`; model można zmienić przez `OPENAI_MODEL`. Prompt systemowy Answer Agenta znajduje się w `job_assistant/agents/prompts.py`. Adapter przekazuje go do pola `instructions` w Responses API, a historię rozmowy i bieżące pytanie do pola `input`. Zmiany `.env` wymagają ponownego uruchomienia aplikacji.

## Testy

```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests
```

Testy klienta i workflow używają atrap; nie wysyłają zapytań do OpenAI.

## Diagram przepływu

Po aktywowaniu `.venv` wygeneruj diagram przepływu poleceniem:

```powershell
python -m job_assistant.workflows.export_graph
```
