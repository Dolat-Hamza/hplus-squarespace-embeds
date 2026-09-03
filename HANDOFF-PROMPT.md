# Prompt for Thomas's Claude — H+ Therapy Companion onboarding forms

Copy everything below the line into a new Claude session.

---

You are helping me (Thomas) work on the **H+ Therapy Companion** patient onboarding forms. Read this whole brief first, then ask me what I want to do before making changes.

## What this project is

**H+ Therapy Companion** is a free patient-support service from **Healthcare Deutschland GmbH** (brand "H+", part of United Healthcare Partners). It supports patients on a hard-to-source medication called **Brinsupri (Brensocatib)** (and a handful of other rare-disease meds) with: free home delivery, repeat-prescription coordination, dose/appointment reminders, and a nurse/support line.

The public site is **united-pharma-partners.eu** (built on **Squarespace**). There's a Squarespace staging site at **sm-nautilus-0044.squarespace.com**.

A web agency (**Geevs**) has been building the onboarding forms with me. There are two separate things:

1. **Standalone HTML embed forms** — self-contained HTML/CSS/JS files pasted into Squarespace **Code Blocks**. These are the patient-facing forms. **This is what we mostly work on.**
2. **A Next.js app** (`geevs-onboarding`, deployed on Vercel) that provides the email backend for the HTML forms + an admin dashboard. You usually don't need to touch this.

## Where the code lives

- **Embeds repo (private GitHub):** `https://github.com/Dolat-Hamza/hplus-squarespace-embeds`
  Clone it, or work from the local folder if you have it.
- Key files in that repo:
  - `brinsupri-registration-embed.html` — **the main multi-step patient registration form** (the big one). This is where almost all recent work happened.
  - `brinsupri-registration-embed-consent-page.html` — an alternate variant (HCP prescription consent shown as a full page instead of a popup).
  - `brinsupri-patient-registration-embed.html`, `brinsupri-caregiver-consent-embed.html`, `brinsupri-patient-consent-embed.html`, `brinsupri-medication-checkin-embed.html`, `brinsupri-account-embed.html` — other patient forms.
  - `brinsupri-benefits-only.html` — the "Companion Path" benefits/hero section shown above the form.
  - `therapy-companion-privacy-policy.html`, `-terms-and-conditions.html`, `-delivery-and-collection-services-de/at.html` — legal pages.
  - `*.bak`–`*.bak5` — progressive backups of the registration form (snapshots before each big edit round).

## How the forms are structured

`brinsupri-registration-embed.html` is a **single self-contained file** (~1,800 lines): inline `<style>`, the HTML, and one big inline `<script>` IIFE at the bottom with an `I18N` object (full **German + English**, DE default, toggle top-right). It's a **4-step wizard**:

1. **General information** — patient/caregiver, name, email, phone (optional unless "Phone call" chosen), contact preferences, optional caregiver.
2. **Your medication** — pick medicine (incl. "Other" → editable details), confirm prescription, "have you already received your medication?", first-dose date (label changes accordingly), other meds, **Regular Check-ins** (frequency), **prescription-reminders-when-low** question, and a contact-preferences picker for those automated services.
3. **Delivery & support** (internal sub-steps) — country, support modules, **delivery consent + partner-pharmacy** selection (single "H+ Partner Pharmacy" card, a "list of partner pharmacies" popup, Delivery Preferences address fields), a **free-choice-of-pharmacy popup** on Continue, an **HCP prescription-consent popup**, and a **doctor-details** step (with Google Places practice search).
4. **Review + submit.**

## How submission works (important)

- Most patient embeds POST to a **Vercel email-proxy endpoint**: `https://geevs-onboarding.vercel.app/api/embed/submit?form=<slug>`. It emails the submission (via **Resend**) and keeps API keys server-side. The sending domain must be **verified in Resend** or nothing sends.
- **BUT** `brinsupri-registration-embed.html` currently submits to **HubSpot** (portal `146131370`, region `eu1`, three form GUIDs for registration/medical/delivery) — not the email endpoint. So confirmation emails on that form depend on **HubSpot workflows**, not the Vercel endpoint. If we want it to email instead, we repoint it like the other embeds.

## How we've been working (the workflow)

