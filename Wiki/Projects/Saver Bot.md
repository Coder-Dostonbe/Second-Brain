---
tags:
  - "project"
topics: []
status: seed
created: 2026-10-15
updated: 2026-10-15
sources:
  - "Raw/Sources/Doston holati 2026-10-15.md"
source_count: 1
aliases:
  - "saver bot"
---

# Saver Bot

## Goal

Bir Telegram chatdan boshqasiga xabarlarni nusxalovchi bot. Foydalanuvchi
o'z akkauntini ulaydi, bot shu akkaunt nomidan ishlaydi.

## Status

- `pyTelegramBotAPI` (bot interfeysi) va `telethon` (foydalanuvchi akkaunti)
  birga ishlatiladi.
- Login QR kod orqali, 2FA paroli qo'llab-quvvatlanadi.
- Chatlar inline klaviaturada sahifalab ko'rsatiladi. Manba va maqsad tanlanadi,
  keyin `copy_messages` ishga tushadi. FloodWait ushlanadi, logout bor.
- Oxirgi lokal o'zgarish: 2026-08-03. Papkada git repo yo'q.

## Next steps

- Deploy holatini aniqlash va git'ga olish.

## Related
