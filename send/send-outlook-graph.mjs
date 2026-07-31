#!/usr/bin/env node
/**
 * Send the empeo email template through Outlook / Microsoft 365
 * using the Microsoft Graph API (app-only, client-credentials flow).
 *
 * Sends FROM: parisa.a@gofive.co.th (override with MS_SENDER)
 *
 * Zero external dependencies — uses Node's built-in fetch (Node 18+).
 *
 * Usage:
 *   node --env-file=.env send-outlook-graph.mjs <recipientEmail> "<Full Name>"
 *   # or via npm:  npm run send:graph -- <recipientEmail> "<Full Name>"
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ---------- Config (from environment) ----------
const TENANT_ID = process.env.MS_TENANT_ID;
const CLIENT_ID = process.env.MS_CLIENT_ID;
const CLIENT_SECRET = process.env.MS_CLIENT_SECRET;
const SENDER = process.env.MS_SENDER || 'parisa.a@gofive.co.th';
const SUBJECT = process.env.EMAIL_SUBJECT || 'คำขอลบบัญชีของคุณได้รับการอนุมัติ';

// ---------- CLI args ----------
const [, , toArg, nameArg] = process.argv;
const to = toArg || process.env.TEST_TO;
const fullName = nameArg || 'คุณ';

// ---------- Validate ----------
const missing = ['MS_TENANT_ID', 'MS_CLIENT_ID', 'MS_CLIENT_SECRET'].filter((k) => !process.env[k]);
if (missing.length) {
  console.error(`❌ Missing environment variables: ${missing.join(', ')}`);
  console.error('   Copy .env.example → .env and fill in the values (see send/README.md).');
  process.exit(1);
}
if (!to) {
  console.error('❌ No recipient. Usage: node --env-file=.env send-outlook-graph.mjs <recipient> "<Full Name>"');
  process.exit(1);
}

// ---------- Load + fill template ----------
const templatePath = path.join(__dirname, '..', 'email-templates', 'empeo-account-deletion.html');
const html = fs.readFileSync(templatePath, 'utf8').replaceAll('{{FULL_NAME}}', fullName);

// ---------- Get app-only access token ----------
async function getToken() {
  const res = await fetch(`https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      scope: 'https://graph.microsoft.com/.default',
      grant_type: 'client_credentials',
    }),
  });
  if (!res.ok) throw new Error(`Token request failed (${res.status}): ${await res.text()}`);
  const json = await res.json();
  return json.access_token;
}

// ---------- Send ----------
async function main() {
  const token = await getToken();
  const res = await fetch(
    `https://graph.microsoft.com/v1.0/users/${encodeURIComponent(SENDER)}/sendMail`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: {
          subject: SUBJECT,
          body: { contentType: 'HTML', content: html },
          toRecipients: [{ emailAddress: { address: to } }],
        },
        saveToSentItems: true,
      }),
    },
  );

  if (res.status === 202) {
    console.log(`✅ Sent "${SUBJECT}" to ${to} (from ${SENDER})`);
  } else {
    throw new Error(`sendMail failed (${res.status}): ${await res.text()}`);
  }
}

main().catch((err) => {
  console.error('❌', err.message);
  process.exit(1);
});
