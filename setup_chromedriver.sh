#!/bin/bash

function install_dependencies {
    echo "Atualizando o sistema e instalando dependências..."
    sudo apt update
    sudo apt install -y wget unzip
}

function get_chrome_version {
    echo "Obtendo a versão do Google Chrome..."
    google_chrome_version=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
    echo "Versão do Google Chrome encontrada: $google_chrome_version"
}

function get_chromedriver_version {
    echo "Obtendo a versão correspondente do ChromeDriver..."
    base_url="https://chromedriver.storage.googleapis.com"
    chromedriver_version=$(wget -qO- "$base_url/LATEST_RELEASE_$google_chrome_version")
    if [[ -z $chromedriver_version ]]; then
        chromedriver_version=$(wget -qO- "$base_url/LATEST_RELEASE")
    fi
    echo "Versão do ChromeDriver encontrada: $chromedriver_version"
}

function install_chromedriver {
    echo "Baixando o ChromeDriver..."
    wget -N "$base_url/$chromedriver_version/chromedriver_linux64.zip" -P ~/
    echo "Extraindo o ChromeDriver..."
    unzip ~/chromedriver_linux64.zip -d ~/
    echo "Movendo o ChromeDriver para /usr/local/bin..."
    sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
    sudo chmod +x /usr/local/bin/chromedriver
    echo "Limpando arquivos temporários..."
    rm ~/chromedriver_linux64.zip
    echo "Instalação do ChromeDriver concluída!"
}

install_dependencies
get_chrome_version
get_chromedriver_version
install_chromedriver
