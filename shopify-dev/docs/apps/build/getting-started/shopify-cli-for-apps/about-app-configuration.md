# App configuration

You can configure your apps locally with TOML files, then link them to apps in your Partner Dashboard and deploy your changes using Shopify CLI. You can also configure most of this configuration through the Partner Dashboard. The configuration in the Partner Dashboard always reflects the active version of your app.

**Note:** For app configuration changes to take effect, you need to run the deploy command.

Learn more about managing app configuration files.

**Caution:** The shopify app config push Shopify CLI command is no longer supported. If you're using this command in your workflow, follow these steps to update app configuration with the deploy command.

## App configuration file example

**📁 shopify.app.config-name.toml**
```toml
name = "Example App"
client_id = "a61950a2cbd5f32876b0b55587ec7a27"
application_url = "https://www.app.example.com/"
embedded = true
handle = "example-app"

[access_scopes]
scopes = "read_products"

[access.admin]
direct_api_mode = "online"

[auth]
redirect_urls = [
  "https://app.example.com/api/auth/callback",
  "https://app.example.com/api/auth/oauth/callback",
]

[webhooks]
api_version = "2024-01"

[[webhooks.subscriptions]]
topics = [ "app/uninstalled" ]
compliance_topics = [ "customers/redact", "customers/data_request", "shop/redact" ]
uri = "/webhooks"

[app_proxy]
url = "https://app.example.com/api/proxy"
subpath = "store-pickup"
prefix = "apps"

[pos]
embedded = false

[app_preferences]
url = "https://www.app.example.com/preferences"

[build]
automatically_update_urls_on_dev = false
include_config_on_deploy = true
```

## Reference

### Global

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| name | Yes | string | The name of your app. |
| handle | No | string | The URL slug of your app home, for example https://admin.shopify.com/store/your-store-name/apps/your-app-handle/app. **Warning:** Updating the handle changes the admin URL that appears when you access your app from the side menu. As a result, any embedded app admin links will be broken. |
| client_id | Yes | string | The app's public identifier. |
| application_url | Yes | string matching a valid URL | The URL of your app. **Note:** If you're building an extension-only app, then your application_url will be set to https://shopify.dev/apps/default-app-home by default. |
| embedded | Yes | boolean | Embedded apps let users interact with your app without leaving the context of Shopify. |
| extension_directories | No | array of string paths or glob patterns | The paths that Shopify CLI will search for app extensions. When omitted, defaults to ["extensions/"]. |
| web_directories | No | array of string paths or glob patterns | The paths that Shopify CLI will search for the web files of your app. When omitted, defaults to the app root directory. |

### access_scopes

Define the permissions your app requests, as well as how the permissions are requested.

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| scopes | Yes | string matching a comma-separated list of scopes | Any access scopes that your app will request access to during the authorization process. When a merchant installs your app with Shopify managed install, they're prompted to grant permission to all the access scopes that you defined in this field. Learn how to manage access scopes for your app. |
| optional_scopes | No | array of string access scopes | Any access scopes that your app can request dynamically after installation. Learn how to manage access scopes for your app. |
| use_legacy_install_flow | No | boolean | When omitted or false, scopes are saved in your app's configuration, and are automatically requested when the app is installed on a store or when you update the scopes value. This is referred to as Shopify managed installation. When true, the legacy installation flow requests scopes through a URL parameter during the OAuth flow. The legacy installation flow is still supported, but isn't recommended because your app can end up with different scopes for each installation. |

### access

Settings for defining the ways that your app can access Shopify APIs.

**Note:** For app configuration changes to take effect, you need to run the deploy command.

#### admin

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| direct_api_mode | No | string matching online or offline | The access mode that Direct API access will use. When online, Direct API access is enabled and uses an online access token. When offline, Direct API access is enabled and uses an offline access token. When omitted, defaults to online. |
| embedded_app_direct_api_access | No | boolean | Whether your embedded app has access to Direct API access for calling Admin GraphQL APIs. When omitted or false, Direct API access is disabled for embedded apps. When true, Direct API is enabled and uses the mode defined by direct_api_mode. |

### auth

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| redirect_urls | Yes | array of strings matching a valid URL | Users are redirected to these URLs as part of authorization code grant. You must include at least one redirect URL before making your app public. Learn more about redirection URLs. |

### webhooks

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| api_version | Yes | string matching a valid Shopify version (example: 2022-10) | The API version used to serialize webhooks and cloud service events. |

#### subscriptions

