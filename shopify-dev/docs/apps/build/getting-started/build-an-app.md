# Build a Shopify app using Remix

After you scaffold an app, you can add your own functionality to pages inside and outside of the Shopify admin.

In this tutorial, you'll scaffold an app that makes QR codes for products. When the QR code is scanned, it takes the user to a checkout that's populated with the product, or to the product page. The app logs every time the QR code is scanned, and exposes scan metrics to the app user.

Follow along with this tutorial to build a sample app, or clone the completed sample app.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Update the Prisma database included in the app template.
- Use the @shopify/shopify-app-remix package to authenticate users and query data.
- Use Polaris components to create a UI that adheres to Shopify's App Design Guidelines.
- Use Shopify App Bridge to add interactivity to your app.

## Requirements

**Scaffold an app**
Scaffold an app that uses the Remix template.

**Install qrcode**
Enables creation of QR codes.

**Install @shopify/polaris-icons**
Provides placeholder images for the UI.

**Install tiny-invariant**
Allows loaders to easily throw errors.

## Project

**Framework:** Remix

Remix
View on GitHub

## Add the QR code data model to your database

To store your QR codes, you need to add a table to the database included in your template.

**📝 INFO**
The single table in the template's Prisma schema is the Session table. It stores the tokens for each store that installs your app, and is used by the @shopify/shopify-app-session-storage-prisma package to manage sessions.

### Create the table

Add a QRCode model to your Prisma schema. The model should contain the following fields:

- **id**: The primary key for the table.
- **title**: The app user-specified name for the QR code.
- **shop**: The store that owns the QR code.
- **productId**: The product that this QR code is for.
- **productHandle**: Used to create the destination URL for the QR code.
- **productVariantId**: Used to create the destination URL for the QR code.
- **destination**: The destination for the QR code.
- **scans**: The number times that the QR code been scanned.
- **createdAt**: The date and time when the QR code was created.

The QRCode model contains the key identifiers that the app uses to retrieve Shopify product and variant data. At runtime, additional product and variant properties are retrieved and used to populate the UI.

**📁 schema.prisma** `/prisma/schema.prisma`
```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = "file:dev.sqlite"
}

model Session {
  id          String    @id
  shop        String
  state       String
  isOnline    Boolean   @default(false)
  scope       String?
  expires     DateTime?
  accessToken String
  userId      BigInt?
}

model QRCode {
  id               Int      @id @default(autoincrement())
  title            String
  shop             String
  productId        String
  productHandle    String
  productVariantId String
  destination      String
  scans            Int      @default(0)
  createdAt        DateTime @default(now())
}
```

### Migrate the database

After you add your schema, you need to migrate the database to create the table.

Run the following command to create the table in Prisma:

**Terminal**
```bash
npm run prisma migrate dev -- --name add-qrcode-table
```

To confirm that your migration worked, open Prisma Studio:

**Terminal**
```bash
npm run prisma studio
```

Prisma Studio opens in your browser.

In Prisma Studio, click the QRCode tab to view the table.

You should see a table with the columns that you created, and no data.

## Get QR code and product data

After you create your database, add code to retrieve data from the table.

Supplement the QR code data in the database with product information.

### Create the model

Create a model to get and validate QR codes.

Create an `/app/models` folder. In that folder, create a new file called `QRCode.server.js`.

**📁 QRCode.server.js**
`/app/models/QRCode.server.js`
```javascript
import qrcode from "qrcode";
import invariant from "tiny-invariant";
import db from "../db.server";

export async function getQRCode(id, graphql) {
  const qrCode = await db.qRCode.findFirst({ where: { id } });

  if (!qrCode) {
    return null;
  }

  return supplementQRCode(qrCode, graphql);
}

export async function getQRCodes(shop, graphql) {
  const qrCodes = await db.qRCode.findMany({
    where: { shop },
    orderBy: { id: "desc" },
  });

  if (qrCodes.length === 0) return [];

  return Promise.all(
    qrCodes.map((qrCode) => supplementQRCode(qrCode, graphql))
  );
}

export function getQRCodeImage(id) {
  const url = new URL(`/qrcodes/${id}/scan`, process.env.SHOPIFY_APP_URL);
  return qrcode.toDataURL(url.href);
}

export function getDestinationUrl(qrCode) {
  if (qrCode.destination === "product") {
    return `https://${qrCode.shop}/products/${qrCode.productHandle}`;
  }

  const match = /gid:\/\/shopify\/ProductVariant\/([0-9]+)/.exec(qrCode.productVariantId);
  invariant(match, "Unrecognized product variant ID");

  return `https://${qrCode.shop}/cart/${match[1]}:1`;
}

