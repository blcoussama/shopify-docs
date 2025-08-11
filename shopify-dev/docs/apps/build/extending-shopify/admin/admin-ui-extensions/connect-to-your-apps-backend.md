# Connect UI extensions to your app's backend

This guide is the fourth part of a five-part tutorial series that describes how to build UI extensions that display as actions and blocks in Shopify admin. Before starting this guide, you'll need to build or copy the code for the issue tracker UI extensions from the previous section of the tutorial.

So far you've used direct API access to interact with the GraphQL Admin API. However, your app may have data or functionality that can only be accessed from your app's backend. This tutorial will demonstrate how to fetch data from your app's backend in an admin UI extension.

To demonstrate this, we'll build a new Generate issue button that populates an issue's title and description with suggested values from the app's backend.

An issue title and description automatically generated with an admin action UI extension.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Create a resource route in the Remix app template that an admin UI extension can use to fetch data
- Update your UI extension, so that your action can fetch the data when a merchant presses a button
- Run the UI extensions locally and test them on a development store

## Requirements

### Tutorials
You've completed or copied the code from the admin action tutorial, the admin block tutorial, and the tutorial about connecting admin UI extensions.

## Project

Extension:

React

React
View on GitHub

## Create a new resource route that returns data

Create a resource route in your app, by creating a new route file that doesn't export a default component. This route will return suggested issue titles and descriptions.

When you're returning data from this route, you should wrap the response with the cors helper that's returned from the authenticate.admin() function.

Shopify extensions are hosted on a separate domain, so this route is inaccessible if you don't set the correct CORS headers with this method.

Create and return a list of product issues from your new route.

## Call the route from your UI extension's action

Now that your app has an API to return a suggestion, you can call it from the app's admin action UI extension and use the provided data to populate the extension's title and description fields.

Admin UI extensions can make calls to your app's backend by using fetch(). The extension automatically adds the correct authorization header, manages session tokens, and resolves any relative paths against your app's app_url.

## Test the UI extension

After you've updated the UI extension, test it with the following steps:

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

On the Dev Console page, click on the preview link for the issue tracker UI extension. The product details page opens. If you don't have a product in your store, then you need to create one.

To launch your UI extension, in the top right of the page click the More actions dropdown list and select your UI extension.

A merchant automatically generating an issue title and description in an admin action UI extension.

In the banner, click Generate issue. The issue's title and description are populated with data from your app's backend.

**=Á api.recommendedProductIssue.js** `/app/routes/api.recommendedProductIssue.js`
```javascript
import { json } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }) => {
  // The authenticate.admin method returns a CORS method to automatically wrap responses so that extensions, which are hosted on extensions.shopifycdn.com, can access this route.
  const { cors } = await authenticate.admin(request);

  const productIssues = [
    { title: "Too big", description: "The product was too big." },
    { title: "Too small", description: "The product was too small." },
    {
      title: "Just right",
      description:
        "The product was just right, but the customer is still unhappy.",
    },
  ];

  // Get the product Id from the request
  const url = new URL(request.url);
  const productId = url.searchParams.get("productId");
  var splitStr = productId.split("/");
  var idNumber = parseInt(splitStr[splitStr.length - 1], 10);

  // Our proprietary machine learning algorithm automatically determines the best product issue :).
  const issue = productIssues[idNumber % productIssues.length];

  // Wrap the response in the CORS method so that the extension can access it
  return cors(json({ productIssue: issue }));
};
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
  BlockStack,
  Text,
  ProgressIndicator,
  InlineStack,
  Banner,
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

// The target used here must match the target used in the extension's .toml file at ./shopify.ui.extension.toml
const TARGET = "admin.product-details.action.render";

export default reactExtension(TARGET, () => <App />);

function App() {
  const { close, data, intents } = useApi(TARGET);
  const issueId = intents?.launchUrl
    ? new URL(intents?.launchUrl)?.searchParams?.get("issueId")
    : null;
  const [loadingInfo, setLoadingInfo] = useState(issueId ? true : false);
  const [loadingRecommended, setLoadingRecommended] = useState(false);
  const [issue, setIssue] = useState({ title: "", description: "" });
  const [allIssues, setAllIssues] = useState([]);
  const [formErrors, setFormErrors] = useState(null);
  const [isEditing, setIsEditing] = useState(false);


  useEffect(() => {
    getIssues(data.selected[0].id).then((issues) => {
      setLoadingInfo(false);
      setAllIssues(issues || []);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getIssueRecommendation = useCallback(async () => {
    // Get a recommended issue title and description from your app's backend
    setLoadingRecommended(true);
    // fetch is automatically authenticated and the path is resolved against your app's URL
    const res = await fetch(
      `api/recommendedProductIssue?productId=${data.selected[0].id}`,
    );
    setLoadingRecommended(false);

    if (!res.ok) {
      console.error("Network error");
    }
    const json = await res.json();
    if (json?.productIssue) {
      // If you get an recommendation, then update the title and description fields
      setIssue(json?.productIssue);
    }
  }, [data.selected]);

  const onSubmit = useCallback(async () => {
    const {isValid, errors} = validateForm(issue);
    setFormErrors(errors);

    if (isValid) {
      const newIssues = [...allIssues];
      if (isEditing) {
        // Find the index of the issue that you're editing
        const editingIssueIndex = newIssues.findIndex(
          (listIssue) => listIssue.id == issue.id,
        );
        // Overwrite that issue's title and description with the new ones
        newIssues[editingIssueIndex] = {
          ...issue,
          title: issue.title,
          description: issue.description,
        };
      } else {
        // Add a new issue at the end of the list
        newIssues.push({
          id: generateId(allIssues),
          title: issue.title,
          description: issue.description,
          completed: false,
        });
      }

      // Commit changes to the database
      await updateIssues(data.selected[0].id, newIssues);
      // Close the modal
      close();
    }
  }, [allIssues, close, data.selected, isEditing, issue]);

  useEffect(() => {
    if (issueId) {
      // If opened from the block extension, then find the issue that's being edited
      const editingIssue = allIssues.find(({ id }) => `${id}` === issueId);
      if (editingIssue) {
        // Set the issue's ID in the state
        setIssue(editingIssue);
        setIsEditing(true);
      }
    } else {
      setIsEditing(false);
    }
  }, [issueId, allIssues]);

  if (loadingInfo) {
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

      {/*Create a banner to let the buyer auto fill the issue with the
      recommendation from the backend*/}
      <BlockStack gap="base">
        <Banner>
          <BlockStack gap="base">
            <Text>
              Automatically fill the issue based on past customer feedback
            </Text>
            <InlineStack blockAlignment="center" gap="base">
              {/*When the button is pressed, fetch the reccomendation*/}
              <Button
                onPress={getIssueRecommendation}
                disabled={loadingRecommended}
              >
                Generate issue
              </Button>
              {loadingRecommended && <ProgressIndicator size="small-100" />}
            </InlineStack>
          </BlockStack>
        </Banner>

        <TextField
          value={issue.title}
          error={formErrors?.title ? "Please enter a title" : undefined}
          onChange={(val) => setIssue((prev) => ({ ...prev, title: val }))}
          label="Title"
        />

        <TextArea
          value={issue.description}
          error={
            formErrors?.description ? "Please enter a description" : undefined
          }
          onChange={(val) =>
            setIssue((prev) => ({ ...prev, description: val }))
          }
          label="Description"
        />
      </BlockStack>
    </AdminAction>
  );
}
```