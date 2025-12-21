title: My Mac Kickstart Script for a Fresh Dev Setup
date: 2024-12-20
tags: mac, automation, shell, devtools
---

# My Mac Kickstart Script for a Fresh Dev Setup

Every time I get a new Mac or do a clean install, I go through the same ritual: install Homebrew, install my tools, configure git, set up my dotfiles. It takes hours if done manually.

So I wrote a kickstart script that automates the entire thing. Run it once, grab a coffee, and come back to a fully configured dev machine.

## The Philosophy

Before diving into the script, here's my approach:

1. **Homebrew for everything** - If it can be installed via brew, it should be
2. **Idempotent** - Run it multiple times without breaking things
3. **Opinionated but modular** - Easy to comment out what you don't need
4. **No sudo where possible** - Minimize privilege escalation

## The Script

Save this as `kickstart.sh` and run with `chmod +x kickstart.sh && ./kickstart.sh`:

```bash
#!/bin/bash

set -e  # Exit on error

echo "=========================================="
echo "  Mac Kickstart Script for Developers"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ------------------------------------------
# Xcode Command Line Tools
# ------------------------------------------
log_info "Checking Xcode Command Line Tools..."
if ! xcode-select -p &>/dev/null; then
    log_info "Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "Press any key after Xcode tools installation completes..."
    read -n 1
else
    log_info "Xcode Command Line Tools already installed"
fi

# ------------------------------------------
# Homebrew
# ------------------------------------------
log_info "Checking Homebrew..."
if ! command -v brew &>/dev/null; then
    log_info "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add to path for Apple Silicon
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    log_info "Homebrew already installed, updating..."
    brew update
fi

# ------------------------------------------
# CLI Tools
# ------------------------------------------
log_info "Installing CLI tools..."

CLI_TOOLS=(
    # Core utils
    "git"
    "curl"
    "wget"
    "jq"
    "yq"
    "tree"
    "htop"
    "watch"

    # Modern replacements
    "eza"           # Better ls
    "bat"           # Better cat
    "ripgrep"       # Better grep
    "fd"            # Better find
    "fzf"           # Fuzzy finder
    "zoxide"        # Better cd
    "tldr"          # Simplified man pages

    # Dev tools
    "gh"            # GitHub CLI
    "git-delta"     # Better git diff
    "lazygit"       # Git TUI
    "tmux"          # Terminal multiplexer
    "neovim"        # Editor

    # Shell
    "zsh-autosuggestions"
    "zsh-syntax-highlighting"
    "starship"      # Prompt

    # Networking
    "nmap"
    "httpie"
    "mtr"

    # Containers
    "docker"
    "docker-compose"
    "kubectl"
    "k9s"           # Kubernetes TUI

    # Misc
    "ffmpeg"
    "imagemagick"
    "sqlite"
)

for tool in "${CLI_TOOLS[@]}"; do
    if brew list "$tool" &>/dev/null; then
        log_info "$tool already installed"
    else
        log_info "Installing $tool..."
        brew install "$tool"
    fi
done

# ------------------------------------------
# Programming Languages
# ------------------------------------------
log_info "Installing programming languages..."

# Python (via pyenv)
if ! command -v pyenv &>/dev/null; then
    log_info "Installing pyenv..."
    brew install pyenv pyenv-virtualenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
fi

# Node (via nvm)
if [ ! -d "$HOME/.nvm" ]; then
    log_info "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi

# Go
if ! brew list go &>/dev/null; then
    log_info "Installing Go..."
    brew install go
    echo 'export GOPATH="$HOME/go"' >> ~/.zshrc
    echo 'export PATH="$GOPATH/bin:$PATH"' >> ~/.zshrc
fi

# Rust
if ! command -v rustup &>/dev/null; then
    log_info "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
fi

# ------------------------------------------
# GUI Applications (Casks)
# ------------------------------------------
log_info "Installing applications..."

CASKS=(
    # Browsers
    "arc"
    "firefox"

    # Dev tools
    "visual-studio-code"
    "iterm2"
    "docker"
    "postman"
    "tableplus"         # Database GUI

    # Productivity
    "raycast"           # Spotlight replacement
    "rectangle"         # Window management
    "obsidian"          # Notes
    "notion"

    # Utils
    "1password"
    "the-unarchiver"
    "appcleaner"
    "stats"             # Menu bar system stats

    # Communication
    "slack"
    "discord"
    "zoom"
)

for cask in "${CASKS[@]}"; do
    if brew list --cask "$cask" &>/dev/null; then
        log_info "$cask already installed"
    else
        log_info "Installing $cask..."
        brew install --cask "$cask" || log_warn "Failed to install $cask"
    fi
done

# ------------------------------------------
# Fonts
# ------------------------------------------
log_info "Installing fonts..."
brew tap homebrew/cask-fonts 2>/dev/null || true
FONTS=(
    "font-jetbrains-mono-nerd-font"
    "font-fira-code-nerd-font"
    "font-hack-nerd-font"
)

for font in "${FONTS[@]}"; do
    if brew list --cask "$font" &>/dev/null; then
        log_info "$font already installed"
    else
        log_info "Installing $font..."
        brew install --cask "$font" || log_warn "Failed to install $font"
    fi
done

# ------------------------------------------
# Git Configuration
# ------------------------------------------
log_info "Configuring Git..."

# Only set if not already configured
if [ -z "$(git config --global user.name)" ]; then
    read -p "Enter your Git name: " git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    read -p "Enter your Git email: " git_email
    git config --global user.email "$git_email"
fi

# Sensible defaults
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global fetch.prune true
git config --global diff.colorMoved zebra
git config --global core.editor "nvim"
git config --global core.pager "delta"

# Delta config
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.light false
git config --global delta.line-numbers true

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "reset HEAD --"

# ------------------------------------------
# macOS Defaults
# ------------------------------------------
log_info "Configuring macOS defaults..."

# Finder
defaults write com.apple.finder AppleShowAllFiles YES              # Show hidden files
defaults write com.apple.finder ShowPathbar -bool true             # Show path bar
defaults write com.apple.finder ShowStatusBar -bool true           # Show status bar
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true # Full path in title

# Keyboard
defaults write NSGlobalDomain KeyRepeat -int 2                     # Fast key repeat
defaults write NSGlobalDomain InitialKeyRepeat -int 15             # Short delay
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false # Disable press-and-hold

# Dock
defaults write com.apple.dock autohide -bool true                  # Auto-hide dock
defaults write com.apple.dock autohide-delay -float 0              # No delay
defaults write com.apple.dock tilesize -int 48                     # Icon size
defaults write com.apple.dock show-recents -bool false             # No recent apps

# Screenshots
defaults write com.apple.screencapture location ~/Screenshots      # Save location
defaults write com.apple.screencapture type png                    # Format
mkdir -p ~/Screenshots

# Trackpad
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true

# Restart affected apps
killall Finder 2>/dev/null || true
killall Dock 2>/dev/null || true

# ------------------------------------------
# SSH Key
# ------------------------------------------
log_info "Checking SSH key..."
if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    log_info "Generating SSH key..."
    ssh-keygen -t ed25519 -C "$(git config --global user.email)" -f "$HOME/.ssh/id_ed25519" -N ""
    eval "$(ssh-agent -s)"
    ssh-add --apple-use-keychain ~/.ssh/id_ed25519

    echo ""
    log_warn "Add this SSH key to GitHub:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "Run: gh auth login"
fi

# ------------------------------------------
# Shell Configuration
# ------------------------------------------
log_info "Configuring shell..."

# Starship prompt
if [ ! -f "$HOME/.config/starship.toml" ]; then
    mkdir -p ~/.config
    cat > ~/.config/starship.toml << 'EOF'
[character]
success_symbol = "[➜](bold green)"
error_symbol = "[➜](bold red)"

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = " "

[git_status]
ahead = "⇡${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
behind = "⇣${count}"

[nodejs]
symbol = " "

[python]
symbol = " "

[rust]
symbol = " "

[golang]
symbol = " "
EOF
fi

# Add to .zshrc if not present
if ! grep -q "starship init" ~/.zshrc 2>/dev/null; then
    cat >> ~/.zshrc << 'EOF'

# Starship prompt
eval "$(starship init zsh)"

# Zoxide (better cd)
eval "$(zoxide init zsh)"

# FZF
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Aliases
alias ls="eza --icons"
alias ll="eza -la --icons"
alias cat="bat"
alias grep="rg"
alias find="fd"
alias vim="nvim"
alias lg="lazygit"
alias k="kubectl"

# Quick navigation
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

EOF
fi

# ------------------------------------------
# Create dev directories
# ------------------------------------------
log_info "Creating dev directories..."
mkdir -p ~/dev/{personal,work,sandbox}
mkdir -p ~/scripts

# ------------------------------------------
# Done!
# ------------------------------------------
echo ""
echo "=========================================="
echo -e "${GREEN}  Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Restart your terminal (or run: source ~/.zshrc)"
echo "  2. Install Python: pyenv install 3.12 && pyenv global 3.12"
echo "  3. Install Node: nvm install --lts"
echo "  4. Add SSH key to GitHub: gh auth login"
echo "  5. Clone your dotfiles repo"
echo ""
echo "Installed $(brew list | wc -l | tr -d ' ') packages via Homebrew"
echo ""
```

