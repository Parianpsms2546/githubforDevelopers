# ส่งอีเมล empeo ผ่าน Outlook / Microsoft 365

สคริปต์สำหรับส่งเทมเพลต `email-templates/empeo-account-deletion.html`
ออกจากกล่องเมล **parisa.a@gofive.co.th**

มี 2 วิธี:

| ไฟล์ | วิธี | เหมาะกับ | Dependency |
|------|------|----------|------------|
| `send-outlook-graph.mjs` | **Microsoft Graph API** (แนะนำ) | ส่งอัตโนมัติ/transactional, เสถียร | ไม่มี (ใช้ fetch ในตัว Node) |
| `send-outlook-smtp.mjs` | **SMTP (Office 365)** | ส่งง่าย ๆ จากบัญชี parisa โดยตรง | `nodemailer` |

> ต้องใช้ **Node.js ≥ 20.6** (เพราะใช้ `--env-file`)

---

## เตรียมก่อนเริ่ม (ทั้ง 2 วิธี)

```bash
cd send
cp .env.example .env      # แล้วแก้ค่าใน .env
```

> ⚠️ ห้าม commit ไฟล์ `.env` (มี secret) — ผมตั้ง `.gitignore` กันไว้ให้แล้ว

---

## วิธีที่ 1 — Microsoft Graph API ✅ (แนะนำ)

### 1. สร้าง App Registration บน Azure (ทำครั้งเดียว โดยแอดมิน IT)

1. เข้า **[Azure Portal](https://portal.azure.com)** → **Microsoft Entra ID** → **App registrations** → **New registration**
   - ตั้งชื่อ เช่น `empeo-email-sender` → **Register**
2. หน้า **Overview** จดค่า:
   - **Application (client) ID** → `MS_CLIENT_ID`
   - **Directory (tenant) ID** → `MS_TENANT_ID`
3. **Certificates & secrets** → **New client secret** → คัดลอกค่า **Value** → `MS_CLIENT_SECRET`
   *(ค่านี้โชว์ครั้งเดียว ถ้าไม่ก๊อปต้องสร้างใหม่)*
4. **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**
   → เลือก **`Mail.Send`** → **Add permissions**
   → กด **Grant admin consent for Gofive** (ต้องเป็นแอดมิน)

> 🔒 **จำกัดสิทธิ์ให้ส่งได้เฉพาะกล่อง parisa.a (แนะนำ):** `Mail.Send` แบบ application
> ให้สิทธิ์ส่งแทน**ทุก**กล่องเมลในองค์กร ควรจำกัดด้วย **Application Access Policy**
> ผ่าน Exchange Online PowerShell ให้ส่งได้เฉพาะ mailbox ที่กำหนด:
> ```powershell
> New-ApplicationAccessPolicy -AppId <MS_CLIENT_ID> `
>   -PolicyScopeGroupId parisa.a@gofive.co.th `
>   -AccessRight RestrictAccess -Description "empeo email sender"
> ```

### 2. ใส่ค่าใน `.env`

```
MS_TENANT_ID=...
MS_CLIENT_ID=...
MS_CLIENT_SECRET=...
MS_SENDER=parisa.a@gofive.co.th
```

### 3. ส่ง

```bash
# ส่งหาผู้รับ พร้อมชื่อที่จะไปแทน {{FULL_NAME}}
node --env-file=.env send-outlook-graph.mjs someone@example.com "วริศรา ช."

# หรือผ่าน npm
npm run send:graph -- someone@example.com "วริศรา ช."
```

ได้ `✅ Sent ... to ...` = สำเร็จ (อีเมลจะไปโผล่ใน Sent Items ของ parisa.a ด้วย)

---

## วิธีที่ 2 — SMTP (Office 365)

ง่ายกว่าเพราะไม่ต้องสร้าง app แต่ **Microsoft 365 ปิด Basic Auth SMTP เป็นค่าเริ่มต้น**
แอดมินต้องเปิด **Authenticated SMTP** ให้กล่อง parisa.a ก่อน และถ้าเปิด MFA ต้องใช้ **App Password**

1. `npm install` (ติดตั้ง nodemailer)
2. ใส่ค่าใน `.env`:
   ```
   SMTP_USER=parisa.a@gofive.co.th
   SMTP_PASS=<app-password>
   ```
3. ส่ง:
   ```bash
   npm run send:smtp -- someone@example.com "วริศรา ช."
   ```

ถ้าเจอ error `SmtpClientAuthentication is disabled` → ใช้วิธีที่ 1 (Graph) แทน

---

## ปรับแต่ง

- **หัวข้ออีเมล:** แก้ `EMAIL_SUBJECT` ใน `.env`
- **ผู้ส่ง:** แก้ `MS_SENDER` / `SMTP_SENDER`
- **เนื้อหา:** แก้ในไฟล์ `email-templates/empeo-account-deletion.html` — สคริปต์จะแทน `{{FULL_NAME}}` ให้อัตโนมัติจาก argument ตัวที่ 2
- **ส่งหลายคน:** เขียน loop เรียกฟังก์ชันส่งต่อผู้รับแต่ละคน (บอกผมได้ถ้าอยากได้เวอร์ชันอ่านจากไฟล์ CSV)

---

## เรื่องรูปภาพใน Outlook

เทมเพลตอ้างรูปโลโก้จาก jsDelivr (repo public) — Outlook อาจ **บล็อกรูปจากภายนอกโดยค่าเริ่มต้น**
จนกว่าผู้รับจะกด "Download pictures" (เป็นพฤติกรรมปกติของทุก client เพื่อความเป็นส่วนตัว)

ถ้าต้องการให้รูป **ขึ้นชัวร์ 100% โดยไม่ต้องกดโหลด** → ใช้การฝังรูปแบบ **CID (inline attachment)**
บอกผมได้ เดี๋ยวปรับสคริปต์ให้แนบรูปทั้ง 4 ไปในอีเมลเลย
