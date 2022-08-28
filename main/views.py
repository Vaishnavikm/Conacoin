from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd 
import requests
from sklearn.neighbors import KNeighborsClassifier

from web3 import Web3
infura_url='https://mainnet.infura.io/v3/c0e47c38ff3740b59fd9ac1354e2a96a' 
w3 = Web3(Web3.HTTPProvider(infura_url))
# Create your views here.

knn = KNeighborsClassifier(n_neighbors=5)
data = pd.read_csv("/home/adhok/Hackathon/main/FinalData.csv")
x = ["TopHolding", "ContractRatio"]
y = ["scam"]
knn.fit(data[x], data[y])





def getTokenData(address):
     url = "https://api.ethplorer.io/getTopTokenHolders/"+address+"?apiKey=EK-cQTo5-YwMrjdS-9bY9u&limit=5"
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
         scam = knn.predict([[topShare,contractRatio]])
         if(scam == 1):
            jsonData["scam"] = scam
         jsonData["Address"] = address
         return(jsonData)

def home(request):
    if(request.method == "POST"):
        mAddress = request.POST["address"]
        if(w3.isAddress(mAddress)):
            #check if it is a contract 
            checkContractURL = "https://api.ethplorer.io/getAddressInfo/"+mAddress+"?apiKey=EK-cQTo5-YwMrjdS-9bY9u"
            result = requests.get(checkContractURL).json()
            if("tokenInfo" in result):
                x = getTokenData(mAddress)
                print(x)
                return(render(request, "token_details.html", x))
        return(render(request, "Home.html", {"message" : "Please give a ERC20 contract address"}))
        pass
    else:
        return(render(request, "Home.html"))
