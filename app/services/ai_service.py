import os
import requests

HEADER_DESCRIPTIONS = {
    'content-security-policy': 'Configure a suitable Content-Security-Policy to restrict browser resource loading.',
    'strict-transport-security': 'Configure Strict-Transport-Security when the API is served over HTTPS.',
    'x-frame-options': 'Configure X-Frame-Options to control whether the application can be embedded in frames.',
    'x-content-type-options': 'Configure X-Content-Type-Options, commonly with the value nosniff.',
    'referrer-policy': 'Configure a suitable Referrer-Policy to control referrer information.',
    'permissions-policy': 'Configure Permissions-Policy to restrict browser features the application does not need.'
}

def rule_based_ai(api_data):
    status = api_data.get('status', 0)
    score = max(0.0, min(10.0, float(api_data.get('security_score', 0) or 0)))
    missing = api_data.get('missing_security_headers', []) or []
    time_ms = float(api_data.get('time', 0) or 0)
    if score >= 9: level = 'Excellent'
    elif score >= 8: level = 'Strong'
    elif score >= 5: level = 'Moderate'
    else: level = 'Weak'
    if 200 <= int(status or 0) <= 299: status_text = 'The API request was successful.'
    elif 400 <= int(status or 0) <= 499: status_text = f'The API returned client-side HTTP status {status}.'
    elif int(status or 0) >= 500: status_text = f'The API returned server-side HTTP status {status}.'
    else: status_text = 'The HTTP status could not be classified.'
    fixes = [f'{h}: {HEADER_DESCRIPTIONS[h]}' for h in missing if h in HEADER_DESCRIPTIONS]
    if time_ms > 3000: fixes.append('Response time is high; investigate API/database performance.')
    return (f'Security Header Score: {score:.1f}/10\n'
            f'Security Level: {level}\nAPI Status: {status_text}\n'
            f'Security Issues: {", ".join(missing) if missing else "No configured security headers are missing."}\n'
            f'Recommended Fixes:\n' + ('\n'.join(fixes) if fixes else 'No security-header changes are required.') + '\n'
            f'Overall Assessment: {level} security-header configuration based on the configured checks.')

def analyze_with_ai(api_data):
    # Optional local Ollama integration; rule-based analysis remains available if Ollama is off.
    model = os.getenv('OLLAMA_MODEL', 'qwen2.5:0.5b')
    host = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:11434')
    prompt = f'''You are an API Security Expert. Analyze this API report and give a concise assessment.\n{api_data}\nReturn: security level, risks, missing headers, fixes, conclusion. Under 200 words.'''
    try:
        r = requests.post(f'{host}/api/chat', json={'model': model, 'stream': False,
            'messages': [{'role': 'user', 'content': prompt}]}, timeout=30)
        r.raise_for_status()
        data = r.json()
        text = data.get('message', {}).get('content')
        if text: return text
    except Exception:
        pass
    return rule_based_ai(api_data)
