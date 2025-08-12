# Add a banner to checkout

A custom banner is a notice that you can display to customers. For example, you might want to show a banner that indicates that items are final sale and can't be returned or exchanged.

In this tutorial, you'll use checkout UI extensions to add a customizable banner.

Follow along with this tutorial to build a sample app, or clone the completed sample app.

> **Shopify Plus**
> Checkout UI extensions are available only to Shopify Plus merchants.

The custom banner in checkout, indicating that items are final sale and can't be returned or exchanged.

## What you'll learn

In this tutorial, you'll learn how to do the following:

- Generate a checkout UI extension that appears in the checkout flow using Shopify CLI.
- Set up a banner to display to customers.
- Configure settings that enable app users to control the banner content.
- Support multiple extension targets that enable app users to choose where to render the banner.
- Deploy your extension code to Shopify.

## Requirements

- You've created a Partner account.
- You've created a new development store with the following:
  - Generated test data
  - Checkout and Customer Accounts Extensibility developer preview enabled
- You've created an app that uses Shopify CLI 3.0 or higher.

**Project**
Extension:
- React

[View on GitHub](React)

## Create a checkout UI extension

To create a checkout UI extension, use Shopify CLI, which generates starter code for building your extension.

To create a checkout UI extension, you can use Shopify CLI, which generates starter code for building your extension and automates common development tasks.

1. Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

2. Run the following command to create a new checkout UI extension:

**Terminal**
```bash
shopify app generate extension --template checkout_ui --name my-checkout-ui-extension
```

3. Select a language for your extension. You can choose from TypeScript, JavaScript, TypeScript React, or JavaScript React.

**Tip**
TypeScript or JavaScript is suitable for smaller projects that require a more straightforward API. TypeScript React or JavaScript React is suitable when you want an easy model for mapping state updates to UI updates. With JavaScript or TypeScript, you need to map state updates yourself. This process is similar to writing an application targeting the DOM, versus using react-dom.

You should now have a new extension directory in your app's directory. The extension directory includes the extension script at src/index.{file-extension}. The following is an example directory structure:

Checkout UI extension file structure

```
└── my-app
    └── extensions
        └── my-checkout-ui-extension
            ├── src
            │   └── Checkout.jsx OR Checkout.js // The index page of the checkout UI extension
            ├── locales
            │   ├── en.default.json // The default locale for the checkout UI extension
            │   └── fr.json // The locale file for non-regional French translations
            ├── shopify.extension.toml // The config file for the checkout UI extension
            └── package.json
```

4. Start your development server to build and preview your app:

**Terminal**
```bash
shopify app dev
```

To learn about the processes that are executed when you run dev, refer to the Shopify CLI command reference.

5. Press p to open the developer console. In the developer console page, click on the preview link for your extension.

## Set up a target for your extension

Set up a target for your checkout UI extension. Targets control where your extension renders in the checkout flow.

### Export the extension targets from your script file

In your Checkout.jsx file, set the entrypoints for the checkout extension, and then export them so they can be referenced in your configuration.

For each extension target that you want to use, create a reactExtension function that references your target, and export it using a named export.

- purchase.checkout.block.render
- purchase.checkout.delivery-address.render-before

### Reference the extension targets in your configuration file

You can define more than one target so that app users can add the extension to multiple locations in the checkout.

In your checkout UI extension's configuration file, for each of your targets, create an [[extensions.targeting]] section with the following information:

- **module**: The path to the file that contains the extension code.
- **target**: An identifier that specifies where you're injecting code into Shopify. This needs to match the target that you exported from your file/s.

shopify.extension.toml is the configuration file for your extension. It contains basic information and settings.

**Note**
Whenever you edit your extension configuration file, you need to restart your server for the changes to take effect.

**Terminal**
```bash
shopify app dev
```

## Configure the settings

The settings for a checkout UI extension define fields that the app user can set from the checkout editor.

You can use validation options to apply additional constraints to the data that the setting can store, such as a minimum or maximum value.

### Define the required properties for the settings

Define the settings that you want to expose to app users in shopify.extension.toml. For each setting, define the required properties: key, type, and name.

- The **key** property defines a string that's used to access the setting values from your extension code.
- The **type** property determines the type of information that the setting can store. Each setting types has built-in validation on the setting input.
- The **name** property defines the name for the setting that's displayed to the app user in the checkout editor.

### Define the optional properties for the settings

For each setting, define the optional properties: description and validations.

- The **description** property is displayed to the app user in the checkout editor.
- The **validations** property defines constraints on the setting input that Shopify validates.

## Use the configured settings in the UI extension

Use the values that have been configured by the app user in the checkout UI extension.

### Access app user settings

Retrieve the settings values within your extension. Set default settings so the app can be previewed without being deployed.

In React, the useSettings hook re-renders your extension with the latest values.

When an extension is being installed in the checkout editor, the settings are empty until an app user sets a value. This object is updated in real time as the app user fills in the settings.

- useSettings

### Render the banner

Render the checkout UI extension Banner component with the content from the settings that you configured.

### Add the Banner component

Using the Banner component, create the custom banner.

- Banner

## Preview the extension

Preview your extension to make sure that it works as expected.

### Start your server

Run the Shopify CLI dev command to build your app and preview it on your development store.

Make sure that you select a development store that has enabled the developer preview for Checkout and Customer Accounts Extensibility.

1. In a terminal, navigate to your app directory.
2. Either start or restart your server to build and preview your app:

**Terminal**
```bash
shopify app dev
```

