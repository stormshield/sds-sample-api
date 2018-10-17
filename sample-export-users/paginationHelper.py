import functools

"""
    All methods are used to extract data from api Link header
    The Link header response includes pagination information and contains Hypermedia link relations.

    ex :
        Link: <https://sds.stormshieldcs.eu/api/v1/users?page=1>; rel="first",
              <https://sds.stormshieldcs.eu/api/v1/users?page=4>; rel="prev",
              <https://sds.stormshieldcs.eu/api/v1/users?page=6>; rel="next",
              <https://sds.stormshieldcs.eu/api/v1/users?page=10>; rel="last"
"""

def getInfoLink(stringHeaderLink):
    """Analyze one pagination link to extract information

    Input:
       stringHeaderLink: link string info (ex : <https://sds.stormshieldcs.eu/api/v1/users?page=1>; rel="first")
    return : an array with format [rel, url] (ex : ["first", "https://sds.stormshieldcs.eu/api/v1/users?page=1"])
    """
    OFFSET_REL = 5
    splitComma = stringHeaderLink.split('; ');
    return [ splitComma[1][OFFSET_REL: - 1], splitComma[0][1:- 1]];

def addlink(accumulator,linkData):
    """Add link information in json structure

    Input:
       accumulator: json who received new link
       linkData: one link with format [rel, url] (ex : ["first", "https://sds.stormshieldcs.eu/api/v1/users?page=1"])
    return : json containing new link (ex : {"first": "https://sds.stormshieldcs.eu/api/v1/users?page=1", "last": "https://sds.stormshieldcs.eu/api/v1/users?page=4"})
    """
    accumulator[linkData[0]] = linkData[1];
    return accumulator

def getNextPageUrl(response, pageCurrent):
    """get next url page if exists

    Input:
       response: api response
       pageCurrent: current url value (ex : "https://sds.stormshieldcs.eu/api/v1/users?page=1")
    return : next page url if exists else None)
    """
    # get header
    headers = response.headers
    # read all page links and generate json (format {'next' : url1, 'last': url2})
    filterLinks  = list(map(getInfoLink ,headers['Link'].split(', ')))
    jsonLink = functools.reduce(addlink, filterLinks, {})
    # analyse if it keeps one page to request
    if(jsonLink['next'] == jsonLink['last'] == pageCurrent):
        return None
    else:
        return jsonLink['next']
