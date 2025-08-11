# Build an admin block UI extension

This guide is the second part of a five-part tutorial series that describes how to build UI extensions that display as actions and blocks in Shopify admin. It demonstrates how to build a UI extension for a block that enables users to view and manage existing issues that have been tracked on products.

The issue tracker block on the product details page showing a list of issues with their titles and status.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Create a UI extension for a block that displays on the product details page in Shopify admin.
- Fetch information to populate the UI extension's initial state.
- Create an interface for the UI extension, allowing it to display multiple data objects.
- Update data in the block by allowing merchants to complete issues.
- Run the UI extension locally and test it on a development store.

## Requirements

- Create a Partner account
- Create a development store
- Scaffold an app

Scaffold an app with the write_products access scope that uses Shopify CLI 3.78 or higher.

- If you created a Remix app, then the write_products access scope is automatically granted to your app.
- If you created an extension-only app, then you need to explicitly grant the write_products access scope to your custom app.

Add a product to your development store. The product should not have any custom variants at the start of this tutorial.

**Complete the admin action tutorial**
This tutorial builds on the code from the admin action tutorial. Either complete that tutorial first, or copy its finished code to a file in your development environment.

## Project

Extension:

React

React
View on GitHub

## Create a new UI extension

Use Shopify CLI to generate starter code for your UI extension.

Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

Run the following command to create a new admin block UI extension:

**Terminal**
```bash
shopify app generate extension --template admin_block --name issue-tracker-block --flavor react
```

The command creates a new UI extension template in your app's extensions directory with the following structure:

**Admin block structure**
```
extensions/issue-tracker-block/
├── README.md
├── locales/
│   ├── en.default.json // The default locale for the extension
│   └── fr.json // The French language translations for the extension
├── package.json
├── shopify.extension.toml // The config file for the extension
└── src/
    └── BlockExtension.jsx // The code that defines the block's UI and behavior
```

## Create an interface for the UI extension

To create an interface for the UI extension, complete the following steps:

### Review the configuration

The UI extension's static configuration is stored in its .toml file. To display the issue tracker on product detail pages, validate that the target is set to admin.product-details.block.render.

```
admin.product-details.block.render
```

### Update the title

To update the name that displays when merchants select the action from the menu, edit the name value in the locale files. To localize strings, an admin block UI extension uses the i18n API. This API gives you access to strings stored in locale files, and automatically chooses the correct string for the current user's locale.

### Translate title

Optionally translate your title to French.

### Use components to create the extension's UI

Admin UI extensions are rendered using Remote UI, which is a fast and secure remote-rendering framework. Because Shopify renders the UI remotely, components used in the extensions must comply with a contract in the Shopify host. We provide these components through the admin UI extensions library.

Admin UI extensions components

### Note the export

You can view the source of your extension in the src/BlockExtension.jsx file. This file defines a functional React component exported to run at the extension's target. You can create the extension's body by importing and using components from the @shopify/ui-extensions-react/admin package.

**Caution:** The extension point in the component export must match the extension point defined in your .toml file, or the extension won't render.

### Render a UI

To build your block's UX, return some components from src/BlockExtension.jsx.

**Tip:** At this point, you can use the Dev Console to run your app's server and preview your UI extension. As you preview the UI extension, changes to its code automatically cause it to reload.

## Write the UI extension's logic and connect to the GraphQL Admin API

After defining the extension's UI, use standard React tooling to write the logic that controls it.

When you're writing UI extensions, you don't need proxy calls to the GraphQL Admin API through your app's backend. Instead, your UI extension can use direct API access to create requests directly using fetch. For merchants, this makes UI extensions more performant and responsive.

In this step, you'll create a utility file to contain GraphQL queries that the UI extension uses to read and write data to the metafield API.

Your app can also get data from the extension APIs, which includes data on the current resource from the data API.

Add new file at ./src/utils.js. This file contains the GraphQL queries that the extension uses to read and write data to the GraphQL Admin API.

- getAllProducts
- getIssues
- updateIssues

Import the getIssues utility method and use it to update the extension state.

Optionally import the getAllProducts utility method and use it to allow the block to browse issues from other products with product selection.

Call the updateIssues utility method when a user marks an issue as completed.

## Test the UI extension

After you've built the UI extension, test it with the following steps:

Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

To build and preview your app, either start or restart your server with the following command:

