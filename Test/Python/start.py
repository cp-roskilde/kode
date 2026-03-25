# Denne lille fil viser hvordan man kører et Python program
# og hvordan man "debugger" det (undersøger det undervejs)
#
# 1) Prøv først at køre dette program ved at trykke F5
# 2) Prøv herefter at stå på linjen print(besked), tryk F9 og så F5
#    Skift til Run ude til venstre. Se at besked får en værdi
# 3) Prøv herefter at stå på linjen i = i + 1, tryk F9 og så F5
#    Skift til Run ude til venstre. Se at i tæller en op hver gang
#
# Du har nu lært at køre et program og kan også "debugge" det 🥳

besked = "Mit allerførste program kører nu"
print(besked)

i = 0
while i < 5:
    print(f"  i er nu {i}")
    i = i + 1

print(f"Nu programmet færdigt! i er nu {i}")