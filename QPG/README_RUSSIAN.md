# QGP (Quantum Good Privacy)

Инструмент CLI для безопасного обмена сообщениями, который сочетает:
- ECC (Curve25519)
- Постквантовый обмен ключами (Kyber512)
- Сквозное и будущее шифрование (Double Ratchet)
- Децентрализованный отзыв ключей через IPFS PubSub

---

## Требования

- Python 3.8 или выше
- (Опционально) IPFS-демон на localhost:5001 для отзыва ключей
- Virtualenv (рекомендуется)

---

## Установка

```bash
cd ~/Desktop/QPG
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install ipfshttpclient zstd kyber-py
```

> После установки в PATH будет доступна команда `qgp`.

---

## Структура хранения ключей

Ключи размещаются в `~/.qgp/keys/`:

```text
<label>_ecc.sk   — приватный ECC-ключ (Curve25519)
<label>_ecc.pk   — публичный ECC-ключ
<label>_pq.sk    — приватный постквантовый ключ (Kyber)
<label>_pq.pk    — публичный постквантовый ключ
```

---

## Настройки и логи

- Конфиг: `~/.qgp/config.json`
- Логи:   `~/.qgp/qgp.log`

При необходимости измените `ipfs_address` или `revocation_topic`.

---

## Команды CLI

### keygen
Генерация пары ключей ECC + PQ:
```bash
qgp keygen --label <метка>
```
- `--label`: имя пары (по умолчанию `default`)

### list-keys
Список доступных меток:
```bash
qgp list-keys
```

### send
Шифрование и вывод данных для отправки:
```bash
qgp send \
  --sender <ваша_метка> \
  --to <метка_получателя> \
  --msg "<текст сообщения>"
```
**Вывод:**
```text
# PQ KEM ciphertext (hex): <PQCT_HEX>
# Nonce (hex):               <NONCE_HEX>
# Ciphertext (hex):          <CT_HEX>
```

### receive
Дешифрование полученных данных:
```bash
qgp receive \
  --sender <ваша_метка> \
  --from <метка_отправителя> \
  --pqct <PQCT_HEX> \
  --nonce <NONCE_HEX> \
  --ciphertext <CT_HEX>
```
**Вывод:**
```text
Decrypted message: <оригинальный текст>
```

### revoke
Публикация отзыва ключа:
```bash
qgp revoke --key <метка> [--reason "<причина>"]
```
Печатает CID записи отзыва.

### subscribe
Подписка на уведомления об отзыве:
```bash
qgp subscribe
```
Нажмите Ctrl+C для выхода.

---

## Пример работы

1. Генерация ключей:
   ```bash
   qgp keygen --label bob
   qgp keygen --label alice
   ```
2. Отправка сообщения (Bob → Alice):
   ```bash
   qgp send --sender bob --to alice --msg "Привет, Alice!"
   ```
3. Получение и расшифровка (Alice):
   ```bash
   qgp receive --sender alice --from bob \
     --pqct <PQCT_HEX> --nonce <NONCE_HEX> --ciphertext <CT_HEX>
   ```
4. Отзыв ключа (Bob отзывает Alice):
   ```bash
   qgp revoke --key alice --reason "компрометация"
   qgp subscribe
   ```

---

**Лицензия:** MIT License © <YEAR> <ВАШЕ ИМЯ>
```
