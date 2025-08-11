# Apps in checkout

Merchants use Shopify checkout to accept orders and receive payments wherever they sell online. To augment Shopify checkout with new functionality, build an app with extensions.

## How it works

After a customer adds products to a cart, they use Shopify checkout to enter their customer, shipping, and payment information before placing the order.

To extend checkout, apps can use extensions. For example, apps can use extensions to offer a customer free shipping or other discounts, depending on the contents of their cart.

To install apps on their store, merchants can use the Shopify admin. There, they can can use the checkout editor to place a block for a checkout UI extension in the checkout experience.

Actions that a developer, customer, and merchant take in connection to Shopify checkout

## Customization options

There are various types of Shopify Extensions that you can use to customize checkout:

- UI extensions
- Functions
- Web pixel extensions
- Payments extensions

All customization options are easy to install and upgrade-safe, enabling merchants to benefit from Shopify releases new products such as Shop Pay, or features such as One-page checkout.

For a detailed breakdown of the technologies that can be used to customize checkout, and the ways that you can extend checkout, refer to the options for customizing Shopify checkout.

**Note**
Checkout apps and extensions have design requirements that apply to custom apps as well as public apps. Be sure that your app meets all requirements for its functionality and distribution type.

## Getting started

To learn how to customize and extend checkout, read the following tutorials.

## Checkout UI extensions tutorials

**Pre-purchase product offers**
Build a pre-purchase upsell offer that prompts the customer to add a product to their order.

**Post-purchase checkout extensions**
Create a basic example of a post-purchase checkout extension.

**Thank you and order status extensions**
Build a survey that asks customers how they heard about the store after they made a purchase.

**Custom banners**
Learn how to add a custom banner to checkout.

**Custom fields**
Learn how to add custom fields to checkout that customers can use to add delivery instructions to their order.

**Client-side validation**
Use a checkout UI extension to validate fields at checkout and block customer progress.

**Header**
Use a checkout UI extension and the GraphQL Admin API's checkout branding types to customize the checkout header with custom images, including the back to cart link.

**Footer**
Use a checkout UI extension and the GraphQL Admin API's checkout branding types to customize the checkout footer with store policies.

**Address autocomplete**
Build an extension to customize the address autocomplete provider for the delivery and billing address forms in checkout.

## Shopify Functions tutorials

**Build a discount function**
Use Shopify Functions to create a new discount type for users.

**Create a payments function**
Use Shopify Functions to hide a payment option offered to customers at checkout.

**Build a delivery options function**
Use Shopify Functions to rename a delivery option offered to customers at checkout.

**Create a server-side validation function**
Use Shopify Functions to block progress on a checkout when the cart line quantities exceed a limit.

**Build a location rule function**
Use Shopify Functions to choose a different order location during checkout.

**Add a customized bundle function**
Use Shopify Functions to group products together and sell them as a single unit.

**Build a fulfillment constraints function**
Use Shopify Functions to customize fulfillment and delivery strategies.

**Build a local pickup options function**
Use Shopify Functions to generate local pickup delivery options at checkout.

**Create a local pickup charges function**
Use Shopify Functions to create local pickup charges at checkout.

**Generate a pickup points function**
Use Shopify Functions to generate pickup point delivery options at checkout.

## Upgrade

**Deprecated**
checkout.liquid is now unsupported for the Information, Shipping, and Payment checkout steps. checkout.liquid, additional scripts, and script tags are deprecated for the Thank you and Order status pages and will be sunset on August 28, 2025.

Stores that currently use checkout.liquid for the Thank you and Order status pages need to upgrade to Shopify Extensions in Checkout before the deadline.

Shopify Scripts will continue to work alongside Shopify Extensions in checkout until June 30, 2026.

A report identifying your current checkout customizations is available in the Shopify admin. The report provides high-level guidance to map customizations to Shopify Extensions in Checkout. Use this report to simplify your review of your existing customizations and to help you upgrade to Shopify Extensions in Checkout faster. Learn more.

To upgrade a checkout.liquid customization to Shopify Extensions in Checkout, take one or more of the following actions:

- **Use a public app that's built using extensions.**

