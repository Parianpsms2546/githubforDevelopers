# githubforDevelopers
โปรเจค github

## Email templates

```
templates/email/
├── leave-request-rejected.html   อีเมลแจ้งพนักงานเมื่อเอกสารลาถูกปฏิเสธ
├── assets/                       รูปที่ template อ้างถึงผ่าน cid:
│   ├── empeo-logo.png
│   ├── powered-by-empeo.png
│   ├── icon-facebook.png
│   └── icon-youtube.png
└── build-eml.py                  ประกอบ html + assets เป็นไฟล์ .eml สำหรับพรีวิว
```

### พรีวิว

```bash
python3 templates/email/build-eml.py
```

จะได้ `templates/email/leave-request-rejected.eml` เอาไปเปิดใน Outlook /
Apple Mail เพื่อตรวจการแสดงผลได้ สคริปต์จะไล่หา `src="cid:xxx"` ใน template
แล้วแนบ `assets/xxx.png` ให้อัตโนมัติ — ถ้าเพิ่มรูปใหม่ก็แค่วางไฟล์ชื่อตรงกับ
cid ไว้ใน `assets/`

### ฟอนต์

```
'gofive-regular', 'noto-sans-tc', Helvetica, Arial, Tahoma, sans-serif
```

ใช้ชุดเดียวกันทุกที่ใน template ไม่มี `<link>` โหลด web font เพราะ
`gofive-regular` ไม่ได้ host ไว้บน CDN สาธารณะ — จะขึ้นเฉพาะเครื่องที่ติดตั้ง
ฟอนต์ไว้แล้ว นอกนั้นจะไล่ลงไปตามลำดับ ถ้าวันไหนมีที่ host แบบใช้กับอีเมลได้
ค่อยเพิ่ม `@font-face` ตรงหัวไฟล์ (มีคอมเมนต์บอกจุดไว้แล้ว)

หมายเหตุ: `noto-sans-tc` คือ Noto Sans Traditional Chinese ซึ่งไม่มีอักขระไทย
ดังนั้นตัวไทยจะตกไปถึง Tahoma (ตัวสุดท้ายก่อน `sans-serif`) ในเครื่องที่ยังไม่มี
`gofive-regular`

### ขนาดตัวอักษรในการ์ดเอกสาร

| ส่วน | ขนาด | line-height |
|------|------|-------------|
| ชื่อเอกสาร เช่น `ลาป่วย (L230200033)` | 16px / 600 | 30px |
| ป้ายสถานะ `ปฏิเสธ` | 12px / 500 | 16px |
| `วันที่:` / `รายละเอียด:` (หัวข้อ) | 15px / 400 | 23px |
| ค่าของ `วันที่` / `รายละเอียด` | 15px / 500 | 23px |

ขนาดเขียนเป็น inline style เพราะ email client ส่วนใหญ่ไม่รองรับ CSS ภายนอก —
ถ้าต้องแก้ ให้แก้ `font-size` ที่ `<td>` นั้นโดยตรง และอย่าลืม `line-height`
คู่กันด้วย เพราะ template ใช้ `mso-line-height-rule:exactly` ซึ่ง Outlook จะตัด
วรรณยุกต์ไทยทิ้งถ้า line-height แคบเกินขนาดฟอนต์
