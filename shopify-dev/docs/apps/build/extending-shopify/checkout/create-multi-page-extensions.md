# Create multi-page extensions

In this tutorial, you'll learn how a UI extension can target checkout, the Thank you page, the Order status page, or all of the above, to create a seamless experience for merchants and their customers.

## What you'll learn

In this tutorial, you'll learn how to create a checkout UI extension that can render in checkout, the Thank you page, the Order status page, or all three areas.

## Requirements

- You're familiar with Thank you and Order status page checkout UI extensions.
- You've created a Partner account.
- You've created a new development store with the following:
  - Generated test data
  - Checkout and Customer Accounts Extensibility developer preview enabled
- You've created an app that uses Shopify CLI 3.0 or higher.

## How it works

You can use a checkout UI extension to add custom content across multiple pages of checkout.

Depending on the page and state of Shopify's internal order processing, the targets and APIs available to extensions can vary.

A multi-page extension can be used to add custom content such as final sale details, upsells, surveys and more. The following examples demonstrate how to use targets to target different parts of the flow, depending on your use case.

### Pre-purchase

You can configure a UI extension to display before a purchase is completed by using the `purchase.checkout.cart-line-item.render-after` extension target. This means that merchants can place the extension on the information, payment and shipping steps of checkout (pre-purchase).

**📁 Checkout.tsx**
`src/Checkout.tsx`

```javascript
// Set up the entry point for the extension
const cartLineItemRender = reactExtension("purchase.checkout.cart-line-item.render-after", () => <App />);
export {cartLineItemRender};
```

**📁 shopify.extension.toml**

An image that shows a UI extension in the order summary displaying that the product cannot be shipped to PO boxes

### Post-purchase

You can configure an extension to display after a purchase is completed by using both the `purchase.thank-you.cart-line-item.render-after` and `customer-account.order-status.cart-line-item.render-after` extension targets. This means that merchants can place the extension on the Thank you and Order status pages (post-purchase).

**📁 Checkout.tsx**
`src/Checkout.tsx`

```javascript
// Allow the extension to render on the Thank you page
const thankYouRender = reactExtension("purchase.thank-you.cart-line-list.render-after", () => <App />);
export {thankYouRender};
// Allow the extension to render on the Order status page
const orderDetailsRender = reactExtension("customer-account.order-status.cart-line-item.render-after", () => <App />);
export {orderDetailsRender};
```

**📁 shopify.extension.toml**

An image that shows an extension in the order summary displaying expected shipping delays

### Pre and post purchase

You can configure an extension to display on all areas of the checkout by combining the `purchase.checkout.cart-line-item.render-after`, `purchase.thank-you.cart-line-item.render-after` and `customer-account.order-status.cart-line-item.render-after` extension targets.

**📁 Checkout.tsx**
`src/Checkout.tsx`

```javascript
// Allow the extension to render on the pre-purchase checkout pages
const cartLineItemRender = reactExtension("purchase.thank-you.cart-line-item.render-after", () => <App />);
export {cartLineItemRender};
// Allow the extension to render on the Thank you page
const thankYouRender = reactExtension("purchase.thank-you.cart-line-item.render-after", () => <App />);
export {thankYouRender};
// Allow the extension to render on the Order status page
const orderDetailsRender = reactExtension("customer-account.order-status.cart-line-item.render-after", () => <App />);
export {orderDetailsRender};
```

**📁 shopify.extension.toml**

An image that shows a UI extension in the order summary final sale, no returns or exchanges

## Testing the extension in the checkout editor

1. Follow the guide to test an extension in the editor
2. Use the dropdown list at the top of the page to navigate to the Thank you and Order status pages.

**Note**
In a future release, we'll improve the extension installation in the editor to enable merchants to add an extension to multiple pages at once and share configuration between each placements.

## Next steps

- **Get started with editor extension collections**
  Get started with building editor extension collections to group multi-page extensions