# Migrate to Shopify CLI 3.x

To offer a better and more integrated development experience, apps created using Shopify CLI 3.x follow a conventional directory structure, use simplified configuration files, and manage your Node-based dependencies for you.

If you have an app that was created using a previous version of Shopify CLI, or you've created an app from scratch, then you can use this migration guide to update your app to be compatible with the newest CLI version. This process involves reorganizing your app's folder structure and adding configurations that tell Shopify CLI how your app is organized.

## Requirements

- You've installed Shopify CLI
- The latest version of Chrome or Firefox

## What you'll learn

In this tutorial, you'll learn the following:

- How to create CLI-specific configuration files for your project
- How to migrate your app code

**Tip:** If you want to keep the Git history for your project, then you should update your app in the current root directory instead of creating a new directory.

## Benefits of migration

When you migrate your app to use Shopify CLI 3.x, you can take advantage of the following improvements to the developer experience:

### Conventional directory structure

To offer a better and more integrated development experience, apps built using Shopify CLI 3.x follow a conventional directory structure. This structure allows you to serve and deploy your app and its app extensions at the same time, and generate new app extensions easily.

### Simplified configuration files

To make reading and editing configuration files easier, apps that use Shopify CLI 3.x use TOML instead of YAML. Only a small set of files and settings are required, so configurations can be made and tracked in fewer files, and fewer manual configurations need to be made.

### Node runtime

The Shopify CLI 3.x is implemented in JavaScript to run in the Node runtime, more closely aligning the Shopify CLI and app development experience.

## Web component conventions

Shopify CLI builds and serves the various parts of your app using the following conventions, some of which use information that is defined in configuration files.

### Single process or frontend process

The following conventions apply to apps that run on a single process, such as standard Rails apps, and to the frontend process of apps that have both a frontend and backend process.

#### Configuration

The CLI expects at least one shopify.web.toml configuration file, with roles including frontend, or with no type/roles specified. This file can be at the root of the project, or in a project subdirectory.

In the case of a single-process app, include backend in the list of roles as well.

To explicitly specify the folders where Shopify CLI should look for shopify.web.toml files, and to avoid files being loaded twice due to symlinks, use the web_directories variable in the shopify.app.toml file.

#### Provided variables

The following information is provided to the process as environment variables:

- **SHOPIFY_API_KEY**: The client ID of the app.
- **SHOPIFY_API_SECRET**: The client secret of the app.
- **HOST/APP_URL**: The URL that stores will load.
- **PORT/FRONTEND_PORT/SERVER_PORT**: The port in which the process' server should run.
- **SCOPES**: The app's access scopes.
- **BACKEND_PORT**: The port in which the second, or backend, process will run if the app is a two-process app. The frontend uses 'BACKEND_PORT' to proxy traffic to the backend process.

### Second process or backend process

The following conventions apply to the backend process of two-process apps, or to single-process apps.

#### Configuration

The CLI expects a shopify.web.toml configuration file in any subdirectory of the project, with roles including backend.

The frontend must proxy backend requests to the backend port defined in the environment variable BACKEND_PORT.

#### Provided variables

The following information will be provided as environment variables to the process:

- **SHOPIFY_API_KEY**: The client ID of the app.
- **SHOPIFY_API_SECRET**: The client secret of the app.
- **HOST/APP_URL**: The URL that stores will load.
- **SERVER_PORT/BACKEND_PORT/PORT**: The port in which the process's server should run.
- **SCOPES**: The app's access scopes.
- **FRONTEND_PORT**: The port in which the frontend process will run.

### Background process

You can also specify additional processes that will run in the background and don't require the behavior of frontend or backend processes. This can be useful for service-oriented architectures or custom file-watcher processes.

#### Configuration

The CLI accepts a shopify.web.toml configuration file in any subdirectory of the project, with roles = ["background"].

#### Provided variables

The following information will be provided as environment variables to the process:

- **SHOPIFY_API_KEY**: The client ID of the app.
- **SHOPIFY_API_SECRET**: The client secret of the app.
- **HOST/APP_URL**: The URL that stores will load.
- **SERVER_PORT/PORT**: The port in which the process's server should run, if the process includes a server.
- **SCOPES**: The app's access scopes.
- **FRONTEND_PORT**: The port in which the frontend process will run.
- **BACKEND_PORT**: The port in which the second, or backend, process will run, if the app has a backend.

## Step 1: Migrate your embedded app

Your embedded or web app components can be stored at the root of the project, or any subdirectory that contains a shopify.web.toml file.