## What Gets Installed

### CLI Tools

| Tool | Replaces | Why |
|------|----------|-----|
| `eza` | `ls` | Icons, git status, tree view |
| `bat` | `cat` | Syntax highlighting, line numbers |
| `ripgrep` | `grep` | 10x faster, respects .gitignore |
| `fd` | `find` | Sane defaults, faster |
| `fzf` | - | Fuzzy find everything |
| `zoxide` | `cd` | Learns your habits, jump anywhere |
| `delta` | `diff` | Beautiful git diffs |
| `lazygit` | - | Git operations without memorizing flags |

### Languages

The script uses version managers instead of installing languages directly:

- **Python**: pyenv (so you can switch between 3.10, 3.11, 3.12, etc.)
- **Node**: nvm (manage multiple Node versions)
- **Rust**: rustup (the official way)
- **Go**: Direct from Homebrew (simpler versioning)

### macOS Tweaks

The script also sets sane macOS defaults:

- Show hidden files in Finder
- Fast key repeat (crucial for vim users)
- Auto-hide dock with no delay
- Screenshots save to `~/Screenshots` as PNG
- Three-finger drag on trackpad

## Customizing

Fork this script and make it yours:

1. **Remove what you don't need** - Don't use Rust? Delete those lines
2. **Add your tools** - Append to the arrays
3. **Change the apps** - Swap VS Code for your editor of choice
4. **Add your dotfiles** - Clone your dotfiles repo at the end

## Keeping It Updated

I keep this script in a gist and update it whenever I find a new tool worth adding. When setting up a new machine:

```bash
curl -fsSL https://gist.githubusercontent.com/YOU/GIST_ID/raw/kickstart.sh | bash
```

Or if you don't trust piping to bash (smart):

```bash
curl -fsSL https://gist.githubusercontent.com/YOU/GIST_ID/raw/kickstart.sh -o kickstart.sh
less kickstart.sh  # Review it
chmod +x kickstart.sh && ./kickstart.sh
```

## Time Saved

Manual setup: ~4 hours of clicking, downloading, configuring
With this script: ~20 minutes of automated installation

That's time better spent actually coding.

---

*Got suggestions for tools I'm missing? Let me know.*
