import requests
import time
# from bs4 import BeautifulSoup

class SwiggyClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.cookies = {}

    def start_session(self):
        """
        This simulates a browser visit to swiggy.com and stores all cookies.
        """
        url = "https://www.swiggy.com/instamart"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()

        # Save cookies for reuse in later calls
        self.cookies.update(self.session.cookies.get_dict())

        return True

    # Helper function to get variations
    def get_variations(self, variation_lst):
        SWIGGY_IMAGE_BASE_URL = 'https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_252,h_272/'
        clean_variation_lst = []
        # print(len(variation_lst))
        for variation in variation_lst:
            try:
            # print(variation)
                clean_variation_obj = {}
                clean_variation_obj['quantity'] = variation['quantity']
                clean_variation_obj['price'] = {}
                clean_variation_obj['price']['mrp'] = variation['price']['mrp']
                clean_variation_obj['price']['store_price'] = variation['price']['store_price']
                clean_variation_obj['price']['offer_price'] = variation['price']['offer_price']
                image_ids = variation['images']
                clean_variation_obj['images'] = [f"{SWIGGY_IMAGE_BASE_URL}{img_id}" for img_id in image_ids]

                clean_variation_lst.append(clean_variation_obj)
            except Exception as e:
                print(f'Error in get_variations function: {e}')
        return clean_variation_lst


    # Helper function to get only necessary data
    def get_clean_obj(self, obj):
        try:
            clean_obj = {}
            clean_obj['brand'] = obj['brand']
            clean_obj['category'] = obj['category']
            clean_obj['product_name'] = obj['display_name']
            clean_obj['variations'] = self.get_variations(obj['variations'])
            return clean_obj
        except Exception as e:
            print(f'Error in get_clean_obj func: {e}')
            return {}

    
    # Function used to search products
    def search_products(self, query):
        """
        Performs a POST request to Instamart search API with current session
        """

        self.start_session()

        # Add more headers specific to the POST request
        headers = self.headers.copy()
        headers.update({
            "accept": "*/*",
            "content-type": "application/json",
            "referer": f"https://www.swiggy.com/instamart/search?query={query}",
            "origin": "https://www.swiggy.com",
            "x-build-version": "2.286.0"
        })


        payload = {
            "facets": {},
            "sortAttribute": ""
        }

        scraped_data_lst = []
        page = 0
        offset = 0
        limit = 40

        while True:
            time.sleep(1)
            params = {
                "pageNumber": str(page),
                "searchResultsOffset": str(offset),
                "limit": str(limit),
                "query": query,
                "ageConsent": "false",
                "pageType": "INSTAMART_SEARCH_PAGE",
                "isPreSearchTag": "false",
                "highConfidencePageNo": "0",
                "lowConfidencePageNo": "0",
                "voiceSearchTrackingId": "",
                "storeId": "",
                "primaryStoreId": "",
                "secondaryStoreId": ""
            }

            url = "https://www.swiggy.com/api/instamart/search"

            response = self.session.post(
                url,
                params=params,
                headers=headers,
                cookies=self.cookies,
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"Swiggy returned {response.status_code}")

            try:
                data = response.json()
                obj_lst = data['data']['widgets'][0]['data']
                print(f"🔍 Page {page}: {len(obj_lst)} items")

                if not obj_lst:
                    break  # stop when no more products are returned

                for obj in obj_lst:
                    scraped_data_lst.append(self.get_clean_obj(obj))

                page += 1
                offset += limit

            except Exception as e:
                print("⚠️ Error parsing page:", e)
                break

        return scraped_data_lst
        
# if __name__ == "__main__":
#     client = SwiggyClient()
#     query = input("Enter a search keyword (e.g., milk, bread): ").strip()
#     try:
#         results = client.search_products(query)
#         # for item in results:
#         #     print(f"{item['title']} - {item['brand']} - ₹{item['price']} - {item['weight']}")
#     except Exception as e:
#         print("❌ Error:", e)