We recommend that you store files for your embedded app under web/:

```
<App name>/
├── shopify.app.toml
├── package.json
├── web/
│   ├── shopify.web.toml
│   ├── index.html
│   ├── server.js
│   ├── frontend/
│   └── ...
├── extensions/
│   ├── my-ui-extension/
│   │   ├── shopify.extension.toml
│   │   ├── package.json
│   │   └── ...
│   └── ...
```

If you choose to migrate using a web/ directory or another new subdirectory, then you need to move your embedded app source code, tests, configuration files, and dependency files to this directory. This includes your package.json or your Gemfile, the entry index.html file, and any vite or webpack config files.

Only files that are scoped to the project should remain outside of this subdirectory. This might include files like READMEs, Visual Studio Code configuration files, or CI pipelines.

The steps that you need to follow depend on your project language:

- Node.js or Rails
- PHP

If your app only contains app extensions, then you can skip this step.

**Tip:** To explicitly specify the folders where Shopify CLI should look for shopify.web.toml files, and to avoid files being loaded twice due to symlinks, use the web_directories variable in the shopify.app.toml file.

### Node.js or Rails

Create a shopify.web.toml configuration file with content for your project language:

**📁 shopify.web.toml**
```toml
type="frontend"

[commands]
dev = "npm run dev"
```

The dev command instructs the CLI on how to serve the project. The value might differ depending on how the process is invoked in the project. For example, you might need to use bundle exec rails serve if you don't have a Rails binstub, or pnpm run dev if you have a Node project with pnpm as a package manager.

### PHP

Create two shopify.web.toml configuration files, one for the frontend and one for the backend:

**Frontend**
```toml
type="frontend"

[commands]
dev = "php artisan serve --host=localhost"
```

**Backend**
```toml
type="backend"

[commands]
dev = "npm run --prefix ../.. watch"
```

### App hosting

At runtime, the CLI will expose the variables that you'll need to set up your app. These include SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SCOPES, and HOST. Refer to the Shopify starter Node app for an example of the setup in a Node app using the @shopify/shopify-api npm package.

## Step 2: Create a root configuration file

Create a shopify.app.toml file in your app's root directory. shopify.app.toml is a configuration file that contains app-level configurations and metadata. This file also helps Shopify CLI determine whether the directory represents a Shopify app.

The TOML should contain the following information:

- **name**: The name of your app.
- **scopes**: If you're migrating an embedded app, then enter the value of the SCOPES attribute of your .env file. If your app contains only app extensions, then you don't need to include the scopes in this file.

**📁 shopify.app.toml**
```toml
name = "My migrated app"
scopes = "write_products,write_customers,write_draft_orders,read_themes"
```

## Step 3: Connect your app to the Partner Dashboard

Run the dev command to log in to your Partner account, connect your app to your existing app in the Partner Dashboard, and view the embedded app on a development store using a tunnel:

**Terminal**
```bash
shopify app dev
```

## Step 4: Connect your app extensions

For your app to work with Shopify CLI, you need to update how your app extensions are organized in your project. If your app doesn't have app extensions, then you can skip this step.

Follow the steps below for each app extension that's included in your app. For more information about the expected format of each extension, refer to Extensions.

### Step 4A: Reorganize or point to your app extensions

In the default Shopify CLI 3.x app directory structure, each subdirectory under extensions/ represents a single app extension. The extensions/ directory is also where new app extensions are created.

```
<App name>/
├── shopify.app.toml
├── package.json
├── ...
├── extensions/
│   ├── my-ui-extension/
│   │   ├── shopify.extension.toml
│   │   ├── package.json
│   │   └── ...
│   ├── my-function-extension/
│   │   ├── shopify.extension.toml
│   │   ├── package.json
│   │   └── ...
│   ├── my-theme-extension/
│   │   ├── shopify.extension.toml
│   │   ├── package.json
│   │   └── ...
│   └── ...
└── .env
```

For Shopify CLI to find your app extensions, you can do one of two things:

1. Move the files for each of your app extensions to an extensions/ subdirectory.
2. Point to the location of each of your extensions in shopify.app.toml.

**Note:** For checkout post-purchase extensions, Shopify CLI expects an extension script named index.{ts,js,tsx,jsx} to exist in the extension's directory or the src/ subdirectory.

#### Option 1: Move app extension files to the default directory

1. Navigate to your app directory.
2. If you haven't done so already, create an extensions/ subdirectory.
3. Under extensions/, create a new subdirectory for your extension.
4. Move the extension files to your new subdirectory.

