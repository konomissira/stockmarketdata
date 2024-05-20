import azure.functions as func
import logging
import requests
import os
import json

app = func.FunctionApp()

@app.route(route="FetchStockData", auth_level=func.AuthLevel.ANONYMOUS)
def fetch_stock_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    SYMBOL = req.params.get('symbol')
    if not SYMBOL:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SYMBOL = req_body.get('symbol')

    if SYMBOL:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if 'Time Series (Daily)' in data:
            return func.HttpResponse(
                json.dumps(data),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                f"Error fetching data: {data}",
                status_code=400
            )
    else:
        return func.HttpResponse(
            "Please pass a stock symbol on the query string or in the request body",
            status_code=400
        )
