#!/usr/bin/env node
/**
 * Build a self-contained .eml file from the empeo email template, with the
 * 4 logo/social images EMBEDDED inline (CID) so they always display — even
 * before "Download pictures" and even offline.
 *
 * Double-click the resulting .eml in Outlook → it opens as a NEW editable
 * email (thanks to the `X-Unsent: 1` header) → fill in "To" → replace the
 * name → hit Send.
 *
 * Usage:
 *   node build-eml.mjs ["<Full Name>"]
 *   # default keeps the {{FULL_NAME}} placeholder so you replace it in Outlook
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');

const SUBJECT = process.env.EMAIL_SUBJECT || 'คำขอลบบัญชีของคุณได้รับการอนุมัติ';
const SENDER = process.env.MS_SENDER || 'parisa.a@gofive.co.th';
const fullName = process.argv[2] || '{{FULL_NAME}}';
// Which template to build (default = gray version). e.g. TEMPLATE=empeo-account-deletion-white.html
const templateName = process.env.TEMPLATE || 'empeo-account-deletion.html';

// ---------- Load template, swap placeholders + image URLs → cid: ----------
let html = fs.readFileSync(
  path.join(root, 'email-templates', templateName),
  'utf8',
)
  .replaceAll('{{FULL_NAME}}', fullName)
  // Optional per-template placeholders (default: keep so you can edit in Outlook)
  .replaceAll('{{PAY_PERIOD}}', process.env.PAY_PERIOD || '{{PAY_PERIOD}}')
  .replaceAll('{{DOWNLOAD_URL}}', process.env.DOWNLOAD_URL || '{{DOWNLOAD_URL}}');

// jsDelivr URL (…/assets/<name>.png)  →  cid:<name>
html = html.replace(
  /https:\/\/cdn\.jsdelivr\.net\/gh\/[^"']*\/assets\/([\w-]+)\.png/g,
  (_, name) => `cid:${name}`,
);

// ---------- Helpers ----------
const wrap76 = (b64) => b64.match(/.{1,76}/g).join('\r\n');
const encWord = (s) => `=?UTF-8?B?${Buffer.from(s, 'utf8').toString('base64')}?=`;

// Embed exactly the images this template references (via cid:), in first-seen order.
const imageNames = [...new Set([...html.matchAll(/cid:([\w-]+)/g)].map((m) => m[1]))];
const images = imageNames.map((name) => ({
  name,
  cid: name,
  b64: wrap76(fs.readFileSync(path.join(root, 'email-templates', 'assets', `${name}.png`)).toString('base64')),
}));

// ---------- Assemble MIME (multipart/related) ----------
const BOUNDARY = 'empeo_boundary_5f3a1c9b';
const CRLF = '\r\n';

let eml = '';
eml += `From: empeo <${SENDER}>` + CRLF;
eml += `To: ` + CRLF;
eml += `Subject: ${encWord(SUBJECT)}` + CRLF;
eml += `X-Unsent: 1` + CRLF; // makes Outlook open it as a new, sendable draft
eml += `MIME-Version: 1.0` + CRLF;
eml += `Content-Type: multipart/related; boundary="${BOUNDARY}"` + CRLF + CRLF;

// HTML part (base64 to safely carry Thai + long lines)
eml += `--${BOUNDARY}` + CRLF;
eml += `Content-Type: text/html; charset="UTF-8"` + CRLF;
eml += `Content-Transfer-Encoding: base64` + CRLF + CRLF;
eml += wrap76(Buffer.from(html, 'utf8').toString('base64')) + CRLF + CRLF;

// Inline image parts
for (const img of images) {
  eml += `--${BOUNDARY}` + CRLF;
  eml += `Content-Type: image/png; name="${img.name}.png"` + CRLF;
  eml += `Content-Transfer-Encoding: base64` + CRLF;
  eml += `Content-ID: <${img.cid}>` + CRLF;
  eml += `Content-Disposition: inline; filename="${img.name}.png"` + CRLF + CRLF;
  eml += img.b64 + CRLF + CRLF;
}
eml += `--${BOUNDARY}--` + CRLF;

// ---------- Write ----------
const outPath = path.join(__dirname, templateName.replace(/\.html$/, '.eml'));
fs.writeFileSync(outPath, eml);
console.log(`✅ Wrote ${path.relative(root, outPath)} (${(eml.length / 1024).toFixed(0)} KB, images embedded)`);
console.log(`   Name in body: ${fullName === '{{FULL_NAME}}' ? '{{FULL_NAME}} (replace in Outlook)' : fullName}`);