#### Option 2: Point to the locations of your app extensions

If you don't want to store your app extensions in the extensions/ subdirectory, then you can specify the directory where each app extension is stored using the extension_directories variable in shopify.app.toml.

You can use a glob pattern to point to directories that contain extensions:

**📁 shopify.app.toml**
```toml
name = "My new app"
scopes = "write_customers,write_orders,write_products"
extension_directories = ["extensions/*", "post_purchase_extension" ]
```

### Step 4B: Update package.json files

You need to remove prerequisites and workflows that have been replaced by Shopify CLI.

Use your package manager to delete the following dependencies:
- @shopify/admin-ui-extensions-run
- @shopify/checkout-ui-extensions-run
- @shopify/shopify-cli-extensions

**Terminal**
```bash
npm uninstall -D @shopify/admin-ui-extensions-run @shopify/checkout-ui-extensions-run @shopify/shopify-cli-extensions
```

In your package.json files, remove the following scripts:
- build
- server
- start

### Step 4C: Reorganize your dependencies

Shopify CLI enables you to manage your npm dependencies multiple ways. You can store all of your dependencies in the root package.json file, or you can use your package manager's workspaces functionality. Using workspaces is recommended, and is the default used by Shopify CLI.

If you decide to use the root package.json as the source of truth for dependencies, then you need to move the extension's dependencies and devDependencies from your extension's package.json to the root package.json.

If the extension's package.json has typescript, eslint, and prettier dependencies, then you should also move them to the app's root package.json so the same dependency version is shared across all of the extensions in the app. If you decide to make TypeScript, ESLint, or Prettier dependencies of your entire app, then you should also move the following configuration files if they're present:

- **Typescript**: tsconfig.json
- **ESLint**: .eslintrc.*, or the eslintConfig attribute from the package.json
- **Prettier**: .prettierrc

After you reorganize your dependencies, run your package manager's install command to install the dependencies, and then make sure that there are no incompatibilities in the dependency graph.

### Step 4D: Migrate your configurations to TOML files

Shopify CLI 3.x uses TOML files instead of YAML files and, in some cases, .env files. The following steps vary depending on the type of extension.

#### Theme app extensions

If you're migrating a theme app extension, then do the following:

1. Create a shopify.extension.toml in the extension's directory.
2. The TOML should contain the following information:
   - **name**: The name of your app extension. name should match the EXTENSION_TITLE from your extension's .env file.
   - **type**: Enter theme.

**📁 shopify.extension.toml**
```toml
name = "My theme extension"
type = "theme"
```

3. Optional: delete any remaining .env, extension.config.yml, and .shopify-cli.yml files.

#### UI extensions (checkout post-purchase)

If you're migrating a checkout post-purchase extension, then do the following:

1. Create a shopify.extension.toml in the extension's directory.
2. The TOML should contain the following information:
   - **name**: The name of your app extension. name should match the EXTENSION_TITLE from your extension's .env file.
   - **type**: Enter checkout_post_purchase.

**📁 shopify.extension.toml**
```toml
name = "My checkout post-purchase extension"
type = "checkout_post_purchase"
```

3. If the extension's extension.config.yml has additional attributes besides type and name, then convert them to TOML using a YAML to TOML converter, and then add them to the shopify.extension.toml.

4. If the extension's .env file has any user-defined variables, then move them to the root .env file of the app.

5. Optional: delete any remaining .env, extension.config.yml, and .shopify-cli.yml files.

### Step 4E: Verify the extension

1. Run the info command to verify that each extension subdirectory is recognized by Shopify CLI:

```
...

DIRECTORY COMPONENTS

web
📂 web
  📂 backend    .
  📂 frontend   ./frontend

checkout_post_purchase
📂 shiny-voice-ext-1567   extensions/shiny-voice-ext-1567
    config file          shopify.extension.toml

theme
📂 damp-resonance-ext-2261   extensions/damp-resonance-ext-2261
    config file             shopify.extension.toml
...
```

2. Run the dev command to open the embedded app on a development store. If you haven't logged into your Partner account or connected your app to an app in the Partner Dashboard, then you'll be prompted to do so in this step.

**Terminal**
```bash
shopify app dev
```

3. Run the deploy command to deploy your app extension code to Shopify.

When you run this command, Shopify CLI creates an app version that contains a snapshot of all of your app extensions, including the app extensions that you manage in the Partner Dashboard, and releases the app version to users.