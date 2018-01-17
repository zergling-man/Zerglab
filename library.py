import requests as r
import json
import os
import glob

try:
 f=open('key')
 key=f.read()
 f.close()
except:
 key=None
 print("No key file found, assuming no key set")

def setkey(inp):
 global key
 key=inp
 with open('key','w') as f:
  f.write(inp)
 return True

def cache(thing):
 try:
  with open('{0}.cache'.format(thing)) as a:
   b=json.load(a)
 except FileNotFoundError:
  with open('{0}.cache'.format(thing),'w') as a:
   b=get(thing)
   a.write(json.dumps(b))
 return b

def resetcache():
 for file in glob.glob('*.cache'):
  os.remove(file)
 return True

def get(thing,key=None):
 loc='https://mwo.smurfy-net.de/api/data/%s.json'
 head={}
 if key is not None:
  head['Authorization']='APIKEY %s'%key
 with r.get(loc%thing,headers=head) as a:
  b=a.json()
 return b

def getprices():
 return get('prices')

def getmechs():
 return cache('mechs')

def getmech(id):
 if type(id)==type('a'):
  mechs=cache('mechs')
  return (mech for _,mech in mechs.items() if mech['name']==id).__next__()
 else:
  return mechc()[str(id)]

def getmodules():
 return cache('modules')

def getweapons():
 return cache('weapons')

def getammo():
 return cache('ammo')

def getpods():
 return cache('omnipods')

def getloadout(mechid,loadoutid):
 return get('mechs/{0}/loadouts/{1}'.format(mechid,loadoutid))

def getuser():
 return get('user/details',key)

def getbay():
 return get('user/mechbay',key)

def sendmech(mech):
 out=bytes(json.dumps(mech),'utf-8')
 loc='https://mwo.smurfy-net.de/api/data/mechs/%s/loadouts.json'
 head={'content-type':'application/json'}
 pre='loadouts/'
 post='.json'
 with r.post(loc%mech['mech_id'], data=out, headers=head) as a:
  give=a.text
  give=give[give.find(pre)+len(pre):give.find(post)]
  return give