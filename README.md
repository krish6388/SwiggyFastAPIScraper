# 🛒 Swiggy Instamart Scraper API (FastAPI)

This is a FastAPI-based microservice that scrapes product listings from Swiggy Instamart for any given search query (e.g., milk, chocolate, bread). It simulates a browser session to fetch product name, brand, price, quantity, and image.

---

## 🧪 Running Locally

### 🔧 Prerequisites
- Python 3.8 or higher
- `pip` installed

---

### 🚀 Steps

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/swiggy-instamart-api.git
   cd swiggy-instamart-api
   ```

2. **Create and activate virtual environment (optional but recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**  
   ```bash
   uvicorn main:app --reload
   ```

5. **Test in browser or Postman**  
   Open this URL in your browser or Postman:
   ```
   http://127.0.0.1:8000/?query=milk
   ```

You should receive a JSON response with product listings scraped from Swiggy Instamart for your query.
