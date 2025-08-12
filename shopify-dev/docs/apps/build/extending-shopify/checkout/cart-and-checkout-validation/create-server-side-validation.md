# Create a server-side validation function

Shopify Extensions make it possible to build cart and checkout validation functions to ensure that purchases meet certain criteria before checking out or completing an order. In this tutorial, you'll use Shopify Functions to enforce an order maximum for buyers with insufficient order history, preventing them from placing their order.

**Note**
Errors from validation functions are exposed to the Storefront API's Cart object, in themes using the cart template and during checkout.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Generate starter code for Shopify Functions.
- Use GraphQL to define the input of your function.
- Deploy functions to the Shopify platform.
- Review logs for your function.

Screenshot that shows a checkout validation error

Storefront API example response

```json
{
 "data": {
  "cartLinesAdd": {
   "cart": null,
   "userErrors": [
   {
    "code": "VALIDATION_CUSTOM",
    "field": [
     "cartId"
    ],
    "message": "There is an order maximum of $1,000 for customers without established order history"
   }
   ]
  }
 }
}
```

## Requirements

**Tip**
Shopify defaults to Rust as the most performant and recommended language choice to stay within the platform limits. For more information, refer to language considerations.

- You've created a Partner account.
- You've created a development store and enabled the Checkout and Customer Accounts Extensibility developer preview.
- You've created an app that uses Shopify CLI 3.49.5 or higher. If you previously installed Shopify CLI, then make sure that you're using the latest version. If you plan to create a UI for your extension, then start with the Remix app template.
- You've installed Node.js 16 or higher.
- You've installed your app on the development store with the Checkout and Customer Accounts Extensibility developer preview enabled.
- You're using API version 2025-07 or higher for your function.

### Rust-specific requirements

The following requirements are specific to Rust-based development with Shopify Functions.

- You've installed Rust.
- On Windows, Rust requires the Microsoft C++ Build Tools. Make sure to select the Desktop development with C++ workload when installing the tools.
- You've installed the wasm32-wasip1 target:

**Terminal**
```bash
rustup target add wasm32-wasip1
```

## Step 1: Create the validation function

To create your validation function, you can use Shopify CLI to generate a starter function, specify the inputs for your function using an input query, and implement your function logic using Javascript or Rust.

1. Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

2. Run the following command to create a new validation function:

**Terminal**
```bash
shopify app generate extension --template cart_checkout_validation --name cart-checkout-validation
```

**Tip**
Shopify Functions support any language that compiles to WebAssembly (Wasm), such as Rust, AssemblyScript, or TinyGo. You specify the Wasm template option when you're using a language other than Rust and can conform to the Wasm API. Learn more about the Wasm API.

3. Choose the language that you want to use. For this tutorial, you should select either Rust or JavaScript.

Shopify defaults to Rust as the most performant and recommended language choice to stay within the platform limits. For more information, refer to language considerations.

**Terminal**
```bash
?  What would you like to work in?
> (1) Rust
  (2) JavaScript
  (3) TypeScript
  (4) Wasm
```

4. Navigate to extensions/cart-checkout-validation:

**Terminal**
```bash
cd extensions/cart-checkout-validation
```

5. Replace the contents of src/cart_validations_generate_run.graphql file with the following code.

cart_validations_generate_run.graphql defines the input for the function. You need the customer's order count and current cart subtotal.

The query differs slightly in Rust and JavaScript due to code generation requirements.

**=� cart_validations_generate_run.graphql**
`src/cart_validations_generate_run.graphql`

Rust input query:
```graphql
query Input {
      cart {
        buyerIdentity {
          customer {
            numberOfOrders
          }
        }
        cost {
          subtotalAmount {
            amount
          }
        }
      }
    }
```

JavaScript input query:
```graphql
query Input {
      cart {
        buyerIdentity {
          customer {
            numberOfOrders
          }
        }
        cost {
          subtotalAmount {
            amount
          }
        }
      }
    }
```

6. If you're using JavaScript, then run the following command to regenerate types based on your input query:

**Terminal**
```bash
shopify app function typegen
```

7. Replace the src/cart_validations_generate_run.rs or src/cart_validations_generate_run.js file with the following code.

This function logic checks for order subtotals greater than a set value and errors when a new customer is detected. You can adjust the subtotal limit or new customer detection logic as needed.

**Tip**
You can associate a validation error with a specific checkout UI field by specifying the target property. The target property follows the pattern that's provided in the Validation API reference. For example, $.cart.deliveryGroups[0].deliveryAddress.postalCode.

**📁 cart_validations_generate_run.rs**
`src/cart_validations_generate_run.rs`

