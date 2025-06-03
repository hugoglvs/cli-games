#!/usr/bin/env bash

text_installed="dependencies installed correctly \n\n"
text_not_installed="dependencies not installed, please refer the problem log above"

get_game_directories() {
    # Find all directories that don't start with "_" and store them in an array
    local game_dirs=()
    while IFS= read -r dir; do
        game_dirs+=("$dir")
    done < <(find . -maxdepth 1 -type d -not -path "*/\.*" -not -path "*/_*" -not -path "." | sed 's|^\./||' | sort)
    echo "${game_dirs[@]}"
}



check_game_files() {
    local game_dir="$1"
    local has_python=false
    local has_node=false

    if [ -f "$game_dir/requirements.txt" ]; then
        has_python=true
    fi
    if [ -f "$game_dir/package.json" ]; then
        has_node=true
    fi

    cd "$game_dir"

    if [ "$has_python" = true ]; then
        echo "Installing Python dependencies for $game_dir..."
        if python3 -m pip install --break-system-packages -r requirements.txt; then
            :
        else
            printf "$game_dir $text_not_installed"
            exit 1
        fi
    fi

    if [ "$has_node" = true ]; then
        echo "Installing Node.js dependencies for $game_dir..."
        npm install . || {
            printf "$game_dir $text_not_installed"
            exit 1
        }

        if [[ -d node_modules ]]; then
            printf "$game_dir $text_installed"
        else
            printf "$game_dir $text_not_installed"
            exit 1
        fi
    fi

    if [ "$has_python" = false ] && [ "$has_node" = false ]; then
        echo "No dependencies files found in $game_dir"
    fi

    cd ..
}

main() {
    printf "Starting game dependencies installation...\n"
    game_dirs=$(get_game_directories)
    for dir in $game_dirs; do
        check_game_files "$dir"
    done
    printf "All dependencies installed successfully.\n"
    exit 0
}

main
