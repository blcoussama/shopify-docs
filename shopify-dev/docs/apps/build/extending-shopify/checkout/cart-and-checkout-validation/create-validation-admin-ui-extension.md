# Create an admin UI extension for a cart and checkout validation function

To ensure that purchases meet certain criteria before customers can complete an order, you can use the Cart and Checkout Validation Function API and an admin UI extension.

In this tutorial, you'll use Shopify Functions to enforce product limits on store merchandise.

**Note**
Errors from validation functions are exposed to the Storefront API's Cart object, in themes using the cart template, and during checkout.

A checkout with an error about a product quantity that is too high

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Generate starter code for Shopify Functions.
- Use GraphQL to define the input of your function.
- Deploy functions to the Shopify platform.
- Review logs for your function.
- Create an admin UI extension to configure your function.

## Requirements

**Tip**
Shopify defaults to Rust as the most performant and recommended language choice to stay within the platform limits. For more information, refer to language considerations.

- You've created a Partner account.
- You've created a development store and enabled the Checkout and Customer Accounts Extensibility developer preview.
- You've created an app that uses Shopify CLI 3.49.5 or higher. If you previously installed Shopify CLI, then make sure that you're using the latest version. Start with an extension-only app and let Shopify host it for you.
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

To create a validation function, use Shopify CLI to generate a starter function, specify the inputs for your function using an input query, and implement your function logic using JavaScript or Rust.

1. Navigate to your app directory:

**Terminal**

```bash
cd <directory>
```

2. Run the following command to create a new validation extension:

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

4. Navigate to the extensions/cart-checkout-validation directory:

**Terminal**

```bash
cd extensions/cart-checkout-validation
```

5. Replace the contents of src/cart_validations_generate_run.graphql file with the following code. The cart_validations_generate_run.graphql file defines the input for the function. You need to retrieve the quantity and merchandise ID of the current cart lines.

Metafields allow your app to store custom data related to the validation function. Using the $app reserved prefix makes the metafield private to your app.

**Note**
The query differs slightly in Rust and JavaScript due to code generation requirements.

**📁 cart_validations_generate_run.graphql**
`src/cart_validations_generate_run.graphql`

Rust input query:

```graphql
query Input {
      cart {
        lines {
          quantity
          merchandise {
            __typename
            ... on ProductVariant {
              id
              product {
                title
              }
            }
          }
        }
      }
      validation {
        metafield(namespace: "$app:product-limits", key: "product-limits-values") {
          jsonValue
        }
      }
    }
```

JavaScript input query:

```graphql
query Input {
      cart {
        lines {
          quantity
          merchandise {
            __typename
            ... on ProductVariant {
              id
              product {
                title
              }
            }
          }
        }
      }
      validation {
        metafield(namespace: "$app:product-limits", key: "product-limits-values") {
          jsonValue
        }
      }
    }
```

6. If you're using JavaScript, then run the following command to regenerate types based on your input query:

**Terminal**

```bash
shopify app function typegen
```

7. If you're using Rust replace the src/main.rs file with the following code that will convert the metafield into a data structure in the Rust program.

**📁 main.rs**
`src/main.rs`

```rust
use shopify_function::prelude::*;
use std::process;

pub mod run;

#[typegen("schema.graphql")]
mod schema {
    #[query(
        "src/run.graphql",
        custom_scalar_overrides = {
            "Input.validation.metafield.jsonValue" => super::run::Configuration
        }
    )]
    pub mod run {}
}

fn main() {
    eprintln!("Please invoke a named export.");
    process::exit(1);
}
```

8. Replace the src/cart_validations_generate_run.rs or src/cart_validations_generate_run.js file with the following code. The function logic checks that the quantity of each cart line isn't above the quantity set in the configuration metafield. You can configure the quantity limits for each product variant using the admin UI extension that you will create in step 2.

**Tip**
You can associate a validation error with a specific checkout UI field, or a global error by specifying the target property. The target property follows the pattern that's provided in the Cart and Checkout Validation API reference. For example, using the global target $.cart will result in a global error at the top of checkout.

**📁 cart_validations_generate_run.rs**
`src/cart_validations_generate_run.rs`

