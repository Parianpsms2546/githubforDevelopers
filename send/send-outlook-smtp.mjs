#!/usr/bin/env node
/**
 * Alternative: send the empeo email template through Outlook / Office 365
 * SMTP using Nodemailer (basic auth / app password).
 *
 * Sends FROM: parisa.a@gofive.co.th (override with SMTP_SENDER)
 *
 * Requires:  npm install   (installs nodemailer)
 *
 * Usage:
 *   node --env-file=.env send-outlook-smtp.mjs <recipientEmail> "<Full Name>"
 *   # or via npm:  npm run send:smtp -- <recipientEmail> "<Full Name>"
 *
 * NOTE: Microsoft 365 disables basic-auth SMTP by default. An admin must enable
 * "Authenticated SMTP" for the mailbox, and you likely need an App Password
 * (if MFA is on). If SMTP AUTH is blocked, use send-outlook-graph.mjs instead.
 */
import nodemailer from 'nodemailer';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ---------- Config ----------
const SMTP_HOST = process.env.SMTP_HOST || 'smtp.office365.com';
const SMTP_PORT = Number(process.env.SMTP_PORT || 587);
const SMTP_USER = process.env.SMTP_USER;
const SMTP_PASS = process.env.SMTP_PASS;
const SENDER = process.env.SMTP_SENDER || SMTP_USER || 'parisa.a@gofive.co.th';
const SUBJECT = process.env.EMAIL_SUBJECT || 'คำขอลบบัญชีของคุณได้รับการอนุมัติ';

// ---------- CLI args ----------
const [, , toArg, nameArg] = process.argv;
const to = toArg || process.env.TEST_TO;
const fullName = nameArg || 'คุณ';

// ---------- Validate ----------
if (!SMTP_USER || !SMTP_PASS) {
  console.error('❌ Missing SMTP_USER / SMTP_PASS. Copy .env.example → .env (see send/README.md).');
  process.exit(1);
}
if (!to) {
  console.error('❌ No recipient. Usage: node --env-file=.env send-outlook-smtp.mjs <recipient> "<Full Name>"');
  process.exit(1);
}

// ---------- Load + fill template ----------
const templatePath = path.join(__dirname, '..', 'email-templates', 'empeo-account-deletion.html');
const html = fs.readFileSync(templatePath, 'utf8').replaceAll('{{FULL_NAME}}', fullName);

// ---------- Send ----------
const transporter = nodemailer.createTransport({
  host: SMTP_HOST,
  port: SMTP_PORT,
  secure: SMTP_PORT === 465, // 587 uses STARTTLS
  requireTLS: true,
  auth: { user: SMTP_USER, pass: SMTP_PASS },
});

try {
  const info = await transporter.sendMail({
    from: `"empeo" <${SENDER}>`,
    to,
    subject: SUBJECT,
    html,
  });
  console.log(`✅ Sent "${SUBJECT}" to ${to} (from ${SENDER}) — id: ${info.messageId}`);
} catch (err) {
  console.error('❌', err.message);
  process.exit(1);
}
