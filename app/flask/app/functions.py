import requests,json,base64


def api_request(totemo_username, totemo_password, method, url):

    #Generate Basic Auth String
    basic_auth = (f"{totemo_username}:{totemo_password}").encode('ascii')
    basic_auth = base64.b64encode(basic_auth)
    basic_auth = basic_auth.decode('ascii')
    if (method == "GET"):
        req_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json', 'cache-control' : 'no-cache', 'Authorization' : f"Basic {basic_auth}" }
        r=requests.get(f"{url}",headers=req_headers,verify=False)
        if (r.status_code ==403):
            print("Wrong Username or Password / HTTP Fehler 403")
        output=json.loads(r.text)
        
        return output

    if (method == "POST"):
        req_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/octet-stream', 'cache-control' : 'no-cache', 'Authorization' : f"Basic {basic_auth}" }
        r=requests.post(f"{url}",headers=req_headers,verify=False)
        return r


def get_pubkey(keytype, email, totemo_username, totemo_password, totemo_baseurl):
    user_pubkeys=api_request(totemo_username, totemo_password, "GET",f"{totemo_baseurl}/api/v1/certificate?type=User&subject={email}&limit=100")
    if len(user_pubkeys) == 0: #If no public key is found for the user, exit function
        return None


    selected_pubkeys=[]
    for key in user_pubkeys:
        if (key['type'] == keytype): #Check if key is smime or pgp, and filter for selection
            selected_pubkeys.append(key) 

    if (keytype == "smime"):
        mostRecentPubKey = max(selected_pubkeys, key=lambda x:x['validFrom']) #If there is more than one public key, select the most recent one from totemo. (validFrom closest to the current date)
        request=api_request(totemo_username, totemo_password, "POST",f"{totemo_baseurl}/api/v1/certificate/download/public?certificateId={mostRecentPubKey['id']}")
        open(f"./cert/{email}_keyID_{mostRecentPubKey['id']}.cer", 'wb').write(request.content)
        return f"{email}_keyID_{mostRecentPubKey['id']}.cer"

    if(keytype == "pgp"):
        mostRecentPubKey = max(selected_pubkeys, key=lambda x:x['validTo']) #Totemo returns for PGP keys as "validFrom" attribute always none (why???), so we have to use the "validTo" to find the longest expiration date / most recent certificate
        request=api_request(totemo_username, totemo_password, "POST",f"{totemo_baseurl}/api/v1/certificate/download/public?certificateId={mostRecentPubKey['id']}")
        open(f"./cert/{email}_keyID_{mostRecentPubKey['id']}.asc", 'wb').write(request.content)
        return f"{email}_keyID_{mostRecentPubKey['id']}.asc"