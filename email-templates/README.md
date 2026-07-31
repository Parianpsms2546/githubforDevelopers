# empeo Email Template

เทมเพลตอีเมล HTML แบบ **responsive** (รองรับทั้ง mobile และ desktop) และ **bulletproof**
(แสดงผลถูกต้องบน Outlook desktop, Gmail, Apple Mail, mobile client) สำหรับแบรนด์ empeo

ไฟล์ในโฟลเดอร์นี้:

| ไฟล์ | คำอธิบาย |
|------|----------|
| `empeo-account-deletion.html` | เทมเพลตอีเมลแจ้ง "อนุมัติคำขอลบบัญชี" ตามดีไซน์ที่ให้มา |

---

## ✨ คุณสมบัติ

- **Responsive** — ปรับตาม mobile / desktop อัตโนมัติด้วย `@media` query + fluid tables
- **รองรับ Outlook** — ใช้ table-based layout, MSO conditional comments, และปุ่ม VML (`v:roundrect`)
  เพื่อให้ปุ่มโค้งมนแสดงผลถูกต้องบน Outlook for Windows
- **Dark mode** — มี `@media (prefers-color-scheme: dark)` + รองรับ Outlook.com (`[data-ogsc]`)
- **Preheader text** — ข้อความ preview ในกล่อง inbox
- **Merge field** — `{{FULL_NAME}}` สำหรับใส่ชื่อผู้รับ
- **ฟอนต์ Thai** — ใช้ `Prompt` (Google Fonts) เป็น fallback ของ GoFive Font และ `Tahoma`
  สำหรับ Outlook (ซึ่ง render ภาษาไทยได้ดี)

---

## 🖼️ รูปโลโก้ — host แล้ว ✅

รูปทั้ง 4 ถูก commit ไว้ใน `email-templates/assets/` และ **ผูก URL ในไฟล์ HTML ให้เรียบร้อยแล้ว**
ผ่าน **jsDelivr CDN** (ดึงจาก repo นี้ ล็อกที่ commit เพื่อให้ cache นิ่ง):

| ตำแหน่ง | ไฟล์ | ขนาดแสดงผล |
|---------|------|-----------|
| Header | `assets/empeo-logo.png` | 140 × 34 px |
| Footer | `assets/powered-by-empeo.png` | 120 × 30 px |
| Footer | `assets/icon-facebook.png` | 28 × 28 px |
| Footer | `assets/icon-youtube.png` | 28 × 28 px |

รูปแบบ URL ที่ใช้:
```
https://cdn.jsdelivr.net/gh/Parianpsms2546/githubforDevelopers@<commit-sha>/email-templates/assets/<file>.png
```

> ⚠️ **jsDelivr ใช้ได้เฉพาะ repo แบบ public** — ถ้า repo นี้เป็น private รูปจะไม่ขึ้น
> ให้ย้ายรูปทั้ง 4 ไป host บน CDN/S3/Cloudflare R2 หรือ storage ของ ESP แล้วแก้ 4 URL ในไฟล์ HTML แทน
>
> 🔁 **อยากใช้โลโก้ official จาก Figma/Brand?** แค่นำไฟล์มาแทนใน `assets/` (ใช้ชื่อไฟล์เดิม)
> แล้ว commit — โครง URL ไม่ต้องแก้ (ถ้าใช้ commit ใหม่ ให้อัปเดต `<commit-sha>` ใน URL ให้ตรง)

> 💡 โลโก้ในโฟลเดอร์นี้เป็นเวอร์ชันที่วาดใหม่ให้ตรงต้นฉบับ (สี Flame `#F1592A`, PNG พื้นหลังโปร่งใส)

---

## 🔗 ขั้นตอนที่ 2 — แก้ลิงก์ให้ตรงจริง

ในไฟล์ HTML แก้ URL เหล่านี้ให้ตรงกับของจริง:

