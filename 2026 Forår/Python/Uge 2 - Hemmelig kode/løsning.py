tekst = input("Skriv den tekst der skal gøres hemmelig: \n")

kode = {
   'a':  'n',
   'b':  'o',
   'c':  'p',
   'd':  'q',
   'e':  'r',
   'f':  's',
   'g':  't',
   'h':  'u',
   'i':  'v',
   'j':  'w',
   'k':  'x',
   'l':  'y',
   'm':  'z',
   'n':  'a',
   'o':  'b',
   'p':  'c',
   'q':  'd',
   'r':  'e',
   's':  'f',
   't':  'g',
   'u':  'h',
   'v':  'i',
   'w':  'j',
   'x':  'k',
   'y':  'l',
   'z':  'm'
}

resultat = ""

for tegn in tekst:
  if tegn in kode:
    tegn = kode[tegn]
  resultat = resultat + tegn

print(resultat)

print("Færdig")