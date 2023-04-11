import discogs_client


d = discogs_client.Client('MyApp', user_token='ZxOYlSZlyJrjGopmaEoHzbwbdayDeqgcnLZaKbkY')


results = d.search('Duality', artist='Slipknot')
# vyhledání shody podle názvů umělce, skladby a alba


release = results[0]
#print(release.data.keys())
#print(release)

t = release.title
f = str(t)
f = f.split("-",1)
print(f[0])

print(release.title)
print("".join(release.genres))
print("Rok vydání: " + str(release.year))




