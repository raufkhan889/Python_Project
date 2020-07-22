# this is google api project 
# modules
import urllib.request, urllib.parse, urllib.error 
import ssl 
import json 

# ignore ssl certification 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE 

# set api key for geo 
api_key = False 

if api_key is False :
  api_key = 42 
  geo = "http://py4e-data.dr-chuck.net/json?"

# empty dict 
dict = dict()

print("Hit Enter to end!")
# infinite loop 
while True :
  # get each time an address
  address = input("Enter Location: ")
  
  # enter to break the loop 
  if len(address) < 1 :
    break 
   
  # insert address into dict 
  dict["address"] = address 
  
  # now insert api key 
  if api_key is not False :
    dict["key"] = api_key 
    
  # encode address into url form 
  url = server + urllib.parse.urlencode(dict)
  print("URL:", url)
  
  # url oprn handle 
  handle = urllib.request.urlopen(url, context=ctx)
  # read into string and decode 
  data = handle.read().decode()
  
  # retrived data length 
  print("Retrieved length:", len(data), "characters")
  
  # try to load with json
  try :
    js = json.loads(data)
    print("==== Successfully load with JSON! ====")
  except:
    print("==== Failed to Load! ====")
    
  # if json status is ok 
  if "status" not in js or js["status"] != "OK" :
    print("==== Does not get Status ====")
    
  # getting the location address  
  place = js["results"][0]["formatted_address"]
  print("Location:", place)
  print("")
  
print("\n\nThank You!")
