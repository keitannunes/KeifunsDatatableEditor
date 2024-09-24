# Variables
NAME = KeifunsDatatableEditor
MAIN_FILE = main.py
ICON = ./src/assets/icon.ico
ASSETS_DIR = ./src/assets
TEMPLATES = ./templates
BIN = ./bin/*
VERSION_FILE = ./version_info.txt

# PyInstaller command
PYINSTALLER = pyinstaller

# PyInstaller options
PYINSTALLER_OPTS = --onefile --windowed --icon=$(ICON) --name $(NAME) --version-file=$(VERSION_FILE)
PYINSTALLER_DEBUG_OPTS = --onefile --icon=$(ICON) --name "$(NAME) Debug" --version-file=$(VERSION_FILE)


# Build command
.PHONY: build
build: clean
	$(PYINSTALLER) $(PYINSTALLER_OPTS) \
		--add-data "$(ASSETS_DIR);src/assets" \
		--add-data "$(TEMPLATES);templates" \
		--add-binary "$(BIN);bin" \
		$(MAIN_FILE)

.PHONY: debug
debug:
	$(PYINSTALLER) $(PYINSTALLER_DEBUG_OPTS) \
		--add-data "$(ASSETS_DIR);src/assets" \
		--add-data "$(TEMPLATES);templates" \
		--add-binary "$(BIN);bin" \
		$(MAIN_FILE)

# Clean command
.PHONY: clean
clean:
	@echo "Cleaning previous builds..."
	@if exist dist rmdir /S /Q dist
	@if exist build rmdir /S /Q build
	@if exist $(NAME).spec del /F /Q $(NAME).spec