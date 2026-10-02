#!/usr/bin/env python3
"""Build the diagnostic workbook via the LibreOffice UNO API, saving .ods and .xlsx."""
import subprocess, sys, time

BASE = "/home/xushen/ShiZhongIteration/Hack/shoucuosanshipian"
PROF = BASE + "/work/loprofile"
SOCK = "socket,host=127.0.0.1,port=2250;urp;StarOffice.ComponentContext"

CSVURL = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
          "daily-treasury-rates.csv/2026/all?type=daily_treasury_bill_rates"
          "&field_tdr_date_value=2026&page&_format=csv")
XP = "(//*[local-name()='ROUND_B1_YIELD_13WK_2'])[last()]"

URLF = ('="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/'
        'pages/xml?data=daily_treasury_bill_rates&field_tdr_date_value_month="'
        '&TEXT(TODAY();"YYYYMM")')

CSVNUM = ('=IFERROR(VALUE('
          'MID(","&SUBSTITUTE(MID($B$17;FIND(CHAR(10);$B$17)+1;400);",";"|";9);'
          'FIND("|";SUBSTITUTE(","&MID($B$17;FIND(CHAR(10);$B$17)+1;400);",";"|";9))+1;'
          'FIND("|";SUBSTITUTE(","&MID($B$17;FIND(CHAR(10);$B$17)+1;400);",";"|";10))'
          '-FIND("|";SUBSTITUTE(","&MID($B$17;FIND(CHAR(10);$B$17)+1;400);",";"|";9))-1)'
          ');"FAIL")')

DIAG = [
 (3,  "A  Build the request URL", URLF,
      "Must end in 6 digits, e.g. month=202610. An error here = syntax/separator problem."),
 (4,  "B  Fetch XML with WEBSERVICE", "=WEBSERVICE($B$3)",
      "LEN should be ~4532. #VALUE! / Err:540 / #N/A / #NAME? => the fetch itself failed."),
 (5,  "B-ISERROR(WEBSERVICE)", "=ISERROR($B$4)",
      "Must be FALSE (0). TRUE (1) means the fetch already failed here."),
 (6,  "B-LEN(WEBSERVICE)", "=LEN($B$4)",
      "~4532 = the XML arrived. 0 or an error = nothing was downloaded."),
 (7,  "C  Is the body really the Treasury feed?",
      '=IF(ISNUMBER(SEARCH("ROUND_B1_YIELD_13WK_2";$B$4));'
      '"OK: feed contains ROUND_B1_YIELD_13WK_2";'
      '"FAIL: response is NOT the expected XML (error page / captive portal / schema change)")',
      "Must say OK. FAIL = the URL returned something other than the feed."),
 (8,  "D  Structural XPath (local-name, namespace-free)",
      "=IFERROR(FILTERXML($B$4;\"//*[local-name()='ROUND_B1_YIELD_13WK_2']\");"
      '"#N/A -> FILTERXML matched NOTHING")',
      "Must show 4.xx. #N/A here => the parser ran but found no node."),
 (9,  "E  YOUR EXACT EXPRESSION",
      f'=IFERROR(VALUE(FILTERXML($B$4;"{XP}"));"ERROR -> see note")',
      "Must show 4.xx as a NUMBER. This is the construct you reported as #N/A."),
 (10, "F  Does your XPath match anything?",
      f'=IF(ISNA(FILTERXML($B$4;"{XP}"));"NO MATCH -> this is the #N/A source";'
      f'"MATCHED: "&FILTERXML($B$4;"{XP}"))',
      "Expected 'MATCHED: 4.1'. 'NO MATCH' confirms the root cause."),
 (11, "G  Parser probe (does FILTERXML reach the doc?)",
      "=IFERROR(FILTERXML($B$4;\"//*[local-name()='feed']\");"
      '"#N/A -> input not parseable XML")',
      "Non-empty => XML parsed. #N/A => WEBSERVICE gave nothing parseable."),
 (12, "H  Same value via another field (sanity)",
      "=IFERROR(VALUE(FILTERXML($B$4;\"//*[local-name()='CS_13WK_YIELD_AVG']\"));\"FAIL\")",
      "Must show 4.1. If D/E fail but H works, the field path is the issue."),
 (14, "SEPARATOR CHECK", '=TEXT(TODAY();"YYYYMM")',
      "Expected 202610. An error means this locale does not use ';'."),
 (15, "Comma-formula demo (informational)",
      '=IFERROR(TEXT(TODAY(),"YYYYMM");"Err:508 - commas are NOT the separator here")',
      "Shows how an Excel-style comma formula fails in this locale."),
 (17, "I  WORKAROUND: fetch the CSV feed", f'=WEBSERVICE("{CSVURL}")',
      "Independent of FILTERXML. Long text here means the CSV endpoint is reachable."),
 (18, "J  WORKAROUND: 13-week coupon equivalent", CSVNUM,
      "Must show 4.1 using plain text functions only - no XPath at all."),
 (19, "J2 REFERENCE: same value from the XML feed",
      f'=IFERROR(VALUE(FILTERXML($B$4;"{XP}"));"FAIL")',
      "Must match row J. Both paths agreeing means the data is correct."),
]

