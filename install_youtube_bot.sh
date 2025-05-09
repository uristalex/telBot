#!/bin/bash
set -e # Прерывать выполнение при любой ошибке

### Конфигурация цветов ###
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Сброс цвета

### Пути и файлы ###
UNINSTALL_FILE="$HOME/uninstall_$(date +%s).sh" # Файл для удаления
LOG_FILE="/tmp/install_$(date +%s).log" # Лог установки
REPO_URL="https://github.com/uristalex/telBot.git"

### Функция записи действий для последующего удаления ###
log_uninstall() {
  echo "$1" >> "$UNINSTALL_FILE"
}

### Начало работы ###
clear
echo -e "${GREEN}=== Автоматический установщик приложений ===${NC}"

#### Проверка прав ###
#if [ "$EUID" -eq 0 ]; then
#  echo -e "${RED}ОШИБКА: Не запускайте скрипт от root!${NC}"
#  exit 1
#fi

### Получение информации о пользователе ###
USER_NAME=$(whoami)
echo -e "${BLUE}Пользователь: ${USER_NAME}${NC}"

### Запрос URL репозитория ###
# shellcheck disable=SC2162
# read -p "${YELLOW}Введите URL GitHub репозитория: ${NC}" REPO_URL

### Генерация уникальных имен ###
PROJECT_DIR="$HOME/$(basename "${REPO_URL%.git}")_$(date +%s)"
VENV_DIR="$HOME/venv_$(basename "${REPO_URL%.git}")_$(date +%s)"
SERVICE_NAME="$(basename "${REPO_URL%.git}")_service"

### Запись информации для удаления ###
{
  echo "PROJECT_DIR='$PROJECT_DIR'"
  echo "VENV_DIR='$VENV_DIR'"
  echo "SERVICE_NAME='$SERVICE_NAME'"
  echo "REPO_URL='$REPO_URL'"
} > "$LOG_FILE"

### Установка системных зависимостей ###
echo -e "${BLUE}[1/5] Проверка системных зависимостей...${NC}"
sudo apt-get update 2>&1 | tee -a "$LOG_FILE"
sudo apt-get install -y git python3-venv 2>&1 | tee -a "$LOG_FILE"

### Клонирование репозитория ###
echo -e "${BLUE}[2/5] Клонирование репозитория...${NC}"
git clone "$REPO_URL" "$PROJECT_DIR" 2>&1 | tee -a "$LOG_FILE"

### Создание виртуального окружения ###
echo -e "${BLUE}[3/5] Создание виртуального окружения...${NC}"
python3 -m venv "$VENV_DIR" 2>&1 | tee -a "$LOG_FILE"

### Установка зависимостей ###
echo -e "${BLUE}[4/5] Установка пакетов...${NC}"
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt" 2>&1 | tee -a "$LOG_FILE"
else
  echo -e "${YELLOW}Файл requirements.txt не найден${NC}" | tee -a "$LOG_FILE"
fi

### Настройка автозагрузки ###
echo -e "${BLUE}[5/5] Настройка системы...${NC}"
# shellcheck disable=SC2162
read -p "${YELLOW}Добавить в автозагрузку? (y/n): ${NC}" choice

if [[ $choice =~ ^[Yy] ]]; then
  # Создание службы systemd
  sudo tee /etc/systemd/system/"$SERVICE_NAME.service" > /dev/null <<EOF
[Unit]
Description=Service for $SERVICE_NAME
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$PROJECT_DIR
ExecStart=$VENV_DIR/bin/python $PROJECT_DIR/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

  # Активация службы
  sudo systemctl daemon-reload
  sudo systemctl enable "$SERVICE_NAME"
  sudo systemctl start "$SERVICE_NAME"

  # Запись команд удаления
  log_uninstall "sudo systemctl stop $SERVICE_NAME"
  log_uninstall "sudo systemctl disable $SERVICE_NAME"
  log_uninstall "sudo rm -f /etc/systemd/system/$SERVICE_NAME.service"
fi

### Создание скрипта удаления ###
cat > "$UNINSTALL_FILE" <<EOF
#!/bin/bash
set -e

# Автоматически сгенерированный скрипт удаления
echo -e "\033[31m=== Начало удаления ===\033[0m"

# Загрузка параметров установки
source "$LOG_FILE"

# Удаление службы
if systemctl is-active --quiet \$SERVICE_NAME; then
  sudo systemctl stop \$SERVICE_NAME
  sudo systemctl disable \$SERVICE_NAME
fi
sudo rm -f /etc/systemd/system/\$SERVICE_NAME.service
sudo systemctl daemon-reload

# Удаление файлов
[ -d "\$PROJECT_DIR" ] && rm -rf "\$PROJECT_DIR"
[ -d "\$VENV_DIR" ] && rm -rf "\$VENV_DIR"
[ -f "\$LOG_FILE" ] && rm -f "\$LOG_FILE"

echo -e "\033[32mУдаление завершено!\033[0m"
echo -e "Удаленные ресурсы:"
echo -e "• Проект: \$PROJECT_DIR"
echo -e "• Виртуальное окружение: \$VENV_DIR"
echo -e "• Служба: \$SERVICE_NAME"

# Самоудаление скрипта
rm -- "\$0"
EOF

chmod +x "$UNINSTALL_FILE"

### Финал ###
echo -e "${GREEN}Установка завершена!${NC}"
echo -e "Для удаления выполните: ${RED}sudo $UNINSTALL_FILE${NC}"
echo -e "Лог установки: ${BLUE}$LOG_FILE${NC}"
