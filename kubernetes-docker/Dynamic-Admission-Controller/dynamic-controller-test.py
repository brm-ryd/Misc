#!/usr/bin/python3

# test app for Dynamic Admission Controllers 
# kubernetes controller inspect all pod CREATE request for label dev & prod

import json
import os

from flask import jsonify, Flask, request

app = Flask(__name__)

@app.route('/', method=['POST'])

def validation():
    review = request.get_json()
    app.logger.info('Validating AdmissionReview request: %s', 
            json.dumps(review, indent=4))

    labels = review['request']['object']['metadata']['labels']
    response = {}

    msg = None
    if 'environment' not in list(labels):
        msg = "Every Pod requires an 'environment' label."
        response ['allowed'] = False
    elif labels['environment'] not in ('dev', 'prod',):
        msg = "'environment' must be one of 'dev' or 'prod'"
        response['allowed'] = False
    else:
        response['allowed'] = True

    status = {
            'metadata': {},
            'message': msg
            }
    response['status'] = status

    review['response'] = response
    return jsonify(review), 200

context = (
        os.environ.get('WEBHOOK_CERT', '/tls/webhook.crt'),
        os.environ.get('WEBHOOK_KEY', '/tls/webhook.key'),
        )

app.run(host='0.0.0.0', port='443', debug=True, ssl_context=context)