```rust
use shopify_function::prelude::*;
use shopify_function::Result;
use super::schema;
use std::collections::HashMap;

#[derive(Deserialize, Default, PartialEq)]
pub struct Configuration {
    limits: HashMap<String, i32>
}

#[shopify_function]
fn run(input: schema::run::Input) -> Result<schema::CartValidationsGenerateRunResult> {
    let mut operations = Vec::new();
    let mut errors = Vec::new();

    let configuration = if let Some(metafield) = input.validation().metafield() {
        metafield.json_value()
    } else {
      return Ok(schema::FunctionRunResult { errors: vec![] });
    };

    input
      .cart()
      .lines()
      .iter()
      .for_each(|line| {
        let quantity = line.quantity();
        match &line.merchandise() {
          schema::run::input::cart::lines::Merchandise::ProductVariant(variant) => {
              let limit = configuration.limits.get(variant.id()).unwrap_or(&i32::MAX);
              let product_name = variant.product().title();

              // Check item quantity in the cart against the configured limit
              if quantity > limit {
                errors.push(schema::ValidationError {
                  message: format!("Orders are limited to a maximum of {} of {}", limit, product_name),
                  target: "cart".to_owned(),
                });
              }
          },
          _ => {},
        };
      });

    let operation = schema::ValidationAddOperation { errors };
    operations.push(schema::Operation::ValidationAdd(operation));
    Ok(schema::FunctionRunResult { errors })
}
```

**📁 cart_validations_generate_run.js**
`src/cart_validations_generate_run.js`

```javascript
// @ts-check

    /**
    * @typedef {import("../generated/api").CartValidationsGenerateRunInput} CartValidationsGenerateRunInput
    * @typedef {import("../generated/api").CartValidationsGenerateRunResult} CartValidationsGenerateRunResult
  */

    /**
    * @param {CartValidationsGenerateRunInput} input
    * @returns {CartValidationsGenerateRunResult}
  */
  export function cartValidationsGenerateRun({ cart, validation }) {
      // Read persisted data about product limits from the associated metafield
      /** @type {Array<{productVariantId: string; quantityLimit: number}>} */
      const configuration = validation.metafield?.value ?? {};
      const errors = [];

      for (const { quantity, merchandise } of cart.lines) {
        if ("id" in merchandise) {
          const limit = configuration[merchandise.id] ?? Infinity;
          const title = merchandise.product.title || "Unknown product";

          // Check item quantity in the cart against the configured limit
          if (quantity > limit) {
            errors.push({
              message: `Orders are limited to a maximum of ${limit} of ${title}`,
              target: "cart",
            });
          }
        }
      }

      const operations = [
        {
          validationAdd: {
            errors
          },
        },
      ];

      return { operations };
    }
```

9. If you're using Rust, then build the function's Wasm module:

**Terminal**

```bash
cargo build --target=wasm32-wasip1 --release
```

If you encounter any errors, then ensure that you've installed Rust and the wasm32-wasip1 target.

## Step 2: Create the validation user interface in admin

The following steps show how to build an admin UI extension that enables merchants to configure a validation function.

Admin UI extension for configuring the validation function

1. Navigate to your app directory:

**Terminal**

```bash
cd <directory>
```

2. Run the following command to create a new validation rule UI extension:

**Terminal**

```bash
shopify app generate extension --template validation_settings_ui --name validation-settings
```

3. Choose the language that you want to use.

**Terminal**

```bash
?  What would you like to work in?
> (1) JavaScript React
  (2) JavaScript
  (3) TypeScript React
  (4) TypeScript
```

4. Navigate to the extensions/validation-settings directory:

**Terminal**

```bash
cd extensions/validation-settings
```

5. Replace the validation settings UI code with the following code:

**📁 ValidationSettings.jsx**
`src/ValidationSettings.jsx`

