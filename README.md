# Shutdown Timer

Небольшая утилита на Python + Tkinter для отложенного выключения, гибернации, сна или перезагрузки Windows.

Файлы
- `shutdown.py` — основной скрипт с GUI и логикой таймера.
- `shutdown.exe` — (опционально) собранный исполняемый файл после PyInstaller.
- `build/` — временная папка сборки PyInstaller.

Требования
- Python 3.8+ (рекомендовано 3.10+)
- Библиотека `tkinter` (обычно идёт в стандартной библиотеке на Windows)
- PyInstaller для сборки exe

Установка зависимостей
- PyInstaller устанавливается через pip:

```pwsh
pip install pyinstaller
```

Сборка exe

В корне проекта выполните команду (PowerShell/cmd):

```pwsh
python -m PyInstaller --onefile --windowed --distpath . --workpath build --specpath build shutdown.py
```

Параметры:
- `--onefile` — упаковать в один .exe
- `--windowed` — без консольного окна при старте
- `--distpath .` — поместить готовый exe в текущую папку
- `--workpath build`/`--specpath build` — временные и spec файлы в `build/`

Запуск и тестирование
- После сборки в директории `.` появится `shutdown.exe`. Запустите его двойным кликом.
- Введите часы и минуты и нажмите "Запустить".

Ограничения времени
- Минимальное время: 1 секунда (код проверяет `seconds > 0`).
- Максимум: 24 часа (ограничение в коде — 86400 секунд).

Поддерживаемые режимы
- `hibernate` — гибернация (выполняется `rundll32.exe powrprof.dll,SetSuspendState Hibernate`).
- `sleep` — переход в спящий режим (выполняется `rundll32.exe powrprof.dll,SetSuspendState Sleep`).
- `shutdown` — выключение (`shutdown /s`).
- `restart` — перезагрузка (`shutdown /r`).

Как формируется команда
- В зависимости от выбранного режима формируется одна из команд:
	- `timeout /t <seconds> /nobreak && rundll32.exe powrprof.dll,SetSuspendState Hibernate`
	- `timeout /t <seconds> /nobreak && rundll32.exe powrprof.dll,SetSuspendState Sleep`
	- `timeout /t <seconds> /nobreak && shutdown /s`
	- `timeout /t <seconds> /nobreak && shutdown /r`
- Команда запускается через `cmd` в новом консольном окне с помощью `subprocess.Popen(..., creationflags=CREATE_NEW_CONSOLE)`.

Поведение консольного окна
- При срабатывании таймера появится отдельное окно cmd, выполняющее `timeout` и затем вызывающее выбранную системную команду. Это намеренное поведение текущей реализации.
- Если вам нужно убрать видимое окно, варианты:
	- заменить `timeout` на собственный Python‑таймер (в отдельном потоке) и вызвать `shutdown` через `subprocess.Popen` с `creationflags=subprocess.CREATE_NO_WINDOW`;
	- или запускать `cmd` с флагами, скрывающими окно (но `timeout` в скрытом окне может не вести себя ожидаемо).

Примечания и предупреждения
- Команды `rundll32.exe powrprof.dll,SetSuspendState ...` зависят от настроек питания Windows и могут требовать прав/настроек для корректной работы.
- Убедитесь, что в папке проекта нет локального файла `shutdown.exe`, если вы тестируете упакованный файл; это может привести к конфликту имён.





