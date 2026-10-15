---
tags:
  - "project"
topics:
  - "O'zbekiston IT Ish Bozori"
  - "Agentic Engineering va AI Automation"
status: stable
created: 2026-08-07
updated: 2026-10-15
sources:
  - "Raw/Sources/Job Agent Vault Eksporti.md"
  - "Raw/Sources/Ish bozori digesti 2026-08-07.md"
  - "Raw/Sources/Doston holati 2026-10-15.md"
source_count: 3
aliases:
  - "Job Agent"
---

# Job Agent Vault Integratsiyasi

> [!note] 2026-10-15 holati
> Doston ishga kirdi ([[BMS Smart House]]), shuning uchun ish qidiruv
> dolzarbligini yo'qotdi. Endi bu loyiha asosan portfolio va
> [[Agentic Engineering va AI Automation]] bo'yicha tajriba namunasi sifatida
> qadrli: LLM'ni pipeline'ga xavfsiz qo'shish (fail-open filtr, batch'lab
> chaqirish, health check, CI ogohlantirishlari).

## Maqsad

`job-agent` — kuniga bir marta hh.uz, olx.uz va Telegram kanallaridan ish
e'lonlarini yig'ib, filtrlab, ballab, Telegram'ga hisobot yuboradigan agent.
Integratsiyaning maqsadi: o'sha hisobot chatda ko'milib ketmasin, balki shu
vaultga xom manba bo'lib tushsin va ustidan [[O'zbekiston IT Ish Bozori]]
notasi o'ssin.

Umumiy naqsh: [[Kunlik Digest Eksporti]].

## Hozirgi holat

- Agent tomonida `vault_export.py` moduli yozilgan va 15 ta test bilan
  qoplangan (repo bo'ylab 223 ta test o'tadi).
- Lokal mashinada yoqilgan: `.env` da `VAULT_PATH` shu vault ildiziga
  ko'rsatadi.
- Birinchi haqiqiy digest tushdi:
  `Raw/Sources/Ish bozori digesti 2026-08-07.md` (120 e'lon, 47 mos,
  20 hisobotda).
- Agent repozitoriysida o'zgarishlar hali commit qilinmagan — tasdiqlash
  kutilmoqda.

## Ma'lumot yo'li

```
hh.uz / olx.uz / Telegram
        ↓ yig'ish, takrorni tashlash
   "bu ish o'rnimi" filtri (kalit so'z + Claude Haiku)
        ↓
   keyword ball (boshlang'ich 40) → eng yaxshilariga AI tahlili
        ↓
   vault_export  →  Raw/Sources/Ish bozori digesti YYYY-MM-DD.md
        ↓
   Telegram hisoboti
```

Vaultga yozish Telegram'ga yuborishdan **oldin** turadi — sababi
[[Kunlik Digest Eksporti]] da.

## Ma'lum cheklovlar

- **Jadval bo'yicha run'lar vaultga yozmaydi.** `VAULT_PATH` faqat lokal
  mashinada bor; GitHub Actions runnerida vault yo'q. Ya'ni vault faqat
  qo'lda ishga tushirilgan lokal run'lardan to'ladi va kunlar tushib qolishi
  mumkin.
- **Lokal run'da AI tahlili ishlamaydi** — 2026-08-07 digestida birorta AI
  bali yo'q. Actions'dagi run'da kalit bor, lekin u vaultga yozmaydi. Ya'ni
  hozircha "to'liq tahlil" va "vaultga tushish" bir vaqtda bo'lmaydi.
- **Telegram kanallari lokal run'da yig'ilmagan** — 2026-08-07 kesimida
  manbalar faqat hh.uz va olx.uz.

## Keyingi qadamlar

- Bir necha kunlik digest to'plangach [[O'zbekiston IT Ish Bozori]] notasini
  tendensiya bilan yangilash (hozir u bitta kunlik kesimga tayanadi).
- Yuqoridagi birinchi cheklovni hal qilish: Actions'ni vaultga yozdirishning
  yo'li bormi (repoga commit qilish? artefakt?), yoki lokal run'ni jadvalga
  qo'yish kerakmi.
