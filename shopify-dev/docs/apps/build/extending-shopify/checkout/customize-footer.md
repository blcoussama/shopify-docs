# Customize the footer that displays at checkout

You can customize the checkout footer with trust-building information such as links to policies for shipping and returns.

This guide explains how to customize the footer using Shopify Extensions in Checkout. You'll use checkout UI extensions and the GraphQL Admin API's checkout branding fields to render a customized footer on the Checkout and Thank you pages.

**Note**
Toggling the visibility for footer policies affects only the Checkout and Thank you pages. The Order Status and customer account pages aren't affected.

Follow this guide for an end-to-end example. Then, explore the API documentation to suit your customization needs.

> **Shopify Plus**
> Checkout UI extensions and styling customizations are available only to Shopify Plus merchants.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Hide the default footer, including the default policy links.
- Set the footer to full width.
- Configure an extension for multiple targets, such as the Checkout and Thank you pages.
- Populate the footer with custom links.
- Deploy your extension code to Shopify.

## Requirements

- The store that you're modifying with the branding API must be on a Shopify Plus plan.
- You've created a Partner account.
- You've created a new development store with the following:
  - Generated test data
  - Checkout and Customer Accounts Extensibility developer preview enabled
- You've created an app that uses Shopify CLI 3.0 or higher.
- Your app can make authenticated requests to the GraphQL Admin API.
- Installed GraphiQL or created an app
- You've either installed the GraphiQL app on your store or created an app, with the read_checkout_branding_settings and write_checkout_branding_settings access scopes.
- You're using API version 2024-04 or higher.
- You're familiar with the GraphQL Admin API's branding structures.

**Project**
Extension:
- React

[View on GitHub](React)

## Retrieve the store's published checkout profile ID

Checkout styling properties apply to a checkout profile.

In this step, you'll retrieve the ID of the checkout profile to which you'll apply changes to the footer.

Query checkoutProfiles to retrieve a list of checkout profile IDs.

The is_published parameter indicates which checkout profile is currently applied to your store's live checkout.

Make note of your corresponding ID from the list. You'll supply the ID in subsequent mutations.

**POST** `https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json`

GraphQL query | JSON response

```graphql
query checkoutProfiles {
  checkoutProfiles(first: 1, query: "is_published:true") {
    edges {
      node {
        id
        name
      }
    }
  }
}
```

## Hide the default footer policy links and make the footer full width

To replace the default footer with customized content, you first need to hide it. After the default is hidden, you can use a checkout UI extension to add the custom footer.

**Note**
If you insert the HIDDEN and END values from the variables into the mutation, then remove the string delimiters as these are enum values.

Make a request to the checkoutBrandingUpsert mutation's customizations object. You'll hide the default footer, and expand the footer to full width so that your extensions can render across the entire page.

**POST** `https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json`

GraphQL mutation | Query variables | JSON response

```graphql
mutation updateCheckoutBranding($checkoutBrandingInput: CheckoutBrandingInput!, $checkoutProfileId:ID!) {
  checkoutBrandingUpsert(checkoutBrandingInput:$checkoutBrandingInput, checkoutProfileId:$checkoutProfileId) {
    checkoutBranding {
      customizations {
        footer {
          content {
            visibility
          }
          position
        }
      }
    }
  }
}
```

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

## Set up multiple targets for your extension

Targets control where your extension renders in the checkout flow. Extensions can support one or multiple targets.

This example uses purchase.checkout.footer.render-after and purchase.thank-you.footer.render-after to render the extension on the Checkout and Thank you pages, respectively.

To support multiple targets, you must provide a separate file for each extension target using the export default declaration.

**Note**
You'll import and reference Extension.jsx, which will be created in a later step.

### Export the target from your Checkout script file

In your Checkout.jsx file, set the entrypoint for the checkout extension on the checkout page, and then export it so that you can reference it in your configuration.

- purchase.checkout.footer.render-after

### Export the target from your Thank you script file

Create a new file in your extension's src directory called ThankYou.jsx. You'll use this to set the checkout extension's entrypoint on the Thank you page.

Set the entrypoint for the checkout extension, and then export it so that you can reference it in your configuration.

- purchase.thank-you.footer.render-after

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

## Populate the extension with custom content

In this step, you'll populate the footer with links to store policies, which you'll retrieve with the StandardApi.

### Create the Extension.jsx file

Create a new file in your extension's src directory named Extension.jsx.

This will render the footer content for both targets that you previously set up in Checkout.jsx and ThankYou.jsx

### Render links in a two column layout

Using the InlineStack component, create two groups of links that will become the left and right columns of the footer.

