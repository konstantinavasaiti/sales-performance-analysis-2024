# Data Quality Report

**Ημερομηνία:** 2024-XX-XX
**Συντάκτης:** *[το όνομά σου]*
**Αρχεία που εξετάστηκαν:** `FactSales.csv`, `DimCustomers.csv`, `DimProducts.csv`, `Budget.csv`, `Expenses.csv`, `Payments.csv`

## Methodology

Έγινε έλεγχος σε κάθε αρχείο για:
- Missing values
- Duplicate records / duplicate keys
- Referential integrity (foreign keys μεταξύ fact και dimension tables)
- Λογικά όρια τιμών (negative/zero όπου δεν έχει νόημα)
- Consistency μεταξύ συνδεδεμένων πεδίων (π.χ. `Category` σε δύο αρχεία)
- Ορθότητα υπολογισμένων πεδίων (`NetSales` έναντι αναμενόμενου υπολογισμού)
- Κάλυψη χρονικού εύρους (μήνες/ημερομηνίες)

## Summary of Findings

| # | Issue | Αρχείο | Σοβαρότητα | Πλήθος εγγραφών |
|---|-------|--------|------------|------------------|
| 1 | Missing `Category` | `FactSales.csv` | Μεσαία | 10 / 1.500 (0,67%) |
| 2 | Αρνητικό `Quantity` με ασύμβατο `NetSales` | `FactSales.csv` | Υψηλή | 8 / 1.500 (0,53%) |
| 3 | — *(χωρίς ευρήματα — δες "Clean Areas" παρακάτω)* | — | — | — |

## Detailed Findings

### Finding 1: Missing values στη στήλη `Category` (FactSales)

**Περιγραφή:** 10 από τις 1.500 γραμμές του `FactSales.csv` έχουν κενή τιμή στη στήλη `Category`, παρόλο που το αντίστοιχο `ProductID` υπάρχει κανονικά στο `DimProducts.csv` με γνωστή κατηγορία.

**Επίπτωση:** Αν η ανάλυση γίνει με βάση τη στήλη `Category` του `FactSales` (αντί να γίνει join με `DimProducts`), αυτές οι 10 γραμμές θα εξαιρεθούν λανθασμένα από ανάλυση ανά κατηγορία.

**Προτεινόμενη διόρθωση (Day 2):** Αντί να γίνει drop ή imputation, η σωστή λύση είναι να **αγνοηθεί η στήλη `Category` του FactSales** και να γίνεται πάντα join με `DimProducts.Category` ως single source of truth. Επιβεβαιώθηκε ότι σε καμία γραμμή δεν υπάρχει ασυμφωνία μεταξύ των δύο πηγών (0 mismatches στις 1.490 γραμμές που έχουν τιμή).

**Παράδειγμα γραμμών:**
```
InvoiceID   ProductID   Category (FactSales)
INV00070    P025        NaN
INV00273    P023        NaN
INV00364    P028        NaN
... (+7 ακόμα)
```

### Finding 2: Αρνητικό `Quantity` με θετικό `NetSales` (FactSales)

**Περιγραφή:** 8 γραμμές έχουν `Quantity = -1`. Σε φυσιολογικό σενάριο επιστροφής (return), θα περιμέναμε `NetSales` και `Cost` να είναι επίσης αρνητικά. Όμως σε όλες τις 8 γραμμές, το `NetSales` και το `Cost` παραμένουν **θετικά**, και η τιμή τους ταιριάζει με τον υπολογισμό `|Quantity| × UnitPrice × (1 − DiscountPct)` — δηλαδή σαν να είχε χρησιμοποιηθεί η απόλυτη τιμή της ποσότητας στον υπολογισμό, αλλά το πρόσημο πέρασε λάθος μόνο στη στήλη `Quantity`.

**Επίπτωση:** Αυτό δεν φαίνεται να είναι πραγματική επιστροφή προϊόντος, αλλά πιθανό **σφάλμα καταχώρησης δεδομένων** (data entry error) στο πρόσημο της ποσότητας. Αν αφεθεί ως έχει, θα μειώσει τεχνητά το συνολικό `Quantity` σε αναλύσεις ανά προϊόν/μήνα, χωρίς αντίστοιχη μείωση στα έσοδα.

