# Build an admin print action UI extension

This guide demonstrates how to build a UI extension for a print action in Shopify admin. This extension lets users print invoices and packing slips directly from order detail pages.

A UI extension for a print action, as displayed in Shopify admin

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Serve a printable document from your app's backend.
- Create a UI extension for an admin print action that displays on the order details page.
- Create an interface for the extension, allowing merchants to select the documents to print.
- Run your extension locally and test it on a development store.

## Requirements

- Create a Partner account
- Create a development store
- Scaffold an app

Scaffold an app with the read_orders access scope that uses Shopify CLI 3.78 or higher.

- You need to explicitly grant the read_orders access scope to your custom app.
- You need to request the read_all_orders access scope. You will need this for your extension to work with orders that are more than 60 days old.
- You need to request access to protected customer data.
- You need to create at least one order in your development store to test the extension. Make sure to mark the order as paid to convert it from a draft order to a fulfilled order.

## Project

Extension:

React

React
View on GitHub

## Create a route to serve the printable document

To begin, you need to create a route in your app that returns the printable documents for an order. You can use JavaScript to customize the document on your app's backend, but the route must return static HTML without any scripts.

Add a new route file at app/routes/print.js. This file contains the route that will serve the printable document.

**Remix routes**

- Use authenticate.admin(request) to authenticate your request and retrieve the cors utility.
- Define and handle any routes or URL parameters so you can configure the order and documents to be printed.
- After you've authenticated your app, you can query the GraphQL Admin API to fetch data which you can use to populate the document.
- Using the data you've fetched, return the printable document as an HTML response. Be sure to wrap your response in the cors method to automatically set CORS headers. If you need to set CORS headers manually, then set Access-Control-Allow-Origin: "*" after authenticating the request.
- Set the title for the printable document using the <title> element. Most browsers will include the document's title by default on the final printed page.
- If your extension will return multiple documents, be sure to create visual breaks in the CSS so each document is printed as a separate page and users know where each document begins.
- We recommend using the CSS @media print rule and styles here to ensure that the document prints correctly.

Shopify CLI uses Cloudflare tunnels to serve your app. These tunnels default to obfuscating email addresses in the app.

Wrap the email in a magic comment to ensure that the email address is visible in the document.

**Cloudflare email obfuscation**

## Create an admin print action UI extension

After you've created a route to serve the printable document, you can create a new UI extension for a print action that displays on the order details page of Shopify admin. The UI extension will use the route you created in the previous step to fetch the documents.

Use Shopify CLI to generate starter code for your UI extension.

Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

Run the following command to create a new UI extension for a print action in Shopify admin:

**Terminal**
```bash
shopify app generate extension --template admin_print --flavor react
```

The command creates a new UI extension template in your app's extensions directory with the following structure:

**Admin print action structure**
```
extensions/admin-print/
├── README.md
├── locales/
│   ├── en.default.json // The default locale for the extension
│   └── fr.json // The French language translations for the extension
├── package.json
├── shopify.extension.toml // The config file for the extension
└── src/
    └── PrintActionExtension.jsx // The code that defines the print action's UI and behavior
```

## Create the interface for the UI extension

You can configure the UI extension's interface to allow merchants to select the documents they want to print.

Complete the following steps to create the interface for the UI extension:

### Review the configuration

The UI extension's static configuration is stored in its .toml file. To ensure that the print action displays on the order details page, validate that the target is set to admin.order-details.print-action.render.

```
admin.order-details.print-action.render
```

### Use components to create the extension's UI

Admin UI extensions are rendered using Remote UI, which is a fast and secure remote-rendering framework. Because Shopify renders the UI remotely, components used in the extensions must comply with a contract in the Shopify host. We provide these components through the admin UI extensions library.

Admin UI extensions components

### Note the export

You can view the source of your extension in the src/PrintActionExtension.jsx file. This file defines a functional React component exported to run at the extension's target. If you ever want to expose the extension at a different target, you need to update the value here and in the .toml file.

**Troubleshooting**

Configure your app's state to set the printable source URL based on the user's inputs. Passing the ID of the current resource to the AdminPrintAction component sets the document to be previewed and printed.