We're adding new checkout apps to the Shopify App Store on a regular basis. If there currently isn't a suitable public app for your customization, then consider simplifying your checkout temporarily and adding new apps to your store as they become available.

- **Build a custom app using extensions, or hire a service partner to build one for you.**

In some cases, after you've upgraded you can revert to checkout.liquid until its sunset dates.

If you're upgrading a store to Shopify Extensions in Checkout, we recommend planning your in-checkout, Thank you page, and Order status page upgrades together, when possible, for the following benefits:

- Avoid maintaining multiple tech stacks, like UI extensions and checkout.liquid.
- Apply styling once to the entire experience.
- Manage one sunset date for checkout.liquid rather than one date for pre-purchase pages and another for Thank you and Order status pages.

If this isn't possible, then we recommend prioritizing the upgrade for in-checkout pages first and upgrading after-purchase pages after that.

## Best practices

To optimize your app development experience, Shopify has established a set of best practices that you can refer to when developing an app that extends checkout.

**Tip**
We also recommend getting familiar with Polaris accessibility and content guidelines.

**Create multi-page extensions**
Learn more about building extensions that can render on any checkout page.

**UX for checkout**
Learn how to improve the quality of checkout experiences by following our UX guidelines for checkout.

**Network requests from extensions**
Learn about Cross-Origin Resource Sharing (CORS) and other security considerations when making network requests to your own server.

**App Design Guidelines**
Get practical guidance on how to design a user interface for the Shopify admin.

## Product roadmap

Some checkout customization features are in development and will be released later this year. The following are the features on our roadmap and our estimated launch dates:

**Note**
This roadmap is being shared for informational purposes and is subject to change. Bug fixes and improvements will be added as we hear from the community. Share your feedback or request new features by creating a new issue in the Shopify developer community forum.

## UI extensions

Stores that subscribe to the Shopify Plus plan can add UI extensions to their Checkout, Thank you and Order status pages. Stores on Basic, Shopify, and Advanced plans can only add UI extensions to their Thank you and Order status pages. Merchants can install apps from the Shopify App Store or build custom apps that contain UI extensions.

We'll continue adding API capabilities to help you access the right functionality in extensions. We'll also continue adding UI components that offer performant patterns on our design best practices. We release new components and APIs into the unstable API version first, and promote to the next stable release based on Shopify's API version release schedule.

| Feature | Target launch date |
|---------|-------------------|
| Checkout and accounts editor setting to display the discount code field by default on mobile devices | June 2024 (shipped) |
| Support for conditional component rendering on mobile checkouts | June 2024 (shipped) |
| Support for one-time use addresses in Storefront Cart API and UI Extension API | July 2024 (shipped) |
| Support for UI extensions in draft order invoice checkouts | July 2024 (shipped) |
| Default a buyer to a merchant-provided address, with an option for the buyer to enter new address | August 2024 (early access) |
| Support for conditionally hiding the input field for 1st-party gift cards | November 2024 (shipped) |
| Support for styling order summary line items with the Branding API | December 2024 (shipped) |
| Support for integrating 3rd-party chat applications into checkout | December 2024 (shipped) |
| Support for reading app-owned metafields in checkout UI extensions and Customer Account UI extensions | April 2025 (shipped) |
| Input query API for customizing the data available to UI extensions | Q3 2025 |

## Shopify Functions

We'll continue to add new Shopify Functions APIs to further customize checkout business logic.

| Milestone | Target |
|-----------|--------|
| Introduced a new Discount API that supports any combination of product, order, and shipping savings from a single function extension | April 2025 (shipped) |
| Support for cart metafields on function input queries | July 2025 |
| Addition to the Discount API to optionally reject the triggering discount code and return a custom message when no discounts should be applied | Q3 2025 |
| Addition to the Discount API to support complex conditions for BXGY and discount combination logic | Q4 2025 |
| Changes to the Discount API to stack multiple discounts on the same product line item | Q1 2026 |

## Pixels

We'll continue to add new custom pixel and app pixel events and features.

| Milestone | Target |
|-----------|--------|
| Added new standard events: tracking errors during checkout | October 2024 (shipped) |
| Support for extending data fields on standard events | Q1 2025 |