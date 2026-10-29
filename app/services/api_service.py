import requests

SECURITY_HEADERS = [
    'content-security-policy', 'strict-transport-security', 'x-frame-options',
    'x-content-type-options', 'referrer-policy', 'permissions-policy'
]
ALLOWED_METHODS = {'GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS'}

def analyze_api(url: str, method: str = 'GET'):
    method = method.upper().strip()
    if method not in ALLOWED_METHODS:
        return {'error': f'Unsupported HTTP method: {method}'}
    try:
        response = requests.request(method=method, url=url, timeout=10)
        response_time = response.elapsed.total_seconds() * 1000
        headers = {k.lower(): v for k, v in response.headers.items()}
        content_type = headers.get('content-type', '')
        try:
            body = response.json()
        except ValueError:
            body = response.text[:200000]
        present = [h for h in SECURITY_HEADERS if h in headers]
        missing = [h for h in SECURITY_HEADERS if h not in headers]
        total = len(SECURITY_HEADERS)
        score = round(len(present) / total * 10, 1) if total else 0
        missing_pct = round(len(missing) / total * 100, 2) if total else 0
        return {'status': response.status_code, 'time': response_time,
                'content_type': content_type, 'headers': headers, 'body': body,
                'security_score': score, 'present_security_headers': present,
                'missing_security_headers': missing,
                'missing_header_percentage': missing_pct}
    except requests.exceptions.Timeout:
        return {'error': 'API request timed out.'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Unable to connect to the API.'}
    except requests.exceptions.InvalidURL:
        return {'error': 'Invalid API URL.'}
    except requests.exceptions.RequestException as e:
        return {'error': f'API request failed: {e}'}
    except Exception as e:
        return {'error': f'API analysis failed: {e}'}