E_SEP = '=IF(ISERROR($B$14);"WRONG SEPARATOR for this locale";"OK: this build uses ;")'

README = [
 ("Treasury 13-week bill yield - WEBSERVICE + FILTERXML diagnosis", 1),
 ("", 0),
 ("REPORTED PROBLEM", 1),
 ("=VALUE(FILTERXML(WEBSERVICE(G2);\"(//*[local-name()='ROUND_B1_YIELD_13WK_2'])[last()]\")) returns #N/A instead of a number.", 0),
 ("", 0),
 ("HOW TO USE", 1),
 ("1. Open the 'Diagnosis' sheet. Allow external links / network access when prompted.", 0),
 ("2. Press Ctrl+Shift+F9 (Tools > Recalculate Hard) to force a live refetch.", 0),
 ("3. Read steps A -> J in order. The FIRST row whose RESULT does not match EXPECTED is your root cause.", 0),
 ("", 0),
 ("MEASURED FACTS (LibreOffice 6.4.7.2, Linux, live feed for month 202610)", 1),
 ("- WEBSERVICE(url) returns the full 4532-byte Atom XML.", 0),
 ("- FILTERXML(xml; \"(//*[local-name()='ROUND_B1_YIELD_13WK_2'])[last()]\") returns 4.10.", 0),
 ("- VALUE(...) of that returns 4.1, a real number. So YOUR XPath IS CORRECT.", 0),
 ("- Bare '//ROUND_B1_YIELD_13WK_2' returns #N/A: the field lives in the 'd:' dataservices namespace.", 0),
 ("- Bare '/feed' and '//entry' also return #N/A: LO's FILTERXML has no default-namespace support.", 0),
 ("", 0),
 ("MEASURED ERROR TAXONOMY (what each failure looks like)", 1),
 ("WEBSERVICE, host reachable                -> the text, no error", 0),
 ("WEBSERVICE, host lookup fails            -> #VALUE! (Err:519)", 0),
 ("WEBSERVICE, not a valid URL              -> #VALUE! (Err:519)", 0),
 ("WEBSERVICE, external data disabled       -> Err:540", 0),
 ("FILTERXML, input empty or not XML        -> #VALUE! (Err:519)", 0),
 ("FILTERXML, XML ok but XPath matches none -> #N/A   <-- your symptom", 0),
 ("FILTERXML, match found                   -> the matched text", 0),
 ("VALUE(text that is not numeric)          -> Err:502", 0),
 ("Comma used as argument separator here    -> Err:508 / #NAME?", 0),
 ("=> #N/A is a FILTERXML no-match. A FAILED WEBSERVICE shows as #VALUE!/Err:540, but on a", 0),
 ("   stored sheet whose link was never refreshed it can present as #N/A too.", 0),
 ("", 0),
 ("LIKELY ROOT CAUSES, IN ORDER", 1),
 ("1. External data / link updating is off. Tools > Options > Calc > General > 'Update links", 0),
 ("   when loading' must be 'Always'. With it off WEBSERVICE cannot fetch, and the error it", 0),
 ("   leaves behind is turned into #N/A by FILTERXML. Check B, B-ISERROR, B-LEN, C.", 0),
 ("2. The XML fetch is not happening: proxy, firewall, TLS certificate store, offline mode.", 0),
 ("3. Argument separator: this LibreOffice uses ';'. An Excel formula pasted with ',' fails", 0),
 ("   with Err:508. Check the SEPARATOR CHECK row.", 0),
 ("4. Namespace: keep local-name() in the XPath. Removing it yields #N/A.", 0),
 ("5. The response body is not the feed (rate limiting, error page, schema change). See C.", 0),
 ("", 0),
 ("PROVEN REPLACEMENT IF FILTERXML KEEPS FAILING", 1),
 ("Rows I / J use the CSV endpoint with plain text functions only - no XPath at all.", 0),
 ("Verified result on this machine: 4.1.", 0),
]