```javascript
import React, { useState } from "react";
import {
  reactExtension,
  useApi,
  Text,
  Box,
  FunctionSettings,
  Section,
  NumberField,
  BlockStack,
  Banner,
  InlineStack,
  Image,
} from "@shopify/ui-extensions-react/admin";

const TARGET = "admin.settings.validation.render";

export default reactExtension(TARGET, async (api) => {
  const existingDefinition = await getMetafieldDefinition(api.query);
  if (!existingDefinition) {
    // Create a metafield definition for persistence if no pre-existing definition exists
    const metafieldDefinition = await createMetafieldDefinition(api.query);

    if (!metafieldDefinition) {
      throw new Error("Failed to create metafield definition");
    }
  }

  // Read existing persisted data about product limits from the associated metafield
  const configuration = JSON.parse(
    api.data.validation?.metafields?.[0]?.value ?? "{}",
  );

  // Query product data needed to render the settings UI
  const products = await getProducts(api.query);

  return (
    <ValidationSettings configuration={configuration} products={products} />
  );
});

function ValidationSettings({ configuration, products }) {
  const [errors, setErrors] = useState([]);
  // State to keep track of product limit settings, initialized to any persisted metafield value
  const [settings, setSettings] = useState(
    createSettings(products, configuration),
  );

  const { applyMetafieldChange } = useApi(TARGET);

  const onError = (error) => {
    setErrors(errors.map((e) => e.message));
  };

  const onChange = async (variant, value) => {
    setErrors([]);
    const newSettings = {
      ...settings,
      [variant.id]: Number(value),
    };
    setSettings(newSettings);

    // On input change, commit updated product variant limits to memory.
    // Caution: the changes are only persisted on save!
    const result = await applyMetafieldChange({
      type: "updateMetafield",
      namespace: "$app:product-limits",
      key: "product-limits-values",
      value: JSON.stringify(newSettings),
    });

    if (result.type === "error") {
      setErrors([result.message]);
    }
  };

  return (
    // Note: FunctionSettings must be rendered for the host to receive metafield updates
    <FunctionSettings onError={onError}>
      <ErrorBanner errors={errors} />
      <ProductQuantitySettings
        products={products}
        settings={settings}
        onChange={onChange}
      />
    </FunctionSettings>
  );
}

function ProductQuantitySettings({ products, settings, onChange }) {
  function Header() {
    return (
      <InlineStack>
        <Box minInlineSize="5%" />
        <Box minInlineSize="5%">
          <Text fontWeight="bold">Variant Name</Text>
        </Box>
        <Box minInlineSize="50%">
          <Text fontWeight="bold">Limit</Text>
        </Box>
      </InlineStack>
    );
  }

  // Render table of product variants and inputs to assign limits
  return products.map(({ title, variants }) => (
    <Section heading={title} key={title}>
      <BlockStack paddingBlock="large">
        <Header />
        {variants.map((variant) => {
          const limit = settings[variant.id];
          return (
            <InlineStack columnGap="none" key={variant.id}>
              <Box minInlineSize="5%">
                {variant.imageUrl ? (
                  <Image alt={variant.title} src={variant.imageUrl} />
                ) : (
                  <Text>No image</Text>
                )}
              </Box>
              <Box minInlineSize="5%">
                <Text>{variant.title}</Text>
              </Box>
              <Box minInlineSize="50%">
                <NumberField
                  value={limit}
                  min={0}
                  max={99}
                  label="Set a limit"
                  defaultValue={String(limit)}
                  onChange={(value) => onChange(variant, value)}
                ></NumberField>
              </Box>
            </InlineStack>
          );
        })}
      </BlockStack>
    </Section>
  ));
}

function ErrorBanner({ errors }) {
  if (errors.length === 0) return null;

  return (
    <Box paddingBlockEnd="large">
      {errors.map((error, i) => (
        <Banner key={i} title="Errors were encountered" tone="critical">
          {error}
        </Banner>
      ))}
    </Box>
  );
}

async function getProducts(adminApiQuery) {
  const query = `#graphql
  query FetchProducts {
    products(first: 5) {
      nodes {
        title
        variants(first: 5) {
          nodes {
            id
            title
            image {
              url
            }
          }
        }
      }
    }
  }`;

  const result = await adminApiQuery(query);

  return result?.data?.products.nodes.map(({ title, variants }) => {
    return {
      title,
      variants: variants.nodes.map((variant) => ({
        title: variant.title,
        id: variant.id,
        imageUrl: variant?.image?.url,
      })),
    };
  });
}

const METAFIELD_NAMESPACE = "$app:product-limits";
const METAFIELD_KEY = "product-limits-values";

async function getMetafieldDefinition(adminApiQuery) {
  const query = `#graphql
    query GetMetafieldDefinition {
      metafieldDefinitions(first: 1, ownerType: VALIDATION, namespace: "${METAFIELD_NAMESPACE}", key: "${METAFIELD_KEY}") {
        nodes {
          id
        }
      }
    }
  `;

  const result = await adminApiQuery(query);

  return result?.data?.metafieldDefinitions?.nodes[0];
}

async function createMetafieldDefinition(adminApiQuery) {
  const definition = {
    access: {
      admin: "MERCHANT_READ_WRITE",
    },
    key: METAFIELD_KEY,
    name: "Validation Configuration",
    namespace: METAFIELD_NAMESPACE,
    ownerType: "VALIDATION",
    type: "json",
  };

  const query = `#graphql
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
            id
          }
        }
      }
  `;

  const variables = { definition };
  const result = await adminApiQuery(query, { variables });

  return result?.data?.metafieldDefinitionCreate?.createdDefinition;
}

function createSettings(products, configuration) {
  const settings = {};

  products.forEach(({ variants }) => {
    variants.forEach(({ id }) => {
      // Read existing product limits from metafield
      const limit = configuration[id];

      if (limit) {
        settings[id] = limit;
      }
    });
  });

  return settings;
}
```

**📁 ValidationSettings.js**
`src/ValidationSettings.js`

