# Build an admin action UI extension

This guide is the first part of a five-part tutorial series that describes how to build UI extensions that display as actions and blocks in Shopify admin. It demonstrates how to build a UI extension for an action that enables users to log trackable, resolvable issues on products.

The issue tracker action over a modal. The action has input fields for a title and description.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Create a UI extension for an action that displays on the product details page in Shopify admin.
- Fetch information to populate the UI extension's initial state.
- Create an interface for the UI extension, allowing it to gather input from merchants.
- Update the data using GraphQL based on merchant input.
- Run the UI extension locally and test it on a development store.

## Requirements

- Create a Partner account
- Create a development store
- Scaffold an app

Scaffold an app with the write_products access scope that uses Shopify CLI 3.78 or higher.

- If you created a Remix app, then the write_products access scope is automatically granted to your app.
- If you created an extension-only app, then you need to explicitly grant the write_products access scope to your custom app.

Add a product to your development store. The product should not have any custom variants at the start of this tutorial.

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

Run the following command to create a new admin action UI extension:

**Terminal**
```bash
shopify app generate extension --template admin_action --name issue-tracker-action --flavor react
```

The command creates a new UI extension template in your app's extensions directory with the following structure:

**Admin action structure**
```
extensions/issue-tracker-action/
├── README.md
├── locales/
│   ├── en.default.json // The default locale for the extension
│   └── fr.json // The French language translations for the extension
├── package.json
├── shopify.extension.toml // The config file for the extension
└── src/
    └── AdminAction.jsx // The code that defines the action's UI and behavior
```

## Create an interface for the UI extension

To create an interface for the UI extension, complete the following steps:

### Review the configuration

The UI extension's static configuration is stored in its .toml file. To display the issue tracker on product detail pages, validate that the target is set to admin.product-details.action.render.

```
admin.product-details.action.render
```

### Update title

To update the name that displays when merchants select the action from the menu, edit the name value in the locale files. To localize strings, an admin action UI extension uses the i18n API. This API gives you access to strings stored in locale files, and automatically chooses the correct string for the current user's locale.

### Translate title

Optionally translate your title to French.

### Use components to create the extension's UI

Admin UI extensions are rendered using Remote UI, which is a fast and secure remote-rendering framework. Because Shopify renders the UI remotely, components used in the extensions must comply with a contract in the Shopify host. We provide these components through the admin UI extensions library.

Admin UI extensions components

### Note the export

You can view the source of your extension in the src/ActionExtension.jsx file. This file defines a functional React component exported to run at the extension's target. You can create the extension's body by importing and using components from the @shopify/ui-extensions-react/admin package.

**Caution:** The extension point in the component export must match the extension point defined in your .toml file, or the extension won't render.

### Render a UI

To build your action's UX, return some components from src/ActionExtension.jsx.

**Tip:** At this point, you can use the Dev Console to run your app's server and preview your UI extension. As you preview the UI extension, changes to its code automatically cause it to reload.

## Write the UI extension's logic and connect to the GraphQL Admin API

After defining the extension's UI, use standard React tooling to write the logic that controls it.

When you're writing UI extensions, you don't need proxy calls to the GraphQL Admin API through your app's backend. Instead, your UI extension can use direct API access to create requests directly using fetch. For merchants, this makes UI extensions more performant and responsive.

In this step, you'll create a utility file to contain GraphQL queries that the UI extension uses to read and write data to the metafield API.

Your app can also get data from the extension APIs, which includes data on the current resource from the data API.

Add new file at ./src/utils.js. This file contains the GraphQL queries that the extension uses to read and write data to the GraphQL Admin API.

- metafieldDefinitionCreate
- metafieldsSet

Import the getIssues utility method and use it to update the extension state.

Call the updateIssues utility method when the form is submitted.

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

In the Dev Console, click on the preview link for the issue tracker extension.

The product details page opens. If you don't have a product in your store, then you need to create one.

To launch your extension, select it from the More actions dropdown found at the top-right of the page.

