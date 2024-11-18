import asyncio
import json
import requests
from requests.exceptions import RequestException

class GoatAPI:
    @staticmethod
    async def get_link(shoe, callback):
        url = "https://2fwotdvm2o-dsn.algolia.net/1/indexes/*/queries"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
            "Content-Type": "application/json",
        }
        params = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.25.1;react (16.9.0);react-instantsearch (6.2.0);JS Helper (3.1.0)",
            "x-algolia-application-id": "2FWOTDVM2O",
            "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a",
        }
        body = json.dumps({
            "requests": [{
                "indexName": "product_variants_v2",
                "params": f"distinct=true&maxValuesPerFacet=1&page=0&query={shoe['styleID']}&facets=%5B%22instant_ship_lowest_price_cents"
            }]
        })

        try:
            response = requests.post(url, headers=headers, params=params, data=body)
            response.raise_for_status()
            json_response = response.json()
            
            hits = json_response["results"][0]["hits"]
            if hits:
                first_hit = hits[0]
                lowest_price = first_hit["lowest_price_cents_usd"] / 100
                if lowest_price != 0:
                    shoe["lowestResellPrice"]["goat"] = lowest_price
                shoe["resellLinks"]["goat"] = f"http://www.goat.com/sneakers/{first_hit['slug']}"
                shoe["goatProductId"] = first_hit["product_template_id"]
            await callback()
        except RequestException as e:
            error_message = f"Could not connect to Goat while searching '{shoe['styleID']}'. Error: {e}"
            print(error_message)
            await callback(error_message)

    @staticmethod
    async def get_prices(shoe, callback):
        if not shoe.get("resellLinks", {}).get("goat"):
            await callback()
            return

        api_link = f"http://www.goat.com/web-api/v1/product_variants/buy_bar_data?productTemplateId={shoe['goatProductId']}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0",
            "Content-Type": "application/json",
        }
        price_map = {}

        try:
            response = requests.get(api_link, headers=headers)
            response.raise_for_status()
            json_response = response.json()
            
            for item in json_response:
                if item["shoeCondition"] == "used":
                    continue
                size = item["sizeOption"]["value"]
                price = item["lowestPriceCents"]["amount"] / 100
                if size in price_map:
                    price_map[size] = min(price_map[size], price)
                else:
                    price_map[size] = price
            
            shoe["resellPrices"]["goat"] = price_map
            await callback()
        except RequestException as e:
            error_message = f"Could not connect to Goat while fetching prices for '{shoe['styleID']}'. Error: {e}"
            print(error_message)
            await callback(error_message)

# Example usage
async def main():
    shoe = {
        "styleID": "example_id",
        "lowestResellPrice": {},
        "resellLinks": {},
        "resellPrices": {},
    }

    async def on_complete(err=None):
        if err:
            print("Error:", err)
        else:
            print("Shoe data:", shoe)

    await GoatAPI.get_link(shoe, on_complete)
    await GoatAPI.get_prices(shoe, on_complete)

# Run the example
asyncio.run(main())

