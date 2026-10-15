---
tags:
  - "concept"
topics:
  - "O'zbekiston IT Ish Bozori"
status: seed
created: 2026-08-07
updated: 2026-08-07
sources:
  - "Raw/Sources/Job Agent Vault Eksporti.md"
source_count: 1
aliases:
  - "Digest Eksporti"
---

# Kunlik Digest Eksporti

## Ta'rif

Tashqi agent har kuni ishlab, natijasini vaultning `Raw/Sources/` qatlamiga
Markdown fayl qilib yozadigan naqsh. Agent vaultga faqat **xom dalil** qo'shadi;
undan Wiki notasi kompilyatsiya qilish odam va agent ishi bo'lib qoladi
([[Raw Source Vs Wiki Note]]).

Amaldagi misol: `job-agent` kunlik ish bozori digestini yozadi — qarang
[[Job Agent Vault Integratsiyasi]].

## Nega chat emas, fayl

Yetkazish kanali (Telegram, email) xabarni bir marta o'qitadi va keyin ko'madi.
Undan ham muhimi: agentning **o'z bazasi ham** hamma narsani saqlamaydi. Job
Agent bazasida `url, source, title, score, ai_score` bor, lekin kompaniya,
maosh, AI verdikti va CV maslahati faqat hisobot qurilayotgan paytda mavjud.
Ya'ni vaultga yozilmasa, ular hech qayerda qolmaydi.

Shundan qoida: **eksport ma'lumot hali to'liq turgan nuqtada olinadi**, keyin
bazadan qayta yig'ilmaydi.

## Naqshning qoidalari

- **Yuborishdan oldin yozish.** Eksport yetkazishdan oldin bajariladi, shunda
  yozuv yiqilsa ogohlantirish o'sha kunning xabariga tushadi. Keyin
  bajarilganda xatoni faqat log ko'radi — vault oylab jimgina bo'sh qolishi
  mumkin.
- **Fayl nomi sanaga bog'lanadi.** Kun ichidagi takroriy run avvalgi faylni
  yangilaydi, ikkinchi nusxa yaratmaydi.
- **Papka yaratilmaydi.** Yo'l xato bo'lsa `mkdir` uni "muvaffaqiyat" qilib
  ko'rsatardi va fayllar hech kim qaramaydigan papkaga oqib ketaverardi.
  Mavjud bo'lmagan vault — sozlama xatosi, ogohlantirish sababi.
- **Eksport hech qachon istisno ko'tarmaydi.** Vault — yon mahsulot; u
  yiqilgani uchun asosiy ish yo'qolmasligi kerak. Lekin jim ham qolmaydi:
  nosozlik agentning diagnostika qatorida ko'rinadi.
- **Matn zararsizlantiriladi, tozalanmaydi.** Tashqi matndan kelgan
  `[[wikilink]]`, qator boshidagi `#` va alohida `---` — uchalasi ham
  Obsidian'da ma'no kasb etadi. Ular ma'nosidan mahrum qilinadi, lekin matn
  o'qilishicha qoladi.
- **`Processed: false` — agentning ishi emas.** Uni `true` ga o'tkazish faqat
  Wiki notasi yozilgandan keyin, `source-scan --update` orqali bo'ladi.
  Yozilmagan notani "qayta ishlangan" deb belgilash vaultning eng muhim
  invariantini buzadi.

## Nima yozilmaydi

Agent Wiki notasini o'zi yozmaydi. Sabab shakli emas, ishonchi: xom digest —
o'lchov, Wiki notasi esa xulosa. Xulosani o'lchov bilan bir vaqtda, bir
manbadan avtomat yozib qo'yish [[Raw Source Vs Wiki Note]] ajratmasini
ma'nosiz qiladi.

## Ochiq savollar

- Kunlik fayllar yig'ilib ketganda ularni qanday siqish kerak — oylik
  jamlanma manba, yoki eskilarini arxivga ko'chirish?