```javascript
import {
  extend,
  Text,
  Box,
  FunctionSettings,
  Section,
  NumberField,
  BlockStack,
  Banner,
  InlineStack,
  Image,
} from "@shopify/ui-extensions/admin";

const TARGET = "admin.settings.validation.render";

export default extend(TARGET, async (root, api) => {
  const existingDefinition = await getMetafieldDefinition(api.query);
  if (!existingDefinition) {
    // Create a metafield definition for persistence if no pre-existing definition exists
    const metafieldDefinition = await createMetafieldDefinition(api.query);

    if (!metafieldDefinition) {
      throw new Error("Failed to create metafield definition");
    }
  }

  // Read existing persisted data about product limits from the associated metafield
  const configuration = JSON.parse(
    api.data.validation?.metafields?.[0]?.value ?? "{}",
  );

  // Query product data needed to render the settings UI
  const products = await getProducts(api.query);

  renderValidationSettings(root, configuration, products, api);
});

function renderValidationSettings(root, configuration, products, api) {
  let errors = [];
  // State to keep track of product limit settings, initialized to any persisted metafield value
  let settings = createSettings(products, configuration);

  const onError = (newErrors) => {
    errors = newErrors.map((e) => e.message);
    renderContent();
  };

  const onChange = async (variant, value) => {
    errors = [];
    const newSettings = {
      ...settings,
      [variant.id]: Number(value),
    };
    settings = newSettings;

    // On input change, commit updated product variant limits to memory.
    // Caution: the changes are only persisted on save!
    const result = await api.applyMetafieldChange({
      type: "updateMetafield",
      namespace: "$app:product-limits",
      key: "product-limits-values",
      value: JSON.stringify(newSettings),
    });

    if (result.type === "error") {
      errors = [result.message];
      renderContent();
    }
  };

  const renderErrors = (errors, root) => {
    if (!errors.length) {
      return [];
    }

    return errors.map((error, i) =>
      root.createComponent(
        Banner,
        {
          title: "Errors were encountered",
          tone: "critical",
        },
        root.createComponent(Text, {}, error),
      ),
    );
  };

  const renderContent = () => {
    return root.append(
      root.createComponent(
        // Note: FunctionSettings must be rendered for the host to receive metafield updates
        FunctionSettings,
        { onError },
        ...renderErrors(errors, root),
        ...products.map((product) =>
          renderProductQuantitySettings(root, product, settings, onChange),
        ),
      ),
    );
  };

  renderContent();
}

function renderProductQuantitySettings(root, product, settings, onChange) {
  const heading = root.createComponent(
    InlineStack,
    {},
    root.createComponent(Box, { minInlineSize: "5%" }),
    root.createComponent(
      Box,
      { minInlineSize: "5%" },
      root.createComponent(Text, { fontWeight: "bold" }, "Variant Name"),
    ),
    root.createComponent(
      Box,
      { minInlineSize: "50%" },
      root.createComponent(Text, { fontWeight: "bold" }, "Limit"),
    ),
  );

  const renderVariant = (variant, settings, root) => {
    const limit = settings[variant.id];

    return root.createComponent(
      InlineStack,
      { columnGap: "none" },
      root.createComponent(
        Box,
        { minInlineSize: "5%" },
        variant.imageUrl
          ? root.createComponent(Image, {
              source: variant.imageUrl,
              alt: variant.title,
            })
          : null,
      ),
      root.createComponent(
        Box,
        { minInlineSize: "5%" },
        root.createComponent(Text, {}, variant.title),
      ),
      root.createComponent(
        Box,
        { minInlineSize: "50%" },
        root.createComponent(NumberField, {
          label: "Set a limit",
          value: limit,
          min: 0,
          max: 99,
          defaultValue: String(limit),
          onChange: (value) => onChange(variant, value),
        }),
      ),
    );
  };

  // Render table of product variants and inputs to assign limits
  return root.createComponent(
    Section,
    { heading: product.title },
    root.createComponent(
      BlockStack,
      { paddingBlock: "large" },
      heading,
      ...product.variants.map((variant) =>
        renderVariant(variant, settings, root),
      ),
    ),
  );
}

async function getProducts(adminApiQuery) {
  const query = `#graphql
  query FetchProducts {
    products(first: 5) {
      nodes {
        title
        variants(first: 5) {
          nodes {
            id
            title
            image {
              url
            }
          }
        }
      }
    }
  }`;

  const result = await adminApiQuery(query);

  return result?.data?.products.nodes.map(({ title, variants }) => {
    return {
      title,
      variants: variants.nodes.map((variant) => ({
        title: variant.title,
        id: variant.id,
        imageUrl: variant?.image?.url,
      })),
    };
  });
}

const METAFIELD_NAMESPACE = "$app:product-limits";
const METAFIELD_KEY = "product-limits-values";

async function getMetafieldDefinition(adminApiQuery) {
  const query = `#graphql
    query GetMetafieldDefinition {
      metafieldDefinitions(first: 1, ownerType: VALIDATION, namespace: "${METAFIELD_NAMESPACE}", key: "${METAFIELD_KEY}") {
        nodes {
          id
        }
      }
    }
  `;

  const result = await adminApiQuery(query);

  return result?.data?.metafieldDefinitions?.nodes[0];
}

async function createMetafieldDefinition(adminApiQuery) {
  const definition = {
    access: {
      admin: "MERCHANT_READ_WRITE",
    },
    key: METAFIELD_KEY,
    name: "Validation Configuration",
    namespace: METAFIELD_NAMESPACE,
    ownerType: "VALIDATION",
    type: "json",
  };

  const query = `#graphql
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
            id
          }
        }
      }
  `;

  const variables = { definition };
  const result = await adminApiQuery(query, { variables });

  return result?.data?.metafieldDefinitionCreate?.createdDefinition;
}

function createSettings(products, configuration) {
  const settings = {};

  products.forEach(({ variants }) => {
    variants.forEach(({ id }) => {
      // Read existing product limits from metafield
      const limit = configuration[id];

      if (limit) {
        settings[id] = limit;
      }
    });
  });

  return settings;
}
```

