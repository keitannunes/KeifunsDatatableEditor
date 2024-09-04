# Variables
NAME = KeifunsDatatableEditor
MAIN_FILE = main.py
ICON = ./src/assets/icon.ico
ASSETS = ./src/assets/*.png
TEMPLATES = ./templates
BIN = ./bin/*
HOOKS_DIR = ./hooks

# PyInstaller command
PYINSTALLER = pyinstaller

# PyInstaller options
PYINSTALLER_OPTS = --onefile --windowed --icon=$(ICON) --name $(NAME)

# Build command
.PHONY: build
build: clean
	$(PYINSTALLER) $(PYINSTALLER_OPTS) \
		--add-data "$(ASSETS);src/assets/" \
		--add-data "$(TEMPLATES);templates" \
		--add-binary "$(BIN);bin" \
		--additional-hooks-dir=$(HOOKS_DIR) \
		$(MAIN_FILE)

# Clean command
.PHONY: clean
clean:
	@echo "Cleaning previous builds..."
	@if exist dist rmdir /S /Q dist
	@if exist build rmdir /S /Q build
	@if exist $(NAME).spec del /F /Q $(NAME).spec

# Run full setup (clean, hook creation, and build)
.PHONY: all
all: clean create_hook_tja2fumen build

