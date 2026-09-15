# Automatic deployment — what we need from your IT team

Today every change has to be sent over and published by hand, which adds a day or
two to even a one-line fix. This removes that step: once set up, anything merged to
`main` is live on your server within about a minute, with no files to pass around.

## How it works

1. We push a change to `main` in this GitHub repository.
2. GitHub runs the workflow in `.github/workflows/deploy.yml`.
3. It checks the pages are well-formed, copies them to your web server over SSH,
   and confirms the site still responds.

Only `.html` files are copied. Nothing else on the server is touched.

## What we need from you

Five values, added in GitHub under **Settings → Secrets and variables → Actions**.
They are encrypted and cannot be read back by anyone, including us.

| Secret | Meaning | Example |
| --- | --- | --- |
| `DEPLOY_HOST` | server hostname or IP | `srv01.example.com` |
| `DEPLOY_USER` | the user the deploy runs as | `deploy` |
| `DEPLOY_PATH` | folder the pages are served from | `/var/www/tc/public` |
| `DEPLOY_SSH_KEY` | private half of a key pair made for this | full contents of the private key |
| `DEPLOY_PORT` | only if SSH is not on 22 | `2222` |

Optional: `HEALTHCHECK_URL` — a page we can request after deploying to confirm the
site is still up, e.g. `https://tc.united-healthcare.eu/`.

## Creating the deploy key

On any machine:

```bash
ssh-keygen -t ed25519 -C "github-deploy-tc" -f tc_deploy -N ""
```

- Put the **public** half (`tc_deploy.pub`) in `~/.ssh/authorized_keys` for the deploy user.
- Give us the **private** half (`tc_deploy`) to store as `DEPLOY_SSH_KEY`, or paste it
  into the GitHub secret yourselves — you never have to send it to us.

## Security notes

- The deploy user only needs write access to the one folder in `DEPLOY_PATH`.
  It does not need sudo or shell access anywhere else.
- Restrict the key in `authorized_keys` if you want to be strict, for example:
  `command="rsync --server -vlogDtprze.iLsfxC . /var/www/tc/public",no-pty,no-port-forwarding ssh-ed25519 AAAA...`
- Deployments are logged in the Actions tab: who deployed, what changed, when.
- Rolling back is one click — re-run an earlier successful deployment.

## If SSH is not available

Tell us what the server does allow (SFTP, FTPS, a control panel, or a pull from Git
on the server) and we will adjust the workflow. SSH is simply the most common and
the easiest to lock down.

## Worth deciding separately: the medication list

Even with automatic deployment, adding a new medication is still a code change and
therefore still involves us. If that list is expected to change often, it is worth
moving it out of the code so it can be edited directly — either from HubSpot or a
small file your team controls. The forms would read it at load time and no
deployment would be needed at all. Happy to quote that separately.