**Προτεινόμενη διόρθωση (Day 2):** Να επιβεβαιωθεί με τον Manager/πελάτη αν πρόκειται για:
- (α) σφάλμα καταχώρησης → διόρθωση σε `Quantity = +1`, ή
- (β) πραγματικές επιστροφές με λάθος πρόσημο στο `NetSales`/`Cost` αντί στο `Quantity`

Μέχρι επιβεβαίωση, οι 8 γραμμές θα **flagged** με νέα στήλη `data_quality_flag` αντί να διορθωθούν σιωπηλά.

**Πλήρης λίστα:**
```
InvoiceID    Quantity  UnitPrice    DiscountPct  NetSales    Cost
INV00076     -1        282.36       0.00         1411.81     988.27
INV00092     -1        43.44        0.05         82.53       41.26
INV00331     -1        521.20       0.05         2475.70     1931.04
INV00775     -1        791.51       0.00         3166.05     2786.12
INV01039     -1        835.34       0.15         3550.21     3124.19
INV01265     -1        243.54       0.00         1461.24     1022.87
INV01286     -1        35.07        0.20         112.23      56.12
INV01350     -1        852.05       0.00         5112.28     4498.81
```

## Clean Areas (επιβεβαιωμένα χωρίς προβλήματα)

Οι παρακάτω έλεγχοι έγιναν και **δεν** βρέθηκαν προβλήματα:

- ✅ **Referential integrity:** Όλα τα `CustomerID` και `ProductID` στο `FactSales` αντιστοιχίζονται σωστά σε `DimCustomers` / `DimProducts`. Όλα τα `CustomerID` στο `Payments` αντιστοιχίζονται σωστά σε `DimCustomers`.
- ✅ **Duplicate keys:** Δεν βρέθηκαν διπλά `InvoiceID`, `CustomerID`, ή `ProductID` στα αντίστοιχα αρχεία τους.
- ✅ **Category consistency:** Καμία ασυμφωνία μεταξύ `FactSales.Category` και `DimProducts.Category` στις γραμμές που έχουν τιμή.
- ✅ **Ημερομηνίες:** Όλες οι τιμές `InvoiceDate` είναι valid και μέσα στο εύρος 2024-01-01 έως 2024-12-31. Δεν βρέθηκαν unparseable dates.
- ✅ **Χρονική κάλυψη:** Τα `Budget.csv`, `Expenses.csv`, και `FactSales.csv` καλύπτουν όλους τους 12 μήνες του 2024 — άμεσα συγκρίσιμα χωρίς gaps.
- ✅ **DiscountPct εύρος:** Όλες οι τιμές είναι μέσα στο λογικό εύρος [0, 1].
- ✅ **DaysToPay:** Καμία αρνητική τιμή στο `Payments.csv`.
- ✅ **UnitPrice / Cost:** Καμία μηδενική ή αρνητική τιμή (εκτός των 8 σημειωμένων γραμμών στο Finding 2, όπου τα ποσά είναι θετικά).

## Recommendations for Day 2 (Cleaning)

1. Κατά το join `FactSales` ↔ `DimProducts`, χρησιμοποίησε το `Category` του `DimProducts` ως αυθεντική πηγή· drop ή αγνόησε τη στήλη `Category` του `FactSales`.
2. Δημιούργησε flag column `data_quality_flag` για τις 8 γραμμές με αρνητικό `Quantity`, ώστε να παραμείνουν ορατές αλλά να μπορούν να εξαιρεθούν εύκολα από αθροιστικές αναλύσεις μέχρι να υπάρξει επιβεβαίωση.
3. Τεκμηρίωσε στο `validation_report.md` (Day 2) τον αριθμό γραμμών πριν/μετά το cleaning, ώστε να υπάρχει διαφάνεια στο πόσα δεδομένα άλλαξαν.

## Open Questions for Manager Feedback

- Οι 8 γραμμές με αρνητικό `Quantity` — επιστροφές προϊόντων ή σφάλμα καταχώρησης;
- Είναι αποδεκτό να αγνοηθεί η στήλη `Category` του `FactSales` υπέρ του `DimProducts.Category`, ή υπάρχει λόγος που υπάρχει ξεχωριστά (π.χ. ιστορικό snapshot τιμής κατηγορίας τη στιγμή της πώλησης)?