Subscribe your app to Shopify webhook topics so that your app is alerted when an event occurs on a merchant's store. Learn more about webhook subscriptions.

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| topics | Yes | array of strings matching a valid topic | The topics that your app subscribes to. Refer to a complete list of topics in the webhooks reference. |
| compliance_topics | No | array of strings matching a valid compliance topic | The topics to manage the requests to view or erase customer personal information. Valid options: customers/redact, customers/data_request or shop/redact. These are required topics to subscribe to for all apps distributed in the Shopify App Store. |
| uri | Yes | string matching a valid URI | Your app's endpoint to handle the events. It can be a HTTPS URL, a relative path starting with a slash, a Google Pub/Sub URI or an Amazon EventBridge Amazon Resource Name (ARN). |
| filter | No | string | A set of rules specified using Shopify API's Search Syntax. Ensures only webhooks that match the filter are delivered. Learn more. |
| include_fields | No | array of strings | Specifies the fields that will be sent in a webhook's event message. If null, then all fields will be sent. Learn more. |

**Info:** The following is the structure of the URL you should use for the URI when working with Google Cloud Pub/Sub:

```
pubsub://{project-id}:{topic-id}
```

Where {project-id} is the ID of your Google Cloud Platform project, and {topic-id} is the ID of the topic that you set up in Google Cloud Pub/Sub.

For Amazon EventBridge, your URL will be similar to the following example:

```
arn:aws:events:<aws_region>::event-source/aws.partner/shopify.com/<app_id>/<event_source_name>
```

### app_proxy

Let Shopify act as a proxy when sending requests to your app. Learn more about app proxy.

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| url | Yes if app_proxy defined | string matching a valid URL | URL of your app proxy server |
| subpath | Yes if app_proxy defined | string containing letters, numbers, underscores, and hyphens up to 30 characters. The value may not be admin, services, password, or login. | The combination of prefix and subpath defines where the app proxy is accessed from a merchant's shop. |
| prefix | Yes if app_proxy defined | string matching a, apps, community, or tools | The combination of prefix and subpath defines where the app proxy is accessed from a merchant's shop. |

### pos

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| embedded | No | boolean | Load your app in Shopify POS using Shopify App Bridge. Learn more. |

### app_preferences

**Note:** For app configuration changes to take effect, you need to run the deploy command.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| url | No | string matching a valid URL | URL for your app's preferences page |

### build

**Note:** For app configuration changes to take effect, you need to run the deploy command.

Settings for running your app through Shopify CLI.

| Property | Required? | Value | Description |
|----------|-----------|-------|-------------|
| automatically_update_urls_on_dev | No | boolean | When true, your app URL and redirect URLs will be automatically updated on dev. This is useful when using the built-in tunnel for development. When false, your URLs won't be updated on dev. Recommended for production apps. When omitted, you will be prompted to choose an option on dev. |
| include_config_on_deploy | No | boolean | Soon, this will no longer be optional and configuration will be included on every deploy. When true, your local app configuration will be included in the app version created on deploy. Recommended for all apps. When omitted or false, your app configuration won't be updated on deploy. The active configuration will be re-used in the new app version. Not recommended, since you can only update app configuration from the Partner Dashboard. |
| dev_store_url | No | string matching a valid store URL | The name of the dev store used to preview your app. |

## Migrate from config push

The shopify app config push Shopify CLI command is no longer supported. Instead, you can release your app configuration and extensions together with the deploy command.

### Migrate interactively

If you use the shopify app config push command without the --force flag, then follow these steps to migrate to the deploy command:

1. Upgrade Shopify CLI to the latest version.
2. Remove all references to the shopify app config push command in any scripts or aliases.
3. When you're ready to deploy both app configuration and all extensions, run the deploy command.

**Terminal**
```bash
shopify app deploy
```

4. Shopify CLI will ask if you want to start including app configuration on deploy. Answer Yes, always, and your choice will be saved in your app configuration file.
5. Continue the rest of the deploy flow to release a new app version to users.
6. Push your app configuration file to source control, so all contributors use the same app configuration. This ensures that the app and Shopify CLI commands behave the same way in each contributor's environment.

### Update your CI/CD workflow

If you use the shopify app config push with the --force flag, follow these steps to migrate to the deploy command:

1. Upgrade Shopify CLI to the latest version.
2. Remove all references to the shopify app config push command.
3. Add the line `include_config_on_deploy = true` to the [build] section in your app configuration file. Once set, both app configuration and extensions will be included when you deploy.

**📁 shopify.app.config-name.toml**
```toml
[build]
include_config_on_deploy = true
```

4. Add the deploy command with the --force flag to your workflow, if it's not there already. Refer to the example workflows for more details.