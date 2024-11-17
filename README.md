# RMarkdown-VSCode-Knitter

A cross-platform GUI tool that enables knitting R Markdown files to HTML outside of RStudio. Perfect for users who prefer working with R Markdown in VSCode or other text editors.

## Features

- Simple, intuitive GUI interface with dark mode support
- Real-time console output showing knitting progress 
- Automatic detection of R and Pandoc installations
- Cross-platform support (Windows, macOS, Linux)
- Configurable paths for R and Pandoc executables

## Prerequisites

- Python 3.8 or higher
- R installation
- RStudio (for Pandoc) or standalone Pandoc installation
- Required R packages:
  - rmarkdown
  - knitr

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/squigglykip/RMarkdown-VSCode-Knitter.git
   cd RMarkdown-VSCode-Knitter
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This will install required packages like:
   - customtkinter
   - PyYAML
   - packaging

3. Install required R packages:
   ```r
   install.packages(c("rmarkdown", "knitr"))
   ```

4. Install as a Python package (optional):
   ```bash
   # For development install
   pip install -e .
   
   # For regular install
   pip install .
   ```
   This will make the `rmd-knitter` command available globally.

Note: If you have multiple Python versions installed, you may need to use `pip3` instead of `pip`.

## Usage

1. Launch the application:
   - If installed as package: `rmd-knitter`
   - If running from source: `python src/main.py`

2. Select your working directory containing the .Rmd file
3. Choose your .Rmd file
4. Click "Knit to HTML"

## Configuration

The application automatically detects R and Pandoc installations on first run. Supported paths include:

### Windows
- RScript:
  - C:/Program Files/R/R-x.x.x/bin/Rscript.exe
  - C:/Program Files (x86)/R/R-x.x.x/bin/Rscript.exe
  - User-specific installations in AppData

- Pandoc:
  - C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools
  - C:/Program Files/RStudio/bin/pandoc
  - User-specific installations in AppData

### macOS
- RScript:
  - /usr/local/bin/Rscript
  - /Library/Frameworks/R.framework/Resources/bin/Rscript
  - /opt/homebrew/bin/Rscript

- Pandoc:
  - /Applications/RStudio.app/Contents/Resources/app/bin/quarto/bin/tools
  - /Applications/RStudio.app/Contents/Resources/app/bin/pandoc
  - /usr/local/bin/pandoc

### Linux
- RScript:
  - /usr/bin/Rscript
  - /usr/local/bin/Rscript
  - /opt/R/*/bin/Rscript

- Pandoc:
  - /usr/lib/rstudio/bin/quarto/bin/tools
  - /usr/lib/rstudio/bin/pandoc
  - /usr/bin/pandoc

If the automatic detection fails, you can manually set paths through the Settings button.

## Troubleshooting

1. **Path Detection Issues**
   - Use the Settings button to manually set R and Pandoc paths
   - Ensure R and RStudio/Pandoc are properly installed

2. **Knitting Errors**
   - Check R console output in the application window
   - Verify required R packages are installed
   - Ensure working directory contains all necessary files

3. **Package Dependencies**
   - In R, install required packages:
```R
install.packages(c("rmarkdown", "knitr"))
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.