**📁 ValidationSettings.tsx**
`src/ValidationSettings.tsx`

```typescript
import React, { useState } from "react";
import {
  reactExtension,
  useApi,
  Text,
  Box,
  FunctionSettings,
  Section,
  NumberField,
  BlockStack,
  Banner,
  InlineStack,
  Image,
  type FunctionSettingsError,
} from "@shopify/ui-extensions-react/admin";
import { type ValidationSettingsApi } from "@shopify/ui-extensions/admin";

const TARGET = "admin.settings.validation.render";

export default reactExtension(
  TARGET,
  async (api: ValidationSettingsApi<typeof TARGET>) => {
    const existingDefinition = await getMetafieldDefinition(api.query);
    if (!existingDefinition) {
      // Create a metafield definition for persistence if no pre-existing definition exists
      const metafieldDefinition = await createMetafieldDefinition(api.query);

      if (!metafieldDefinition) {
        throw new Error("Failed to create metafield definition");
      }
    }

    // Read existing persisted data about product limits from the associated metafield
    const configuration = JSON.parse(
      api.data.validation?.metafields?.[0]?.value ?? "{}",
    );

    // Query product data needed to render the settings UI
    const products = await getProducts(api.query);

    return (
      <ValidationSettings configuration={configuration} products={products} />
    );
  },
);

function ValidationSettings({
  configuration,
  products,
}: {
  configuration: Object;
  products: Product[];
}) {
  const [errors, setErrors] = useState<string[]>([]);
  // State to keep track of product limit settings, initialized to any persisted metafield value
  const [settings, setSettings] = useState<Record<string, number>>(
    createSettings(products, configuration),
  );

  const { applyMetafieldChange } = useApi(TARGET);

  const onError = (errors: FunctionSettingsError[]) => {
    setErrors(errors.map((e) => e.message));
  };

  const onChange = async (variant: ProductVariant, value: number) => {
    setErrors([]);
    const newSettings = {
      ...settings,
      [variant.id]: Number(value),
    };
    setSettings(newSettings);

    // On input change, commit updated product variant limits to memory.
    // Caution: the changes are only persisted on save!
    const result = await applyMetafieldChange({
      type: "updateMetafield",
      namespace: "$app:product-limits",
      key: "product-limits-values",
      value: JSON.stringify(newSettings),
    });

    if (result.type === "error") {
      setErrors([result.message]);
    }
  };

  return (
    // Note: FunctionSettings must be rendered for the host to receive metafield updates
    <FunctionSettings onError={onError}>
      <ErrorBanner errors={errors} />
      <ProductQuantitySettings
        products={products}
        settings={settings}
        onChange={onChange}
      />
    </FunctionSettings>
  );
}

function ProductQuantitySettings({
  products,
  settings,
  onChange,
}: {
  products: Product[];
  settings: Record<string, number>;
  onChange: (variant: ProductVariant, value: number) => Promise<void>;
}) {
  function Header() {
    return (
      <InlineStack>
        <Box minInlineSize="5%" />
        <Box minInlineSize="5%">
          <Text fontWeight="bold">Variant Name</Text>
        </Box>
        <Box minInlineSize="50%">
          <Text fontWeight="bold">Limit</Text>
        </Box>
      </InlineStack>
    );
  }

  // Render table of product variants and inputs to assign limits
  return products.map(({ title, variants }) => (
    <Section heading={title} key={title}>
      <BlockStack paddingBlock="large">
        <Header />
        {variants.map((variant) => {
          const limit = settings[variant.id];
          return (
            <InlineStack columnGap="none" key={variant.id}>
              <Box minInlineSize="5%">
                {variant.imageUrl ? (
                  <Image alt={variant.title} src={variant.imageUrl} />
                ) : (
                  <Text>No image</Text>
                )}
              </Box>
              <Box minInlineSize="5%">
                <Text>{variant.title}</Text>
              </Box>
              <Box minInlineSize="50%">
                <NumberField
                  value={limit}
                  min={0}
                  max={99}
                  label="Set a limit"
                  defaultValue={String(limit)}
                  onChange={(value) => onChange(variant, value)}
                ></NumberField>
              </Box>
            </InlineStack>
          );
        })}
      </BlockStack>
    </Section>
  ));
}

function ErrorBanner({ errors }: { errors: string[] }) {
  if (errors.length === 0) return null;

  return (
    <Box paddingBlockEnd="large">
      {errors.map((error, i) => (
        <Banner key={i} title="Errors were encountered" tone="critical">
          {error}
        </Banner>
      ))}
    </Box>
  );
}

type Product = {
  title: string;
  variants: ProductVariant[];
};

type ProductVariant = {
  id: string;
  title: string;
  imageUrl?: string;
};

async function getProducts(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
): Promise<Product[]> {
  const query = `#graphql
  query FetchProducts {
    products(first: 5) {
      nodes {
        title
        variants(first: 5) {
          nodes {
            id
            title
            image {
              url
            }
          }
        }
      }
    }
  }`;

  type ProductQueryData = {
    products: {
      nodes: Array<{
        title: string;
        variants: {
          nodes: Array<{
            id: string;
            title: string;
            image?: {
              url: string;
            };
          }>;
        };
      }>;
    };
  };

  const results = await adminApiQuery<ProductQueryData>(query);

  return (
    results?.data?.products.nodes.map(({ title, variants }) => {
      return {
        title,
        variants: variants.nodes.map((variant) => ({
          title: variant.title,
          id: variant.id,
          imageUrl: variant?.image?.url,
        })),
      };
    }) ?? []
  );
}

const METAFIELD_NAMESPACE = "$app:product-limits";
const METAFIELD_KEY = "product-limits-values";

async function getMetafieldDefinition(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
) {
  const query = `#graphql
    query GetMetafieldDefinition {
      metafieldDefinitions(first: 1, ownerType: VALIDATION, namespace: "${METAFIELD_NAMESPACE}", key: "${METAFIELD_KEY}") {
        nodes {
          id
        }
      }
    }
  `;

  type MetafieldDefinitionsQueryData = {
    metafieldDefinitions: {
      nodes: Array<{
        id: string;
      }>;
    };
  };

  const result = await adminApiQuery<MetafieldDefinitionsQueryData>(query);

  return result?.data?.metafieldDefinitions?.nodes[0];
}

async function createMetafieldDefinition(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
) {
  const definition = {
    access: {
      admin: "MERCHANT_READ_WRITE",
    },
    key: METAFIELD_KEY,
    name: "Validation Configuration",
    namespace: METAFIELD_NAMESPACE,
    ownerType: "VALIDATION",
    type: "json",
  };

  const query = `#graphql
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
            id
          }
        }
      }
  `;

  type MetafieldDefinitionCreateData = {
    metafieldDefinitionCreate: {
      createdDefinition?: {
        id: string;
      };
    };
  };

  const variables = { definition };
  const result = await adminApiQuery<MetafieldDefinitionCreateData>(query, {
    variables,
  });

  return result?.data?.metafieldDefinitionCreate?.createdDefinition;
}

function createSettings(
  products: Product[],
  configuration: Object,
): Record<string, number> {
  const settings = {};

  products.forEach(({ variants }) => {
    variants.forEach(({ id }) => {
      // Read existing product limits from metafield
      const limit = configuration[id];

      if (limit) {
        settings[id] = limit;
      }
    });
  });

  return settings;
}
```

