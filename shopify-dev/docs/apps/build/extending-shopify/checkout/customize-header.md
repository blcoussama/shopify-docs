# Customize the header that displays at checkout

You can customize the checkout header for custom navigation experiences. For example, you can hide the default back-to-cart link and add custom breadcrumbs.

This guide explains how to customize the header using checkout UI extensions and the GraphQL Admin APIs checkout branding fields to render a customized header on the Checkout page.

Learn from an end-to-end example in this guide, and then explore the API documentation to suit your customization needs.

> **Shopify Plus**
> Checkout UI extensions and styling customizations are available only to Shopify Plus merchants.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Hide the default back-to-cart link and buyer journey breadcrumbs.
- Configure a checkout UI extension for a single target to render in the header.
- Add custom breadcrumbs to the header.
- Deploy your UI extension to Shopify.

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

In this step, you'll retrieve the ID of the checkout profile to which you'll apply changes to the header.

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

## Hide the default back-to-cart icon and buyer journey breadcrumbs

Make a request to the checkoutBrandingUpsert mutation's CheckoutBrandingCustomizationsInput object. You'll hide the default back-to-cart icon and the buyer journey breadcrumbs. In a later step, you'll replace these default elements with your own customized breadcrumbs.

**POST** `https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json`

GraphQL mutation | Query variables | JSON response

```graphql
mutation updateCheckoutBranding($checkoutBrandingInput: CheckoutBrandingInput!, $checkoutProfileId:ID!) {
  checkoutBrandingUpsert(checkoutBrandingInput:$checkoutBrandingInput, checkoutProfileId:$checkoutProfileId) {
    checkoutBranding {
      customizations {
        buyerJourney {
          visibility
        }
        cartLink {
          visibility
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
├── my-app
    ├── extensions
        ├── my-checkout-ui-extension
            ├── src
            │   ├── Checkout.jsx OR Checkout.js // The index page of the checkout UI extension
            ├── locales
            │   ├── en.default.json // The default locale for the checkout UI extension
            │   ├── fr.json // The locale file for non-regional French translations
            ├── shopify.extension.toml // The config file for the checkout UI extension
            ├── package.json
```

4. Start your development server to build and preview your app:

**Terminal**
```bash
shopify app dev
```

To learn about the processes that are executed when you run dev, refer to the Shopify CLI command reference.

5. Press p to open the developer console. In the developer console page, click on the preview link for your extension.

## Set up the target for your extension

Targets control where your extension renders in the checkout flow.

This example uses purchase.checkout.header.render-after.

**Note**
You'll import and reference Extension.jsx, which you'll create in a later step.

There is a corresponding purchase.thank-you.header.render-after target on the Thank you page. While this breadcrumbs example only renders in the Checkout, other use cases could benefit from targeting both Checkout and Thank you pages.

### Export the target from your Checkout script file

In your Checkout.jsx file, set the entrypoint for the checkout extension on the checkout page, and then export it so that you can reference it in your configuration.

- purchase.checkout.header.render-after

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

## Render the custom breadcrumb

In this step you'll populate the header with custom breadcrumb navigation.

### Create the Extension.jsx file

Create a new file in your extension's src directory named Extension.jsx.

This will render the breadcrumbs in the header for the target that you previously set up in Checkout.jsx

### Add custom translations for strings

Add custom translations for your "cart" string.

To better support buyers in different locales, you should avoid using hard-coded strings in your extensions. The translated cart string is used in line 20 of Extension.jsx.

- Localization

### Get the appropriate state to populate your breadcrumbs

As the buyer steps through a checkout, their activeStep will update to reflect where they are currently in the buyer journey. You may want to provide different treatments for visited steps, the activeStep, and steps in the future.

**Note**
steps can vary between store setups, such as stores with one-page versus three-page checkout. They can also vary between buyers, such as those purchasing digital-only goods where a "Shipping" step may be omitted.

- useBuyerJourneySteps
- useBuyerJourneyActiveStep

### Add custom breadcrumbs