Create links to your storefront's pages using the useShop hook to retrieve the storefrontUrl.

Add the two groups of links to an InlineLayout component, which enables the links to render in two columns.

The StandardApi object is automatically made available to all targets.

- useShop
- Icon
- InlineLayout
- InlineStack
- Link
- Text

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
4. In the developer console page, click on the preview link for the custom footer extension.
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

**📁 Checkout.jsx**
`/extensions/custom-footer/src/Checkout.jsx`

```javascript
import {reactExtension} from '@shopify/ui-extensions-react/checkout';

import Extension from './Extension.jsx';

export default reactExtension('purchase.checkout.footer.render-after', () => (
  <Extension />
));
```

**📁 ThankYou.jsx**
`/extensions/custom-footer/src/ThankYou.jsx`

```javascript
import {reactExtension} from '@shopify/ui-extensions-react/checkout';

import Extension from './Extension.jsx';

export default reactExtension('purchase.thank-you.footer.render-after', () => (
  <Extension />
));
```

**📁 shopify.extension.toml**
`/extensions/custom-footer/shopify.extension.toml`

```toml
# Learn more about configuring your checkout UI extension:
# https://shopify.dev/api/checkout-extensions/checkout/configuration

# The version of APIs your extension will receive. Learn more:
# https://shopify.dev/docs/api/usage/versioning
api_version = "2024-01"

[[extensions]]
type = "ui_extension"
name = "custom-footer"
handle = "custom-footer"

# Controls where in Shopify your extension will be injected,
# and the file that contains your extension's source code. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/extension-targets-overview

[[extensions.targeting]]
module = "./src/Checkout.jsx"
target = "purchase.checkout.footer.render-after"

[[extensions.targeting]]
module = "./src/ThankYou.jsx"
target = "purchase.thank-you.footer.render-after"

[extensions.capabilities]
# Gives your extension access to directly query Shopify's storefront API.
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/configuration#api-access
# api_access = true
```

**📁 Extension.jsx**
`/extensions/custom-footer/src/Extension.jsx`

```javascript
import {
  Icon,
  InlineLayout,
  InlineStack,
  Link,
  Text,
  View,
  useShop,
} from '@shopify/ui-extensions-react/checkout';

export default function Extension() {
  const {storefrontUrl} = useShop();

  return (
    <InlineLayout
      blockAlignment="center"
      columns={["auto", "fill"]}
      accessibilityRole="navigation"
    >
      <InlineStack
        spacing="extraTight"
        blockAlignment="center"
        accessibilityRole="orderedList"
      >
        <InlineStack
          accessibilityRole="listItem"
          blockAlignment="center"
          spacing="extraTight"
        >
          <Link to={storefrontUrl}>Home</Link>
          <Icon source="chevronRight" size="extraSmall" />
        </InlineStack>
        <InlineStack
          accessibilityRole="listItem"
          blockAlignment="center"
          spacing="extraTight"
        >
          <Link to={new URL("/collections", storefrontUrl).href}>Shop</Link>
          <Icon source="chevronRight" size="extraSmall" />
        </InlineStack>
        <InlineStack accessibilityRole="listItem">
          <Text appearance="subdued">Checkout</Text>
        </InlineStack>
      </InlineStack>

      <InlineStack
        spacing="tight"
        inlineAlignment="end"
        accessibilityRole="orderedList"
      >
        <View accessibilityRole="listItem">
          <Link to={new URL("/sizing", storefrontUrl).href}>Sizing</Link>
        </View>
        <View accessibilityRole="listItem">
          <Link to={new URL("/terms", storefrontUrl).href}>Terms</Link>
        </View>
        <View accessibilityRole="listItem">
          <Link to={new URL("/privacy", storefrontUrl).href}>Privacy</Link>
        </View>
        <View accessibilityRole="listItem">
          <Link to={new URL("/faq", storefrontUrl).href}>FAQ</Link>
        </View>
        <View accessibilityRole="listItem">
          <Link to={new URL("/accessibility", storefrontUrl).href}>
            Accessibility
          </Link>
        </View>
      </InlineStack>
    </InlineLayout>
  );
}
```

## Tutorial complete!

Nice work - what you just built could be used by Shopify merchants around the world!

Keep the momentum going with these related tutorials and resources.

## Next steps

- **Localize your extension**
  Learn how to localize the text and number formats in your extension.

- **Explore the checkout UI extension component reference**
  Learn about all the components you can use in your checkout UI extensions.

- **Explore the checkout branding API**
  Learn about other properties that are exposed in the GraphQL Admin API's checkout branding types.