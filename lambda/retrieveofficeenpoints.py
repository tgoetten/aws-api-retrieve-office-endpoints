import json
import urllib.request
import uuid

def webApiGet(methodName, instanceName, clientRequestId):
    ws = "https://endpoints.office.com"
    requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
    request = urllib.request.Request(requestPath)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())

def retrieveOfficeEndpoints(iptype):
    clientRequestId = str(uuid.uuid4())
    # invoke endpoints method to get the new data
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])
    flatIps4 = []
    flatIps6 = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            # IPv4 strings have dots while IPv6 strings have colons
            ip4s = [ip for ip in ips if '.' in ip]
            ip6s = [ip for ip in ips if ':' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps4.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])
            flatIps6.extend([(category, ip, tcpPorts, udpPorts) for ip in ip6s])

    flat_list_of_ipsv4 = (' \n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps4]))))
    flat_list_of_ipsv6 = (' \n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps6]))))
    if iptype == 'ipv6':
        return flat_list_of_ipsv6
    else: 
        return flat_list_of_ipsv4

def handler(event, context):
    
    if event['path'] == '/ipv6':
        body= '{}\n'.format(retrieveOfficeEndpoints('ipv6'))
    else:
        body= '{}\n'.format(retrieveOfficeEndpoints('ipv4'))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': body
    }