# FISHEK

A set of tools for learning vocabulary with Google Sheets and AI-powered flashcard generation.

## Projects

- **fishek-desktop** — clipboard listener that saves words directly to a Google Sheet
- **fishek-flashcard-builder** — desktop app for generating and translating flashcards using an AI model (Ollama) and saving them via the Fishek API

---

## fishek-desktop

### Linux (Fedora)

**Installation:**

1. Download the latest `fishek-linux-rpm.zip` from the [Actions](https://github.com/KTokarski2/fishek/actions) tab on GitHub, then unzip it.
2. Install the package:
```bash
sudo dnf install fishek-1.0.0-1.x86_64.rpm
```
3. Create the configuration directory:
```bash
mkdir -p ~/.config/fishek
```
4. Create `~/.config/fishek/.env` with the following content:
```
SPREADSHEET_ID=your_spreadsheet_id
```
5. Copy your `client_secrets.json` to `~/.config/fishek/client_secrets.json`.
6. Launch from the GNOME Activities menu or by running `fishek` in the terminal.
7. On first launch a browser window opens for Google authentication. The token is saved automatically and refreshed when needed.

**Uninstallation:**
```bash
sudo dnf remove fishek
rm -rf ~/.config/fishek
```

---

### Windows

**Installation:**

1. Download the latest `fishek-windows-installer.zip` from the [Actions](https://github.com/KTokarski2/fishek/actions) tab on GitHub, then unzip it.
2. Run `fishek-setup.exe` and follow the installation wizard.
3. Open File Explorer, navigate to `%APPDATA%\fishek` (type this in the address bar). Create the folder if it does not exist.
4. Create a `.env` file inside that folder:
```
SPREADSHEET_ID=your_spreadsheet_id
```
5. Copy your `client_secrets.json` to the same folder.
6. Launch from the Desktop shortcut or the Start menu.
7. On first launch a browser window opens for Google authentication. The token is saved automatically and refreshed when needed.

**Uninstallation:**

1. Go to **Settings → Apps → Installed apps**, find **FISHEK Desktop** and click **Uninstall**.
2. Open File Explorer, navigate to `%APPDATA%` and delete the `fishek` folder.

---

## fishek-flashcard-builder

A GUI application that:
- downloads word/language pairs from a Google Sheet
- translates them using an AI model running locally via Ollama
- lets you accept, refine, or drop each translation
- saves accepted flashcards to the Fishek API

### Prerequisites

- [Ollama](https://ollama.com) running locally with a model pulled (default: `qwen2.5:7b`)
- Fishek API running and accessible
- Google Sheets API credentials (`client_secrets.json`)

### Linux (Fedora)

**Installation:**

1. Download the latest `fishek-flashcard-builder-linux-rpm.zip` from the [Actions](https://github.com/KTokarski2/fishek/actions) tab on GitHub, then unzip it.
2. Install the package:
```bash
sudo dnf install fishek-flashcard-builder-1.0.0-1.x86_64.rpm
```
3. Create the configuration directory (shared with fishek-desktop):
```bash
mkdir -p ~/.config/fishek
```
4. Create or update `~/.config/fishek/.env` with the following content:
```
SPREADSHEET_ID=your_spreadsheet_id
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TEMPERATURE=0.1
FLASHCARD_API_BASE_URL=http://localhost:8080
FLASHCARD_API_EMAIL=your_email
FLASHCARD_API_PASSWORD=your_password
```
5. Copy your `client_secrets.json` to `~/.config/fishek/client_secrets.json`.
6. Launch from the GNOME Activities menu or by running `fishek-flashcard-builder` in the terminal.
7. On first launch a browser window opens for Google authentication. The token is saved automatically and refreshed when needed.

**Uninstallation:**
```bash
sudo dnf remove fishek-flashcard-builder
rm -rf ~/.config/fishek
```

---

### Windows

**Installation:**

1. Download the latest `fishek-flashcard-builder-windows-installer.zip` from the [Actions](https://github.com/KTokarski2/fishek/actions) tab on GitHub, then unzip it.
2. Run `fishek-flashcard-builder-setup.exe` and follow the installation wizard.
3. Open File Explorer, navigate to `%APPDATA%\fishek`. Create the folder if it does not exist.
4. Create a `.env` file inside that folder:
```
SPREADSHEET_ID=your_spreadsheet_id
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TEMPERATURE=0.1
FLASHCARD_API_BASE_URL=http://localhost:8080
FLASHCARD_API_EMAIL=your_email
FLASHCARD_API_PASSWORD=your_password
```
5. Copy your `client_secrets.json` to the same folder.
6. Launch from the Desktop shortcut or the Start menu.
7. On first launch a browser window opens for Google authentication. The token is saved automatically and refreshed when needed.

**Uninstallation:**

1. Go to **Settings → Apps → Installed apps**, find **FISHEK Flashcard Builder** and click **Uninstall**.
2. Open File Explorer, navigate to `%APPDATA%` and delete the `fishek` folder.

---

## Building releases

Releases are built automatically by GitHub Actions on every tag push matching `v*`:

```bash
git tag v1.0.0
git push origin main --tags
```

Artifacts are available in the [Actions](https://github.com/KTokarski2/fishek/actions) tab after the pipeline finishes:

| Artifact | Contents |
|---|---|
| `fishek-linux-rpm` | RPM installer for fishek-desktop |
| `fishek-windows-installer` | EXE installer for fishek-desktop |
| `fishek-flashcard-builder-linux-rpm` | RPM installer for fishek-flashcard-builder |
| `fishek-flashcard-builder-windows-installer` | EXE installer for fishek-flashcard-builder |