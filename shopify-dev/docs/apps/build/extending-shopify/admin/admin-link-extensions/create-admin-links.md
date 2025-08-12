# Create admin link extensions

This tutorial will guide you through creating new admin link extensions for your app that let you direct merchants from key pages in the admin to contextually relevant pages in your app.

## Requirements

Before starting this tutorial, you'll need:

- A scaffolded Shopify embedded app with the write_products permission
- An upgraded Shopify CLI on version 3.71 or higher

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Generate a new admin link extension
- Modify the link extension .toml to change the extension's location and target page
- Localize your admin link extension
- Test your admin link extension's functionality with the CLI
- Deploy your extension to all stores that have your app installed

## Step 1: Generate a new link extension template

To create an admin link extension, generate a new extension from your app's directory.

**Terminal**
```bash
shopify app generate extension --template admin_link --name admin-link-extension
```

The command creates a new extension template in your app's extensions directory with the following structure:

```
extensions/admin-link-extension/
├── README.md
├── locales/
│   ├── en.default.json     // The default locale for the extension
│   ├── fr.json             // The French language translations for the extension
├── shopify.extension.toml  // The config file for the extension
```

## Step 2: Modify the link extension toml

After creating the template, you can modify its .toml file to change its behavior.

**📁 shopify.extension.toml**
```toml
[[extensions]]
name = "My admin link extension"
handle = "admin-link"
type = "admin_link"

[[extensions.targeting]]
target = "admin.product.action.link"
url = "/relative/app/to/path"
```

1. Change the page where your admin link extension is shown to users by modifying the target value. A full list of locations where you can add admin link extensions can be found in the admin extensions target overview.
2. Change the name parameter will change what label that will be shown to merchants
3. To specify where the link takes the user, you can specify a relative path to a page of your app.

## Step 3: Translate your extension

To translate your extension, you can use a localization key for the extension's title and add translation files with the corresponding key in the locales folder.

**📁 shopify.extension.toml**
```toml
[[extensions]]
name = "t:name"
handle = "admin-link"
type = "admin_link"

[[extensions.targeting]]
target = "admin.product.action.link"
url = "/relative/app/path"
```

**📁 locales/en.default.json**
```json
{
  "name": "My admin link extension"
}
```

**📁 locales/fr.json**
```json
{
  "name": "Mon extension de lien d'administration"
}
```

## Step 4: Test your link extension on a dev store

To test your admin link extension, try running your app locally.

**Terminal**
```bash
shopify app deploy
```

Once your app is running, navigate to the target location and verify that the link takes you to the correct page of your app when it is clicked.

## Step 5: Deploy your link extensions

After you've tested your admin link extension, you can release the changes to users by deploying a new app version.

To deploy a new version run the following command:

**Terminal**
```bash
shopify app deploy
```

Releasing an app version replaces the current active version provided to stores that have your app installed.