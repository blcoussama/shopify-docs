# Apps in admin

The Shopify admin is where users configure their stores and manage their businesses. Integrating your app with the admin gives users functionality that feels familiar and can be easily found.

This guide explains the different ways that you can use Shopify Extensions to integrate your app with the Shopify admin.

## App home

The primary place where users engage with your app is its app home. This is the location where merchants are directed when they navigate to your app in Shopify.

The Shopify admin provides a surface for apps to render the UX for their app home. On the web, the surface is an iframe and in the Shopify mobile app, the surface is a WebView.

A diagram that shows the Shopify admin. The screenshot highlights an app home. The app navigation is rendered directly in the Shopify admin navigation.

By combining Shopify App Bridge and Polaris React, you can make your app display seamlessly in the Shopify admin. Polaris React enables apps to match the visual appearance of the admin by using the same design components. App Bridge enables apps to communicate with the Shopify admin and create UI elements outside of the app's surface. Such elements include navigation menus, modals that cover the entire screen, and contextual save bars that prevent users from navigating away from the page when they have unsaved changes.

When you're building your app home, follow the App Design Guidelines and the admin performance best practices to ensure that you create a great experience for users.

## UI extensions in admin

To display a user interface in Shopify admin, apps can include UI extensions. Shopify admin can display three types of UI extensions: admin actions, action print actions, and admin blocks.

### Admin actions

Admin actions are powered by UI extensions and enable your app to embed transactional workflows that display as modals. These UI extensions let users interact with your app directly from key pages of the Shopify admin, such as the Products, Customers, and Orders pages. You can also create UI extensions that become available when users select multiple resources in an index table, for example, selecting multiple products on the Products index page.

An example admin action UI extension displaying as a modal on the Products page of the Shopify admin, with fields for merchants to input data.

### Admin print actions

Admin print actions are a special form of UI extension designed to let your app print documents from key pages in the Shopify admin. Unlike a typical admin actions, these UI extensions are found under the Print menu on orders and product pages. Additionally, they contain special APIs to let your app display a preview of a document and print it.

An example admin print action UI extension.

### Admin blocks

Admin block UI extensions let your app embed contextual experiences that display as cards on key pages of the admin, such as the Products, Customers, and Orders pages. Blocks enable your app to persistently display relevant information to users. They also let users edit your app's data and other product data. After admin block UI extensions are built and deployed, users have the option to add your app's block to resource pages and edit its location on the pages.

An example admin block UI extension.

## Admin link extensions

Admin link extensions create links from resource pages in the Shopify admin to related pages of your app. You should use them sparingly because they have the potential to disrupt user workflows with slow, full-page navigations.

## Developer tools and resources

**Shopify App Bridge**
A JavaScript library that lets you embed app pages in the Shopify admin.

**Polaris React design system**
Design patterns and a library of UI components, tokens, and icons to build app home pages.

**App Design Guidelines**
Directives to show you what great Shopify apps look like and how they're crafted.

**Performance best practices**
A set of best practices for building fast and responsive apps in the Shopify admin.

## Next steps

Create an app home page in the Shopify admin.