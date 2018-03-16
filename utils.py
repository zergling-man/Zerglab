import string as st

strawlist={'weapons':['name','translated_name'], 'mechs':['name','family','chassis_translated','translated_name','translated_short_name'], 'modules':['name','translated_name']}

def dealias(alias,dict):
 for name,aliases in dict.items():
  if alias in aliases:
   return name
 return False

def strip(strong):
 return ''.join(a for a in strong.lower() if a in st.digits+st.ascii_lowercase)

def lookup(needle,haystack,straws=['name']):
 if type(needle)==type(0):
  return haystack[str(needle)]
 else:
  needle=strip(needle)
  return [bale for _,bale in haystack.items() if needle in [strip(bale[val]) for val in straws]]