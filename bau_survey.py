try : 
    from bs4 import BeautifulSoup


    import requests 


    # Set the login credentials and submit button
    # tbUser=F&tbPass=F&Button2=%D8%AF%D8%AE%D9%88%D9%84

    username = 'YOUR USERNAME'
    password = 'YOUR PASSWORD'
    button = 'دخول'


    s = requests.Session()
    url = "https://www.bau.edu.jo/UserPortal/UserProfile/Login.aspx"


    # Set the proxy address and port of Burp Suite
    proxy = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

    # Set the headers for the request (optional)
    headers = {'User-Agent': '0x1337team'}

    s.headers.update(headers)

    r = s.get(url, verify=False)
    # Extract the required cookies from the response
    cookies = r.cookies.get_dict()


    # Use Beautiful Soup to parse the HTML response and extract the values of the form fields
    soup = BeautifulSoup(r.text, 'html.parser')
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

    payload = {
        '__LASTFOCUS': '',
        '__VIEWSTATE':viewstate ,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': eventvalidation,
        
        'tbUser': username, 'tbPass': password, 'Button2' : button
        }

    r = s.post(url, data=payload, cookies=cookies, verify=False)


    # -------------------------------------------------------
    # login phase is done 
    # -------------------------------------------------------

    url = "https://www.bau.edu.jo/UserPortal/UserProfile/SurveyNew.aspx?sur_id=39"

    r = s.get(url, verify=False)

    soup = BeautifulSoup(r.text, 'html.parser')
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
    survey_elements = soup.find_all("input", {"name": lambda name: name and name.startswith("SurveyBlock1$")})
    names = [elem["name"] for elem in survey_elements]


    # get the number of survey
    n = names[-2].index('_')
    last_num = int(names[-2][n+1:])


    names = list(set(names))
    # add the new __View
    payload = {
        '__LASTFOCUS': '',
        '__VIEWSTATE':viewstate ,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': eventvalidation,
        
        }

    # we start from 2 here 
    for i in range(len(names)): 
        if 'submit' in names[i] : 
            payload.update({names[i] : 'أرسل+إختيارك'})
            continue
        payload.update({names[i] : [1]})

    r = s.post(url, data=payload, cookies=cookies, verify=False)
except Exception as e:
    print('[' + '\033[35m E \033[0m' + '] ' + str(e))