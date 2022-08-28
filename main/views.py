from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd 


from web3 import Web3
infura_url='https://mainnet.infura.io/v3/c0e47c38ff3740b59fd9ac1354e2a96a' 
w3 = Web3(Web3.HTTPProvider(infura_url))
# Create your views here.





def getTokenData(address):
     url = "https://api.ethplorer.io/getTopTokenHolders/"+address+"?apiKey=EK-cQTo5-YwMrjdS-9bY9u&limit=50"
     jsonData = requests.get(url).json()
     if "error" not in jsonData:
         topShare = 0
         for j in jsonData['holders']:
             topShare += j['share']
         contractShare = 0
         for j in jsonData['holders']:
             holder = j["address"]
             checkContractURL = "https://api.ethplorer.io/getAddressInfo/"+holder+"?apiKey=EK-cQTo5-YwMrjdS-9bY9u"
             result = requests.get(checkContractURL).json()
             if("tokenInfo" in result):
                 contractShare += j["share"]
             # Check if address is contract and add share of it to the contractShare
         contractRatio = contractShare / topShare
         scam = knn.predict([contractRatio, topShare])
         jsonData["scam"] = scam
         # put contractRatio to jsonData
         return(jsonData)

def home(request):
    if(request.method == "POST"):
        address = request.POST["address"]
        if(w3.isAddress(address)):
            #check if it is a contract 
            checkContractURL = "https://api.ethplorer.io/getAddressInfo/"+address+"?apiKey=EK-cQTo5-YwMrjdS-9bY9u"
            result = requests.get(checkContractURL).json()
            if("tokenInfo" in result):
                x = getTokenData(address)
                y = knn.predict(x)


        return(render(request, "Home.html", {"message" : "Please give a ERC20 contract address"}))
        pass
    else:
        return(render(request, "Home.html"))