### Render a UI

To build the interface for your UI extension, return components from src/PrintActionExtension.jsx.

Setting the src prop of the AdminPrintAction container component will display the print preview of the document and enable printing. HTML, PDF, and images are supported.

**Tip**
If there is no document to print, then pass null to the src prop. You might also want to add an error banner to your extension's UI to indicate to the user why no document is available.

## Test the extension

At this point, you can use the Dev Console to run your app's server and preview your UI extension. As you preview the UI extension, changes to its code automatically cause it to reload.

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

In the Dev Console, click on the preview link for your print action UI extension.

The order details page opens. If you don't have an order in your store, then you need to create one.

**Warning**
If you do not have the read_all_orders access scope, ensure that the order you use to test the UI extension is less than 60 days old. Otherwise, your app will fail when fetching the order data.

To launch your UI extension, click the Print dropdown list and select your extension.

Select some options and click Continue to print.

The browser print dialog opens, and you can print the document.

**📁 print.js** `/app/routes/print.js`
```javascript
import { authenticate } from "../shopify.server";

export async function loader({ request }) {
  const { cors, admin } = await authenticate.admin(request);
  const url = new URL(request.url);
  const query = url.searchParams;
  const docs = query.get("printType").split(",");
  const orderId = query.get("orderId");
  const response = await admin.graphql(
      `query getOrder($orderId: ID!) {
      order(id: $orderId) {
        name
        createdAt
        totalPriceSet {
          shopMoney {
            amount
          }
        }
      }
    }`,
      {
        variables: {
          orderId: orderId,
        },
      }
    );
  const orderData = await response.json();
  const order = orderData.data.order;
  const pages = docs.map((docType) => orderPage(docType, order));
  const print = printHTML(pages);
  return cors(
    new Response(print, {
      status: 200,
      headers: {
        "Content-type": "text/html",
      },
    })
  );
}

function orderPage(docType, order) {
  const price = order.totalPriceSet.shopMoney.amount;
  const name = order.name;
  const createdAt = order.createdAt.split("T")[0];
  const email = "<!--email_off-->customerhelp@example.com<!--/email_off-->"
  const orderTemplate = `<main>
      <div>
        <div class="columns">
          <h1>${docType}</h1>
          <div>
            <p style="text-align: right; margin: 0;">
              Order ${name}<br>
              ${createdAt}
            </p>
          </div>
        </div>
        <div class="columns" style="margin-top: 1.5em;">
          <div class="address">
            <strong>From</strong><br>
            Top Quality Copper Ingots<br>
            <p>123 Broadway<br>
              Denver CO, 80220<br>
              United States</p>
            (123) 456-7891<br>
          </div>
        </div>
        <hr>
        <p>Order total: ${price}</p>
        <p style="margin-bottom: 0;">If you have any questions, please send an email to ${email}</p>
      </div>
    </main>`;
  return orderTemplate;
}

const title = `<title>My order printer</title>`;

function printHTML(pages) {
  const pageBreak = `<div class="page-break"></div>`;
  const pageBreakStyles = `
  @media not print {
        .page-break {
          width: 100vw;
          height: 40px;
          background-color: lightgray;
        }
      }
      @media print {
        .page-break {
          page-break-after: always;
        }
      }`;

  const joinedPages = pages.join(pageBreak);
  const printTemplate = `<!DOCTYPE html>
  <html lang="en">
  <head>
    <style>
      body,html {
        font-size: 16px;
        line-height: normal;
        background: none;
        margin: 0;
        padding: 0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      }
      body {
        font-size: 0.688rem;
        color: #000;
      }
      main {
        padding: 3rem 2rem;
        height: 100vh;
      }
      h1 {
        font-size: 2.5rem;
        margin: 0;
      }
      h2,h3 {
        font-size: 0.75rem;
        font-weight: bold;
      }
      h2,h3,p {
        margin: 1rem 0 0.5rem 0;
      }
      .address p {
        margin: 0;
      }
      b,strong {
        font-weight: bold;
      }
      .columns {
        display: grid;
        grid-auto-columns: minmax(0, 1fr);
        grid-auto-flow: column;
        word-break: break-word;
      }
      hr {
        clear: both;
        overflow: hidden;
        margin: 1.5em 0;
        border-top: 1px solid #000;
        border-bottom: none;
      }
      .header-row+.row {
        margin-top: 0px;
      }
      .header-row {
        display: none !important;
      }
      table,td,th {
        width: auto;
        border-spacing: 0;
        border-collapse: collapse;
        font-size: 1em;
      }
      td,th {
        border-bottom: none;
      }
      table.table-tabular,.table-tabular {
        border: 1px solid #e3e3e3;
        margin: 0 0 0 0;
        width: 100%;
        border-spacing: 0;
        border-collapse: collapse;
      }
      table.table-tabular th,
      table.table-tabular td,
      .table-tabular th,
      .table-tabular td {
        padding: 0.5em;
      }
      table.table-tabular th,.table-tabular th {
        text-align: left;
        border-bottom: 1px solid #e3e3e3;
      }
      table.table-tabular td,.table-tabular td {
        border-bottom: 1px solid #e3e3e3;
      }
      table.table-tabular tfoot td,.table-tabular tfoot td {
        border-bottom-width: 0px;
        border-top: 1px solid black;
        padding-top: 1em;
      }
      .row {
        margin: 0;
      }
      ${pageBreakStyles}
    </style>
    ${title}
  </head>
  <body>
    ${joinedPages}
  </body>
  </html>
  `;
  return printTemplate;
}
```

