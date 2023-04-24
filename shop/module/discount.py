def getdiscount(discount,amount):
   if amount > 1000:
      return round((amount*(discount/100)),2)
   else:
      return 0