3. Press p to open the developer console.
4. In the developer console page, click on the preview link for the custom banner extension.
5. The checkout opens.

This section describes how to solve some potential errors when you run dev for an app that contains a checkout UI extension.

### Property token error

If you receive the error ShopifyCLI:AdminAPI requires the property token to be set, then you'll need to use the --checkout-cart-url flag to direct Shopify CLI to open a checkout session for you.

**Terminal**
```bash
shopify app dev --checkout-cart-url cart/{product_variant_id}:{quantity}
```

### Missing checkout link

If you don't receive the test checkout URL when you run dev, then verify the following:

- You have a development store populated with products.
- You're logged in to the correct Partners organization and development store. To verify, check your app info using the following command:

**Terminal**
```bash
shopify app info
```

Otherwise, you can manually create a checkout with the following steps:

1. From your development store's storefront, add some products to your cart.
2. From the cart, click Checkout.
3. From directory of the app that contains your extension, run dev to preview your app:

**Terminal**
```bash
shopify app dev
```

4. On the checkout page for your store, change the URL by appending the ?dev=https://{tunnel_url}/extensions query string and reload the page. The tunnel_url parameter allows your app to be accessed using a unique HTTPS URL.

You should now see a rendered order note that corresponds to the code in your project template.

When you're ready to release your changes to users, you can create and release an app version. An app version is a snapshot of your app configuration and all extensions.

1. Navigate to your app directory.
2. Run the following command.

Optionally, you can provide a name or message for the version using the --version and --message flags.

**Terminal**
```bash
shopify app deploy
```

Releasing an app version replaces the current active version that's served to stores that have your app installed. It might take several minutes for app users to be upgraded to the new version.

**Tip**
If you want to create a version, but avoid releasing it to users, then run the deploy command with a --no-release flag. You can release the unreleased app version using Shopify CLI's release command, or through the Partner Dashboard.

## Test the banner settings

After the extension has been deployed, app users can edit the banner settings in the checkout editor. Test the banner settings so that you can see how they appear to app users.

### Test the the banner settings in the checkout editor

1. In the development store where your app is installed, open the checkout editor: in the Shopify admin for the development store, navigate to **Settings > Checkout > Customize**.
2. In the checkout editor, select **Add an app block**, and then select your extension.
3. In the **App block settings** section, update the banner title, description, and status.
4. To preview your changes, do the following:
   - From your development store's storefront, add products to your cart.
   - Click **Check out**.
   - View the banner on the first page of the checkout. The banner reflects the settings that you set in the checkout editor.

**📁 Checkout.jsx**
`/extensions/custom-banner/src/Checkout.jsx`

```javascript
import React from "react";
import {
  reactExtension,
  Banner,
  useSettings,
} from "@shopify/ui-extensions-react/checkout";

// Set the entry points for the extension
const checkoutBlock = reactExtension("purchase.checkout.block.render", () => <App />);
export { checkoutBlock };

const deliveryAddress = reactExtension("purchase.checkout.delivery-address.render-before", () => <App />);
export { deliveryAddress };

function App() {
  // Use the merchant-defined settings to retrieve the extension's content
  const {title: merchantTitle, description, collapsible, status: merchantStatus} = useSettings();

  // Set a default status for the banner if a merchant didn't configure the banner in the checkout editor
  const status = merchantStatus ?? 'info';
  const title = merchantTitle ?? 'Custom Banner';

  // Render the banner
  return (
    <Banner title={title} status={status} collapsible={collapsible}>
      {description}
    </Banner>
  );
}
```

**📁 shopify.extension.toml**
`/extensions/custom-banner/shopify.extension.toml`

```toml
# Learn more about configuring your checkout UI extension:
# https://shopify.dev/api/checkout-extensions/checkout/configuration

# The version of APIs your extension will receive. Learn more:
# https://shopify.dev/docs/api/usage/versioning
api_version = "2024-07"

[[extensions]]
type = "ui_extension"
name = "custom-banner"
handle = "custom-banner"

# Controls where in Shopify your extension will be injected,
# and the file that contains your extension's source code. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/targets-overview
[[extensions.targeting]]
target = "purchase.checkout.block.render"
module = "./src/Checkout.jsx"
export = "checkoutBlock"

[[extensions.targeting]]
target = "purchase.checkout.delivery-address.render-before"
module = "./src/Checkout.jsx"
export = "deliveryAddress"

[extensions.settings]
  [[extensions.settings.fields]]
  key = "title"
  type = "single_line_text_field"
  name = "Banner title"
  description = "Enter a title for the banner."
  [[extensions.settings.fields]]
  key = "description"
  type = "single_line_text_field"
  name = "Banner description"
  description = "Enter a description for the banner."
  [[extensions.settings.fields]]
  key = "status"
  type = "single_line_text_field"
  name = "Banner status"
    [[extensions.settings.fields.validations]]
    name = "choices"
    value = "[\"info\", \"success\", \"warning\", \"critical\"]"
  [[extensions.settings.fields]]
  key = "collapsible"
  type = "boolean"
  name = "Show collapsible description."
  description = "Display controls to expand or collapse the banner description."
```

## Tutorial complete!

Nice work - what you just built could be used by Shopify merchants around the world! Keep the momentum going with these related tutorials and resources.

## Next steps

- **Localize your extension**
  Learn how to localize the text and number formats in your extension.

- **Explore the checkout UI extension component reference**
  Learn about all of the components that you can use in your checkout UI extension.

- **Explore the checkout UI extension targets API reference**
  Learn about the extension targets offered in the checkout.