- ปุ่ม **ติดต่อเรา** → `https://www.empeo.com/contact`
- **Help Center** → `https://help.empeo.com`
- **Facebook** → `https://www.facebook.com/empeoHR`
- **YouTube** → `https://www.youtube.com/@empeo`
- โลโก้ header ลิงก์ไป → `https://www.empeo.com`

---

## 📤 ขั้นตอนที่ 3 — นำขึ้นใช้จริง

### ผ่าน ESP / Email marketing (SendGrid, Mailchimp, Amazon SES, Brevo ฯลฯ)

1. คัดลอกเนื้อหาทั้งหมดในไฟล์ `.html`
2. สร้าง campaign/template ใหม่ แล้วเลือกโหมด **"Paste in code" / "Custom HTML"**
3. วางโค้ด แล้ว map field ผู้รับเข้ากับ `{{FULL_NAME}}`
   - SendGrid ใช้ `{{full_name}}` (Handlebars) — เปลี่ยน `{{FULL_NAME}}` ให้ตรงระบบ
   - Mailchimp ใช้ merge tag เช่น `*|FNAME|*`
   - Amazon SES (template API) ใช้ `{{FULL_NAME}}` ได้เลย
4. ส่ง **test email** ไปหาตัวเองก่อนเสมอ

### ผ่าน Outlook (ส่งด้วยมือ / ทดสอบ)

Outlook **ไม่สามารถ** paste HTML ในหน้า compose ได้ตรง ๆ ให้ใช้วิธีใดวิธีหนึ่ง:

- **วิธี A (แนะนำ):** ส่งผ่านโค้ด/ESP ที่ใส่ HTML เป็น body ได้ (เช่น Microsoft Graph API
  `sendMail` โดยตั้ง `contentType: "HTML"`, Power Automate, หรือ SMTP script)
- **วิธี B:** เปิดไฟล์ `.html` ใน browser → เปิด Outlook desktop → ตั้งค่า signature/stationery
  หรือใช้ add-in ที่รองรับ paste HTML

> ⚠️ **สำคัญ:** Outlook for Windows ใช้ engine ของ Word ในการ render จึงต้องใช้ table layout
> เทมเพลตนี้ทำมาให้รองรับแล้ว — **อย่าแก้เป็น `<div>` + CSS fl/grid** เพราะจะพังบน Outlook

---

## 🧪 ขั้นตอนที่ 4 — ทดสอบก่อนส่งจริง

แนะนำให้ทดสอบการแสดงผลข้าม client ด้วยเครื่องมือเหล่านี้:

- [Litmus](https://litmus.com) หรือ [Email on Acid](https://www.emailonacid.com) — พรีวิวข้าม client จริง
- ส่ง test ไปยัง Gmail (web + app), Outlook desktop, Apple Mail, iOS Mail
- ตรวจ **dark mode** ทั้งบน iOS Mail และ Outlook.com
- เช็คว่ารูปโหลดขึ้น (ถ้า client บล็อกรูป ต้องเห็น `alt` text แทน)

---

## 🎨 อ้างอิงแบรนด์ (empeo)

| องค์ประกอบ | ค่า |
|-----------|-----|
| สีหลัก (Flame) | `#F1592A` |
| หัวข้อ (Charcoal) | `#2B2D33` |
| เนื้อความ (Iron) | `#5A5E66` |
| ข้อความ footer (muted) | `#8A8F98` |
| พื้นหลังหน้า | `#EEF0F3` |
| พื้นหลัง footer | `#F5F6F7` |
| ฟอนต์ | GoFive Font → fallback: `Prompt`, `Noto Sans Thai`, `Tahoma`, `Arial` |
| ความกว้างสูงสุด | 600px |

---

## 🔁 การนำไปทำเทมเพลตอื่นต่อ

ใช้ไฟล์นี้เป็น base ได้เลย — โครงสร้าง header / body / button / footer เหมือนกันหมด
เพียงแก้ข้อความในส่วน **BODY** และปุ่ม CTA ก็จะได้อีเมลใบใหม่ที่ยังคง brand + responsive
+ รองรับ Outlook เหมือนเดิม
