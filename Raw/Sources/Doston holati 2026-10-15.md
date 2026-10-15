---
Title: "Doston holati 2026-10-15"
Author: "Doston"
Reference: "owned-demo"
ContentType:
  - "markdown"
Created: 2026-10-15
Processed: true
tags:
  - "source"
---

<!-- Ikki qismdan iborat: (1) Dostonning o'z so'zlari, Claude Code suhbatidan; (2) lokal loyiha papkalari va git tarixidan olingan faktlar. -->

## 1. Dostonning o'z so'zlari (2026-10-15)

> BMS smart house kompanyasida integrator sifatida ishlayabman. Suniy intelektni
> aqlli uylarga integratsiya qilaman. Agentic engineering va AI automationni
> o'rganyabman va shu yo'nalish bo'yicha o'sishga harakat qilyabman. O'qish
> davom etyabdi, hozir 3-kursdaman.

Qo'shimcha: profildagi "ish qidiryapti" holati eskirgan, uni yangilash kerak.

## 2. Lokal loyihalar kesimi (2026-10-15)

Oxirgi o'zgarish sanasi bo'yicha (Desktop papkalari):

| Papka | Oxirgi o'zgarish | Repo |
|---|---|---|
| fezotback | 2026-10-10 | git yo'q |
| education-crm | 2026-10-07 | Coder-Dostonbe/EduCrm |
| job-agent | 2026-08-07 | Coder-Dostonbe/Job-agent |
| saver bot | 2026-08-03 | git yo'q |

### education-crm (EduFlow CRM)

- README: "Premium CRM for education centers — Next.js frontend + Django REST API."
- Haqiqiy o'zbek o'quv markazi asosida: o'quvchilar, guruhlar, jadval, davomat,
  imtihonlar, moliya, lead pipeline; o'zbek / rus / ingliz tillarida.
- Struktura: `src/` (Next.js App Router), `backend/` (Django 5 + DRF), `docker-compose.yml`.
- `npm run dev` bitta buyruq bilan API va frontendni birga ko'taradi; migratsiya va
  demo data seed qiladi. API docs: `/api/docs/`. `DATABASE_URL` bo'lmasa SQLite.
- Oxirgi commit: "feat: EduFlow CRM — full stack, single-command dev, Google OAuth,
  role-scoped student experience".
- Repoda `AGENTS.md`, `CLAUDE.md`, `WORKFLOW.md` bor (agentlar bilan ishlash).

### fezotback (Fezot Shop)

- CLAUDE.md: bitta app'li Django e-commerce do'kon (kiyim, brend "fezot"),
  uch tilli UI (uz/ru/en). Loyiha paketi `core`, domen logikasi `shop` app'ida.
- SQLite; API qatlami ishlatilmaydi — server-side template'lar, faqat AJAX
  cart/wishlist/filter endpointlari JSON qaytaradi.
- Asosiy bog'liqliklar: Django 6.0.2, pillow, django-modeltranslation,
  django-widget-tweaks, django-allauth.
- Model tarjimalari qo'lda qilingan (modeltranslation registratsiyasisiz).
- Multi-agent koordinatsiya fayllari bor (`active_files.md`, `active_tasks.md`).

### job-agent

- README: kuniga bir marta hh.uz, OLX.uz va Telegram kanallaridan vakansiya yig'adi,
  vakansiya emaslarini filtrlaydi (kalit so'z + Claude Haiku), profilga qarab ballaydi,
  Telegram'ga digest yuboradi.
- Oxirgi commitlar: "feat(report): rank every vacancy instead of hiding the low ones",
  "feat(health): catch the half-broken scraper, not just the dead one",
  "feat(ci): notify when the run dies before Python can speak".

### saver bot

- `pyTelegramBotAPI` + `telethon==1.36.0` + `qrcode`.
- Foydalanuvchi QR kod orqali o'z Telegram akkauntini ulaydi (2FA qo'llab-quvvatlanadi),
  bot chatlarni ro'yxat qilib ko'rsatadi, tanlangan manba chatdan maqsad chatga
  xabarlarni nusxalaydi (`copy_messages`), FloodWait'ni ushlaydi, logout bor.

## 3. Dostonning qo'shimcha so'zlari (2026-10-15, keyinroq)

> Men Home Assistant bilan tanishish bosqichidaman. Zigbee protokolini o'rgandim.
> Ishni to'liq boshlamaganman hali, sinov bosqichidaman — 2 kundan beri. Bir hafta
> deyilgan sinov davri, keyin stajor davriga o'taman. [Maosh shartlari — shaxsiy,
> `Drafts/` da saqlanadi.] Agentic engineeringga kelsam, o'zim sun'iy intellekt
> agentlari yasamoqchiman va shu orqali zamonaviy dasturlash olamiga kirib
> bormoqchiman.

Hisoblangan sanalar: sinov taxminan 2026-10-13 da boshlangan, ~2026-10-20 gacha;
so'ng 1 oylik stajirovka (~2026-11-20 gacha), keyin maosh oshadi.
