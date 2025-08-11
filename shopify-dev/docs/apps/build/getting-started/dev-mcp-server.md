# Shopify Dev MCP server

Connect your AI assistant to Shopify's development resources. The Shopify Dev Model Context Protocol (MCP) server enables your AI assistant to search Shopify docs, explore API schemas, build Functions, and get up-to-date answers about Shopify APIs.

## How it works

Your AI assistant uses the MCP server to read and interact with Shopify's development resources:

1. Ask your AI assistant to build something or help with Shopify development tasks.

2. The assistant searches Shopify documentation and API schemas based on your prompt.

3. The MCP server gives your AI assistant access to Shopify's development resources, so it can provide accurate code, solutions, and guidance based on current APIs and best practices.

## Requirements

Before you set up the Dev MCP server, make sure you have:

- Node.js 18 or higher installed on your system.
- An AI development tool that supports MCP, such as Cursor or Claude Desktop.

## What you can ask your AI assistant

After you set up the MCP server, you can ask your AI assistant questions like:

- "How do I create a product using the Admin API?"
- "What fields are available on the Order object?"
- "Show me an example of a webhook subscription"
- "How do I authenticate my Shopify app?"
- "What's the difference between Admin API and Storefront API?"

Your AI assistant will use the MCP server to search Shopify's documentation when providing responses.

## Supported APIs

The MCP server provides tools to interact with the following Shopify APIs:

- Admin GraphQL API
- Functions
- Polaris Web Components (optional)

## Set up the server

The server runs locally in your development environment and doesn't require authentication.

### Step 1: Run the server

Open a new terminal window and run the following command. Keep this terminal window open while using the server:

**Terminal**
```bash
npx -y @shopify/dev-mcp@latest
```

### Step 2: Configure your AI development tool

Add configuration code that tells your AI tool how to connect to and use the Dev MCP server. This configuration enables your AI assistant to automatically access Shopify documentation, API schemas, and development guidance when you ask questions.

#### Cursor

Open Cursor and go to **Cursor > Settings > Cursor Settings > Tools and integrations > New MCP server**.

Add this configuration to your MCP servers:

**Cursor configuration**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"]
    }
  }
}
```

**Note:** For more information, see the Cursor MCP documentation.

If you see connection errors on Windows, try this alternative configuration:

**Alternative configuration for Windows**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "cmd",
      "args": ["/k", "npx", "-y", "@shopify/dev-mcp@latest"]
    }
  }
}
```

#### Claude Desktop

Open Claude Desktop and access your configuration file through settings.

Add this configuration to your MCP servers section:

**Claude Desktop configuration**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"]
    }
  }
}
```

**Note:** For more information, read the Claude Desktop MCP guide.

Save your configuration and restart your AI development tool.

### Step 3: (Optional) Configure advanced options

The Dev MCP server supports several advanced configuration options:

#### Disable instrumentation

This package makes instrumentation calls to better understand how to improve the MCP server. To disable them, set the OPT_OUT_INSTRUMENTATION environment variable in Cursor or Claude Desktop:

**Disable instrumentation**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"],
      "env": {
        "OPT_OUT_INSTRUMENTATION": "true"
      }
    }
  }
}
```

#### Enable Polaris support (experimental)

To show Polaris Web Components documentation in Cursor or Claude Desktop, add an env block with the POLARIS_UNIFIED flag to your MCP server configuration:

**Enable Polaris support**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"],
      "env": {
        "POLARIS_UNIFIED": "true"
      }
    }
  }
}
```

**Beta:** This is a developer preview of Polaris Web Components. This documentation will be updated as we release new features.

## Available tools

The Dev MCP server provides the following tools:

| Tool Name | Description | When to Use |
|-----------|-------------|-------------|
| learn_shopify_api | Get up-to-date guidance on supported Shopify APIs and how to use this MCP server's tools effectively. Provides context about which API to use for your specific needs. | Automatically invoked first when you ask about Shopify APIs. It provides essential context about supported APIs and generates a conversation ID for tracking usage across tool calls. |
| search_docs_chunks | Search across all shopify.dev documentation to find relevant information. Returns content from multiple documentation sections, but may have incomplete context due to chunking. | This tool is invoked when you ask broad questions or when the assistant needs to find relevant information across multiple documentation sections. This tool searches through grouped content that allows for better token matching within smaller content pieces, but may miss some context from individual pages. |
| fetch_full_docs | Get complete documentation for specific shopify.dev pages. Provides full context without information loss. Requires the exact documentation path. | Used when complete documentation is needed for a specific API resource and the exact path is known (for example, /docs/api/admin-rest/resources/product). This provides full context without any information loss from chunking. |
| introspect_admin_schema | Search and explore the Shopify Admin API GraphQL schema to understand available types, fields, queries, and mutations. | Invoked when you ask about GraphQL schema structure, available fields, or API capabilities. |

## Related resources

**Shopify CLI**
Command-line tool for building Shopify apps and themes.

**Storefront MCP**
Connect AI assistants to real-time commerce data for customer-facing shopping experiences.

**Shopify dev MCP**
Source code and documentation for the Shopify Dev MCP server.