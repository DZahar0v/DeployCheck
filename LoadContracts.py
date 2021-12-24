import json
import requests
import os

HTTP = requests.session()


class ClientException(Exception):
    message = 'unhandled error'
    def __init__(self, message=None):
        if message is not None:
            self.message = message


def getURL(address):
    url =  "https://api.etherscan.io/api"
    url += "?module=contract"
    url += "&action=getsourcecode"
    url += "&address=" + address
    url += "&apikey=Y4VHI8GSCYU1JWR4KKFVZC1VZUTG81N3Y6"
    return url


def connect(url):
    try:
        req = HTTP.get(url)
    except requests.exceptions.ConnectionError:
        raise ClientException

    if req.status_code == 200:
        # Check for empty response
        if req.text:
            data = req.json()
            status = data.get('status')
            if status == '1' or status == '0':
                return data
            else:
                raise ClientException
    raise ClientException


def getCode(jsonCode, fileName):
    code = jsonCode[0]['SourceCode']
    contractName = jsonCode[0]['ContractName']
    if (code == ''):
        print(fileName + ': not verified yet!')
        return code
    if (code.find('"content": "') == -1):
        return code
    # removing unnecessary braces
    code = code[1:-1]
    code = code.replace("\r", "")
    code = code.replace("\n", "")

    # Etherscan API send bad JSON
    index = code.find('"content": "')
    clearCode = ''
    while index != -1:
        clearCode += code[:index+12]
        code = code[index+12:]
        index2 = code.find('"    },')
        if (index2 == -1):
            index2 = code.find('"    }')
        tmpString = code[:index2]
        tmpString = tmpString.replace('\\"', "'")
        clearCode += tmpString
        code = code[index2:]
        index = code.find('"content": "')
    clearCode += code

    code = json.loads(clearCode)
    contractCode = ''
    for src in code['sources']:
        if (src.find(contractName) != -1):
            contractCode = code['sources'][src]['content']
            break
    return contractCode


if __name__ == "__main__":
    with open("Config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    
    dir = jsonObject['directory']
    addresses = jsonObject['addresses']

    isExist = os.path.exists(dir)
    if not isExist:
        os.makedirs(dir)

    for address in addresses:
        url = getURL(address[1])
        req = connect(url)
        code = getCode(req['result'], address[0])
        if (code == ''):
            continue
        file = open(dir + address[0] + '.sol', "w+")
        file.write(code)
        file.close()
        # File comparison
        print('Open: ' + address[0])
        etherscanCode = dir + address[0] + '.sol'
        githubCode = address[2]
        os.system('meld ' + etherscanCode + ' ' + githubCode)