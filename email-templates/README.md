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

## 🖼️ ขั้นตอนที่ 1 — อัปโหลดรูปโลโก้ (สำคัญมาก)

อีเมลไม่สามารถฝังรูปภาพในไฟล์ได้ **ต้อง host รูปไว้บน URL สาธารณะ (HTTPS)** ก่อน เช่น
CDN, S3, Cloudflare R2, หรือ storage ของ ESP ที่ใช้

อัปโหลดรูป 3 ชุดที่ให้มา แล้วนำ URL จริงไปแทน placeholder ในไฟล์ HTML:

| ตำแหน่ง | รูป | Placeholder ที่ต้องแทนที่ | ขนาดแนะนำ (แสดงผล) |
|---------|-----|--------------------------|--------------------|
| Header | โลโก้ empeo (ภาพที่ 2) | `https://cdn.empeo.com/email/empeo-logo.png` | 140 × 34 px (อัปโหลด 2x = 280px) |
| Footer | Powered by empeo (ภาพที่ 3) | `https://cdn.empeo.com/email/powered-by-empeo.png` | 120 × 30 px |
| Footer | ไอคอน Facebook (ภาพที่ 4) | `https://cdn.empeo.com/email/icon-facebook.png` | 28 × 28 px |
| Footer | ไอคอน YouTube (ภาพที่ 4) | `https://cdn.empeo.com/email/icon-youtube.png` | 28 × 28 px |

> 💡 ใช้ไฟล์ **PNG** (รองรับพื้นหลังโปร่งใส) และอัปโหลดที่ความละเอียด 2 เท่า
> เพื่อความคมชัดบนจอ Retina จากนั้นระบุ `width`/`height` ในโค้ดตามขนาดแสดงผลจริง
> URL ของรูปต้อง **เข้าถึงได้แบบสาธารณะ ไม่ต้อง login**

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
