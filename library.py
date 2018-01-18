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

def cache(thing, tcache=None, key=None):
 if tcache is None:
  tcache=thing
 try:
  with open('{0}.cache'.format(tcache)) as a:
   b=json.load(a)
 except FileNotFoundError:
  with open('{0}.cache'.format(tcache),'w') as a:
   b=get(thing, key)
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
 return cache('user/mechbay',tcache='mechbay',key=key)

def renamemech(mech):
 loc='https://mwo.smurfy-net.de/api/data/user/mechbay.json'
 head={'Authorization':'APIKEY %s'%key}
 out=bytes(json.dumps(mech),'utf-8')
 d=r.put(loc, data=out, headers=head)
 return d.status_code==200

def addtobay(mechs):
 req=preplink(mechs)
 d=r.request('LINK',req[0],headers=req[1])
 return d.headers['links']

def removefrombay(mechs):
 req=preplink(mechs)
 d=r.request('UNLINK',req[0],headers=req[1])
 return d.headers['links']

def modifybay(mechs):
 reqin=preplink(mechs['add'])
 reqout=preplink(mechs['rem'])
 d1=r.request('LINK',reqin[0],headers=reqin[1])
 d2=r.request('UNLINK',reqout[0],headers=reqout[1])
 return d1.headers['links'].extend(d2.headers['links'])

def preplink(mechs):
 loc='https://mwo.smurfy-net.de/api/data/user/mechbay.json'
 loc2='</api/data/mechs/{0}/loadouts/{1}>'
 links=','.join([loc2.format(mech['mechid'],mech['id']) for mech in mechs])
 head={'Authorization':'APIKEY %s'%key,'Link':links}
 return (loc,head)

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