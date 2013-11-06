t=lambda J,m,q,h: int(q+(m+((m<=2)*12)+1)*26/10+((J%h)-(m<=2))*1.25-1.75*(J/100)-0.5)%7
w=['itdssmdmdf', 'moaaooiior', 'pdtmnnetne', 'oaesntntni', 'rytttaswet', 't iaagtora', '  mgg acsg', '  e   ght ', '        a ', '        g ']
s=lambda x,i:x[sum([0,6,5,8,7,7,6,8,8,10,7][0:i]):sum([0,6,5,8,7,7,6,8,8,10,7][0:i+1])];p={}
w=''.join(w)
for i in range(len(w)):
	p.setdefault((i)%10,[]).append(w[i])
w = ''.join([''.join(p[x]) for x in p]).replace(' ','')
m="%s"%s(w,1)
exec "%s"%s(w,1)+" %s"%s(w,3)
c=(("%s"%s(w,3)))+(".%s."%(s(w,3))[:4])+"%s"%s(w,2)
h=(len(c)+1)*5
c=eval(c)
print "%s"%("%s"%s(w,t(*tuple([int(x) for x in tuple(c.__call__().__str__().split("-"))]+[h]))+4).title())

"""
import datetime
def zeller(datum):
	jahr, monat, tag = [int(x) for x in str(datum).split("-")]
	jahrhundert = jahr / 100
	jahr = jahr % 100
	if monat <= 2:
		monat = monat + 12
		jahr = jahr - 1
		if jahr == 99:
			jahrhundert = jahrhundert - 1
	gregorianisch = tag + (monat + 1) * 26/10 + jahr + jahr / 4 + jahrhundert / 4 - 2 * jahrhundert
	return gregorianisch % 7

wochentage = ["Samstag", "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

datum = datetime.date.today()
print wochentage[zeller(datum)]
"""