1. Edit the HTML file directly (big single files — use exact string edits or small Python scripts for surgical changes; the base64 images make some blocks huge).
2. Test locally: run `python3 -m http.server 4599 --directory <folder>` and open the file in a browser. Drive the multi-step form and check each scenario (validation, conditional fields, popups, both DE/EN, mobile width). **Always test multiple scenarios**, including the branch logic (e.g. reminders Yes vs No changes the flow).
3. Validate the JS after edits (`node --check` on the extracted `<script>`).
4. **To deploy: copy the ENTIRE file and paste it into the matching Squarespace Code Block, then Save.** Nothing changes on the live/staging site until it's pasted. One form per page.
5. Keep a `.bak` before big changes. Commit + push to the GitHub repo.

## Conventions & gotchas

- Forms are **mobile-first** (patients on phones). Check layouts at ~390px. Radio/checkbox groups often need "N per line" tweaks.
- All user-facing text is **bilingual** — every change needs both the DE and EN string in the `I18N` object.
- Fields hidden by conditional logic must be **skipped in validation** so they never block silently. **Never let the form fail silently** — always show the user a message when a Continue is blocked.
- The form autosaves to `localStorage` by control **index** — if you add/remove form controls, **bump the `LS_KEY` version** so returning visitors don't get mis-mapped data.
- After editing CSS/fonts you may need to hard-refresh; Squarespace supplies charset, but standalone files include `<meta charset="utf-8">`.

## What I might ask you to do

Help me: make further edits to the registration flow, repoint the form from HubSpot to the email endpoint, verify the Resend sending domain, adjust wording/layout, test scenarios, or paste-ready package a file for Squarespace. Ask me which file and which behavior I mean before editing, and show me a screenshot or a clear description of what changed.

Start by confirming you've read this and asking what I want to work on.

## Common questions (answer these for me if I ask)

### 1) How can I easily view the form?
- **Simplest:** the embed files are fully self-contained, so just **double-click the `.html` file** (or drag it into a browser) and it opens and runs — no server needed. Toggle DE/EN top-right. Resize the window narrow (~390px) to see the mobile layout.
- **As it looks on the real site:** view it on the **Squarespace staging site** (`sm-nautilus-0044.squarespace.com`) after the file is pasted into the page's Code Block.
- **Have Claude show me:** if you're in Claude Code (with browser tools), ask Claude to start a local server (`python3 -m http.server`) and open the file, then screenshot each step or walk the whole flow for me.

### 2) How can I view it in Claude to give feedback?
- **Best:** use **Claude Code** (or a Claude session with browser/preview tools) with the file open. Ask: "open this form in the browser, walk through all 4 steps in German and English, and screenshot each — I want to give feedback." Claude can render it, fill it, trigger the popups, and show screenshots, then apply my feedback directly to the file.
- **Lightweight:** open the file in your own browser, take screenshots of anything you want changed, and paste those screenshots into a Claude chat with your comments. Claude can then edit the HTML to match. (Plain claude.ai can read screenshots and edit the code, but it can't *interactively* run the form — Claude Code is better for that.)

### 3) How do I share a version for the client to test, via Vercel — and what would they see?
The forms are static HTML, so to give the client a **clickable test link** you deploy the HTML to a host. Two easy options:

- **Vercel (recommended for a quick shareable link):** put the embed file(s) in a folder as `index.html` (or a small static site) and deploy to Vercel — either `vercel` CLI, or drag-and-drop the folder at vercel.com, or connect the GitHub repo. You get a URL like `https://hplus-forms.vercel.app`. Share that link. To keep it private, use Vercel's **password protection** (Deployment Protection) so only people with the password can open it.
- **Squarespace staging:** paste into a staging page and **password-protect the page**, then share the staging URL.

**What the client would see and be able to do:**
- The **fully interactive form**, exactly as a patient would — all 4 steps, DE/EN toggle, conditional fields, popups, mobile layout. They can fill it in and **submit test data**.
- On submit, it posts to the **real backend** (the registration form → HubSpot; the other embeds → the Vercel email endpoint), so **test submissions create real records / emails**. Use obviously-fake test data, or first repoint it to a test recipient/sandbox so client testing doesn't pollute production. Tell me if you want that set up.
- They **cannot** see the source code, API keys, or the backend — only the rendered form and its behavior.
