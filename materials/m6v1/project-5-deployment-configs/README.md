## Ссылки
- Systemd за пять минут https://habr.com/ru/companies/slurm/articles/255845/
- Supervisor http://supervisord.org/
- Как установить и настроить SSH https://help.reg.ru/support/servery-vps/oblachnyye-servery/rabota-s-serverom/kak-ustanovit-i-nastroit-ssh#4
- SSH клиент для Windows KiTTY https://www.9bis.net/kitty/#!index.md
- FileZilla https://filezilla-project.org/
- Как создать пользователя в Linux https://linuxize.com/post/how-to-create-users-in-linux-using-the-useradd-command/
- Создать домашнюю директорию для пользователя https://askubuntu.com/questions/335961/how-can-i-retrospectively-create-a-default-home-directory-for-an-existing-user-i
- Как вывести список пользователей в Linux https://linuxize.com/post/how-to-list-users-in-linux/
- Как посмотреть полный лог сервиса в systemctl https://unix.stackexchange.com/questions/225401/how-to-see-full-log-from-systemctl-status-service


## Пример конфига сервиса

```ini
[Unit]
Description=Python Bot
After=network.target

[Service]
User=john
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=/var/projects/demo-bot
ExecStart=/var/projects/demo-bot/venv/bin/python main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Команды

Проверить версию systemd
```shell
systemd --version
```

Проверить установленный systemd
```shell
dpkg -l | grep systemd
```

Обновить пакеты перед установкой новых
```shell
apt update && apt upgrade -y
```

Установить systemd (если ещё не установлен)
```shell
apt install -y systemd
```

Проверить, доступен ли `adduser`
```shell
which adduser
```

Добавить `/sbin` в `PATH` (если ещё не)
```shell
export PATH=$PATH:/sbin
```

Установить `adduser`, если ещё не установлен
```shell
apt install -y adduser
```

Установить `sudo`, если ещё не установлен
```shell
apt install -y sudo
```

Добавить пользователя `john` и создать ему домашнюю директорию `/home/john`
```shell
useradd -m john
```

Проверить, что пользователь создан
```shell
grep john /etc/passwd
```

Если домашняя директория не создана, создать для пользователя `john`
```shell
mkhomedir_helper john
```

Установить пароль пользователю `john`
```shell
passwd john
```

Добавить пользователю `john` разрешение на использование `sudo`
```shell
adduser john sudo
```

Проверить версию `python3`
```shell
python3 -V
```

Установить python virtual env
```shell
apt install python3.11-venv
```

Зайти от имени пользователя `john`
```shell
su john
```

Перейти в папку с кодом бота (укажите настоящий путь)
```shell
cd ~/projects/bot
```

Создать виртуальное окружение
```shell
python3 -m venv venv
```

Активировать виртуальное окружение
```shell
source venv/bin/activate
```

Установить зависимости (в активированное окружение)
```shell
pip install -r requirements.txt
```

Вывести полный путь к файлу
```shell
readlink -f bot.service
```

Добавить ссылку на файл в папку systemd
```shell
ln -s {from-file} /etc/systemd/system/bot.service
```

Проверить содержимое папки system
```shell
ls -l /etc/systemd/system/
```

Обновить список сервисов в systemd
```shell
sudo systemctl daemon-reload
```

Включить автозапуск сервиса (например, после перезагрузки)
```shell
sudo systemctl enable bot-demo
```

Запустить сервис
```shell
sudo systemctl start bot-demo
```

Остановить сервис
```shell
sudo systemctl stop bot-demo
```

Открыть логи сервиса
```shell
sudo journalctl -u bot-demo
```

Вывести последние 30 строчек логов сервиса
```shell
sudo journalctl --unit=bot-demo -n 30 --no-pager
```

Вывести логи сервиса за последние 5 минут
```shell
sudo journalctl --unit=bot-demo --since "5 minutes ago" --no-pager
```

Вывести логи сервиса за последний час
```shell
sudo journalctl --unit=bot-demo --since "1 hour ago" --no-pager
```
