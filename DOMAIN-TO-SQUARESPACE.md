# Moving the H+ domain to Squarespace — what your IT team needs to do

Two ways to do this. **Transferring** moves the registration to Squarespace, so
everything is managed in one place. **Connecting** leaves the domain where it is and
just points it at the site — much faster, and reversible.

If the domain will live with Squarespace long term, transfer it. If you need the site
live this week, connect it now and transfer later.

---

## Option A — Transfer the domain to Squarespace

### Before starting, check the domain is eligible

- Registered or last transferred **at least 60 days ago**. A transfer started inside
  that window will be refused.
- **Registration details have not been changed in the last 60 days** — editing the
  registrant can itself trigger a 60-day lock.
- Not expired or about to expire.
- Fewer than 9 years of registration remaining.
- **DNSSEC must be switched off** before starting — it is a common cause of failure.
- Some country extensions cannot be transferred at all (including `.au`, `.com.au`,
  `.jp`, `.nz`, `.co.nz`). `.eu` and `.de` have their own registry rules, so confirm
  with the current registrar first.

### Steps at the current registrar

1. **Unlock the domain** (sometimes called "transfer lock" or "registrar lock").
2. **Turn off WHOIS / domain privacy** if it is on.
3. **Request the authorization code** — also called the EPP code or transfer key.
   Allow 1–2 days; some registrars email it rather than showing it.
4. **Check the registrant email address is one you can read.** The approval email
   goes there, and the transfer stalls without it.

### Steps in Squarespace

1. Billing details must be on the site first, even on a trial.
2. **Domains** panel → **Use a domain I own** → type the domain → **Transfer Domain**.
3. Paste the authorization code → **Save and Continue**.
4. Check the registration details, confirm, and pay.

### What to expect

- A transfer adds **one year** to the registration and is charged for. Existing time
  is not lost — it is added on top.
- Completion usually takes a few days. If still pending after **15 days**, chase the
  losing registrar.
- After it completes, allow up to **48 hours** for the domain to serve the site.

### Email will keep working, but check first

MX records come across with the domain, so mailboxes keep pointing wherever they
point today. Before starting, confirm with whoever hosts the email that they do not
require the domain to stay registered with them. Note down all current DNS records
(MX, TXT/SPF/DKIM, A, CNAME, SRV) before the transfer so anything custom can be
restored afterwards.

### Why transfers usually fail

Domain still locked · authorization code mistyped · registration details changed in
the last 60 days · DNSSEC still enabled.

---

## Option B — Connect the domain, leave it where it is

Faster and easily undone. The domain stays with the current registrar and DNS records
point it at Squarespace.

Add these at the current DNS provider:

**A records** — host `@` (or blank):

| Host | Points to |
| --- | --- |
| @ | 198.185.159.144 |
| @ | 198.185.159.145 |
| @ | 198.49.23.144 |
| @ | 198.49.23.145 |

**CNAME records:**

| Host | Points to |
| --- | --- |
| `www` | `ext-cust.squarespace.com` |
| *(unique code shown in your Squarespace Domains panel)* | `verify.squarespace.com` |

The verification CNAME matters: without it the domain **unlinks itself after 15 days**.
Squarespace shows the code under Domains → Use a domain I own → Connect.

Allow 24–48 hours to settle.

---

## What we need back from you

- Which domain exactly (and whether `www` should be the main address)
- Whether you want to transfer or connect
- Who the current registrar is, and who can approve at the registrant email address
- Confirmation of where email is hosted, so it is not interrupted

---

*Note: this covers the main H+ domain going to the Squarespace site. The Therapy
Companion subdomain is separate and is not affected by any of the above.*
