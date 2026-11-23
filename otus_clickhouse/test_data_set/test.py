import csv
import numpy as np
from datetime import datetime

# Настройки генерации
TOTAL_ROWS = 10_000_000
CHUNK_SIZE = 1_000_000
NUM_ATMS = 2500  # Количество уникальных банкоматов в сети
OUTPUT_FILE = "atm_transactions_10m.csv"

rng = np.random.default_rng(seed=42)

# 1. Создаем справочник уникальных банкоматов (id -> банк, широта, долгота)
banks = np.array([
    "Сбербанк", "ВТБ", "Т-Банк", "Альфа-Банк", 
    "Газпромбанк", "Райффайзенбанк", "Банк Санкт-Петербург", "Совкомбанк"
])

atm_ids = np.array([f"ATM_{i:05d}" for i in range(1, NUM_ATMS + 1)])
atm_banks = rng.choice(banks, size=NUM_ATMS)
atm_lats = np.round(rng.uniform(59.75, 60.0, size=NUM_ATMS), 6)
atm_lons = np.round(rng.uniform(30.0, 30.5, size=NUM_ATMS), 6)

# 2. Диапазон дат: с 01.11.2026 00:00:00 по 23.11.2026 23:59:59
start_ts = int(datetime(2026, 11, 1, 0, 0, 0).timestamp())
end_ts = int(datetime(2026, 11, 23, 23, 59, 59).timestamp())

# Доступные номиналы для реалистичных сумм снятия (кратные 100 руб.)
amounts_pool = np.arange(100, 100001, 100)

print(f"Начинаю генерацию {TOTAL_ROWS:,} строк в файл {OUTPUT_FILE}...")

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "DateTime", "Id_bankomat", "name_bank", 
        "Latitude", "Longitude", "id_transaction", "amount"
    ])

    for start_idx in range(0, TOTAL_ROWS, CHUNK_SIZE):
        # Генерация случайных дат в заданном диапазоне
        timestamps = rng.integers(start_ts, end_ts + 1, size=CHUNK_SIZE)
        datetimes = timestamps.astype("datetime64[s]").astype(str)
        datetimes = np.char.replace(datetimes, "T", " ")

        # Выбор случайных банкоматов из справочника (сохраняет связку ID -> банк + координаты)
        atm_indices = rng.integers(0, NUM_ATMS, size=CHUNK_SIZE)
        batch_atm_ids = atm_ids[atm_indices]
        batch_banks = atm_banks[atm_indices]
        batch_lats = atm_lats[atm_indices]
        batch_lons = atm_lons[atm_indices]

        # Уникальные ID транзакций
        tx_nums = np.arange(start_idx + 1, start_idx + CHUNK_SIZE + 1)
        batch_tx_ids = np.char.add("TXN_", np.char.zfill(tx_nums.astype(str), 10))

        # Суммы снятия (кратные 100, от 100 до 100 000)
        batch_amounts = rng.choice(amounts_pool, size=CHUNK_SIZE)

        # Запись батча в файл
        rows = zip(
            datetimes, batch_atm_ids, batch_banks,
            batch_lats, batch_lons, batch_tx_ids, batch_amounts
        )
        writer.writerows(rows)
        print(f"Сгенерировано: {start_idx + CHUNK_SIZE:,} / {TOTAL_ROWS:,}")

print("Готово!")