**Terminal**
```bash
shopify app dev
```

Press p to open the Dev Console.

In the Dev Console, click on the preview link for the issue tracker block extension.

The product details page opens. If you don't have a product in your store, then you need to create one.

To view your extension, scroll to the bottom of the page and add the block from the available blocks list.

If you completed the admin action tutorial first, use the admin action to create issues. Then, view the block to interact with the created issues.

Update your code to control the state and write the data to the admin metafield API using the methods from ./src/utils.js.

**📁 shopify.extension.toml** `/extensions/issue-tracker-block/shopify.extension.toml`
```toml
api_version = "2025-01"

[[extensions]]
# Change the merchant-facing name of the extension in locales/en.default.json
name = "t:name"
handle = "issue-tracker-block"
type = "ui_extension"

[[extensions.targeting]]
module = "./src/BlockExtension.jsx"
# The target used here must match the target used in the module file (./src/BlockExtension.jsx)
target = "admin.product-details.block.render"
```

**📁 en.default.json** `/extensions/issue-tracker-block/locales/en.default.json`
```json
{
  "name": "Issue tracker"
}
```

**📁 fr.json** `/extensions/issue-tracker-block/locales/fr.json`
```json
{
  "name": "Suivi des problèmes"
}
```

**📁 BlockExtension.jsx** `/extensions/issue-tracker-block/src/BlockExtension.jsx`
```javascript
import { useCallback, useEffect, useState } from "react";
import {
  reactExtension,
  useApi,
  AdminBlock,
  Button,
  Text,
  Box,
  Select,
  Card,
  DatePicker,
  TextField,
  Checkbox,
} from "@shopify/ui-extensions-react/admin";
import { getIssues, updateIssues, getAllProducts } from "./utils";

const PAGE_SIZE = 3;

// The target used here must match the target used in the extension's .toml file at ./shopify.extension.toml
const TARGET = "admin.product-details.block.render";

export default reactExtension(TARGET, () => <App />);

function App() {
  // connect to the extension's APIs
  const { data, i18n } = useApi(TARGET);
  const [issues, setIssues] = useState([]);
  const [filteredIssues, setFilteredIssues] = useState([]);
  const [currentPageNumber, setCurrentPageNumber] = useState(1);
  const [allProducts, setAllProducts] = useState([]);
  const [currentProduct, setCurrentProduct] = useState(data.selected[0]);
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    getAllProducts().then((products) => setAllProducts(products || []));
  }, []);

  useEffect(() => {
    getIssues(currentProduct.id).then((issues) => {
      setIssues(issues || []);
      setCurrentPageNumber(1);
    });
  }, [currentProduct.id]);

  useEffect(() => {
    let filtered = issues;
    if (statusFilter === "completed") {
      filtered = issues.filter((issue) => issue.completed);
    } else if (statusFilter === "pending") {
      filtered = issues.filter((issue) => !issue.completed);
    }
    setFilteredIssues(filtered);
    setCurrentPageNumber(1);
  }, [issues, statusFilter]);

  const onToggleCompleted = useCallback(
    async (issueId) => {
      const updatedIssues = issues.map((issue) =>
        issue.id === issueId ? { ...issue, completed: !issue.completed } : issue
      );
      setIssues(updatedIssues);
      await updateIssues(currentProduct.id, updatedIssues);
    },
    [issues, currentProduct.id]
  );

  const getCurrentPageIssues = () => {
    const start = (currentPageNumber - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    return filteredIssues.slice(start, end);
  };

  const getTotalPages = () => Math.ceil(filteredIssues.length / PAGE_SIZE);

  const onPreviousPage = useCallback(() => {
    setCurrentPageNumber((prev) => Math.max(prev - 1, 1));
  }, []);

  const onNextPage = useCallback(() => {
    setCurrentPageNumber((prev) => Math.min(prev + 1, getTotalPages()));
  }, []);

  const currentPageIssues = getCurrentPageIssues();
  const totalPages = getTotalPages();

  return (
    <AdminBlock title="Issue tracker">
      {allProducts.length > 0 && (
        <Box paddingBlockEnd="large">
          <Select
            label="Product"
            value={currentProduct.id}
            options={allProducts.map((product) => ({
              value: product.id,
              label: product.title,
            }))}
            onChange={(value) => {
              const product = allProducts.find((p) => p.id === value);
              if (product) setCurrentProduct(product);
            }}
          />
        </Box>
      )}
      <Box paddingBlockEnd="large">
        <Select
          label="Status filter"
          value={statusFilter}
          options={[
            { value: "all", label: "All issues" },
            { value: "pending", label: "Pending issues" },
            { value: "completed", label: "Completed issues" },
          ]}
          onChange={setStatusFilter}
        />
      </Box>
      {currentPageIssues.length > 0 ? (
        <>
          {currentPageIssues.map((issue) => (
            <Card key={issue.id} padding>
              <Box>
                <Box paddingBlockEnd="base">
                  <Text variation="headingMd">{issue.title}</Text>
                </Box>
                <Box paddingBlockEnd="base">
                  <Text>{issue.description}</Text>
                </Box>
                <Checkbox
                  name={`issue-${issue.id}`}
                  checked={issue.completed}
                  onChange={() => onToggleCompleted(issue.id)}
                >
                  {issue.completed
                    ? i18n.translate("completed")
                    : i18n.translate("markAsCompleted")}
                </Checkbox>
              </Box>
            </Card>
          ))}
          {totalPages > 1 && (
            <Box paddingBlockStart="large">
              <Box>
                <Text>
                  Page {currentPageNumber} of {totalPages}
                </Text>
              </Box>
              <Box paddingBlockStart="base">
                <Button onPress={onPreviousPage} disabled={currentPageNumber === 1}>
                  Previous
                </Button>
                <Button onPress={onNextPage} disabled={currentPageNumber === totalPages}>
                  Next
                </Button>
              </Box>
            </Box>
          )}
        </>
      ) : (
        <Text>No issues found for this product.</Text>
      )}
    </AdminBlock>
  );
}
```