**📁 ValidationSettings.ts**
`src/ValidationSettings.ts`

```typescript
import { type RemoteRoot } from "@remote-ui/core";
import {
  extend,
  Text,
  Box,
  FunctionSettings,
  Section,
  NumberField,
  BlockStack,
  Banner,
  InlineStack,
  Image,
  type ValidationSettingsApi,
  type FunctionSettingsError,
} from "@shopify/ui-extensions/admin";

const TARGET = "admin.settings.validation.render";

export default extend(
  TARGET,
  async (root: RemoteRoot, api: ValidationSettingsApi<typeof TARGET>) => {
    const existingDefinition = await getMetafieldDefinition(api.query);
    if (!existingDefinition) {
      // Create a metafield definition for persistence if no pre-existing definition exists
      const metafieldDefinition = await createMetafieldDefinition(api.query);

      if (!metafieldDefinition) {
        throw new Error("Failed to create metafield definition");
      }
    }

    // Read existing persisted data about product limits from the associated metafield
    const configuration = JSON.parse(
      api.data.validation?.metafields?.[0]?.value ?? "{}",
    );

    // Query product data needed to render the settings UI
    const products = await getProducts(api.query);

    renderValidationSettings(root, configuration, products, api);
  },
);

function renderValidationSettings(
  root: RemoteRoot,
  configuration: Object,
  products: Product[],
  api: ValidationSettingsApi<typeof TARGET>,
) {
  let errors: string[] = [];
  // State to keep track of product limit settings, initialized to any persisted metafield value
  let settings = createSettings(products, configuration);

  const onError = (newErrors: FunctionSettingsError[]) => {
    errors = newErrors.map((e) => e.message);
    renderContent();
  };

  const onChange = async (variant: ProductVariant, value: number) => {
    errors = [];
    const newSettings = {
      ...settings,
      [variant.id]: Number(value),
    };
    settings = newSettings;

    // On input change, commit updated product variant limits to memory.
    // Caution: the changes are only persisted on save!
    const result = await api.applyMetafieldChange({
      type: "updateMetafield",
      namespace: "$app:product-limits",
      key: "product-limits-values",
      value: JSON.stringify(newSettings),
    });

    if (result.type === "error") {
      errors = [result.message];
      renderContent();
    }
  };

  const renderErrors = (errors: string[], root: RemoteRoot) => {
    if (!errors.length) {
      return [];
    }

    return errors.map((error, i) =>
      root.createComponent(
        Banner,
        {
          title: "Errors were encountered",
          tone: "critical",
        },
        root.createComponent(Text, {}, error),
      ),
    );
  };

  const renderContent = () => {
    return root.append(
      root.createComponent(
        // Note: FunctionSettings must be rendered for the host to receive metafield updates
        FunctionSettings,
        { onError },
        ...renderErrors(errors, root),
        ...products.map((product) =>
          renderProductQuantitySettings(root, product, settings, onChange),
        ),
      ),
    );
  };

  renderContent();
}

function renderProductQuantitySettings(
  root: RemoteRoot,
  product: Product,
  settings: Record<string, number>,
  onChange: (variant: ProductVariant, value: number) => Promise<void>,
) {
  const heading = root.createComponent(
    InlineStack,
    {},
    root.createComponent(Box, { minInlineSize: "5%" }),
    root.createComponent(
      Box,
      { minInlineSize: "5%" },
      root.createComponent(Text, { fontWeight: "bold" }, "Variant Name"),
    ),
    root.createComponent(
      Box,
      { minInlineSize: "50%" },
      root.createComponent(Text, { fontWeight: "bold" }, "Limit"),
    ),
  );

  const renderVariant = (
    variant: ProductVariant,
    settings: Record<string, number>,
    root: RemoteRoot,
  ) => {
    const limit = settings[variant.id];

    return root.createComponent(
      InlineStack,
      { columnGap: "none" },
      root.createComponent(
        Box,
        { minInlineSize: "5%" },
        variant.imageUrl
          ? root.createComponent(Image, {
              source: variant.imageUrl,
              alt: variant.title,
            })
          : null,
      ),
      root.createComponent(
        Box,
        { minInlineSize: "5%" },
        root.createComponent(Text, {}, variant.title),
      ),
      root.createComponent(
        Box,
        { minInlineSize: "50%" },
        root.createComponent(NumberField, {
          label: "Set a limit",
          value: limit,
          min: 0,
          max: 99,
          defaultValue: String(limit),
          onChange: (value: number) => onChange(variant, value),
        }),
      ),
    );
  };

  // Render table of product variants and inputs to assign limits
  return root.createComponent(
    Section,
    { heading: product.title },
    root.createComponent(
      BlockStack,
      { paddingBlock: "large" },
      heading,
      ...product.variants.map((variant) =>
        renderVariant(variant, settings, root),
      ),
    ),
  );
}

type Product = {
  title: string;
  variants: ProductVariant[];
};

type ProductVariant = {
  id: string;
  title: string;
  imageUrl?: string;
};

async function getProducts(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
): Promise<Product[]> {
  const query = `#graphql
  query FetchProducts {
    products(first: 5) {
      nodes {
        title
        variants(first: 5) {
          nodes {
            id
            title
            image {
              url
            }
          }
        }
      }
    }
  }`;

  type ProductQueryData = {
    products: {
      nodes: Array<{
        title: string;
        variants: {
          nodes: Array<{
            id: string;
            title: string;
            image?: {
              url: string;
            };
          }>;
        };
      }>;
    };
  };

  const result = await adminApiQuery<ProductQueryData>(query);

  return (
    result?.data?.products.nodes.map(({ title, variants }) => {
      return {
        title,
        variants: variants.nodes.map((variant) => ({
          title: variant.title,
          id: variant.id,
          imageUrl: variant?.image?.url,
        })),
      };
    }) ?? []
  );
}

const METAFIELD_NAMESPACE = "$app:product-limits";
const METAFIELD_KEY = "product-limits-values";

async function getMetafieldDefinition(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
) {
  const query = `#graphql
    query GetMetafieldDefinition {
      metafieldDefinitions(first: 1, ownerType: VALIDATION, namespace: "${METAFIELD_NAMESPACE}", key: "${METAFIELD_KEY}") {
        nodes {
          id
        }
      }
    }
  `;

  type MetafieldDefinitionsQueryData = {
    metafieldDefinitions: {
      nodes: Array<{
        id: string;
      }>;
    };
  };

  const result = await adminApiQuery<MetafieldDefinitionsQueryData>(query);

  return result?.data?.metafieldDefinitions?.nodes[0];
}

async function createMetafieldDefinition(
  adminApiQuery: ValidationSettingsApi<typeof TARGET>["query"],
) {
  const definition = {
    access: {
      admin: "MERCHANT_READ_WRITE",
    },
    key: METAFIELD_KEY,
    name: "Validation Configuration",
    namespace: METAFIELD_NAMESPACE,
    ownerType: "VALIDATION",
    type: "json",
  };

  const query = `#graphql
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
            id
          }
        }
      }
  `;

  type MetafieldDefinitionCreateData = {
    metafieldDefinitionCreate: {
      createdDefinition?: {
        id: string;
      };
    };
  };

  const variables = { definition };
  const result = await adminApiQuery<MetafieldDefinitionCreateData>(query, {
    variables,
  });

  return result?.data?.metafieldDefinitionCreate?.createdDefinition;
}

function createSettings(
  products: Product[],
  configuration: Object,
): Record<string, number> {
  const settings = {};

  products.forEach(({ variants }) => {
    variants.forEach(({ id }) => {
      // Read existing product limits from metafield
      const limit = configuration[id];

      if (limit) {
        settings[id] = limit;
      }
    });
  });

  return settings;
}
```