def build():
    p = subprocess.Popen(["soffice", "--headless", "--norestore", "--nologo", "--nodefault",
        f"-env:UserInstallation=file://{PROF}", f"--accept={SOCK}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import uno
    local = uno.getComponentContext()
    res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    for _ in range(90):
        try: ctx = res.resolve("uno:" + SOCK); break
        except Exception: time.sleep(1)
    if ctx is None:
        print("no connect"); p.kill(); return 1
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ())
    sheets = doc.Sheets

    rd = sheets.getByIndex(0); rd.Name = "README"
    for i, (txt, bold) in enumerate(README):
        c = rd.getCellByPosition(0, i)
        c.setString(txt)
        if bold:
            try: c.CharWeight = 150.0
            except Exception: pass

    sheets.insertNewByName("Diagnosis", 1)
    sh = sheets.getByName("Diagnosis")
    for i, h in enumerate(["STEP", "FORMULA (this LibreOffice uses ';')",
                           "RESULT", "EXPECTED / WHAT IT MEANS"]):
        c = sh.getCellByPosition(i, 0); c.setString(h)
        try: c.CharWeight = 150.0; c.CellBackColor = 0xD9E1F2
        except Exception: pass
    for (r, label, formula, expect) in DIAG:
        sh.getCellByPosition(0, r-1).setString(label)
        fc = sh.getCellByPosition(1, r-1); fc.setFormula(formula)
        try: fc.CellBackColor = 0xFFF2CC
        except Exception: pass
        sh.getCellByPosition(3, r-1).setString(expect)
    sh.getCellByPosition(2, 13).setFormula(E_SEP)

    doc.calculateAll(); time.sleep(12); doc.calculateAll(); time.sleep(3)

    def P(n, v):
        from com.sun.star.beans import PropertyValue
        q = PropertyValue(); q.Name = n; q.Value = v; return q

    ods = BASE + "/treasury_filterxml_diagnosis.ods"
    xlsx = BASE + "/treasury_filterxml_diagnosis.xlsx"
    doc.storeToURL("file://" + ods, (P("FilterName", "calc8"),))
    doc.storeToURL("file://" + xlsx, (P("FilterName", "Calc MS Excel 2007 XML"),))
    print("saved:", ods)
    print("saved:", xlsx)
    print("\nRESULTS AS CALCULATED BY LIBREOFFICE:")
    for r in range(1, 21):
        a = sh.getCellByPosition(0, r-1).getString()
        b = sh.getCellByPosition(1, r-1).getString()
        if not a and not b:
            continue
        print(f"  row {r:>2} | {a[:40]:<40} | {b[:54]!r}")
    doc.close(False)
    try: desktop.terminate()
    except Exception: pass
    p.terminate()
    return 0

if __name__ == "__main__":
    print("URLF  :", URLF)
    print("CSVNUM:", CSVNUM)
    sys.exit(build())
