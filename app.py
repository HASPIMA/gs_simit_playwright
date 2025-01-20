import json

from simit import RegistraduriaScraper


def lambda_handler(event, context):
    try:
        # Extract NUIP from the event - assuming API Gateway integration
        if 'body' in event:
            # Handle API Gateway event structure
            body = json.loads(event['body']) if isinstance(
                event['body'], str) else event['body']
            nuip = body.get('nuip')
        else:
            # Direct Lambda invocation
            nuip = event.get('nuip')

        if not nuip:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'NUIP is required'}, ensure_ascii=False),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        # Initialize scraper - always use headless in Lambda
        scraper = RegistraduriaScraper(headless=True)
        scraped_data = scraper.scrape(nuip)

        if not scraped_data:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No data found for the provided NUIP'}, ensure_ascii=False),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        # Convert scraped data to dictionary and return response
        response_data = scraped_data.__dict__
        return {
            'statusCode': 200,
            'body': json.dumps(response_data, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
