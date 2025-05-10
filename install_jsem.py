import os
import subprocess
import getpass
from pathlib import Path

def get_main_script_path(filename: str) -> str:
    path = Path(__file__).parent / filename
    if not path.exists():
        print(f"❌ Script principal não encontrado em: {path}")
        exit(1)
    return str(path.resolve())

def create_bat_launcher(script_path: str, bat_name: str = "jsem.bat") -> str:
    username = getpass.getuser()
    bat_dir = Path(f"C:/Users/{username}/scripts-bin")
    bat_dir.mkdir(parents=True, exist_ok=True)

    bat_path = bat_dir / bat_name
    bat_content = f'''@echo off
        python "{script_path}" %*
    '''

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    print(f"✅ Atalho '{bat_name}' criado em: {bat_path}")
    return str(bat_dir)

def ensure_path_contains(directory: str):
    result = subprocess.run(
        ['powershell', '-Command', '[Environment]::GetEnvironmentVariable("Path", "User")'],
        capture_output=True, text=True
    )
    user_path = result.stdout.strip()
    path_entries = [p.strip().lower() for p in user_path.split(';')]

    if directory.lower() not in path_entries:
        updated_path = f"{user_path};{directory}"
        subprocess.run(['setx', 'Path', updated_path], shell=True)
        print(f"✅ Diretório '{directory}' adicionado ao PATH do usuário.")

def main():
    script_path = get_main_script_path("java_setup_env_manager.py")
    bat_dir = create_bat_launcher(script_path)
    ensure_path_contains(bat_dir)
    print("🚀 Agora você pode usar o comando: jsem <mvn|gradle> <ConfigKey>")

if __name__ == "__main__":
    main()