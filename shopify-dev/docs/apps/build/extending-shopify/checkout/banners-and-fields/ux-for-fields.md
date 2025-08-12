# UX for fields

> **Shopify Plus**
> Checkout UI extensions that render on the information and shipping and payment steps in checkout are available only to stores on a Shopify Plus plan.

This guide introduces UX guidelines for adding custom fields to checkout.

## Placement

A static extension target lets you define the placement for the extension. Depending on your use case, you might also define multiple static targets to place your extension. For example, you might want to give the option to place the delivery instructions extension either before or after the shipping methods section.

**📁 Checkout.jsx**
`src/Checkout.jsx`


```javascript
...
// Set multiple entry points for the extension.
// Add all targets to your configuration file.
const shippingRenderBefore = reactExtension("purchase.checkout.shipping-option-list.render-before", () => <App />);
export shippingRenderBefore;

const shippingRenderAfter= reactExtension("purchase.checkout.shipping-option-list.render-after", () => <App />);
export shippingRenderAfter;

function App() {
  ...
}
```

**📁 Checkout.js**
`src/Checkout.js`

```javascript
...
// Set multiple entry points for the extension.
// Add all targets to your configuration file.
const shippingRenderBefore = export default extension("purchase.checkout.shipping-option-list.render-before", renderApp);
export shippingRenderBefore;

const shippingRenderAfter = export default extension("purchase.checkout.shipping-option-list.render-after", renderApp);
export shippingRenderAfter;

function renderApp(root, api) {
  ...
}
```

Place the delivery instructions extension in close proximity to the checkout step that it's related to. In this case, the static extension targets purchase.checkout.shipping-option-list.render-before or purchase.checkout.shipping-option-list.render-after are the best locations for this extension type because it concerns delivery instructions.

**Note**
In some cases, extensions might not render if the static extension target being used is tied to an area that isn't rendered for the customer. For example, extensions using the purchase.checkout.shipping-option-list.render-after target won't show in a checkout with only digital products, since they will not be shipped.

An example of where the purchase.checkout.shipping-option-list.render-after target will render, below the shipping options at checkout.

## Components

The components to create a custom field to capture delivery instructions depend on the extension's possible states.

The delivery instructions use case can have the following states:

- Checkbox is unchecked
- Checkbox checked, TextField then becomes visible
- TextField with value

Components list for the custom field to capture delivery instructions use case

| Component | Preview | Tips |
|-----------|---------|------|
| Checkbox | The Checkbox component with a label beside it that says 'Provide delivery instructions' | N/A |
| TextField | The TextField component with ghost text inside it that says 'Delivery instructions' | Only show this component when the customer has expressed interest in adding delivery instructions. |

## Layout

You can stack the Checkbox and TextField components in the BlockStack component.

Components list for the delivery instructions use case

| Component | Preview |
|-----------|---------|
| BlockStack | A stacked Checkbox and TextField demonstrating BlockStack |

### BlockStack

In the following example, base is the spacing value between the Checkbox and TextField components, which is typically the default option. It prevents the extension from being too cramped or too spacious.

An example of a BlockStack with base spacing.

An example of a Checkbox and TextField with base spacing.

## UX guidelines

Adhere to the following guidelines when you're designing a delivery instructions use case for checkout UI extensions, so that you can help merchants gain customer trust and provide a great checkout experience:

### Reveal information progressively and strategically

Show a simplified state of the extension by default. In the following example, the customer can choose to add delivery instructions to an order. If the customer chooses to add delivery instructions, then the TextField is displayed. It doesn't display otherwise.

An example of how to use custom fields to capture delivery instructions progressively by revealing information with a checkbox

### Capture and remember customer inputs

Preserve inputs through the experience. For example, if the customer writes their delivery instructions in the TextField component, then unchecks the Checkbox component and checks it again, the instructions should still display rather than having the customer type them again.

## Next steps

- Explore UX guidelines for the entire checkout experience.
- For practical guidance on how to design a user interface for the Shopify admin, refer to Shopify's App Design Guidelines.
- Get familiar with Polaris accessibility and content guidelines.