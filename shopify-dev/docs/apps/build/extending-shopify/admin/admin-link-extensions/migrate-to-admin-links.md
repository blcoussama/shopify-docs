# Migrate to admin link extensions

Admin link extensions replace both admin links and bulk action links, which were previously created from the Extensions section of your app's Partners Dashboard. Admin link extensions let you access the same functionality as admin links and bulk action links, but also give you the opportunity to localize links for users, let you manage links in your app's source control system, and manage their deployment with the Shopify CLI.

This tutorial guides you through the process of migrating from admin links and bulk action links to admin link extensions.

## Requirements

Before starting this tutorial you'll need:

- An existing Shopify app
- Admin links or bulk action links that were previously created on the Shopify Partners dashboard
- An upgraded Shopify CLI on version 3.76.1 or higher

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Use the CLI to migrate your existing admin and bulk action links
- Verify the correct configuration for your admin link extensions
- Test your admin link extension's functionality with the CLI
- Deploy your admin link extension to all stores that have your app installed

## Step 1: Import existing admin links

To import your existing admin links from the Partners dashboard, run the following command.

**Terminal**
```bash
shopify app import-extensions
```

When prompted, select admin links and continue. Once the import is finished, your admin link extensions will be created as new directories in your app's extensions directory. To validate them, inspect the shopify.extension.toml file in each extension directory.

## Step 2: Deploy your link extensions

Finish the migration by deploying a new app version. This removes the existing management from the Partners dashboard so you can manage these extensions as part of your app's source code.

**Terminal**
```bash
shopify app deploy
```

Releasing an app version replaces the current active version that's served to stores that have your app installed. It might take several minutes for app users to be upgraded to the new version.

If you want to edit the extensions or add localization, follow the instructions for modifying link extensions found in the tutorial on creating admin link extensions.