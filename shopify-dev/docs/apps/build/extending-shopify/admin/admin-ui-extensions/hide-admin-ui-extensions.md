# Hide admin UI extensions

This guide is the final part of a five-part tutorial series that describes how to build UI extensions that display as actions and blocks in Shopify admin. Before starting this guide, you'll need to build or copy the code for the issue tracker admin action and admin block from the tutorial for connecting UI extensions to your app's backend.

Alternatively, you can complete this section immediately after completing the build an admin action and build an admin block tutorials.

So far you've created UI extensions that add an action and block that allows merchants to create and track issues in their Shopify admin. In this tutorial, you'll learn how to hide a UI extension when it's not relevant to the target.

To demonstrate conditional logic, we'll check the variant count of a product to determine if the UI extension should be visible. If the product has more than one variant, then the UI extension will be visible. If the product has only one variant, then the UI extension will be hidden.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Minimize the block when it's not relevant to the target.
- Hide the menu item that launches the action when it's not relevant to the target.

## Requirements

### Tutorials
You've completed or copied the code from the admin action tutorial and the admin block tutorial.

## Project

Extension:

React

React
View on GitHub

## Collapse an admin block

If an admin block isn't relevant on a page, then you can collapse it to minimize disruption for merchants, while still enabling them to see that they have pinned it to the page. To minimize an admin block, you can return null inside the AdminBlock component of your UI extension.

## Use the getIssues function to determine if the admin block should be visible.

Initialize a state variable called shouldRender and set it to false. You're already using the getIssues function to get metafield values. Using the same function, check if the product has more than one variant. If it does, then set the shouldRender state to true.

## Conditionally return JSX content based on the result of the getProductVariants function.

If shouldRender is true, then render the block's content. If it's false, then return null to collapse the block.

Use the collapsedSummary to provide meaningful information to the merchant about why the block is collapsed.

## Test hiding the admin block

After you've updated the UI extension, test that the admin block collapses with the following steps:

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

Press p to open the developer console.

In the Dev Console page, click on the preview link for the issue tracker UI extension.

If there are any product variants, delete them and confirm that the admin block is collapsed.

Add a product variant with two options and confirm that the admin block expands.

## Hide an admin action

Hiding a UI extension's admin action uses a second script to control the visibility of the action in the More actions menu. This script only runs after the page is loaded and doesn't maintain state.

- Add a field to your TOML file to specify the path to the shouldRender script.
- Create a condition/shouldRender.js file in the same src directory as the extension that you want to control.
- Use the should-render target of the extension that you want to control.

So, for an extensions with the target admin.product-details.action.render, the should-render target would be admin.product-details.action.should-render.

- Register your module using the global shopify.extend method.
- Create a function called getProductVariants to fetch variants of the product in your utils.js file.
- Use the getProductVariants function to determine the number of variants on the product. Return an object with a key of display and a Boolean value to control whether the action extension menu item is visible.

## Test hiding the admin action

After you've updated the UI extensions that provide your admin action and block, test them with the following steps:

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

Press p to open the developer console.

Delete any variants that were added in the previous section.

If there are any product variants, delete them and confirm that the admin action is not visible in the More actions menu.

Add a product variant with two options and confirm that the admin action is visible in the More actions menu.

