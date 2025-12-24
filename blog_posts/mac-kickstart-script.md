title: My Mac Kickstart Script for a Fresh Dev Setup
date: 2024-12-20
tags: mac, automation, shell, devtools
---

# My Mac Kickstart Script for a Fresh Dev Setup

Every time I get a new Mac or do a clean install, I go through the same ritual: install Homebrew, install my tools, configure git, tweak system settings. It takes hours if done manually.

So I wrote a setup script that automates the entire thing. Run it once, grab a coffee, and come back to a fully configured machine.

## Get the Script

```bash
git clone https://github.com/sek3b/mac-kickstart.git
cd mac-kickstart
chmod +x setup.sh && ./setup.sh
```

## What Gets Installed

### CLI Tools (via Homebrew)

- `git` - Version control
- `wget` / `curl` - File downloads
- `htop` - Process monitoring
- `vim` - Text editor

### Applications (via Homebrew Cask)

| App | Purpose |
|-----|---------|
| Brave | Privacy-focused browser |
| VS Code | Code editor |
| iTerm2 | Terminal replacement |
| Wireshark | Network analysis |
| Obsidian | Notes and knowledge base |
| Slack | Communication |
| Rectangle | Window management |
| Stats | Menu bar system monitor |
| AppCleaner | Clean app uninstalls |

### Shell Setup

The script installs Oh My Zsh with plugins for a better terminal experience.

### VS Code Configuration

Automatically sets up VS Code with the Catppuccin Macchiato theme to match my terminal aesthetic.

### Git Configuration

Sets up sensible defaults and aliases so I don't have to configure git manually on every machine.

### macOS Tweaks

The script applies my preferred system settings:

- **Finder** - Show hidden files, path bar, status bar
- **Dock** - Auto-hide with no delay
- **Keyboard** - Fast key repeat
- **Trackpad** - Three-finger drag
- **Screenshots** - Save to ~/Screenshots as PNG

## Design Principles

1. **Idempotent** - Run it multiple times without breaking things
2. **Homebrew for everything** - One package manager to rule them all
3. **Opinionated but modular** - Comment out what you don't need

## Fork It

The script reflects my preferences. Fork the repo and swap in your own tools and apps.

---

*[github.com/sek3b/mac-kickstart](https://github.com/sek3b/mac-kickstart)*