## Step 3: Link the user interface to the validation function

To link the admin UI extension to the validation function, configure your validation function's TOML file. You can also configure the app's TOML file with necessary access scopes.

1. Navigate to the validation function directory:

**Terminal**

```bash
cd extensions/cart-checkout-validation
```

2. Add the following code to the shopify.extension.toml file associated with the validation function:

**📁 shopify.extension.toml**

```toml
[extensions.ui]
  handle = "validation-settings-ui"
```

3. Make sure that the shopify.app.toml file in your app root folder has the read_products access scope:

**📁 shopify.app.toml**

```toml
[access_scopes]
  scopes = "read_products"
```

**Note**
If you're adding new access scopes to an existing app, then you need to redeploy and reinstall the app on the store.

## Step 4: Test the validation on your development store

Run your development server and test the validation function and the corresponding admin UI extension on your development store. You can test the validation behavior directly on checkout, or using the GraphQL Storefront API.

### Setup

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
5. From the Shopify admin, go to Settings > Checkout.
6. Under Checkout rules, click Add rule. A new page opens and shows a list of checkout rules.

Adding a checkout rule via the Checkout settings page in the Shopify admin

7. Find the cart-checkout-validation function that you want to test and select it.
8. In the validation configuration, set the limit to five for each product variant.
9. Click Save, but don't turn on the validation yet.

