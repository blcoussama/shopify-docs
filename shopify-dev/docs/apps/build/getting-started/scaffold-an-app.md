# Scaffold an app

You're ready to scaffold a new app. You want to set up your development environment so that you can start coding.

In this tutorial, you'll scaffold an app that users can access in the Shopify admin. You'll generate starter code and use Shopify CLI to develop your app.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Initialize a Remix app that uses Shopify CLI
- Install your app on a development store
- Generate a product using your new app

## Requirements

- You've created a Partner account and a development store.
- You're using the latest version of Shopify CLI.
- You're using the latest version of Chrome or Firefox.

## Step 1: Create a new app

You can create a new Shopify app using Shopify CLI

Navigate to the directory where you want to create your app.

Your app will be created in a new subdirectory.

Run the following command to create a new app:

**Terminal**
```bash
shopify app init
```

When prompted, enter a name for your app, and then select Build a Remix app to use the Remix template.

**Tip:** If you want to create an extension-only app, then select Build an extension-only app. Learn more about extension-only apps. We recommend that you use the Remix template for most other cases. However, you can use one of our other templates, or provide your own. Learn more about using other app templates.

A new app is created and Shopify CLI is installed along with all the dependencies that you need to build Shopify apps.

## Step 2: Start a local development server

After your app is created, you can work with using a local development server and the Shopify CLI.

Shopify CLI uses Cloudflare to create a tunnel that enables your app to be accessed using a HTTPS URL.

Navigate to your newly created app directory.

**Terminal**
```bash
cd my-new-app
```

Run the following command to start a local server for your app:

**Terminal**
```bash
shopify app dev
```

Shopify CLI performs the following tasks:

- Guides you through logging into your Partner account and selecting a Partner organization
- Creates an app in the Partner Dashboard, and connects your local code to the app
- Creates your Prisma SQLite database
- Creates a tunnel between your local machine and the development store

To learn more about the processes that are executed when you run dev, refer to the Shopify CLI command reference.

**Caution:** To use a development store or Plus sandbox store with Shopify CLI, you need to be the store owner, or have a staff account on the store. Staff accounts are created automatically the first time you access a development store with your Partner staff account through the Partner Dashboard.

## Step 3: Install your app on your development store

You can install your app on your development store, and automatically populate your development store with products that you can use for app testing.

1. With the server running, press `p` to open your app's preview URL in a browser.

2. When you open the URL, you're prompted to install the app on your development store.

3. Click **Install app** to install the app on the development store.

You now have a development store running with your new app installed.

4. From the home page of the new app, click **Generate a product** to create a product for your development store.

## Next steps

- Follow the Build a Shopify app using Remix tutorial to learn how to add features to an app using the Shopify Remix template and key Shopify tools and libraries.
- Learn how to deploy and distribute your app.