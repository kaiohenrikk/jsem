import sys
import subprocess
import os

if len(sys.argv) < 3:
    print("❌ Uso: jsem <mvn|gradle> <NomeDoProjeto>")
    sys.exit(1)

tool = sys.argv[1].lower()
project = sys.argv[2]

script_dir = os.path.dirname(os.path.abspath(__file__))

if tool == "mvn":
    target_script = os.path.join(script_dir, "java_mvn_env_manager.py")
elif tool == "gradle":
    target_script = os.path.join(script_dir, "java_gradle_env_manager.py")
else:
    print(f"❌ Ferramenta não reconhecida: {tool}. Use 'mvn' ou 'gradle'.")
    sys.exit(1)

if not os.path.exists(target_script):
    print(f"❌ Script de ferramenta não encontrado: {target_script}")
    sys.exit(1)

subprocess.run(["python", target_script, project])