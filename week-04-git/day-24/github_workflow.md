# GitHub Workflow

## Remote

- `git remote -v` — показать подключённые удалённые репозитории
- `git remote add name url` — добавить новый remote
- `git remote remove name` — удалить remote

## Fetch vs Pull

- `git fetch origin` — скачать изменения, не сливая
- `git pull origin main` — скачать и сразу слить в текущую ветку

## Ветки

- `git push -u origin branch-name` — отправить ветку на GitHub и связать с локальной
- `git branch -r` — показать удалённые ветки

## Workflow в команде

1. Создать ветку от `main`
2. Работать в ней, коммитить
3. Запушить ветку на GitHub
4. Открыть Pull Request
5. Пройти code review
6. Слить в `main` после одобрения