# Create cart permalinks

Cart permalinks take customers directly to a store cart or checkout with a pre-loaded cart. When you generate a cart permalink, you direct customers who want to buy a specific product from the sales channel directly to a merchant's store cart or checkout to complete the purchase. Cart permalinks work best for apps that enable customers to buy items from a single merchant.

You can use cart permalinks to apply one or more variant IDs to a cart or checkout, or append query parameters to the cart permalink URL to include additional information and attribute an order to your sales channel.

Building a sales channel with permalinks requires the lowest integration effort because your sales channel app doesn't need to sync orders, handle disputes, or manage refunds.

## What you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Create cart permalinks
- Modify the checkout
- Attribute an order to your sales channel
- Apply discounts
- Add conversion tracking information
- Redirect customers to the Online Store cart instead of checkout

## Limitations

- Selling plans don't work with cart permalinks
- Cart permalinks cannot bypass storefront passwords

## Scenario

You have a sales channel app from which you want to link directly to a merchant's checkout or their online store cart. You want your link to pre-load the cart with two specific products.

## Step 1: Create a cart permalink

Add product variant IDs and quantities to the shop URL.

```
http://{shop}.myshopify.com/cart/#{variant_id}:#{quantity}(,...)
```

The following example adds one each of two products to the cart by specifying the product variant IDs (70881412 and 70881382) with a quantity of one (1):

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1
```

## Step 2 (Optional): Add line item properties

You can add line item properties (up to 25) to the first product. Properties must be Base64 URL-encoded JSON.

For example, consider these line item properties:

```json
{"engraving": "Hello world", "color": "red"}
```

To configure the URL to automatically add these properties to the product, Base64 URL-encode the JSON string. Then, add the encoded string to the URL, as the value of the properties parameter:

```
https://{shop}.myshopify.com/cart/70881412:1?properties=eyJlbmdyYXZpbmciOiAiSGVsbG8gd29ybGQiLCAiY29sb3IiOiAicmVkIn0
```

## Step 3 (Optional): Modify the checkout

You can append checkout query parameters to the cart permalink URL.

The following example includes `[email]` and `[shipping_address]` as the checkout fields. `[shipping_address]``[city]` shows how you can use nesting to populate child fields.

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?checkout[email]=example@example.com&checkout[shipping_address][city]=thisismyhometown
```

### Supported checkout parameters

| Checkout parameter | Description |
|-------------------|-------------|
| `checkout[email]` | The email of the customer making the checkout |
| `checkout[shipping_address][first_name]` | The first name field for the shipping address |
| `checkout[shipping_address][last_name]` | The last name field for the shipping address |
| `checkout[shipping_address][address1]` | The address 1 field for the shipping address |
| `checkout[shipping_address][address2]` | The address 2 field for the shipping address |
| `checkout[shipping_address][city]` | The city field for the shipping address |
| `checkout[shipping_address][province]` | The province field for the shipping address |
| `checkout[shipping_address][country]` | The country field for the shipping address |
| `checkout[shipping_address][zip]` | The postal code field for the shipping address |

## Step 4 (Optional): Attribute an order to a sales channel

To attribute an order to a sales channel, you can add a storefront access token as an additional parameter to the permalink. Merchants can view sales attributions in the Sales by Channel report, which shows the name of the channel that the customer used to place the order. Sales attributions also appear on the sidebar in the Shopify admin.

You can specify a storefront access token in the cart permalink as shown in the following example:

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?access_token=#{access_token}
```

## Step 5 (Optional): Apply discounts

You can append a discount query parameter to apply discounts in the cart permalink URL, as shown in the following example:

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?discount={discount_code}
```

You can also append multiple discounts in the cart permalink URL, separated by a comma `,`:

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?discount={discount_code},{discount_code2}
```

**Note**
You can't pass discount codes that contain a comma, such as savings, today!, using the discount URL parameter.

## Step 6 (Optional): Add conversion tracking information

If you want to add conversion tracking information, then you can append one of the following query parameters to the cart permalink:

- `note`
- `attributes`
- `ref`

You can add multiple attributes parameters. `note` and `attributes` parameters will display in the Notes section on the order details page. The `ref` parameter will display as a referral code in the Conversion summary section on the details page.

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?note=came-from-newsletter-2022-01-01
```

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?attributes[from]=came-from-newsletter-2022-01-01&attributes[example]=example-value
```

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?ref=came-from-newsletter-2022-01-01
```

## Step 7 (Optional): Add the buyer's locale

You can include the buyer's locale in the permalink URL so that they land in a localized checkout. For example, if the buyer's locale is fr:

```
http://{shop}.myshopify.com/fr/cart/70881412:1,70881382:1
```

## Step 8 (Optional): Redirect to the cart instead of checkout

**Note**
This step is optional if you aren't building an app as a sales channel.

If you want the cart permalink to redirect customers to the online store cart instead of the checkout page, then you can append the storefront query parameter in the cart permalink URL:

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?storefront=true
```

## Step 9 (Optional): Send buyers into Shop Pay

To direct buyers to a Shop Pay checkout, add the `payment=shop_pay` parameter to the URL. For example:

```
http://{shop}.myshopify.com/cart/70881412:1,70881382:1?payment=shop_pay
```

## Next steps

Bill for your app