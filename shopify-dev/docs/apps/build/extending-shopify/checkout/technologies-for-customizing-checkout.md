# Technologies for customizing Shopify checkout

This guide describes the various technologies that you can use to customize Shopify checkout, and describes what you can do with them.

## Technologies

You can customize Shopify checkout using the following technologies:

| Technology | Customization type | Availability |
|------------|-------------------|--------------|
| Checkout UI extensions | Add custom UI or content to the checkout process and Order status page | Shopify Plus. Thank you and Order status extensions are available to all plans except Shopify Starter. |
| Checkout UI extensions: post-purchase | Add new content to the post-purchase page | All plans except Shopify Starter. Currently in beta. Can be used without restrictions in a development store. To use post-purchase extensions on a live store, you need to request access. |
| GraphQL Admin API | Customize the look and feel of checkout | Shopify Plus |
| Shopify Functions | Extend or replace key parts of Shopify's backend with custom logic | All plans except Shopify Starter. Some Function APIs are only available in developer preview. Merchants that have checkout.liquid customizations need to upgrade to Shopify Extensions in Checkout to use Function APIs. |
| Web pixel extensions | Track customer behavior | All plans except Shopify Starter. |

The following diagram provides a decision tree for choosing a technology:

A decision diagram for choosing a specific checkout technology

## Use cases

There are a variety of ways that you can customize Shopify checkout. The following table describes some common use cases that you can build:

| Technology | Customization type | Use cases |
|------------|-------------------|-----------|
| Checkout UI extensions | Add custom UI or content to the checkout process and Order status page | - Show a product offer before a customer completes checkout.<br>- Capture additional input from customers.<br>- Build a custom banner that displays in checkout.<br>- Capture a survey of the buying experience, or reviews when orders are fulfilled.<br>- Provide a referral code to new customers.<br>- Add a field validation at checkout that blocks customers from progressing in the checkout if they input invalid data. |
| Checkout UI extensions: post-purchase | Add new content to the post-purchase page | - Show a product offer after customers have checked out, but before they arrive at the order confirmation page.<br>- Capture additional information after customers have checked out, but before they arrive at the order confirmation page. |
| GraphQL Admin API | Customize the look and feel of checkout | - Apply branding changes such as changing the colors and corner radius settings on checkout form fields. |
| Shopify Functions | Extend or replace key parts of Shopify's backend with custom logic | - Create a new type of discount that's offered in the cart and at checkout.<br>- Rename, reorder, and sort the payment options available to customers during checkout.<br>- Rename, reorder, and sort the delivery options available to customers during checkout.<br>- Enforce an order maximum for customers with insufficient order history and prevent them from proceeding through checkout.<br>- Use location rules to rank the possible locations for a line item during checkout.<br>- Use fulfillment constraints to customize fulfillment and delivery strategies during the checkout and fulfillment process.<br>- Generate options for the pickup points that are available to customers. |
| Web pixel extensions | Track customer behavior | - Collect customer behavioral data to measure and optimize marketing campaign performance as well as your online store's conversion funnel. |

## Next steps

- Learn how to get started building for checkout.
- Learn how to use UI extensions in checkout or post-purchase by following one of our use case tutorials.
- Learn how to use Shopify Functions by following one of our use case tutorials.
- Create a web pixel extension to track customer behavior and subscribe to all events emitted by Shopify.
- Use the GraphQL Admin API to apply branding changes to checkout.