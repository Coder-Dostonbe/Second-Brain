---
tags:
  - "log"
topics:
  - "O'zbekiston IT Ish Bozori"
status: seed
created: 2026-08-07
updated: 2026-08-07
sources:
  - "Raw/Sources/Ish bozori digesti 2026-08-07.md"
  - "Raw/Sources/Job Agent Vault Eksporti.md"
source_count: 2
aliases: []
---

# Ingest Job Agent Digest

## Nima o'zgardi

`job-agent` endi kunlik ish bozori digestini shu vaultning `Raw/Sources/`
qatlamiga o'zi yozadi. Ikkita yangi xom manba tushdi: agent yozgan
`Ish bozori digesti 2026-08-07` va agent hujjatlaridan yig'ilgan
`Job Agent Vault Eksporti`.

Ular ustidan uchta nota kompilyatsiya qilindi:

- [[O'zbekiston IT Ish Bozori]] — topic, hozircha bitta kunlik kesim.
- [[Kunlik Digest Eksporti]] — concept, tashqi agent vaultga yozishining
  qoidalari.
- [[Job Agent Vault Integratsiyasi]] — project, holat va cheklovlar.

## Nega

Hisobot Telegram'ga tushib, bir hafta o'tmay qidirib bo'lmaydigan holga
kelardi. Agentning o'z bazasidan ham tiklab bo'lmasdi: u faqat `url, source,
title, score, ai_score` ni saqlaydi, kompaniya/maosh/AI izohi esa run tugashi
bilan yo'qolardi. Vault aynan shu ma'lumotni saqlash uchun mos.

## E'tiborga olinishi kerak

Birinchi kesimni tendensiya deb o'qib bo'lmaydi: lokal run'da AI tahlili
umuman ishlamagan, Telegram kanallari yig'ilmagan, to'rtta e'lonning tavsifi
yuklanmagan. Skill statistikasi yuklangan tavsiflar ustidan hisoblanadi, ya'ni
u bozorni emas, o'qilgan matnlarni o'lchaydi.
