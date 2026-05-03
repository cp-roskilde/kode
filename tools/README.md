# PDF til Markdown Konverter (pdf2md.py)

Dette scriptværktøj konverterer automatisk en PDF-fil til en Markdown-fil (`.md`) og udtrækker samtidig alle billederne fra PDF'en.

Billederne bliver automatisk lagt i en undermappe kaldet `images`, og den resulterende fil bliver navngivet `README.md`, så den nemt kan blive vist korrekt på platforme som GitHub eller i kode-editorer.

## Hvordan man bruger værktøjet

For at konvertere en fil, skal du åbne en terminal (fx PowerShell eller kommandoprompt) og bruge `python` til at køre scriptet. Som parameter skal du angive stien til den PDF-fil, der skal konverteres.

**Generel kommando:**
```powershell
python tools\pdf2md.py "Stien\Til\Din\Fil.pdf"
```
> **Tip:** Husk altid at bruge anførselstegn (`""`) omkring stien, hvis der indgår mellemrum i mappenavnene eller i selve filnavnet.

**Eksempel på brug:**
```powershell
python tools\pdf2md.py "2025 Efterår\Grafisk\Bue og pil\Bue og pil.pdf"
```

### Resultatet efter konvertering
Hvis du konverterer en fil kaldet `Bue og pil.pdf`, vil mappen den ligger i, komme til at se sådan ud efter scriptet er kørt:

```
📁 Bue og pil/
 ├── 📄 Bue og pil.pdf     (Din originale fil)
 ├── 📄 README.md          (Den nye Markdown tekst)
 └── 📁 images/            (Mappen med alle udtrukne billeder)
```

## Forudsætninger
- Computeren skal have **Python** installeret.
- Scriptet benytter pakkerne `pymupdf4llm` og `pymupdf`. **Scriptet sørger dog automatisk selv for at installere disse via pip**, hvis de mangler på din maskine. Du behøver derfor ikke at installere noget manuelt.
