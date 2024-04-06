# List available commands
default:
    just --list --unsorted --list-heading $'Available commands\n'

# Send encoded multipart data
send:
    #!/bin/zsh

    . $HOME/.rye/env
    . .venv/bin/activate

    python sender/main.py

# Bootstrap repo for development
bootstrap:
    #!/bin/zsh

    curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
    . $HOME/.rye/env
    rye sync
