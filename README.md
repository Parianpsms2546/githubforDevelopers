# githubforDevelopers
โปรเจค github

## Email templates

| ไฟล์ | ใช้เมื่อ |
|------|---------|
| `templates/email/leave-request-rejected.html` | แจ้งพนักงานเมื่อเอกสารลาถูกปฏิเสธ |

### Placeholder ที่ต้องแทนค่าตอนส่งอีเมล

| Placeholder | ค่าที่ใส่ |
|-------------|----------|
| `{{logoUrl}}` | โลโก้ empeo ด้านบน (180×42) |
| `{{documentUrl}}` | ลิงก์ปุ่ม "ดูเอกสาร" |
| `{{poweredByLogoUrl}}` | โลโก้ Powered by empeo ใน footer (124×26) |
| `{{facebookUrl}}` / `{{facebookIconUrl}}` | ลิงก์และไอคอน Facebook |
| `{{youtubeUrl}}` / `{{youtubeIconUrl}}` | ลิงก์และไอคอน YouTube |

### ขนาดตัวอักษรในการ์ดเอกสาร

| ส่วน | ขนาด |
|------|------|
| ชื่อเอกสาร เช่น `ลาป่วย (L230200033)` | **18px** (bold) |
| ป้ายสถานะ `ปฏิเสธ` | 14px |
| หัวข้อ `วันที่:` / `รายละเอียด:` | 16px |
| ค่าของ `วันที่` | 16px |
| ค่าของ `รายละเอียด` เช่น `เป็นไข้ใจ` | **16px** (bold) |

ขนาดตัวอักษรเขียนเป็น inline style เพราะ email client ส่วนใหญ่ไม่รองรับ CSS
ภายนอก — ถ้าต้องแก้ขนาด ให้แก้ที่ `font-size` ของ element นั้นโดยตรง
(ชื่อเอกสารมี class `doc-title` สำหรับ override บนจอมือถือด้วย)