**📁 shopify.extension.toml** `/extensions/admin-print/shopify.extension.toml`
```toml
api_version = "2025-01"

[[extensions]]
name = "admin-print"
handle = "admin-print"
type = "ui_extension"

# Only 1 target can be specified for each admin print action extension
[[extensions.targeting]]
module = "./src/PrintActionExtension.jsx"
# The target used here must match the target used in the module file (./src/PrintActionExtension.tsx)
target = "admin.order-details.print-action.render"
```

**📁 PrintActionExtension.jsx** `/extensions/admin-print/src/PrintActionExtension.jsx`
```javascript
import { useEffect, useState } from "react";
import {
  reactExtension,
  useApi,
  AdminPrintAction,
  BlockStack,
  Checkbox,
  Text,
} from "@shopify/ui-extensions-react/admin";

// The target used here must match the target used in the extension's toml file (./shopify.extension.toml)
const TARGET = "admin.order-details.print-action.render";

export default reactExtension(TARGET, () => <App />);

function App() {
  // The useApi hook provides access to several useful APIs like i18n and data.
  const {i18n, data} = useApi(TARGET);
  const [src, setSrc] = useState(null);

  const [printInvoice, setPrintInvoice] = useState(true);
  const [printPackingSlip, setPrintPackingSlip] = useState(false);

  useEffect(() => {
    const printTypes = []
    if (printInvoice) {
      printTypes.push("Invoice");
    };
    if (printPackingSlip) {
      printTypes.push("Packing Slip");
    };

    if (printTypes.length) {
      const params = new URLSearchParams({
        printType: printTypes.join(','),
        orderId: data.selected[0].id
      });

      const fullSrc = `/print?${params.toString()}`;
      setSrc(fullSrc);

    } else {
      setSrc(null);
    }
  }, [data.selected, printInvoice, printPackingSlip]);

  return (
    <AdminPrintAction src={src}>
      <BlockStack blockGap="base">
        <Text fontWeight="bold">{i18n.translate('documents')}</Text>
        <Checkbox name="Invoice" checked={printInvoice} onChange={(value)=>{setPrintInvoice(value)}}>
          Invoice
        </Checkbox>
        <Checkbox name="Packing Slips" checked={printPackingSlip} onChange={(value)=>{setPrintPackingSlip(value)}}>
          Packing Slips
        </Checkbox>
      </BlockStack>
    </AdminPrintAction>
  );
}
```

## Next steps

**Action and block UI extensions**
Complete a tutorial series that describes how to build an UI extension for an issue tracker, using actions and blocks in Shopify admin.

**Extension targets**
Learn about the various places in Shopify admin where UI extensions can be displayed.

**Components**
Learn about the full set of available components for writing admin UI extensions.