async function supplementQRCode(qrCode, graphql) {
  const qrCodeImagePromise = getQRCodeImage(qrCode.id);

  const response = await graphql(
    `
      query supplementQRCode($id: ID!) {
        product(id: $id) {
          title
          images(first: 1) {
            nodes {
              altText
              url
            }
          }
        }
      }
    `,
    {
      variables: {
        id: qrCode.productId,
      },
    }
  );

  const {
    data: { product },
  } = await response.json();

  return {
    ...qrCode,
    productDeleted: !product?.title,
    productTitle: product?.title,
    productImage: product?.images?.nodes[0]?.url,
    productAlt: product?.images?.nodes[0]?.altText,
    destinationUrl: getDestinationUrl(qrCode),
    image: await qrCodeImagePromise,
  };
}

export function validateQRCode(data) {
  const errors = {};

  if (!data.title) {
    errors.title = "Title is required";
  }

  if (!data.productId) {
    errors.productId = "Product is required";
  }

  if (!data.destination) {
    errors.destination = "Destination is required";
  }

  if (Object.keys(errors).length) {
    return errors;
  }
}
```

### Get QR codes

Create a function to get a single QR code for your QR code form, and a second function to get multiple QR codes for your app's index page. You'll create a QR code form later in this tutorial.

QR codes stored in the database can be retrieved using the Prisma FindFirst and FindMany queries.

### Get the QR code image

A QR code takes the user to `/qrcodes/$id/scan`, where `$id` is the ID of the QR code. Create a function to construct this URL, and then use the qrcode package to return a base 64-encoded QR code image src.

### Get the destination URL

Scanning a QR code takes the user to one of two places:

- The product details page
- A checkout with the product in the cart

Create a function to conditionally construct this URL depending on the destination that the merchant selects.

### Retrieve additional product and variant data

The QR code from Prisma needs to be supplemented with product data. It also needs the QR code image and destination URL.

Create a function that queries the GraphQL Admin API for the product title, and the first featured product image's URL and alt text. It should also return an object with the QR code data and product data, and use the getDestinationUrl and getQRCodeImage functions that you created to get the destination URL's QR code image.

### Validate QR codes

To create a valid QR code, the app user needs to provide a title, and select a product and destination. Add a function to ensure that, when the user submits the form to create a QR code, values exist for all of the required fields.

The action for the QR code form will return errors from this function.

## Create a QR code form

Create a form that allows the app user to manage QR codes.

To create this form, you'll use a Remix route, Polaris components and App Bridge.

### Set up the form route

Create a form that can create, update or delete a QR code.

In the `app > routes` folder, create a new file called `app.qrcodes.$id.jsx`.

**Dynamic segments**
This route uses a dynamic segment to match the URL for creating a new QR code and editing an existing one.

If the user is creating a QR code, the URL is `/app/qrcodes/new`. If the user is updating a QR code, the URL is `/app/qrcodes/1`, where 1 is the ID of the QR code that the user is updating.

**Remix layouts**
The Remix template includes a Remix layout at `app/routes/app.jsx`. This layout should be used for authenticated routes that render inside the Shopify admin. It's responsible for configuring App Bridge and Polaris, and authenticating the user using shopify-app-remix.

**📁 app.qrcodes.$id.jsx**
`/app/routes/app.qrcodes.$id.jsx`
```javascript
import { useState } from "react";
import { json, redirect } from "@remix-run/node";
import {
  useActionData,
  useLoaderData,
  useNavigation,
  useSubmit,
  useNavigate,
} from "@remix-run/react";
import { authenticate } from "../shopify.server";
import {
  Card,
  Bleed,
  Button,
  ChoiceList,
  Divider,
  EmptyState,
  InlineStack,
  InlineError,
  Layout,
  Page,
  Text,
  TextField,
  Thumbnail,
  BlockStack,
  PageActions,
} from "@shopify/polaris";
import { ImageMajor, AlertDiamondMajor } from "@shopify/polaris-icons";

