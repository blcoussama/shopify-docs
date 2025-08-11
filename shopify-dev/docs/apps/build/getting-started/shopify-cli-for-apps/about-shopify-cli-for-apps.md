# About Shopify CLI for apps

Shopify CLI is a command-line interface tool that helps you build Shopify apps. It quickly generates Shopify apps and generates app extensions. You can also use it to automate many common development tasks.

This documentation explains how to use Shopify CLI for app development. To learn how to use Shopify CLI for other tasks, refer to the following documentation:

- Shopify CLI for themes
- Shopify CLI for Hydrogen storefronts

## Features

Shopify CLI accelerates your app development process with the following features:

- Creates new apps using app templates
- Generates app extensions in your app
- Creates app records in the Partner Dashboard
- Builds your app and extensions, and creates a tunnel to let you preview your work in a development store
- Deploys your app configuration and app extensions
- Lets you search the Shopify Dev Docs

## Requirements

- You're using the latest version of Shopify CLI.
- You're using the latest version of Chrome or Firefox.

## Getting started

Because Shopify CLI requires a conventional directory structure, you should run this command to initialize your app:

**Terminal**
```bash
shopify app init
```

**Tip:** You can specify the app template that you want to use with the `--template` flag. You can specify a Shopify app template, or pass a URL to a template hosted in GitHub.

If you have an existing app that wasn't built using Shopify CLI, you can migrate your app to Shopify CLI for a fully integrated development experience.

Refer to the following tutorials for additional details about creating an app that works with Shopify CLI, or to learn how to work on an existing app that uses Shopify CLI 3.0 or higher:

**Scaffold an app**
Learn how to set up your app development environment and start building.

**Build an app**
After creating your app, follow this in-depth tutorial to learn how to add features to your app using Shopify templates, tools, and libraries.

## App structure

To offer a better and more integrated development experience, apps created using Shopify CLI follow a conventional directory structure. This structure allows you to serve and deploy your web app and app extensions at the same time, easily generate new app extensions, and manage all of your app's dependencies in one place.

Learn more about the structure of apps built with Shopify CLI.

## Using Shopify CLI for continuous integration

If you have app configuration and extensions that you want to deploy to Shopify regularly, then you can integrate Shopify CLI into your CI/CD pipeline to programmatically deploy your app components using the deploy command.

Learn more about running Shopify CLI in a CI/CD pipeline.

## Migrate from a Partner Dashboard-managed app

If you've been using the Partner Dashboard to manage your app, then you should consider importing it and using Shopify CLI to manage it instead.

## Migrate to Shopify CLI 3.x

To offer a better and more integrated development experience, apps created Shopify CLI 3.x follow a conventional directory structure and manage your Node-based dependencies for you.

If you have an app that was created using a previous version of Shopify CLI, or without Shopify CLI, then you can migrate your app so you can use the newest version of Shopify CLI.

## Usage reporting

Anonymous usage statistics are collected by default. To opt out, you can use the environment variable `SHOPIFY_CLI_NO_ANALYTICS=1`.

## Switch to a global executable or local dependency

Shopify CLI can be globally installed or used as a local dependency when working with Shopify apps. This following sections explains the reasons for using each installation method and the process for switching between them.

### Switch to a global Shopify CLI executable

Global installation is the default recommended approach for using Shopify CLI. Global installation has the advantage of a single install and upgrade point for all your Shopify app, theme, and Hydrogen development.

If you have an existing app which has Shopify CLI as a local dependency in its package.json, use the following steps to move to a global install:

1. Use your package manager to delete @shopify/cli and (if present) @shopify/app from your dependencies:

**Terminal**
```bash
npm uninstall -D @shopify/cli @shopify/app
```

2. Install Shopify CLI as a global package.

3. Invoke Shopify CLI directly when working in your app. For example:

**Terminal**
```bash
shopify app generate extension
```

### Switch an app to a local Shopify CLI dependency

Adding Shopify CLI as a local dependency is useful if you wish to synchronize Shopify CLI versions within a team, or use different Shopify CLI versions across multiple apps in your development environment.

To switch an app to use Shopify CLI as a local dependency:

1. Install the @shopify/cli package with one of the following commands:

**Terminal**
```bash
npm install -D @shopify/cli
```

**Note:** As of Shopify CLI version 3.59.0, you no longer need to install the @shopify/app package as it is bundled with @shopify/cli.

2. Invoke Shopify CLI commands with your package manager. For example:

**Terminal**
```bash
npm run shopify app generate extension
```

## Where to get help

**Open a GitHub issue** - To report bugs or request new features, open an issue in the Shopify CLI repository.

**.dev Community** - Visit our forums to connect with the community and learn more about Shopify CLI development.

## Command reference

**Shopify CLI app commands**
Explore the commands available to build apps with Shopify CLI.