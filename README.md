# FISHEK Desktop

## Installation of Fishek desktop extension

### Linux (Fedora)

**Installation:**

1. Download the latest `fishek-linux-rpm.zip` from the [Actions](https://github.com/KTokarski2/fishek/actions) tab on GitHub, then unzip it.
2. Install the package:
```bash
   sudo dnf install fishek-1.0.0-1.x86_64.rpm
```
3. Create the configuration directory and add your credentials:
```bash
   mkdir -p ~/.config/fishek
```
   Create `~/.config/fishek/.env` with the following content:
```
   SPREADSHEET_ID=your_spreadsheet_id
```
   Copy your `client_secrets.json` to `~/.config/fishek/client_secrets.json`.

4. Launch the application from the GNOME Activities menu or by running `fishek` in the terminal.
5. On first launch, a browser window will open for Google authentication. After logging in, the token will be saved automatically.

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
3. Open File Explorer and navigate to `%APPDATA%\fishek` (type this directly in the address bar). Create the folder if it does not exist.
4. Create a `.env` file inside that folder with the following content:
```
   SPREADSHEET_ID=your_spreadsheet_id
```
   Copy your `client_secrets.json` to the same folder.
5. Launch the application from the Desktop shortcut or the Start menu.
6. On first launch, a browser window will open for Google authentication. After logging in, the token will be saved automatically.

**Uninstallation:**

1. Go to **Settings → Apps → Installed apps**, find **FISHEK Desktop** and click **Uninstall**.
2. Remove the configuration folder manually:
   - Open File Explorer, navigate to `%APPDATA%` and delete the `fishek` folder.