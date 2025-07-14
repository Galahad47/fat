import PyInstaller.__main__
import shutil
import os
import subprocess

# Конфигурация
APP_NAME = "AudioToText";ENTRY_SCRIPT = "prog_ver_1.py";ICON_PATH = "icon.ico";ADDITIONAL_FILES = [("ffmpeg/bin", "ffmpeg/bin"),"logo.png","large-v3.pt"]
INSTALLER_SCRIPT = "AudioToText.nsi"

def build_exe():
    cmd = ["--name=" + APP_NAME,"--onefile","--windowed","--add-binary=ffmpeg/bin;ffmpeg/bin","--add-data=logo.png;.","--add-data=large-v3.pt;.","--icon=" + ICON_PATH if os.path.exists(ICON_PATH) else "",ENTRY_SCRIPT]
    PyInstaller.__main__.run([p for p in cmd if p])

def create_installer():
    nsis_script = f"""
    !define APP_NAME "{APP_NAME}"
    !define COMP_NAME "Отдел ЦЦТ Ковалёв А.С."
    !define WEB_SITE "https://kunstkamera.ru"
    !define VERSION "0.0.1 - beta"
    !define COPYRIGHT "© 2025 Kunstkamera"
    !define DESCRIPTION "Audio to Text v0.0.1 - beta"
    !define INSTALLER_NAME "setup_{APP_NAME}.exe"
    !define MAIN_APP_EXE "{APP_NAME}.exe"
    
    InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
    
    !include "MUI2.nsh"
    
    Name "${{APP_NAME}}"
    OutFile "${{INSTALLER_NAME}}"
    SetCompressor LZMA
    
    !insertmacro MUI_PAGE_WELCOME
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    !insertmacro MUI_LANGUAGE "Russian"
    
    Section "MainSection" SEC01
        SetOutPath "$INSTDIR"
        File /r "dist\\{APP_NAME}\\*.*"
        CreateDirectory "$INSTDIR\\Готовый текст"
        CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}.lnk" "$INSTDIR\\${{MAIN_APP_EXE}}"
        CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{MAIN_APP_EXE}}"
    SectionEnd
    
    Section -Post
        WriteUninstaller "$INSTDIR\\uninstall.exe"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
    SectionEnd
    """
    
    with open(INSTALLER_SCRIPT, "w", encoding="utf-8") as f:
        f.write(nsis_script)
    subprocess.call(f'makensis "{INSTALLER_SCRIPT}"', shell=True)

if __name__ == "__main__":
    build_exe()
    shutil.copytree("ffmpeg", f"dist/{APP_NAME}/ffmpeg")
    shutil.copy("logo.png", f"dist/{APP_NAME}")
    shutil.copy("large-v3.pt", f"dist/{APP_NAME}")
    create_installer()