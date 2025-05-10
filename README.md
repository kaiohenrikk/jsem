# Gerenciador de Setup para Java & Ferramentas de Build

Este script foi desenvolvido para facilitar a configuração das variáveis de ambiente `JAVA_HOME`, `PATH:mavenbin` e `PATH:gradlebin` no Windows. Com ele, você pode configurar rapidamente diferentes versões do JDK, Maven e Gradle para diferentes ambientes.

**IMPORTANTE:** Caso tenha o Maven, o JDK e o Gradle já configurados nas suas variáveis de ambiente, o ideal é apagá-los para garantir que o script funcione como o esperado.

## Requisitos

- **Python 3.x** instalado na sua máquina.
- **Permissões de administrador** para alterar as variáveis de ambiente do sistema.
- **JDK**, **Maven** e **Gradle** baixados no computador em um diretório de sua escolha.

## Passo a Passo

### 1. Instalar o Python 3

Caso ainda não tenha o Python 3 instalado, siga os passos abaixo:

1. Acesse a página de [downloads do Python](https://www.python.org/downloads/).
2. Baixe a versão mais recente do Python 3 e siga as instruções de instalação.
3. Durante a instalação, **marque a opção "Add Python to PATH"** para garantir que o Python seja adicionado às variáveis de ambiente do sistema.
4. Após a instalação, verifique se o Python foi instalado corretamente executando o seguinte comando no terminal:

```bash
python --version
```

Caso o Python tenha sido instalado corretamente, o terminal irá exibir a versão do Python.

### 2. Rodar script de instalação do JSEM
- É necessário estar no diretório `jsem`.
- E, então, basta executar o comando:
```bash
python install_jsem.py
```

### 3. Adicionar os setups no arquivo `config.json`
- Existe um modelo que deve ser seguido já exemplificado no arquivo;
- Basta adicionar o caminho para o JDK em questão e o caminho para o mavenbin ou gradlebin em questão.

## 4. Utilização do script
- Basta rodar em um terminal com privilégios de ADMIN:
```bash
jsem <mvn|gradle> <CHAVE_OBJETO_EM_CONFIG>
```