# githubforDevelopers

Transactional email templates for empeo, built as `.eml` files that open as
editable drafts in Outlook.

## Email templates

**Read `email-templates/SHELL-SPEC.md` before touching any template.** The header,
footer, font stack, colours and vertical rhythm are locked and shared by every
template — only the rows between the greeting and the CTA change per email.

- Edit `email-templates/src/<name>.html`, never the generated `.eml`.
- Rebuild with `cd email-templates && python3 build-eml.py <name> "<Subject>"`.
- `src/empeo-account-inactive.html` is the reference shell (no CTA);
  `src/empeo-account-deletion-grayfooter.html` is the same shell with one;
  `src/empeo-payslip-grayfooter.html` adds the content components.
- Images are inline `cid:` parts resolved against `assets/<cid>.png`. Email clients
  do not render SVG — rasterise it and keep the vector in `assets/` as the source.
