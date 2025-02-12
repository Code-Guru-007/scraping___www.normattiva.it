import sys
import urllib.request
import ssl
import urllib.parse

encoded_url = "https://www.italgiure.giustizia.it/xway/application/nif/clean/hc.dll%3Fverbo%3Dattach%26db%3Dsnpen%26id%3D./20250206/snpen@s70@a2025@n04976@tO.clean.pdf"
decoded_url = urllib.parse.unquote(encoded_url)

# print("Decoded URL:", decoded_url)


# Create an unverified SSL context (disables SSL verification)
context = ssl._create_unverified_context()

if sys.version_info[0] == 3:
    # Create an opener with a proxy
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({
            'http': 'http://brd-customer-hl_79944553-zone-residential_proxy1:b53is0s89h7v@brd.superproxy.io:33335',
            'https': 'http://brd-customer-hl_79944553-zone-residential_proxy1:b53is0s89h7v@brd.superproxy.io:33335'
        })
    )

    # Install opener as the default opener
    urllib.request.install_opener(opener)

    # Open the URL using urlopen with SSL context
    response = urllib.request.urlopen(decoded_url, context=context)

    print(response.read())
