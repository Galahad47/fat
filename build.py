import PyInstaller.__main__
import shutil
import os
import subprocess
import sys

# Конфигурация
APP_NAME = "AudioToText"
ENTRY_SCRIPT = "prog_ver_1.py"
ICON_PATH = "icon.ico" if os.path.exists("icon.ico") else None
WORK_PATH = "build"
DIST_PATH = "dist"
INSTALLER_SCRIPT = "AudioToText.nsi"

def build_exe():
    cmd = [
        '--name', APP_NAME,
        '--windowed',
        '--workpath', WORK_PATH,
        '--distpath', DIST_PATH,
        '--add-data', 'logo.png;.',
        '--add-data', 'large-v3.pt;.',
        '--add-binary', 'ffmpeg/bin/ffmpeg.exe;ffmpeg/bin',
        '--add-binary', 'ffmpeg/bin/ffprobe.exe;ffmpeg/bin',
    ]
    
    if ICON_PATH:
        cmd.extend(['--icon', ICON_PATH])
    
    cmd.append(ENTRY_SCRIPT)
    
    PyInstaller.__main__.run(cmd)

def create_installer():
    nsis_script = f"""
    !define APP_NAME "{APP_NAME}"
    !define COMP_NAME "Отдел ЦЦТ Ковалёв А.С."
    !define WEB_SITE "https://kunstkamera.ru"
    !define VERSION "0.0.1 - beta"
    !define COPYRIGHT "© 2025 Kunstkamera"
    !define DESCRIPTION "Audio to Text"
    !define INSTALLER_NAME "setup_{APP_NAME}.exe"
    !define MAIN_APP_EXE "{APP_NAME}.exe"
    
    ; Установка русского языка
    !include "MUI2.nsh"
    !insertmacro MUI_LANGUAGE "Russian"
    
    ; Настройки
    Name "${{APP_NAME}}"
    OutFile "${{INSTALLER_NAME}}"
    InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
    SetCompressor /SOLID lzma
    RequestExecutionLevel admin
    
    ; Страницы установщика
    !insertmacro MUI_PAGE_WELCOME
    !insertmacro MUI_PAGE_LICENSE "license.txt"
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    
    ; Страницы удаления
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    
    Section "MainSection" SEC01
        SetOutPath "$INSTDIR"
        File /r "{os.path.join(DIST_PATH, APP_NAME)}\\*.*"
        
        ; Создаем папку для результатов
        CreateDirectory "$INSTDIR\\Результаты"
        
        ; Создаем ярлыки
        CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}.lnk" "$INSTDIR\\${{MAIN_APP_EXE}}"
        CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{MAIN_APP_EXE}}"
    SectionEnd
    
    Section -Post
        ; Создаем деинсталлятор
        WriteUninstaller "$INSTDIR\\uninstall.exe"
        
        ; Добавляем запись в реестр
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" \
            "DisplayName" "${{APP_NAME}}"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" \
            "UninstallString" "$INSTDIR\\uninstall.exe"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" \
            "Publisher" "${{COMP_NAME}}"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" \
            "URLInfoAbout" "${{WEB_SITE}}"
    SectionEnd
    
    Section "Uninstall"
        ; Удаляем файлы
        RMDir /r "$INSTDIR"
        
        ; Удаляем ярлыки
        Delete "$SMPROGRAMS\\${{APP_NAME}}.lnk"
        Delete "$DESKTOP\\${{APP_NAME}}.lnk"
        
        ; Удаляем запись из реестра
        DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
    SectionEnd
    """
    
    with open(INSTALLER_SCRIPT, "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    try:
        subprocess.run(f'makensis "{INSTALLER_SCRIPT}"', check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка создания установщика: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Создаем временную лицензию (можно заменить реальным файлом)
    if not os.path.exists("license.txt"):
        with open("license.txt", "w", encoding="utf-8") as lic:
            lic.write("Лицензионное соглашение\n")
    
    build_exe()
    
    # Копируем дополнительные файлы
    app_dir = os.path.join(DIST_PATH, APP_NAME)
    os.makedirs(app_dir, exist_ok=True)
    
    # Копируем необходимые файлы
    shutil.copy("logo.png", app_dir)
    shutil.copy("large-v3.pt", app_dir)
    shutil.copytree("ffmpeg", os.path.join(app_dir, "ffmpeg"), dirs_exist_ok=True)
    
    create_installer()