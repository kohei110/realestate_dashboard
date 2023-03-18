import requests

ZILLOW_API_KEY = 'your_zillow_api_key_here'
SEARCH_REGION = 'Texas'

def get_search_results(api_key, region):
    url = f'http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id={api_key}&state={region}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f'Error: {response.status_code}')

def parse_data(xml_data):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)

    results = []
    for region in root.findall('.//response/list/region'):
        name = region.find('name').text
        zindex = region.find('zindex').text if region.find('zindex') is not None else None
        rentzestimate = region.find('rentzestimate').text if region.find('rentzestimate') is not None else None
        results.append({
            'name': name,
            'zindex': zindex,
            'rentzestimate': rentzestimate
        })

    return results

def main():
    xml_data = get_search_results(ZILLOW_API_KEY, SEARCH_REGION)
    results = parse_data(xml_data)

    print('Housing prices and expected rent revenues in Texas:')
    for result in results:
        print(f"{result['name']} - Housing Price: ${result['zindex']} | Expected Rent Revenue: ${result['rentzestimate']}")

if __name__ == '__main__':
    main()