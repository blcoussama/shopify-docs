# Start building for checkout

To get started with checkout UI extensions, Shopify Functions or web pixel extensions, you can use Shopify CLI, which generates starter code for building your extension and automates common development tasks.

The following is a lightweight guide for getting started to build. You can alternatively learn how to use the GraphQL Admin API to style checkout for a brand, such as changing the colors and corner radius settings on checkout form fields.

## Requirements

- You've created a Partner account.
- You've created a new development store. Depending on the extension type that you're generating, you might also need to enable the Checkout and Customer Accounts Extensibility developer preview.
- You're using the latest version of Shopify CLI.
- You're using the latest version of Chrome or Firefox.

## Language-specific requirements for writing Shopify Functions in Rust

- You've installed Rust.

On Windows, Rust requires the Microsoft C++ Build Tools. Make sure to select the Desktop development with C++ workload when installing the tools.

- You've installed the wasm32-wasip1 build target.

**Terminal**
```bash
rustup target add wasm32-wasip1
```

## Get started

1. Scaffold an app:

**Terminal**
```bash
shopify app init
```

2. Navigate to your app directory:

**Terminal**
```bash
cd <directory>
```

3. Run the following command to create a new extension:

**Terminal**
```bash
shopify app generate extension --name my-extension
```

4. Choose from one of the following extension types:

- Checkout UI
- Function (any of the sub-types)
- Post-purchase UI
- Web Pixel

5. Select a language for your extension.

For this quickstart, if you chose a Function extension type, then select either Rust or JavaScript.

6. Complete one of the following steps:

If you chose a Checkout UI, Post-purchase UI or Web Pixel extension type, then start your development server to build and preview your app:

**Terminal**
```bash
shopify app dev
```

Press p to open the developer console. In the developer console page, click on the preview link for your extension.

If you chose a Function extension type, then navigate to extensions/my-extension and build the function's Wasm module:

**Terminal**
```bash
cd extensions/my-extension
cargo build --target=wasm32-wasip1 --release
```

To test your function, you need to make it available to your development store. Learn more.

## Next steps

Learn how to use checkout UI and post-purchase extensions by following one of our use case tutorials.