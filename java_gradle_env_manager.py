import subprocess
import os
import sys
import json
import ctypes
from pathlib import Path

def require_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print("🔴 É necessário rodar o script em um terminal com privilégios de ADMIN.")
        sys.exit(1)

def load_config() -> dict:
    config_path = Path(__file__).parent / 'config.json'
    if not config_path.exists():
        print(f"❌ Arquivo de configuração não encontrado: {config_path}")
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)

def get_env_name() -> str:
    if len(sys.argv) < 2:
        print("❌ Nenhum nome de ambiente fornecido. Uso: jsem gradle <NomeDoAmbiente>")
        sys.exit(1)
    return sys.argv[1]

def set_java_home(java_home: str):
    current = subprocess.run(
        ['powershell', '-Command', '[Environment]::GetEnvironmentVariable("JAVA_HOME", "Machine")'],
        capture_output=True, text=True
    ).stdout.strip()

    if current.lower() != java_home.lower():
        subprocess.run(['setx', 'JAVA_HOME', java_home, '/M'], shell=True)
        print(f"✅ JAVA_HOME definido como variável de ambiente do sistema: {java_home}")
    else:
        print(f"ℹ️ JAVA_HOME já está corretamente configurado: {java_home}")

def get_user_path_entries() -> list[str]:
    result = subprocess.run(
        ['powershell', '-Command', '[Environment]::GetEnvironmentVariable("Path", "User")'],
        capture_output=True, text=True
    )
    return [p.strip() for p in result.stdout.strip().split(';') if p.strip()]

def is_old_java_or_gradle_bin(path: str) -> bool:
    path = path.lower()
    return (
        (("jdk" in path or "java" in path) and path.endswith("bin")) or
        ("gradle" in path and path.endswith("bin"))
    )

def update_user_path(java_bin: str, gradle_bin: str):
    original_entries = get_user_path_entries()
    filtered_entries = []
    removed = []

    for path in original_entries:
        if is_old_java_or_gradle_bin(path) and path.lower() not in [java_bin.lower(), gradle_bin.lower()]:
            removed.append(path)
        else:
            filtered_entries.append(path)

    added_java = java_bin.lower() not in [p.lower() for p in filtered_entries]
    added_gradle = gradle_bin.lower() not in [p.lower() for p in filtered_entries]

    if added_java:
        filtered_entries.append(java_bin)
        print(f"✅ Adicionando java_bin ao PATH do usuário: {java_bin}")
    else:
        print("ℹ️ O binário do JDK já existe no PATH do usuário.")

    if added_gradle:
        filtered_entries.append(gradle_bin)
        print(f"✅ Adicionando gradle_bin ao PATH do usuário: {gradle_bin}")
    else:
        print("ℹ️ O binário do Gradle já existe no PATH do usuário.")

    if removed or added_java or added_gradle:
        new_path = ";".join(filtered_entries)
        subprocess.run(['setx', 'Path', new_path], shell=True)
        print("✅ PATH do usuário atualizado com sucesso.")
        if removed:
            print("🧹 Entradas antigas removidas do PATH:")
            for path in removed:
                print(f"   - {path}")
        if added_java:
            print("✅ O caminho do Java foi adicionado ao PATH.")
        if added_gradle:
            print("✅ O caminho do Gradle foi adicionado ao PATH.")
    else:
        print("ℹ️ Nenhuma alteração foi necessária no PATH do usuário.")

def main():
    require_admin()
    env_name = get_env_name()
    config = load_config()

    if env_name not in config['gradle']:
        print(f"❌ Ambiente '{env_name}' não encontrado na configuração para gradle.")
        sys.exit(1)

    env_config = config['gradle'][env_name]
    java_home = env_config['jdkPath']
    gradle_bin = env_config['gradleBinPath']
    java_bin = os.path.join(java_home, "bin")

    set_java_home(java_home)
    update_user_path(java_bin, gradle_bin)

    print("✅ Processo finalizado.")

if __name__ == "__main__":
    main()