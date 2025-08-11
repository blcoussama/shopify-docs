# About admin UI extensions

UI extensions enable you to seamlessly integrate your app's functionality into the Shopify admin using blocks and actions. These UI extensions enable your app to embed workflows and UX on core admin pages while automatically matching the Shopify admin's look and feel. By giving merchants access to your app's functionality, without the need to navigate away from their current task, these UI extensions help merchants be more efficient and productive.

You can create UI extensions for actions and blocks by using UI Extensions and targeting the appropriate extension target. For the full list of admin pages that you can extend, refer to the extension target reference.

## Admin actions

Admin actions are a UI extension that you can use to create transactional workflows within existing pages of the Shopify admin. Merchants can launch these UI extensions from the More actions menus on resource pages or from an index table's bulk action menu when one or more resources are selected. After the UI extensions are launched, they display as modals. After they're closed, the page updates with the changes from the action.

An example admin action UI extension.

## Admin print actions

Admin print actions are a special form of UI extension designed to let your app print documents from key pages in the Shopify admin. Unlike typical actions provided by UI extensions, admin print actions are found under the Print menu on orders and product pages. Additionally, they contain special APIs to let your app display a preview of a document and print it.

An example admin print action UI extension.

## Admin blocks

Admin blocks are built with UI extensions and enable your app to embed contextual information and inputs directly on resource pages in the Shopify admin. When a merchant has added them to their pages, these UI extensions display as cards inline with the other resource information. Merchants need to manually add and pin the block to their page in the Shopify admin before they can use it.

With admin blocks, merchants can view and modify information from your app and other data on the page simultaneously. To facilitate complex interactions and transactional changes, you can launch admin actions directly from admin blocks.

An example admin block UI extension on the product page showing created issues.

## Getting started

Follow the getting started tutorials to learn how to build UI extensions that display as admin action and admin blocks. These tutorials are designed to be completed together to illustrate how UI extensions complement one another, and how admin blocks and admin actions can be used together to build features for your app.

**Learn how to build an admin action**
Build a UI extension with an action that enables merchants to create tracked issues for their products.

**Learn how to build an admin block**
Build a UI extension with a block that enables merchants to see and manage tracked issues for their products.

**Learn to connect admin UI extensions**
Modify the admin actions and admin blocks for issue tracking so merchants can edit existing tracked issues for their products.

**Learn to connect UI extensions to your backend**
Enable the UI extension's admin action to fetch data from an app's backend when creating new issues.

**Learn to conditionally hide admin UI extensions**
Collapse the admin block and hide the admin action from the More actions menu when they aren't relevant.

**Learn how to enable printing from resource pages**
Create a UI extension that prints order invoices.

## Developer tools and resources

**Admin UI extensions API reference**
Consult the API reference for admin UI extension targets and their respective types.

**Components for admin UI extensions**
Learn about the components that are available in admin UI extensions.

**Admin UI extension targets**
Learn about the locations where you can create admin UI extensions.

**Extension configuration**
Learn about how to configure your extension from its .toml file.

**Design guidelines for admin apps**
Learn the design guidelines for building apps in the Shopify admin.

**Admin extensions UI kit**
The Figma UI kit contains components, screens, and examples to help you build and understand admin UI extensions.

## Next steps

Learn how to build an admin action extension that enables merchants to create tracked issues for their products directly from the product details page.