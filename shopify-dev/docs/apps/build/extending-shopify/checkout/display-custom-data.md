# Display custom data at checkout

Checkout UI extensions can read and display custom data that's stored in metafields. For example, in this guide you'll learn how to read watering instructions for plants and display that data next to the plant in the order summary at checkout. Learn from an end-to-end example here, and you can use what you've learned to display other types of metafield data at other checkout UI extension targets.

Follow along with this tutorial to build a sample app, or clone the completed sample app.

> **Shopify Plus**
> Checkout UI extensions are available only to Shopify Plus merchants.

Products in the order summary displaying their watering instructions

## What you'll learn

In this tutorial, you'll learn how to do the following:

- Add custom data to products using a metafield
- Generate a checkout UI extension that appears in the checkout flow using Shopify CLI
- Set up configurations for your checkout UI extension in the extension TOML file
- Render metadata next to products at checkout
- Deploy your extension code to Shopify

## Requirements

- You've created a Partner account.
- You've created a new development store with the following:
  - Generated test data
  - Checkout and Customer Accounts Extensibility developer preview enabled
- You've created an app that uses Shopify CLI 3.0 or higher.

**Project**
Extension:

- React

## Create a metafield for a product

In the Shopify admin, define a metafield and add data to it.

### Add a metafield definition

Add a metafield for the product. For this tutorial, set the Name and the Namespace and key with the following values:

- **Name**: Watering instructions
- **Namespace and key**: The namespace is instructions and the key is watering, entered as instructions.watering.
- Set the **Type** as Single line text.

### Add metafield data

1. Select a product.
2. Under Product metafields, in the text field for the metafield definition that you added, enter the data that you want to display in the checkout UI extension. For example, "Average water needed".
3. Click Save.
4. Repeat these steps for another product, and add different data. For example, "Very little water needed".

## Create a checkout UI extension

To create a checkout UI extension, you'll use Shopify CLI, which generates starter code for building your extension.

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

## Set up an extension target

Set up a target for your checkout UI extension. Targets control where your extension renders in the checkout flow.

### Export the target from your script file

In your Checkout.jsx file, set the entrypoint for the checkout extension, and then export it so that it can be referenced in your configuration.

Create a reactExtension function that references your target, and export it using the default export.

This extension uses the purchase.checkout.cart-line-item.render-after target, to display the custom data after the product.

- reactExtension
- purchase.checkout.cart-line-item.render-after

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

### Reference the metafield in the configuration file

In your checkout UI extension's configuration file, reference the metafield definition so that the extension code in your Checkout.jsx file can read it.

### Add the metafield definition to the extension TOML

Create an [[extensions.metafields]] section with the metafield namespace and key. This needs to match the metafield definition that you created in the Shopify admin.

## Render the extension

Import checkout UI extension resources to render the extension and the metadata in the checkout UI.

### Import the following checkout UI extension resources to render the extension

- **useCartLines**: Return the current line item for the checkout.
- **Text**: Provide semantic value to the text that you're rendering.
- **useAppMetafields**: Return the metafield data for the product.

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
4. In the developer console page, click on the preview link for the custom field extension.
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

**📁 shopify.extension.toml**
`/extensions/read-custom-data/shopify.extension.toml`

```toml
# Learn more about configuring your checkout UI extension:
# https://shopify.dev/api/checkout-extensions/checkout/configuration

# The version of APIs your extension will receive. Learn more:
# https://shopify.dev/docs/api/usage/versioning
api_version = "2024-01"

[[extensions]]
type = "ui_extension"
name = "read-custom-data"
handle = "read-custom-data"

# Controls where in Shopify your extension will be injected,
# and the file that contains your extension's source code. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/targets-overview
[[extensions.targeting]]
target = "purchase.checkout.cart-line-item.render-after"
module = "./src/Checkout.jsx"

[extensions.capabilities]
# Gives your extension access to directly query Shopify's storefront API.
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/configuration#api-access
# api_access = true

# Loads metafields on checkout resources, including the cart,
# products, customers, and more. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/configuration#metafields
[[extensions.metafields]]
namespace = "instructions"
key = "watering"
```

**📁 Checkout.jsx**
`/extensions/read-custom-data/src/Checkout.jsx`

```javascript
import { useEffect, useState } from "react";
import {
  useCartLineTarget,
  Text,
  useAppMetafields,
  reactExtension,
} from "@shopify/ui-extensions-react/checkout";

// Set the entry points for the extension
export default reactExtension("purchase.checkout.cart-line-item.render-after", () => <App />);

function App() {
  // Use the merchant-defined metafield for watering instructions and map it to a cart line
  const wateringMetafields = useAppMetafields({
    type: "product",
    namespace: "instructions",
    key: "watering"
  });
  const cartLineTarget = useCartLineTarget();

  const [wateringInstructions, setWateringInstructions] = useState("");

  useEffect(() => {
    // Get the product ID from the cart line item
    const productId = cartLineTarget?.merchandise?.product?.id;
    if (!productId) {
      return;
    }

    const wateringMetafield = wateringMetafields.find(({target}) => {
      // Check if the target of the metafield is the product from our cart line
      return `gid://shopify/Product/${target.id}` === productId;
    });

    // If we find the metafield, set the watering instructions for this cart line
    if (typeof wateringMetafield?.metafield?.value === "string") {
      setWateringInstructions(wateringMetafield.metafield.value);
    }
  }, [cartLineTarget, wateringMetafields]);

  // Render the watering instructions if applicable
  if (wateringInstructions) {
    return (
        <Text>
          {wateringInstructions}
        </Text>
      );
  }

  return null;
}
```

## Tutorial complete

Nice work - what you just built could be used by Shopify merchants around the world! Keep the momentum going with these related tutorials and resources.

## Next steps

- **Learn more about metafields**
  Learn more about adding and storing additional information about Shopify resources.

- **Localize your extension**
  Learn how to localize text and number formats in your extension.

- **Explore the checkout UI extension component reference**
  Learn about the components that you can use in your checkout UI extension.

- **Explore the checkout UI extension targets API reference**
  Learn about the extension targets that are offered in the checkout.
