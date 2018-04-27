import os
import ssl

from library.content import app

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 18000))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.crt', 'server_secret.key')

    app.run(host=host, port=port, ssl_context=context)