import db from "../db.server";
import { getQRCode, validateQRCode } from "../models/QRCode.server";

export async function loader({ request, params }) {
  const { admin } = await authenticate.admin(request);

  if (params.id === "new") {
    return json({
      destination: "product",
      title: "",
    });
  }

  return json(await getQRCode(Number(params.id), admin.graphql));
}

export async function action({ request, params }) {
  const { session } = await authenticate.admin(request);
  const { shop } = session;

  const data = {
    ...Object.fromEntries(await request.formData()),
    shop,
  };

  if (data.action === "delete") {
    await db.qRCode.delete({ where: { id: Number(params.id) } });
    return redirect("/app");
  }

  const errors = validateQRCode(data);

  if (errors) {
    return json({ errors }, { status: 422 });
  }

  const qrCode =
    params.id === "new"
      ? await db.qRCode.create({ data })
      : await db.qRCode.update({ where: { id: Number(params.id) }, data });

  return redirect(`/app/qrcodes/${qrCode.id}`);
}

export default function QRCodeForm() {
  const errors = useActionData()?.errors || {};

  const qrCode = useLoaderData();
  const [formState, setFormState] = useState(qrCode);
  const [cleanFormState, setCleanFormState] = useState(qrCode);
  const isDirty = JSON.stringify(formState) !== JSON.stringify(cleanFormState);

  const nav = useNavigation();
  const isSaving =
    nav.state === "submitting" && nav.formData?.get("action") !== "delete";
  const isDeleting =
    nav.state === "submitting" && nav.formData?.get("action") === "delete";

  const navigate = useNavigate();
  const submit = useSubmit();

  function selectProduct() {
    shopify.resourcePicker({
      type: "product",
      action: "select", // customized action verb, either 'select' or 'add',
    }).then(({ selection }) => {
      setFormState({
        ...formState,
        productId: selection[0].id,
        productVariantId: selection[0].variants[0].id,
        productTitle: selection[0].title,
        productHandle: selection[0].handle,
        productAlt: selection[0].images[0]?.altText,
        productImage: selection[0].images[0]?.originalSrc,
      });
    });
  }

  function handleSave() {
    const data = {
      title: formState.title,
      productId: formState.productId || "",
      productVariantId: formState.productVariantId || "",
      productHandle: formState.productHandle || "",
      destination: formState.destination,
    };

    setCleanFormState({ ...formState });
    submit(data, { method: "post" });
  }

  return (
    <Page>
      <ui-title-bar title={qrCode.id ? "Edit QR code" : "Create QR code"}>
        <button variant="breadcrumb" onClick={() => navigate("/app")}>
          QR codes
        </button>
      </ui-title-bar>
      <Layout>
        <Layout.Section>
          <BlockStack gap="500">
            <Card>
              <BlockStack gap="500">
                <Text as={"h2"} variant="headingLg">
                  Title
                </Text>
                <TextField
                  id="title"
                  helpText="Only store staff can see this title"
                  label="title"
                  labelHidden
                  autoComplete="off"
                  value={formState.title}
                  onChange={(title) => setFormState({ ...formState, title })}
                  error={errors.title}
                />
              </BlockStack>
            </Card>
            <Card>
              <BlockStack gap="500">
                <InlineStack align="space-between">
                  <Text as={"h2"} variant="headingLg">
                    Product
                  </Text>
                  {formState.productId ? (
                    <Button variant={"plain"} onClick={selectProduct}>
                      Change product
                    </Button>
                  ) : null}
                </InlineStack>
                {formState.productId ? (
                  <InlineStack blockAlign="center" gap="500">
                    <Thumbnail
                      source={formState.productImage || ImageMajor}
                      alt={formState.productAlt}
                    />
                    <Text as="span" variant="headingMd" fontWeight="semibold">
                      {formState.productTitle}
                    </Text>
                  </InlineStack>
                ) : (
                  <BlockStack gap="200">
                    <Button onClick={selectProduct} id="select-product">
                      Select product
                    </Button>
                    <InlineError
                      message={errors.productId}
                      fieldID="myFieldID"
                    />
                  </BlockStack>
                )}
              </BlockStack>
            </Card>
            <Card>
              <BlockStack gap="500">
                <Text as={"h2"} variant="headingLg">
                  Destination
                </Text>
                <ChoiceList
                  title="Scan destination"
                  titleHidden
                  choices={[
                    { label: "Link to product page", value: "product" },
                    {
                      label: "Link to checkout page with product in the cart",
                      value: "cart",
                    },
                  ]}
                  selected={[formState.destination]}
                  onChange={(destination) =>
                    setFormState({ ...formState, destination: destination[0] })
                  }
                />
                <InlineError
                  message={errors.destination}
                  fieldID="myFieldID"
                />
              </BlockStack>
            </Card>
          </BlockStack>
        </Layout.Section>
        <Layout.Section variant="oneThird">
          <Card>
            <Text as={"h2"} variant="headingLg">
              QR code
            </Text>
            {qrCode ? (
              <EmptyState image={qrCode.image} imageContained={true}>
                <p>Embed this QR code in your product or marketing materials</p>
                <BlockStack gap="300">
                  <Button
                    url={`/qrcodes/${qrCode.id}`}
                    external={true}
                    variant="plain"
                  >
                    Go to public URL
                  </Button>
                  <Button
                    download
                    url={qrCode.image}
                    variant="plain"
                  >
                    Download
                  </Button>
                </BlockStack>
              </EmptyState>
            ) : (
              <EmptyState image="https://cdn.shopify.com/s/files/1/0262/4071/2726/files/emptystate-files.png">
                <p>Your QR code will appear here after you save</p>
              </EmptyState>
            )}
          </Card>
        </Layout.Section>
        <Layout.Section>
          <PageActions
            secondaryActions={
              qrCode.id
                ? [
                    {
                      content: "Delete",
                      loading: isDeleting,
                      disabled: !qrCode.id || isSaving || isDeleting,
                      destructive: true,
                      outline: true,
                      onAction: () =>
                        submit({ action: "delete" }, { method: "post" }),
                    },
                  ]
                : undefined
            }
            primaryAction={{
              content: "Save",
              loading: isSaving,
              disabled: !isDirty || isSaving || isDeleting,
              onAction: handleSave,
            }}
          />
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

### Authenticate the user

Authenticate the route using shopify-app-remix.

If the user isn't authenticated, authenticate.admin handles the necessary redirects. If the user is authenticated, then the method returns an admin object.

You can use the authenticate.admin method for the following purposes:

- Getting information from the session, such as the shop
- Accessing the GraphQL Admin API
- Within methods to require and request billing
- Authenticating admin requests

### Return a JSON Response

Using the json util, return a Response that can be used to show QR code data.

If the id parameter is new, return JSON with an empty title, and product for the destination. If the id parameter isn't new, then return the JSON from getQRCode to populate the QR code state.

### Manage the form state

Maintain the state of the QR code form state using the following variables:

- **errors**: If the app user doesn't fill all of the QR code form fields, then the action returns errors to display. This is the return value of validateQRCode, which is accessed through the Remix useActionData hook.
- **formState**: When the user changes the title, selects a product, or changes the destination, this state is updated. This state is copied from useLoaderData into React state.
- **cleanFormState**: The initial state of the form. This only changes when the user submits the form. This state is copied from useLoaderData into React state.
- **isDirty**: Determines if the form has changed. This is used to enable save buttons when the app user has changed the form contents, or disable them when the form contents haven't changed.
- **isSaving and isDeleting**: Keeps track of the network state using useNavigation. This state is used to disable buttons and show loading states.

### Add a product selector

Using the App Bridge ResourcePicker action, add a modal that allows the user to select a product. Save the selection to form state.

### Save form data

Use the useSubmit Remix hook to save the form data.

Copy the data that Prisma needs from formState and set the cleanFormState to the current formState.

### Lay out the form

Using Polaris components, build the layout for the form. Use Page, Layout, and BlockStack to structure the page. The page should have two columns.

Polaris is the design system for the Shopify admin. Using Polaris components ensures that your UI is accessible, responsive, and displays consistently with the Shopify Admin.

### Add breadcrumbs

Use an App Bridge ui-title-bar action to display a title that indicates to the user whether they're creating or editing a QR code. Include a breadcrumb link to go back to the QR code list.

### Add a title field

Use TextField for updating the title. It should setFormState, have some helpText and show title errors from useActionData.

Wrap the area in a Card, and use BlockStack to space the content correctly.

### Add a way to select the product

If the user hasn't selected a product, then display a Button that triggers selectProduct.

If the user has selected a product, use Thumbnail to display the product image. Make sure to handle the case where a product has no image.

Use inlineError to display an error from useActionData if the user submits the form without selecting a product.

### Add destination options

Use ChoiceList to render different destinations. It should setFormState when the selection changes.

If the user is editing a QR code, use a Button to link to the destination URL in a new tab.

### Display a preview of the QR code

After saving a QR code, or when editing an existing QR code, provide ways to preview the QR code that the app user created.

If a QR code is available, then use EmptyState to render the QR code. If no QR code is available, then use an EmptyState component with a different configuration.

Add buttons to download the QR code, and to preview the public URL.

### Add save and delete buttons

Use PageActions to render Save and Delete buttons.

Add a primaryAction to save the QR code and a secondaryAction. Make sure to handle loading and disabled states.

### Create, update, or delete a QR code

Create an action to create, update, or delete a QR code.

The action should use the store from the session. This ensures that the app user can only create, update, or delete QR codes for their own store.

The action should return errors for incomplete data using your validateQRCode function.

If the action deletes a QR code, redirect the app user to the index page. If the action creates a QR code, redirect to app/qrcodes/$id, where $id is the ID of the newly created QR code.

## List QR codes

To allow app users to navigate to QR codes, list the QR codes in the app home.

### Load QR codes

In the app's index route, load the QR codes using a Remix loader.

The loader should load QR codes using the qrcodes function from app/models/QRCode.server.js, and return them in a JSON Response.

**📁 app._index.jsx**
`/app/routes/app._index.jsx`
```javascript
import { json } from "@remix-run/node";
import { useLoaderData, Link, useNavigate } from "@remix-run/react";
import { authenticate } from "../shopify.server";
import {
  Card,
  EmptyState,
  Layout,
  Page,
  IndexTable,
  Thumbnail,
  Text,
  Icon,
  InlineStack,
} from "@shopify/polaris";

import { getQRCodes } from "../models/QRCode.server";
import { AlertDiamondIcon, ImageIcon } from "@shopify/polaris-icons";

export async function loader({ request }) {
  const { admin, session } = await authenticate.admin(request);
  const qrCodes = await getQRCodes(session.shop, admin.graphql);

  return json({
    qrCodes,
  });
}

const EmptyQRCodeState = ({ onAction }) => (
  <EmptyState
    heading="Create unique QR codes for your product"
    action={{
      content: "Create QR code",
      onAction,
    }}
    image="https://cdn.shopify.com/s/files/1/0262/4071/2726/files/emptystate-files.png"
  >
    <p>Allow customers to scan codes and buy products using their phones.</p>
  </EmptyState>
);

function truncate(str, { length = 25 } = {}) {
  if (!str) return "";
  if (str.length <= length) return str;
  return str.slice(0, length) + "…";
}

const QRTable = ({ qrCodes }) => (
  <IndexTable
    resourceName={{
      singular: "QR code",
      plural: "QR codes",
    }}
    itemCount={qrCodes.length}
    headings={[
      { title: "Thumbnail", hidden: true },
      { title: "Title" },
      { title: "Product" },
      { title: "Date created" },
      { title: "Scans" },
    ]}
    selectable={false}
  >
    {qrCodes.map((qrCode) => (
      <QRTableRow key={qrCode.id} qrCode={qrCode} />
    ))}
  </IndexTable>
);

const QRTableRow = ({ qrCode }) => (
  <IndexTable.Row id={qrCode.id} position={qrCode.id}>
    <IndexTable.Cell>
      <Thumbnail
        source={qrCode.productImage || ImageIcon}
        alt={qrCode.productTitle}
        size="small"
      />
    </IndexTable.Cell>
    <IndexTable.Cell>
      <Link to={`qrcodes/${qrCode.id}`}>{truncate(qrCode.title)}</Link>
    </IndexTable.Cell>
    <IndexTable.Cell>
      {qrCode.productDeleted ? (
        <InlineStack align="start" gap="200">
          <span style={{ width: "20px" }}>
            <Icon source={AlertDiamondIcon} tone="critical" />
          </span>
          <Text tone="critical" as="span">
            product has been deleted
          </Text>
        </InlineStack>
      ) : (
        truncate(qrCode.productTitle)
      )}
    </IndexTable.Cell>
    <IndexTable.Cell>
      {new Date(qrCode.createdAt).toDateString()}
    </IndexTable.Cell>
    <IndexTable.Cell>{qrCode.scans}</IndexTable.Cell>
  </IndexTable.Row>
);

export default function Index() {
  const { qrCodes } = useLoaderData();
  const navigate = useNavigate();

  return (
    <Page>
      <ui-title-bar title="QR codes">
        <button variant="primary" onClick={() => navigate("/app/qrcodes/new")}>
          Create QR code
        </button>
      </ui-title-bar>
      <Layout>
        <Layout.Section>
          <Card padding="0">
            {qrCodes.length === 0 ? (
              <EmptyQRCodeState onAction={() => navigate("qrcodes/new")} />
            ) : (
              <QRTable qrCodes={qrCodes} />
            )}
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

### Create an empty state

If there are no QR codes, use EmptyState to present a call to action to create QR codes.

### Create an index table

If there are QR codes present, then use the Polaris IndexTable component to list them.

The table should have columns for the product image, QR code title, product name, the date the QR code was created, and the number of times the QR code was scanned.

### Create index table rows

Map over each QR code and render an IndexTable.Row that uses Polaris components to structure the row and render QR code information.

### Warn if a product is deleted

A merchant can delete a product after creating a QR code for it. The data returned from supplementQRCode includes an isDeleted property. isDeleted is true if the product title returned from the GraphQL Admin API is an empty string.

Render a warning to the user if a product is deleted.

For a full list of the icons included in the @shopify/polaris-icons package, refer to the Icons reference.

### Lay out the page

After you create your empty state and index table, adjust the layout of the index page to return the markup that you created.

Create a layout using Polaris components. Render the empty state and table inside a Polaris Card.

Use the App Bridge ui-title-bar to render the title bar with a title. Add a primary button to navigate to the QR code creation form.

## Add a public QR code route

Make QR codes scannable by customers by exposing them using a public URL. When a customer scans a QR code, the scan count should increment, and the customer should be redirected to the destination URL.

### Create a public QR code route

Create a public page to render a QR code.

In the `app > routes` folder, create a new file called `qrcodes.$id.jsx`.

Because the `qrcodes.$id.jsx` doesn't require authentication or need to be rendered inside of the Shopify admin, it doesn't use the app layout.

**📁 qrcodes.$id.jsx**
`/app/routes/qrcodes.$id.jsx`
```javascript
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import invariant from "tiny-invariant";

import { authenticate } from "../shopify.server";
import { getQRCodeImage } from "../models/QRCode.server";
import db from "../db.server";

export const loader = async ({ params }) => {
  invariant(params.id, "Could not find QR code destination");

  const id = Number(params.id);
  const qrCode = await db.qRCode.findFirst({ where: { id } });

  invariant(qrCode, "Could not find QR code destination");

  return json({
    title: qrCode.title,
    image: await getQRCodeImage(id),
  });
};

export default function QRCode() {
  const { image, title } = useLoaderData();

  return (
    <>
      <h1>{title}</h1>
      <img src={image} alt={`QR Code for product`} />
    </>
  );
}
```

### Load the QR code

Create a loader to load the QR code on the external route.

In the function, check that there's an ID in the URL. If there isn't, throw an error using tiny-invariant.

If there's an ID in the URL, load the QR code with that ID using Prisma:

If there is no matching QR code ID in the table, throw an error using tiny-invariant.
If there is a matching ID, return the QR code using a Remix json function.

### Render a public QR code image

In the route's default export, render an img tag for the QR code image. Scanning this image takes the user to the destination URL. This is the next route to implement.

## Redirect the customer to the destination URL

When a QR code is scanned, redirect the customer to the destination URL. You can also increment the QR code scan count to reflect the number of times the QR code has been used.

### Create the scan route

Create a public route that handles QR code scans.

In the `app > routes` folder, create a new file called `qrcodes.$id.scan.jsx`.

**📁 qrcodes.$id.scan.jsx**
`/app/routes/qrcodes.$id.scan.jsx`
```javascript
import { redirect } from "@remix-run/node";
import invariant from "tiny-invariant";
import db from "../db.server";

import { getDestinationUrl } from "../models/QRCode.server";

export const loader = async ({ params }) => {
  invariant(params.id, "Could not find QR code destination");

  const id = Number(params.id);
  const qrCode = await db.qRCode.findFirst({ where: { id } });

  invariant(qrCode, "Could not find QR code destination");

  await db.qRCode.update({
    where: { id },
    data: { scans: { increment: 1 } },
  });

  return redirect(getDestinationUrl(qrCode));
};
```

### Validate the QR code ID

Create a loader function to load the QR code from the database.

In this function, check there is an ID in the URL. If the ID isn't present, then throw an error using tiny-invariant.

Load the QR code from the Prisma database. If a QR code with the specified ID doesn't exist, then throw an error using tiny-invariant.

### Increment the scan count

If the loader returns a QR code, then increment the scan count in the database.

Redirect to the destination URL for the QR code using getDestinationUrl and the Remix redirect utility.

### Redirect

The loader should return the destination URL for the QR code it incremented. Use getDestinationUrl from app/models/QRCode.server.js to get that URL. Use redirect from Remix to redirect the user to that URL.

## Preview and test your app

Use the CLI to preview your app. If you make changes, you'll see those changes hot reload in the browser.

### Start your server

Run the Shopify CLI dev command to build your app and preview it on your development store.

In a terminal, navigate to your app directory.

Either start or restart your server to build and preview your app:

**Terminal**
```bash
shopify app dev
```

Press p to open the developer console. In the developer console page, click on the preview link for your app home.

If you're prompted to install the app, then click Install.

### Test the QR code index and form

Follow these steps to test the routes that are exposed to the app user in the Shopify admin. These routes include the app index and the QR code form.

1. In the index page for your app home, click **Create QR code** to go to the QR code form.

2. The QR code form opens at `/app/qrcode/new`. The title of the page is **Create QR code**.

3. Try to submit the QR code form with an empty title, or without selecting a product.

   An error is returned.

4. Create a few QR codes for different products and destinations.

5. Click the **QR codes** breadcrumb to return to the index page.

   The QR code list is populated with the QR codes that you created.

6. Select a QR code from the list.

   The QR code form opens at `/app/qrcode/<id>`. The title of the page is **Edit QR code**.

7. On the **Edit QR code** page, click **Delete**.

   You're taken back to the index page, and the deleted QR code is removed from the list.

### Test QR code scanning functionality

Scan the QR code that you created in the previous step.

1. From the app index page, click an existing QR code or create a new one.

2. On the QR code form, click **Go to public URL**.

   A new tab opens for the public URL for the QR code.

3. Scan the QR code with your phone.

   You're taken the destination URL.

4. Return to your app index page.

   The scan count for the QR code that just scanned is incremented.

## Tutorial Complete!

Congratulations! You built a QR code app using Remix, Polaris, App Bridge and Prisma. Keep the momentum going with these related tutorials and resources.

## Next steps

### Use webhooks

You can use webhooks to stay in sync with Shopify, or execute code after a specific event occurs in the store.

For example, if a merchant updates a product's handle, you can use the products/update webhook to trigger an update to the handle in your database.

### Explore the GraphQL Admin API

The GraphQL Admin API lets you read and write Shopify data, including products, customers, orders, inventory, fulfillment, and more.

Explore the GraphQL Admin API to learn about the available types and operations.

### Learn more about extending Shopify

Learn about the most common places where apps can add functionality to the Shopify platform, and the related APIs and tools available for building.

### Select an app distribution method

Decide how you want to share your app with users. For example, you might make your app available in the Shopify App Store, and bill customers for usage.

### Deploy your app

Follow our guide to deploy your Remix app to a testing or production environment.