### Using checkout

1. Before turning on the validation, create a cart that exceeds the quantity limit you set. For example, in your development store, create a cart with a quantity of 10 products.
2. Go back to the checkout rules page in the Shopify admin and enable this validation by clicking on Turn on.

Configure a checkout rule via the Checkout settings page in the Shopify admin

3. Optional. Control how checkout behaves when encountering runtime exceptions by selecting the validation under Checkout rules and toggling Allow all customers to complete checkout.
4. Complete a checkout in your online store and verify that the validation error message displays.

A checkout with an error about a product quantity that is too high

5. Verify that checkout progress is blocked. Clicking the Continue to shipping button in 3-page checkout, or the Pay now button in 1-page checkout, shouldn't redirect the user.

### Using GraphQL

You can also verify through the GraphQL Storefront API. Once the validation is turned on, create a cart with the cartCreate mutation:

Create a cart

```graphql
mutation cartCreate {
  cartCreate(input: {
    lines: []
  }) {
    cart {
      id
    }
  }
}
```

Using the Storefront API cartLinesAdd mutation, confirm that the mutation's userErrors field contains the function's error message, and that executing the mutation was unsuccessful.

Add line items to a cart

```graphql
mutation cartCreate {
  cartCreate(input: {
    lines: []
  }) {
    cart {
      id
    }
  }
}
```

Output:

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
          "message": "Orders are limited to a maximum of 5 of Monstera"
        }
      ]
    }
  }
}
```

### Debugging using logs

1. Open your terminal where shopify app dev is running, and review your function executions.

When testing functions on development stores, the output of dev includes executions of your functions, any debug logging you have added to them, and a link to a local file with the full function execution details.

2. In a new terminal window, use the Shopify CLI app function replay command to replay a function execution locally, and debug your function without the need to re-trigger the function execution on Shopify.

**Terminal**

```bash
shopify app function replay
```

3. Select the function execution from the top of the list. Press q to quit when you are finished debugging.

## Step 5: Deploy to production

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

## Next steps

- Learn more about how Shopify Functions work and the benefits of using Shopify Functions.
- Consult the API references for Shopify Functions.
- Learn how to use variables in your input query.
