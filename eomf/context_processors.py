def gmaps(request):
    """
    Pulls the Google Maps API key depending on the current domain.
    """
    domain2key = {
        'eomf-dev.ou.edu': 'ABQIAAAAmuvLtH3m9h8LpbkjVzUDhBSlwqE0rvKpWCh5bR7kcxcL-uObnhSHmmW2v_NFLCrqvDPPFWGybhFjfA',
        'eomf.ou.edu': 'ABQIAAAAmuvLtH3m9h8LpbkjVzUDhBThC4sbWo1IQHfoXctdcTSR5grrVRTjCdvcyEjcREzUOUuAagcw3aC53g',
        'www.eomf.ou.edu': 'ABQIAAAAE7jH76TvSwj2EbGtTFztGBSZQPaKzcJUNBmscSu8lUTMp7T2MxRd9I3aSZGU4Qk1Ibht_Cu0cZYCqQ',
    }
    try:
        server_name = request.META['HTTP_HOST']
        key = domain2key[server_name]
    except KeyError:
        key = domain2key['www.palewire.com']

    return {'gmaps_api_key': key }

