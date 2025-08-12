# Create client-side validation with checkout UI extensions

**Note**
Blocking checkout progress behavior doesn't apply to express checkout options, such as Shop Pay, Google Pay, and Apple Pay.

You can block customers from progressing through the checkout based on information that they provide. For example, you might want to block the checkout based on the age or address entered by the customer.

This tutorial uses checkout UI extensions to collect input and validate it.

Using the buyerJourney intercept and block_progress capabilities, customers are blocked from progressing in checkout and shown a validation error. The extension UI adjusts to handle cases where the user doesn't allow the extension to block the checkout progress.

This tutorial explains the process to validate a customer's age, but you can use it as an example to build other customizations for field validation, such as the following:

- Address
- Tax code
- Phone number
- PO box address
- Name

Follow along with this tutorial to build a sample app, or clone the completed sample app.

> **Shopify Plus**
> Checkout UI extensions are available only to Shopify Plus merchants.

## What you'll learn

In this tutorial, you'll learn how to do the following:

- Generate a checkout UI extension that appears in the checkout flow using Shopify CLI.
- Set up the extension target and capabilities to block the checkout progress.
- Intercept and prevent a customer's progress through the checkout, and display an error message at the field and page level.
- Check whether you have the ability to block the checkout progress.

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

## Set up an extension target and configure capabilities

Set up a target for your checkout UI extension. Targets control where your extension renders in the checkout flow.

In your extension configuration, add the optional capabilities that you want to use. Capabilities allow you to access additional functionality in your extension.

### Export the targets from your script file

In your Checkout.jsx file, set the entrypoints for the checkout UI extension, and then export them so they can be referenced in your configuration.

For each target that you want to use, create a reactExtension function that references your target, and export it using the default export.

This example code uses the purchase.checkout.contact.render-after target to render the extension after the contact form element.

You can define more than one static target so that app users can add the extension to multiple locations in the checkout. You can do this by using multiple reactExtension functions with different static targets.

- reactExtension
- purchase.checkout.contact.render-after

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

### Configure the block_progress capability

In your checkout UI extension's configuration file, for each of your targets, create an [extensions.capabilities] section with block_progress set to true.

The block_progress capability enables the extension to block checkout progress if the app user allows it when configuring the extension within the checkout editor.

- block_progress

## Check for the ability to block checkout progress

The block_progress capability allows extensions to block a customer's progress through checkout.

Adding the block_progress capability to your shopify.extension.toml file doesn't guarantee that the extension can block checkout progress. The user can allow or disallow this capability in the checkout editor.

Your extension should update its functionality based on whether the user has allowed the extension to block checkout progress.

### Subscribe to block_progress capabilities

Use the useExtensionCapability hook to subscribe to the block_progress capability. This hook returns a Boolean value that indicates whether the app user has allowed the extension to block checkout progress.

- useExtensionCapability
- block_progress

## Render the custom field

Render a text field where the customer can enter their age.

### Add a text field

Use the TextField component to create a new field.

- TextField

### Update the text field based on the block progress setting

Depending on the value of the canBlockProgress variable that's returned from the useExtensionCapability hook, set the required attribute for the TextField component.

In the Shopify checkout, if a field is marked as required, then the customer must fill out the field before they can continue through the checkout.

You should adjust your extension UI to handle cases where the user doesn't allow the extension to block the checkout progress, including adjusting the UI accordingly. In this example, the label of the TextField updates to indicate if the field is required.

- useExtensionCapability
- TextField

## Perform validation

Use the buyerJourney intercept to show an error message in the checkout UI and block checkout progress when the customer inputs an invalid age.

### Add the buyerJourney intercept

Use the buyerJourney intercept to conditionally block checkout progress and update errors in the checkout UI.

### Block the checkout progress

When the customer's age isn't set, or is less than the target age, block the checkout progress by returning an object with a key of behavior and a value of block.

### Update field validation errors

When the customer's age isn't set, update the field validation errors by setting the perform property to a function that updates the field error message.

