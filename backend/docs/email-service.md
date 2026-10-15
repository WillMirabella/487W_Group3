# Which email service to use (issue #17)

_Researched October 14, 2026. Free tiers change often, so recheck the links before relying on them._

## What we need

- Send one email per sign-up attempt containing a 6-digit code, to `@psu.edu` addresses.
- No budget, and no domain of our own (we don't own `lionlift.com` or similar).
- Volume is small. The verification code limits each address to at most 5 emails per hour.

## Options

| Service | Free tier | Needs our own domain? | Notes |
|---|---|---|---|
| **Gmail SMTP** (project Gmail account) | 500 messages per rolling 24 h | **No** | Requires 2-Step Verification and an App Password; plain-password SMTP login was shut off in 2025. Mail comes from the Gmail address. |
| **Resend** | 3,000/month, 100/day | **Yes** to email anyone else | The built-in `resend.dev` sender can only email the account owner's own address. |
| **Mailgun** | 100/day | Includes 1 custom sending domain | A domain is needed to send to real users. |
| **Brevo** | 300/day | Not confirmed in this research | Account must be approved before sending. Adds Brevo branding to every email. |
| **SendGrid** | None | n/a | The free plan was retired in 2025. Only a 60-day trial is left. |

Sources: [Gmail SMTP settings and limits](https://developer.nylas.com/docs/cookbook/email/gmail-smtp-settings/),
[Resend: resend.dev restriction](https://resend.com/docs/knowledge-base/403-error-resend-dev-domain),
[Resend free-tier domains](https://resend.com/changelog/three-domains-on-the-free-tier),
[Mailgun pricing](https://www.mailgun.com/pricing/),
[Free tiers compared](https://cli.nylas.com/guides/email-api-free-tiers-compared),
[SendGrid free plan retirement](https://www.twilio.com/en-us/changelog/changes-coming-to-sendgrid-s-free-plans).

## Recommendation

**Use Gmail SMTP with a dedicated project Gmail account** (for example `lionlift.abington@gmail.com`).

1. It is the only free option above that works **without buying a domain**.
2. 500 emails per day is far more than a class project will use.
3. Setup takes about five minutes and needs no new library.

**Upgrade path.** If the team buys a domain, move to Resend or Mailgun. Both offer SMTP, so this is only a change to environment variables. `email_sender.SmtpEmailSender` works with any SMTP provider, so no code changes are needed.

## Setting up Gmail

1. Create the project Gmail account, using a shared login for the team.
2. Turn on **2-Step Verification** in Google Account → Security.
3. Create an **App Password** in Google Account → Security → App passwords. Google shows the 16-character password once.
4. In `backend/.env` (copied from `.env.example`, never committed):
   ```
   EMAIL_BACKEND=smtp
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_SECURITY=starttls
   SMTP_USERNAME=lionlift.abington@gmail.com
   SMTP_PASSWORD=<the app password>
   EMAIL_FROM=LionLift <lionlift.abington@gmail.com>
   ```
   `EMAIL_FROM` should be the same Gmail address. Gmail rewrites or flags a different From address.
5. Request a code for your own `@psu.edu` address. Check that the email arrives, including in Junk and Quarantine. University mail filtering is outside our control, so test with a real PSU inbox before the demo.

## Known limits

- **The Gmail quota is shared by all users.** The per-address limits (5 codes per hour) stop one address from being flooded. Someone cycling through many different addresses could still use up the 500/day quota. A global cap on sends per day would close this. That is a follow-up and was not needed for #12.
- **The App Password is a secret.** Keep it in `.env` only. Changing the Gmail account password revokes it.
