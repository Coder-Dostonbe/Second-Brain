---
Title: "Job Agent — vault eksporti"
Author: "job-agent (vault_export.py, README.md)"
Reference: "job-agent repo @ 2e97064 — vault_export.py, README.md"
ContentType:
  - "markdown"
Created: 2026-08-07
Processed: true
tags:
  - "source"
---

# Job Agent — vault eksporti

Bu manba `job-agent` repozitoriysining o'z hujjatlaridan yig'ilgan:
`vault_export.py` (modul va funksiya izohlari), `README.md` ning "Second Brain
vault" bo'limi, `config.py` va `main.py` dagi tegishli qatorlar. Kod holati:
2026-08-07, `origin/main` = `2e97064` ustida commit qilinmagan o'zgarish.

## Job Agent nima qiladi

Kunlik agent uchta manbadan ish e'lonlarini yig'adi (hh.uz, olx.uz, Telegram
kanallari), URL bo'yicha takrorlarni tashlaydi, "bu haqiqatan ish o'rnimi"
degan filtrdan o'tkazadi (kalit so'z qoidalari + Claude Haiku), keyword
bo'yicha ballaydi va eng istiqbollilarini chuqurroq AI tahlilidan o'tkazadi.
Natija — Telegram'ga yuboriladigan kunlik hisobot.

Ball hisoblash boshlang'ich qiymati 40. `REPORT_GOOD_SCORE = 40` kesish
chegarasi emas, bo'lim chegarasi: undan yuqorisi asosiy ro'yxatga, pasti
"past ballilar" bo'limiga tushadi. Hech bir topilgan e'lon yashirilmaydi.
Dasturlash bo'lmagan rol `ROLE_PENALTY = -40` oladi, ya'ni rad etilmaydi —
past ballilar ro'yxatida sababi bilan ko'rinib turadi. Ball manfiy bo'la
oladi.

## Nega vaultga yoziladi

Hisobot Telegram'da bir marta o'qiladi va o'sha yerda ko'miladi: kompaniya
nomlari, maosh raqamlari, AI verdiktlari va kunlik skill statistikasi bir
hafta o'tmay qidirib bo'lmaydigan holga keladi.

Bu ma'lumotni agentning o'z bazasidan tiklab bo'lmaydi. `storage.py` faqat
`url, source, title, score, ai_score` ni saqlaydi. Kompaniya, maosh, AI
sababi va CV maslahati faqat hisobot qurilayotgan paytda mavjud — run tugashi
bilan yo'qoladi. Vaultga qimmatlisi esa aynan o'shalar.

## Qanday ishlaydi

- Yoqilishi: `.env` dagi `VAULT_PATH` — vault ildiziga yo'l. Bo'sh bo'lsa
  modul umuman ishga tushmaydi va hisobotda ham ko'rinmaydi.
- Yoziladigan joy: `<VAULT_PATH>/Raw/Sources/Ish bozori digesti YYYY-MM-DD.md`.
- Fayl nomi sanaga bog'langan: kun ichidagi takroriy run avvalgisini
  yangilaydi, ikkinchi nusxa yaratmaydi.
- Eksport hisobot **yuborilishidan oldin** chaqiriladi. Yozuv yiqilsa,
  ogohlantirish o'sha kunning hisobotiga tushadi. Yuborishdan keyin
  chaqirilganda xatoni faqat log ko'rardi, ya'ni vault oylab jimgina bo'sh
  qolishi mumkin edi.
- Papka o'zi yaratilmaydi. Yo'l xato yozilgan bo'lsa `mkdir` uni jimgina
  "muvaffaqiyat" qilib ko'rsatardi va fayllar hech kim qaramaydigan papkaga
  oqib ketaverardi. Mavjud bo'lmagan vault — sozlama xatosi.
- Eksport hech qachon istisno ko'tarmaydi. Vault — hisobotning yon mahsuloti;
  diskda joy qolmagani kunlik hisobotni yo'qotishga arzimaydi. Lekin jim ham
  qolmaydi: xato hisobotning diagnostika qatoriga chiqadi (`vault yozilmadi ⚠️`).

## Matnni zararsizlantirish

E'lon sarlavhasidan chiqadigan uchta belgi Obsidian'da ma'no kasb etadi va
shuning uchun zararsizlantiriladi:

- `[[...]]` — wikilink. "Python [[Junior]] dev" sarlavhasi vaultda mavjud
  bo'lmagan notaga havola yasaydi va grafikni soxta tugunlar bilan to'ldiradi.
- Qator boshidagi `#` — sarlavha yoki teg, hujjat tuzilishini buzadi.
- Alohida qatordagi `---` — frontmatter chegarasi.

Bu tozalash emas, zararsizlantirish: matn o'qilishi kerak bo'lgan holicha
qoladi, faqat sintaktik kuchi olib tashlanadi.

## Processed bayrog'i

Fayl `Processed: false` bilan yoziladi va agent uni hech qachon o'zgartirmaydi.
Uni `true` ga o'tkazish — Wiki notasi yozilgandan keyin vault tomonining ishi
(`wiki_tool.py source-scan --update`). Yozilmagan notani "qayta ishlangan" deb
ko'rsatish vaultdagi eng muhim invariantni buzadi.

## Digest ichida nima bor

Kunlik sarlavha raqamlari (yangi e'lonlar, mos kelganlari, hisobotga
tushgani, ish o'rni emas deb rad etilgani), asosiy ro'yxat (har biri uchun
manba, kompaniya, maosh, tajriba, keyword ball, mavjud bo'lsa AI bali,
verdikti, izohi va CV maslahati, URL), past ballilar ro'yxati, o'sha kuni
so'ralgan skillar statistikasi va manbalar holati qatori.

Tavsifi yuklanmagan vakansiya alohida belgilanadi: uning past bali sifat
haqida emas, ma'lumot to'liqligi haqida gapiradi. Bu belgi bo'lmasa, oylar
o'tib tuzilgan statistika soxta xulosa beradi.

## Cheklov

`VAULT_PATH` faqat lokal mashinada mavjud. GitHub Actions runnerida vault yo'q,
ya'ni jadval bo'yicha ishlaydigan run'lar vaultga yozmaydi — vault to'lishi
qo'lda ishga tushiriladigan lokal run'ga bog'liq.