Render custom breadcrumbs using checkout UI components and the steps and activeStep returned from the buyer journey hooks.

- Divider
- InlineLayout
- Link
- Text
- View

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
4. In the developer console page, click on the preview link for the custom header extension.
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
`/extensions/custom-header/src/Checkout.jsx`

```javascript
import {reactExtension} from '@shopify/ui-extensions-react/checkout';

import Extension from './Extension.jsx';

export default reactExtension('purchase.checkout.header.render-after', () => (
  <Extension />
));
```

**📁 shopify.extension.toml**
`/extensions/custom-header/shopify.extension.toml`

```toml
# Learn more about configuring your checkout UI extension:
# https://shopify.dev/api/checkout-extensions/checkout/configuration

# The version of APIs your extension will receive. Learn more:
# https://shopify.dev/docs/api/usage/versioning
api_version = "2024-04"

[[extensions]]
type = "ui_extension"
name = "custom-header"
handle = "custom-header"

# Controls where in Shopify your extension will be injected,
# and the file that contains your extension's source code. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/extension-targets-overview

[[extensions.targeting]]
module = "./src/Checkout.jsx"
target = "purchase.checkout.header.render-after"

[extensions.capabilities]
# Gives your extension access to directly query Shopify's storefront API.
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/configuration#api-access
# api_access = true
```

**📁 Extension.jsx**
`/extensions/custom-header/src/Extension.jsx`

```javascript
import {
  Divider,
  InlineLayout,
  Link,
  Text,
  View,
  useBuyerJourneySteps,
  useBuyerJourneyActiveStep,
  useShop,
  useTranslate,
} from '@shopify/ui-extensions-react/checkout';

export default function Extension() {
  const steps = useBuyerJourneySteps();
  const activeStep = useBuyerJourneyActiveStep();
  const {storefrontUrl} = useShop();
  const translate = useTranslate();

  const assembledSteps = [
    {label: translate('cart'), handle: 'cart', to: new URL('/cart', storefrontUrl).href},
    ...steps,
  ];

  const activeStepIndex = assembledSteps.findIndex(
    ({handle}) => handle === activeStep?.handle,
  );

  return (
    <InlineLayout
      accessibilityRole="orderedList"
      spacing="none"
      maxInlineSize="fill"
      border="base"
      padding="none"
      cornerRadius="base">
      {assembledSteps.map(({label, handle, to}, index) => (
        <InlineLayout
          accessibilityRole="listItem"
          inlineAlignment="end"
          blockAlignment="center"
          key={handle}
          spacing="none"
          columns={['fill', 'auto']}>
          <View
            inlineAlignment="center"
            minInlineSize="100%"
            padding="extraTight"
            cornerRadius={
              index === assembledSteps.length - 1
                ? ['none', 'base', 'base', 'none']
                : 'none'
            }
            background={
              activeStep?.handle === handle ? 'subdued' : 'transparent'
            }>
            {index < activeStepIndex || handle === 'cart' ? (
              <Link to={to}>{label}</Link>
            ) : (
              <Text
                emphasis={activeStep?.handle === handle ? 'bold' : undefined}
                appearance={
                  activeStep?.handle !== handle ? 'subdued' : undefined
                }>
                {label}
              </Text>
            )}
          </View>
          {index < assembledSteps.length - 1 ? (
            <Divider direction="block" />
          ) : null}
        </InlineLayout>
      ))}
    </InlineLayout>
  );
}
```

**📁 en.default.json**
`/extensions/custom-header/locales/en.default.json`

```json
{
  "cart": "My Cart"
}
```

## Tutorial complete!

Nice work - what you just built could be used by Shopify merchants around the world! Keep the momentum going with these related tutorials and resources.

## Next steps

- **Localize your extension**
  Learn how to localize the text and number formats in your extension.

- **Explore the checkout UI extension component reference**
  Learn about all the components you can use in your checkout UI extensions.

- **Explore the checkout branding API**
  Learn about other properties that are exposed in the GraphQL Admin API's checkout branding types.