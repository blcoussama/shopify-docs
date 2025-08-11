# Connect admin UI extensions

This guide is the third part of a five-part tutorial series that describes how to build UI extensions that display as actions and blocks in Shopify admin. Before starting this guide, you'll need to build or copy code from the admin action UI extension and admin block UI extension guides.

A buyer clicking the edit button on an issue in the admin block UI extension, editing it, and saving it. The edited data appears on the block.

At this point in the tutorial series, you can create new issues using an admin action and you can view and delete the created issues using an admin block. While this is functional, the merchant experience would be better if all of the features could be used in the same location.

Now, you'll modify the block and action so that merchants can create and edit issues directly from the block.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Update your admin block UI extension to launch admin action UI extensions with an intent, to indicate whether it should edit or create a resource
- Update your admin action UI extension, so that it can listen for the intent and edit the appropriate resource
- Run the UI extensions locally and test them on a development store

## Requirements

### Tutorials
You've completed or copied the code from the admin action tutorial and the admin block tutorial.

## Project

Extension:

React

React
View on GitHub

## Add a button to open your action form

Add a button that lets merchants create new issues directly from the block so that they don't have to navigate to More actions at the top of the page.

This button launches the same UI extension for an admin action that you've already written, so you don't have to duplicate your code.

- Access the navigation method from the API.
- Add a button to call navigation.navigate, passing your extension handle to the method as extension:{extension-handle}. The extension handle is defined in your extension's shopify.extension.toml file.

**Note**
Currently, it's only possible to navigate between UI extensions on the same resource page in admin. For example, you can navigate from a block on the product details page (admin.product-details.block.render) to an action on the product details page (admin.product-details.action.render).

- Add a button to display when there are no issues to show.

## Modify the block to launch actions with intents for editing

Add an Edit button to each issue displayed by the UI extension's block. When clicked, this button launches the action using the same navigation API that you used in the previous part of this tutorial.

- Add a button for each issue. This time, when you call navigate for the Edit button, you'll also add a URL parameter that specifies the ID of issue as extension:admin-issue-tracker-action?issueId={id}.

## Modify the action to edit an issue when launched with an intent

Edit your UI extension, so the action checks for the presence of the parameter that you passed.

You'll use the intents API, which gives your extension access to information about how it's been launched. When the action extension detects an issueId parameter in the launch URL from the API, it edits the issue with the ID that that's been passed. To enable editing, you'll first fetch the issue's existing data, and then use it to populate the form.

When the user saves the issue, you'll edit the existing issue instead of creating a new one.

## Test the UI extensions

Navigate to your app directory.

To build and preview your app, either start or restart your server with the following command:

**Terminal**
```bash
shopify app dev
```

Press p to open the developer console.

On the Dev Console page, click on the preview link for the issue tracker UI extension.

The product details page opens. If you don't have a product in your store, then you need to create one.

To find your block, scroll to the bottom of the page. It should display the issues that you've created so far.

On one of the issues, click Edit button. This should open up an action that's pre-populated with the issue details.

Edit the issue and save it. The updated issue should be reflected in the block at the bottom of the page.

A gif showing a user clicking the edit button on an issue from the block extension, editing it in the action and saving it. The edited data appears on the block.

**=Á BlockExtension.jsx** `/extensions/issue-tracker-block/src/BlockExtension.jsx`
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
  const { navigation, data, i18n } = useApi(TARGET);
  const [loading, setLoading] = useState(true);
  const [initialValues, setInitialValues] = useState([]);
  const [issues, setIssues] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const productId = data.selected[0].id;
  const issuesCount = issues.length;
  const totalPages = issuesCount / PAGE_SIZE;

  useEffect(() => {
    (async function getProductInfo() {
      // Load the product's metafield of type issues
      const productData = await getIssues(productId);

      setLoading(false);
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
  }, []);

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
  }, [issues, currentPage]);

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

  return loading ? (
    <InlineStack blockAlignment='center' inlineAlignment='center'>
      <ProgressIndicator size="large-100" />
    </InlineStack>
  ) : (
    <AdminBlock
      // Translate the block title with the i18n API, which uses the strings in the locale files
      title={i18n.translate("name")}
    >
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
                            <Text fontWeight="bold" textOverflow="ellipsis">{title}</Text>
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
                          <InlineStack
                            inlineSize="100%"
                            blockAlignment="center"
                            inlineAlignment="end"
                            gap="base"
                          >
                            <Button
                              variant="tertiary"
                              onPress={() =>
                                navigation?.navigate(
                                  `extension:issue-tracker-action?issueId=${id}`
                                )
                              }
                            >
                              <Icon name="EditMinor" />
                            </Button>
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
            <Divider />
            <Box paddingBlockStart="base">
              <Button
                onPress={() => navigation?.navigate(`extension:issue-tracker-action`)}
              >
                Add issue
              </Button>
            </Box>
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
            <Button
              onPress={() => navigation?.navigate(`extension:issue-tracker-action`)}
            >
              Add your first issue
            </Button>
          </>
        )}
      </Form>
    </AdminBlock>
  );
}
```

**=Á ActionExtension.jsx** `/extensions/issue-tracker-action/src/ActionExtension.jsx`
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
  const { close, data, intents } = useApi(TARGET);
  const issueId = intents?.launchUrl
    ? new URL(intents?.launchUrl)?.searchParams?.get("issueId")
    : null;
  const [loading, setLoading] = useState(issueId ? true : false);
  const [issue, setIssue] = useState({ title: "", description: "" });
  const [allIssues, setAllIssues] = useState([]);
  const [formErrors, setFormErrors] = useState(null);
  const { title, description, id } = issue;
  const isEditing = id !== undefined;

  useEffect(() => {
    getIssues(data.selected[0].id).then((issues) => {
      setLoading(false);
      setAllIssues(issues || []);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = useCallback(async () => {
    const {isValid, errors} = validateForm(issue);
    setFormErrors(errors);

    if (isValid) {
      const newIssues = [...allIssues];
      if (isEditing) {
        // Find the index of the issue that you're editing
        const editingIssueIndex = newIssues.findIndex(
          (listIssue) => listIssue.id == issue.id
        );
        // Overwrite that issue's title and description with the new ones
        newIssues[editingIssueIndex] = {
          ...issue,
          title,
          description,
        };
      } else {
        // Add a new issue at the end of the list
        newIssues.push({
          id: generateId(allIssues),
          title,
          description,
          completed: false,
        });
      }
      // Commit changes to the database
      await updateIssues(data.selected[0].id, newIssues);
      // Close the modal using the 'close' API
      close();
    }
  }, [issue, allIssues, isEditing, data.selected, close, title, description]);

  useEffect(() => {
    if (issueId) {
      // If opened from the block extension, you find the issue that's being edited
      const editingIssue = allIssues.find(({ id }) => `${id}` === issueId);
      if (editingIssue) {
        // Set the issue's ID in the state
        setIssue(editingIssue);
      }
    }
  }, [issueId, allIssues]);

  if (loading) {
    return <></>;
  }

  return (
    <AdminAction
      title={isEditing ? "Edit your issue" : "Create an issue"}
      primaryAction={
        <Button onPress={onSubmit}>{isEditing ? "Save" : "Create"}</Button>
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

## Next steps

**Connect your app's backend**
Complete the next guide in this tutorial series by connecting to your app's backend.

**Admin UI extension APIs**
Learn about admin UI extensions, components, and APIs.

**Deployment**
Learn how to deploy your UI extensions to merchants.

**Issues**
File any issues or feature requests on the UI Extensions GitHub repository.