**📁 BlockExtension.jsx** `/extensions/issue-tracker-conditional-block/src/BlockExtension.jsx`
```javascript
import { useEffect, useMemo, useState } from "react";
import {
  AdminBlock,
  Box,
  Button,
  Divider,
  Form,
  Icon,
  InlineStack,
  ProgressIndicator,
  Select,
  Text,
  reactExtension,
  useApi,
} from "@shopify/ui-extensions-react/admin";

import { getIssues, updateIssues } from "./utils";

// The target used here must match the target used in the extension's .toml file at ./shopify.extension.toml
const TARGET = "admin.product-details.block.render";
export default reactExtension(TARGET, () => <App />);

const PAGE_SIZE = 3;

function App() {
  const { data, i18n } = useApi(TARGET);
  const [issues, setIssues] = useState([]);

  const productId = data.selected[0].id;
  const issuesCount = issues.length;
  const totalPages = issuesCount / PAGE_SIZE;

  const [loading, setLoading] = useState(true);
  const [initialValues, setInitialValues] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    (async function getProductInfo() {
      const productData = await getIssues(productId);

      setLoading(false);

      if (productData?.data?.product?.variants?.edges.length > 1) {
        setShouldRender(true);
      }
      if (productData?.data?.product?.metafield?.value) {
        const parsedIssues = JSON.parse(
          productData.data.product.metafield.value
        );
        setInitialValues(
          parsedIssues.map(({ completed }) => Boolean(completed))
        );
        setIssues(parsedIssues);
      }
    })();
  }, [productId]);

  const paginatedIssues = useMemo(() => {
    if (issuesCount <= PAGE_SIZE) {
      // It's not necessary to paginate if there are fewer issues than the page size
      return issues;
    }

    // Slice the array after the last item of the previous page
    return [...issues].slice(
      (currentPage - 1) * PAGE_SIZE,
      currentPage * PAGE_SIZE
    );
  }, [issuesCount, issues, currentPage]);

  const handleChange = async (id, value) => {
    // Update the local state of the extension to reflect changes
    setIssues((currentIssues) => {
      // Create a copy of the array so that you don't mistakenly mutate the state
      const newIssues = [...currentIssues];
      // Find the index of the issue that you're interested in
      const editingIssueIndex = newIssues.findIndex(
        (listIssue) => listIssue.id == id
      );
      // Overwrite that item with the new value
      newIssues[editingIssueIndex] = {
        // Spread the previous item to retain the values that you're not changing
        ...newIssues[editingIssueIndex],
        // Update the completed value
        completed: value === "completed" ? true : false,
      };
      return newIssues;
    });
  };

  const handleDelete = async (id) => {
    // Create a new array of issues, leaving out the one that you're deleting
    const newIssues = issues.filter((issue) => issue.id !== id);
    // Save to the local state
    setIssues(newIssues);
    // Commit changes to the database
    await updateIssues(productId, newIssues);
  };

  const onSubmit = async () => {
    // Commit changes to the database
    await updateIssues(productId, issues);
  };

  const onReset = () => {};

  const blockMarkup = loading ? (
    <InlineStack blockAlignment="center" inlineAlignment="center">
      <ProgressIndicator size="large-100" />
    </InlineStack>
  ) : (
    <>
      <Text>Issues</Text>
      <Form id={`issues-form`} onSubmit={onSubmit} onReset={onReset}>
        {issues.length ? (
          <>
            {paginatedIssues.map(
              ({ id, title, description, completed }, index) => {
                return (
                  <>
                    {index > 0 && <Divider />}
                    <Box key={id} padding="base small">
                      <InlineStack
                        blockAlignment="center"
                        inlineSize="100%"
                        gap="large"
                      >
                        <Box inlineSize="53%">
                          <Box inlineSize="100%">
                            <Text fontWeight="bold" textOverflow="ellipsis">
                              {title}
                            </Text>
                          </Box>

                          <Box inlineSize="100%">
                            <Text textOverflow="ellipsis">{description}</Text>
                          </Box>
                        </Box>
                        <Box inlineSize="22%">
                          <Select
                            label="Status"
                            name="status"
                            defaultValue={
                              initialValues[index] ? "completed" : "todo"
                            }
                            value={completed ? "completed" : "todo"}
                            onChange={(value) => handleChange(id, value)}
                            options={[
                              { label: "Todo", value: "todo" },
                              {
                                label: "Completed",
                                value: "completed",
                              },
                            ]}
                          />
                        </Box>
                        <Box inlineSize="25%">
                          <InlineStack inlineSize="100%" inlineAlignment="end">
                            <Button
                              onPress={() => handleDelete(id)}
                              variant="tertiary"
                            >
                              <Icon name="DeleteMinor" />
                            </Button>
                          </InlineStack>
                        </Box>
                      </InlineStack>
                    </Box>
                  </>
                );
              }
            )}
            <InlineStack
              paddingBlockStart="large"
              blockAlignment="center"
              inlineAlignment="center"
            >
              <Button
                onPress={() => setCurrentPage((prev) => prev - 1)}
                disabled={currentPage === 1}
              >
                <Icon name="ChevronLeftMinor" />
              </Button>
              <InlineStack
                inlineSize={25}
                blockAlignment="center"
                inlineAlignment="center"
              >
                <Text>{currentPage}</Text>
              </InlineStack>
              <Button
                onPress={() => setCurrentPage((prev) => prev + 1)}
                disabled={currentPage >= totalPages}
              >
                <Icon name="ChevronRightMinor" />
              </Button>
            </InlineStack>
          </>
        ) : (
          <>
            <Box paddingBlockEnd="large">
              <Text fontWeight="bold">No issues for this product</Text>
          </Box>
          </>
        )}
      </Form>
    </>
  );
  // Only render the block body if there is more than one variant, otherwise, return null to collapse the block
  return (
    <AdminBlock
      // Translate the block title with the i18n API, which uses the strings in the locale files
      title={i18n.translate("name")}
      collapsedSummary={!shouldRender ? "Not enough product variants." : null}
    >
      {shouldRender ? blockMarkup : null}
    </AdminBlock>
  );
}
```

**📁 shopify.extension.toml** `/extensions/issue-tracker-conditional-action/shopify.extension.toml`
```toml
api_version = "2025-01"

[[extensions]]
# Change the merchant-facing name of the extension in locales/en.default.json
name = "t:name"
handle = "issue-tracker-conditional-action"
type = "ui_extension"
[[extensions.targeting]]
module = "./src/ActionExtension.jsx"
# The target used here must match the target used in the module file (./src/ActionExtension.jsx)
target = "admin.product-details.action.render"

[extensions.targeting.should_render]
module = "./src/condition/shouldRender.js"
```

**📁 shouldRender.js** `/extensions/issue-tracker-conditional-action/src/condition/shouldRender.js`
```javascript
import { getProductVariants } from "../utils";

const TARGET = "admin.product-details.action.should-render";

export default shopify.extend(TARGET, async ({ data }) => {
  const variants = await getProductVariants(data);
  const shouldDisplay = variants.length > 1

  return { display: shouldDisplay };
});
```

**📁 utils.js** `/extensions/issue-tracker-conditional-action/src/utils.js`
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
export async function getProductVariants(data) {
  const getProductQuery = {
    query: `query Product($id: ID!) {
      product(id: $id) {
        title
        variants(first: 2) {
          edges {
            node {
              id
            }
          }
        }
      }
    }`,
    variables: {id: data.selected[0].id},
  };

  const res = await fetch("shopify:admin/api/graphql.json", {
    method: "POST",
    body: JSON.stringify(graphQLQuery),
  });

  if (!res.ok) {
    console.error('Network error');
  }

  const productData = await res.json();
  return productData.data.product.variants.edges;
};
```

## Tutorial complete!

Congratulations! You learned how to hide your UI extension's admin blocks and actions when they are not relevant to a given target. Keep the momentum going with these related resources.

**Admin UI extension APIs**
Learn about the admin UI extension APIs.

**Participate**
File any issues or feature requests on the UI Extensions GitHub repository.

**Deploy**
Learn how to deploy your UI extensions to merchants.