**📁 utils.js** `/extensions/issue-tracker-block/src/utils.js`
```javascript
export async function getAllProducts() {
  // This example uses metafields to store the data. For more information, refer to https://shopify.dev/docs/apps/custom-data/metafields.
  const res = await makeGraphQLQuery(
    `query GetProducts {
      products(first: 250) {
        nodes {
          id
          title
        }
      }
    }`,
    {}
  );

  return res?.data?.products?.nodes || [];
}

export async function updateIssues(id, newIssues) {
  // This example uses metafields to store the data. For more information, refer to https://shopify.dev/docs/apps/custom-data/metafields.
  return await makeGraphQLQuery(
    `mutation SetMetafield($namespace: String!, $ownerId: ID!, $key: String!, $type: String!, $value: String!) {
    metafieldDefinitionCreate(
      definition: {namespace: $namespace, key: $key, name: "Tracked Issues", ownerType: PRODUCT, type: $type, access: {admin: MERCHANT_READ_WRITE}}
    ) {
      createdDefinition {
        id
      }
    }
    metafieldsSet(metafields: [{ownerId:$ownerId, namespace:$namespace, key:$key, type:$type, value:$value}]) {
      userErrors {
        field
        message
        code
      }
    }
  }
  `,
    {
      ownerId: id,
      namespace: "$app:issues",
      key: "issues",
      type: "json",
      value: JSON.stringify(newIssues),
    }
  );
}

export async function getIssues(productId) {
  // This example uses metafields to store the data. For more information, refer to https://shopify.dev/docs/apps/custom-data/metafields.
  const res = await makeGraphQLQuery(
    `query Product($id: ID!) {
      product(id: $id) {
        metafield(namespace: "$app:issues", key:"issues") {
          value
        }
      }
    }
  `,
    { id: productId }
  );

  if (res?.data?.product?.metafield?.value) {
    return JSON.parse(res.data.product.metafield.value);
  }
}

async function makeGraphQLQuery(query, variables) {
  const graphQLQuery = {
    query,
    variables,
  };

  const res = await fetch("shopify:admin/api/graphql.json", {
    method: "POST",
    body: JSON.stringify(graphQLQuery),
  });

  if (!res.ok) {
    console.error("Network error");
  }

  return await res.json();
}
```

## Next steps

**Connect admin UI extensions**
In the next tutorial in this series, you'll modify the admin actions and admin blocks for issue tracking so merchants can edit existing tracked issues for their products.

**Extension targets**
Learn about the various places in Shopify admin where UI extensions can be displayed.

**Components**
Learn about the full set of available components for writing admin UI extensions.