This callback is called when all interceptors finish. You should set errors or reasons for blocking at this stage so that all the errors in the UI show up at the same time.

### Add checkout errors

When the customer's age is less than the target age, add an error message by setting the errors field of the object returned by the buyerJourney intercept. This error is rendered outside of the extension UI.

### Allow the checkout to continue

When the customer's age is greater than the target age, allow the checkout progress by returning an object with a key of behavior and a value of allow.

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
4. In the developer console page, click on the preview link for the custom client validation extension.
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

## Test the extension functionality

Test your extension to make sure that the custom field validation works as expected.

1. In the checkout, navigate to the Contact page.
2. In the Your age field, enter a value that's less than the target age (18).
3. An error is returned and you aren't able to proceed to the next page of the checkout.

If you're running an extension locally, then you're automatically granted the block_progress capability as long as it's set in your shopify.extension.toml file.

To simulate a case where the app user hasn't granted the capability to block checkout progress, you can set the capability to false in your shopify.extension.toml file, and then restart the extension server.

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

**📁  Checkout.jsx**
`/extensions/client-validation/src/Checkout.jsx`

```javascript
import {
  reactExtension,
  TextField,
  useExtensionCapability,
  useBuyerJourneyIntercept,
} from "@shopify/ui-extensions-react/checkout";
import React, { useState } from "react";
// Set the entry point for the extension
export default reactExtension("purchase.checkout.contact.render-after", () => <App />);

function App() {
  // Set the target age that a buyer must be to complete an order
  const ageTarget = 18;

  // Set up the app state
  const [age, setAge] = useState("");
  const [validationError, setValidationError] = useState("");
  // Merchants can toggle the `block_progress` capability behavior within the checkout editor
  const canBlockProgress = useExtensionCapability("block_progress");
  const label = canBlockProgress ? "Your age" : "Your age (optional)";
  // Use the `buyerJourney` intercept to conditionally block checkout progress
  useBuyerJourneyIntercept(({ canBlockProgress }) => {
    // Validate that the age of the buyer is known, and that they're old enough to complete the purchase
    if (canBlockProgress && !isAgeSet()) {
      return {
        behavior: "block",
        reason: "Age is required",
        perform: (result) => {
          // If progress can be blocked, then set a validation error on the custom field
          if (result.behavior === "block") {
            setValidationError("Enter your age");
          }
        },
      };
    }

    if (canBlockProgress && !isAgeValid()) {
      return {
        behavior: "block",
        reason: `Age is less than ${ageTarget}.`,
        errors: [
          {
            // Show a validation error on the page
            message:
              "You're not legally old enough to buy some of the items in your cart.",
          },
        ],
      };
    }

    return {
      behavior: "allow",
      perform: () => {
        // Ensure any errors are hidden
        clearValidationErrors();
      },
    };
  });
  function isAgeSet() {
    return age !== "";
  }

  function isAgeValid() {
    return Number(age) >= ageTarget;
  }

  function clearValidationErrors() {
    setValidationError("");
  }
  // Render the extension
  return (
    <TextField
      label={label}
      type="number"
      value={age}
      onChange={setAge}
      onInput={clearValidationErrors}
      required={canBlockProgress}
      error={validationError}
    />
  );
}
```

**📁  shopify.extension.toml**
`/extensions/client-validation/shopify.extension.toml`

```toml
# Learn more about configuring your checkout UI extension:
# https://shopify.dev/api/checkout-extensions/checkout/configuration

# The version of APIs your extension will receive. Learn more:
# https://shopify.dev/docs/api/usage/versioning
api_version = "2024-07"

[[extensions]]
type = "ui_extension"
name = "client-validation"
handle = "client-validation"

# Controls where in Shopify your extension will be injected,
# and the file that contains your extension's source code. Learn more:
# https://shopify.dev/docs/api/checkout-ui-extensions/unstable/targets-overview
[[extensions.targeting]]
target = "purchase.checkout.contact.render-after"
module = "./src/Checkout.jsx"
[extensions.capabilities]
block_progress = true
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