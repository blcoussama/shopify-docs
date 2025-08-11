# Select a networking option for local development

When developing apps with shopify app dev, you have multiple options for connecting your local development server to Shopify:

- Cloudflare Quick Tunnels (default)
- Localhost-based development
- Bring your own tunnel (such as ngrok)

Choose the option that best fits your development needs and environment.

## Cloudflare Quick Tunnels

By default, Shopify uses Cloudflare Quick Tunnels to open a publicly accessible tunnel to your app. Tunneling provides a secure (HTTPS) URL to your local environment.

**Tip:** If you're experiencing connectivity errors with Cloudflare Quick Tunnels, refer to Cloudflare guidance on firewall requirements, or try one of the alternatives in this guide.

## Localhost-based development

When using Shopify CLI version 3.80 or higher, passing the --use-localhost argument serves your app using localhost (127.0.0.1) with a self-signed HTTPS certificate. Shopify CLI creates this certificate for you using mkcert.

To serve your app using localhost, run the following command:

**Terminal**
```bash
shopify app dev --use-localhost
```

Shopify CLI runs a reverse proxy server on port 3458 which forwards to your app. You can override this port by passing the --localhost-port.

**Note:** Localhost-based development isn't compatible with the Shopify features that directly invoke your app, such as Webhooks, App proxy, and Flow actions, and features that require you to test your app from another device, such as POS.

## Localhost-based development with Windows Subsystem for Linux (WSL)

When you run the shopify app dev command on WSL, mkcert installs the HTTPS root certificate in the Linux environment, but not in Windows. This results in certificate errors when you attempt to preview your app in a Windows-based browser.

To install the certificate in Windows, do the following. This is only needed the first time you run an app with --use-localhost.

1. In a WSL terminal, navigate to your app's directory.
2. Run the following command:

**Terminal**
```bash
certutil.exe -user -addstore root "$(wslpath -w "$(./.shopify/mkcert -CAROOT)/rootCA.pem")"
```

## Manual certificate installation

If you've disabled Windows interop or Windows PATH in WSL, then you can manually install the certificate with the following steps:

1. In an Explorer window, navigate to \\wsl.localhost\<distribution>\usr\local\share\ca-certificates.
   For example, \\wsl.localhost\Ubuntu\usr\local\share\ca-certificates
2. Double click on the mkcert_development_CA certificate file found at this path.
3. Click Open
4. Select Local Machine and click Next.
5. Select Place all certificates in the following store.
6. Click Browse.
7. Select Trusted Root Certification Authorities.
8. Click Next and Finish.

## Bring your own tunnel

The --tunnel-url argument allows you to specify the URL of an alternate network tunnel to your app. You can use this argument with ngrok with the following steps:

1. Set up an ngrok account.
2. Install the ngrok CLI.
3. Follow the steps in the ngrok documentation to set up your access token.
4. In a terminal, start ngrok using the following command. You can alternatively choose another port number.

**Terminal**
```bash
ngrok http 3000
```

5. Note the URL ending in ngrok-free.app that's returned - you'll need this URL in the following command - and leave ngrok running.
6. Run app dev using the --tunnel-url argument. If you've chosen another port number, then use that instead.

**Terminal**
```bash
shopify app dev --tunnel-url=https://<ngrok-URL>:3000
```