```rust
use super::schema;
    use shopify_function::prelude::*;
    use shopify_function::Result;

    #[shopify_function]
    fn run(input: schema::run::Input) -> Result<schema::CartValidationsGenerateRunResult> {
        let mut operations = Vec::new();
        let mut errors = Vec::new();
        let error = schema::ValidationError {
            message:
                "There is an order maximum of $1,000 for customers without established order history"
                    .to_owned(),
            target: "cart".to_owned(),
        };

        let order_subtotal: f64 = input.cart().cost().subtotal_amount().amount().as_f64();

        if order_subtotal > 1000.0 {
            if let Some(buyer_identity) = input.cart().buyer_identity() {
                if let Some(customer) = buyer_identity.customer() {
                    if *customer.number_of_orders() < 5 {
                        errors.push(error);
                    }
                } else {
                    errors.push(error);
                }
            } else {
                errors.push(error);
            }
        }

        let operation = schema::ValidationAddOperation { errors };
        operations.push(schema::Operation::ValidationAdd(operation));

        Ok(schema::CartValidationsGenerateRunResult { operations })
    }
```

**📁 cart_validations_generate_run.js**
`src/cart_validations_generate_run.js`

```javascript
// @ts-check

    // Use JSDoc annotations for type safety
    /**
    * @typedef {import("../generated/api").CartValidationsGenerateRunInput} CartValidationsGenerateRunInput
    * @typedef {import("../generated/api").CartValidationsGenerateRunResult} CartValidationsGenerateRunResult
  */

    // The configured entrypoint for the 'cart.validations.generate.run' extension target
    /**
    * @param {CartValidationsGenerateRunInput} input
    * @returns {CartValidationsGenerateRunResult}
  */
  export function cartValidationsGenerateRun(input) {
      // The error
      const error = {
        message:
            "There is an order maximum of $1,000 for customers without established order history",
        target: "cart"
      };
      // Parse the decimal (serialized as a string) into a float.
      const orderSubtotal = parseFloat(input.cart.cost.subtotalAmount.amount);
      const errors = [];

      // Orders with subtotals greater than $1,000 are available only to established customers.
      if (orderSubtotal > 1000.0) {
        // If the customer has ordered less than 5 times in the past,
        // then treat them as a new customer.
        const numberOfOrders = input.cart.buyerIdentity?.customer?.numberOfOrders ?? 0;

        if (numberOfOrders < 5) {
          errors.push(error);
        }
      }

      // A single validation operation
      const operations = [
        {
          validationAdd: {
            errors
          },
        },
      ];

      return { operations };
    };
```

## Step 2: Preview the function on a development store

To test your function, you need to make it available to your development store.

1. If you're developing a function in a language other than JavaScript or TypeScript, ensure you have configured build.watch in your function extension configuration.
2. Navigate back to your app root:

**Terminal**
```bash
cd ../..
```

3. Use the Shopify CLI dev command to start app preview:

**Terminal**
```bash
shopify app dev
```

You can keep the preview running as you work on your function. When you make changes to a watched file, Shopify CLI rebuilds your function and updates the function extension's drafts, so you can immediately test your changes.

4. Follow the CLI prompts to preview your app, and install it on your development store.

## Step 3: Activate the validation

1. From the Shopify admin, go to Settings > Checkout.
2. In the Checkout Rules section of the page click Add rule.
3. A dialog opens and shows the cart-checkout-validation function that you just deployed.
4. To add a validation, click Add rule and select the validation.
5. Click Activate to activate the validation.
6. Click on Save.
7. Optional: Control how checkout behaves when encountering runtime exceptions by clicking on the validation and selecting or deselecting Allow all customers to submit checkout.

## Step 4: Test the validation

1. From your online store, without logging in, create a cart with more then $1,000 in merchandise.
2. Proceed to Checkout and verify that a warning message displays.
3. Verify that checkout progress is blocked. Clicking the Continue to shipping button shouldn't redirect the user.
4. Using the Storefront API cartLinesAdd mutation, confirm that the mutation's userErrors field contains the function's error message, and that executing the mutation was unsuccessful.
5. Open your terminal where shopify app dev is running, and review your function executions.

When testing functions on development stores, the output of dev includes executions of your functions, any debug logging you have added to them, and a link to a local file with the full function execution details.

6. In a new terminal window, use the Shopify CLI app function replay command to replay a function execution locally, and debug your function without the need to re-trigger the function execution on Shopify.

**Terminal**
```bash
shopify app function replay
```

7. Select the function execution from the top of the list. Press q to quit when you are finished debugging.

## Next steps

- Learn more about how Shopify Functions work and the benefits of using Shopify Functions.
- Consult the API references for Shopify Functions.
- Learn how to use variables in your input query.