Fill out the modal and click Create.

Validate that the metafield is created and populated with your issue text, by navigating to the metafields card at the bottom of the page, and select Show all.

Update your code to the control the form and write the data to the admin metafield API using the methods from ./src/utils.js.

**📁 shopify.extension.toml** `/extensions/issue-tracker-action/shopify.extension.toml`
```toml
api_version = "2025-01"

[[extensions]]
# Change the merchant-facing name of the extension in locales/en.default.json
name = "t:name"
handle = "issue-tracker-action"
type = "ui_extension"
[[extensions.targeting]]
module = "./src/ActionExtension.jsx"
# The target used here must match the target used in the module file (./src/ActionExtension.jsx)
target = "admin.product-details.action.render"
```

**📁 en.default.json** `/extensions/issue-tracker-action/locales/en.default.json`
```json
{
  "name": "Create an issue"
}
```

**📁 fr.json** `/extensions/issue-tracker-action/locales/fr.json`
```json
{
  "name": "Créer un problème"
}
```

**📁 ActionExtension.jsx** `/extensions/issue-tracker-action/src/ActionExtension.jsx`
```javascript
import { useCallback, useEffect, useState } from "react";
import {
  reactExtension,
  useApi,
  TextField,
  AdminAction,
  Button,
  TextArea,
  Box,
} from "@shopify/ui-extensions-react/admin";
import { getIssues, updateIssues } from "./utils";

function generateId (allIssues) {
  return !allIssues?.length ? 0 : allIssues[allIssues.length - 1].id + 1;
};

function validateForm ({title, description}) {
  return {
    isValid: Boolean(title) && Boolean(description),
    errors: {
      title: !title,
      description: !description,
    },
  };
};

// The target used here must match the target used in the extension's .toml file at ./shopify.extension.toml
const TARGET = "admin.product-details.action.render";

export default reactExtension(TARGET, () => <App />);

function App() {
  //connect with the extension's APIs
  const { close, data } = useApi(TARGET);
  const [issue, setIssue] = useState({ title: "", description: "" });
  const [allIssues, setAllIssues] = useState([]);
  const [formErrors, setFormErrors] = useState(null);
  const { title, description } = issue;

  useEffect(() => {
    getIssues(data.selected[0].id).then(issues => setAllIssues(issues || []));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = useCallback(async () => {
    const {isValid, errors} = validateForm(issue);
    setFormErrors(errors);

    if (isValid) {
      // Commit changes to the database
      await updateIssues(data.selected[0].id, [
        ...allIssues,
        {
          id: generateId(allIssues),
          completed: false,
          ...issue,
        }
      ]);
      // Close the modal using the 'close' API
      close();
    }
  }, [issue, data.selected, allIssues, close]);

  return (
    <AdminAction
      title="Create an issue"
      primaryAction={
        <Button onPress={onSubmit}>Create</Button>
      }
      secondaryAction={<Button onPress={close}>Cancel</Button>}
    >
      <TextField
        value={title}
        error={formErrors?.title ? "Please enter a title" : undefined}
        onChange={(val) => setIssue((prev) => ({ ...prev, title: val }))}
        label="Title"
        maxLength={50}
      />
      <Box paddingBlockStart="large">
        <TextArea
          value={description}
          error={
            formErrors?.description ? "Please enter a description" : undefined
          }
          onChange={(val) =>
            setIssue((prev) => ({ ...prev, description: val }))
          }
          label="Description"
          maxLength={300}
        />
      </Box>
    </AdminAction>
  );
}
```

**📁 utils.js** `/extensions/issue-tracker-action/src/utils.js`
```javascript
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

**Admin block UI extension**
In the next tutorial in this series, you'll build a UI extension that lists the issues created by your action extension. This new extension will display as a block in Shopify admin.

**Extension targets**
Learn about the various places in Shopify admin where UI extensions can be displayed.

**Components**
Learn about the full set of available components for writing admin UI extensions.