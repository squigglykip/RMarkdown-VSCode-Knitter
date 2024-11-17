import os
import platform
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PathFinder:
    @staticmethod
    def find_rstudio_pandoc():
        """Attempt to automatically find RStudio's Pandoc installation"""
        possible_paths = []
        system = platform.system()
        logger.info(f"Detecting Pandoc paths for {system}")
        
        if system == "Windows":
            possible_paths = [
                "C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools",
                "C:/Program Files/RStudio/bin/quarto/bin/tools",
                "C:/Program Files/RStudio/resources/app/bin/pandoc",
                "C:/Program Files/RStudio/bin/pandoc",
                "C:/Users/*/AppData/Local/Programs/RStudio/bin/quarto/bin/tools",
                "C:/Users/*/AppData/Local/RStudio/bin/quarto/bin/tools"
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/RStudio.app/Contents/Resources/app/bin/quarto/bin/tools",
                "/Applications/RStudio.app/Contents/MacOS/quarto/bin/tools",
                "/Applications/RStudio.app/Contents/Resources/app/bin/pandoc",
                "/usr/local/bin/pandoc",
                "~/Library/Application Support/RStudio/bin/quarto/bin/tools"
            ]
        elif system == "Linux":
            possible_paths = [
                "/usr/lib/rstudio/bin/quarto/bin/tools",
                "/usr/lib/rstudio/bin/pandoc",
                "/usr/bin/pandoc",
                "~/.local/share/rstudio/bin/quarto/bin/tools",
                "/opt/rstudio/bin/quarto/bin/tools"
            ]
        
        # Expand user paths
        possible_paths = [os.path.expanduser(p) for p in possible_paths]
        # Expand wildcards in Windows paths
        if system == "Windows":
            expanded_paths = []
            for path in possible_paths:
                if "*" in path:
                    expanded_paths.extend(Path("/").glob(path[3:]))  # Remove "C:/" for glob
                else:
                    expanded_paths.append(Path(path))
            possible_paths = expanded_paths
        
        for path in possible_paths:
            path = Path(path)
            if path.exists():
                logger.info(f"Found Pandoc at: {path}")
                return str(path)
                
        logger.warning("No Pandoc installation found")
        return None

    @staticmethod
    def find_rscript():
        """Attempt to automatically find R installation"""
        system = platform.system()
        logger.info(f"Detecting R installation for {system}")
        
        if system == "Windows":
            # Search in both Program Files directories
            r_paths = [
                Path("C:/Program Files/R"),
                Path("C:/Program Files (x86)/R"),
                Path("C:/Users/*/AppData/Local/Programs/R")
            ]
            
            versions = []
            for base_path in r_paths:
                if base_path.exists():
                    # Get all R versions
                    versions.extend([x for x in base_path.glob("R-*") if x.is_dir()])
            
            if versions:
                latest = max(versions)
                rscript = latest / "bin" / "Rscript.exe"
                if rscript.exists():
                    logger.info(f"Found R at: {rscript}")
                    return str(rscript)
                    
        elif system == "Darwin":
            possible_paths = [
                "/usr/local/bin/Rscript",
                "/Library/Frameworks/R.framework/Resources/bin/Rscript",
                "/opt/homebrew/bin/Rscript",
                "~/Library/R/*/bin/Rscript"
            ]
        elif system == "Linux":
            possible_paths = [
                "/usr/bin/Rscript",
                "/usr/local/bin/Rscript",
                "/opt/R/*/bin/Rscript"
            ]
            
        # For non-Windows systems
        if system != "Windows":
            possible_paths = [os.path.expanduser(p) for p in possible_paths]
            for path in possible_paths:
                # Handle wildcards
                if "*" in path:
                    matches = list(Path("/").glob(path[1:]))  # Remove leading "/" for glob
                    if matches:
                        path = str(max(matches))  # Use latest version if multiple found
                
                if os.path.exists(path):
                    logger.info(f"Found R at: {path}")
                    return path
        
        logger.warning("No R installation found")
        return None