# Business Request

## Client / Stakeholder
*[π.χ. Sales Director, ΧΥΖ Retail Company]*

## Date Requested
2024-XX-XX

## Background

*Περιγραφή 2-3 προτάσεων: ποιο είναι το context; Γιατί ζητείται αυτή η ανάλυση τώρα;*

Παράδειγμα:
> Η εταιρεία θέλει να κατανοήσει την πορεία πωλήσεων για το 2024 ανά κατηγορία προϊόντος και περιοχή, ώστε να αξιολογήσει αν τα στόχοι πωλήσεων (budget) επιτεύχθηκαν και να εντοπίσει ευκαιρίες/ρίσκα για το επόμενο τρίμηνο.

## Business Question(s)

*Τι ακριβώς θέλει να μάθει ο πελάτης; Γράψε τα ως ερωτήσεις, όχι ως tasks.*

1. Πόσο κοντά ήμασταν στο budget πωλήσεων ανά μήνα/τρίμηνο για το 2024;
2. Ποιες κατηγορίες προϊόντων και ποιες περιοχές αποδίδουν καλύτερα/χειρότερα;
3. Πώς συγκρίνονται τα έξοδα (Marketing, Payroll, Rent) με τα έσοδα στη διάρκεια του έτους;
4. Υπάρχει πρόβλημα στην ταχύτητα πληρωμών πελατών (DaysToPay) που επηρεάζει το cash flow;

## Success Criteria / Deliverables

*Τι θα παραδοθεί στο τέλος; Πώς ξέρουμε ότι το engagement πέτυχε τον στόχο του;*

- [ ] Καθαρισμένο, validated dataset έτοιμο για ανάλυση
- [ ] Data Quality Report με τα προβλήματα που εντοπίστηκαν και πώς διορθώθηκαν
- [ ] Exploratory Data Analysis με βασικά insights (trends, outliers, comparisons)
- [ ] Συγκεκριμένες, actionable συστάσεις προς τον πελάτη

## Scope

**Μέσα στο scope:**
- *[π.χ. Δεδομένα πωλήσεων, εξόδων και πληρωμών για το έτος 2024]*

**Εκτός scope:**
- *[π.χ. Forecasting/πρόβλεψη για 2025, ανάλυση customer churn]*

## Data Sources Provided

| Αρχείο | Περιγραφή |
|--------|-----------|
| `FactSales.csv` | Συναλλαγές πωλήσεων (invoice-level) |
| `DimCustomers.csv` | Στοιχεία πελατών και περιοχή |
| `DimProducts.csv` | Κατάλογος προϊόντων και κατηγορία |
| `Budget.csv` | Μηνιαίος στόχος πωλήσεων (budget) |
| `Expenses.csv` | Μηνιαία έξοδα (Marketing, Payroll, Rent) |
| `Payments.csv` | Ημέρες πληρωμής ανά πελάτη |

## Constraints / Assumptions

*[π.χ. Τα δεδομένα καλύπτουν μόνο το 2024. Δεν υπάρχει πρόσβαση σε δεδομένα προηγούμενων ετών για year-over-year comparison.]*

## Timeline

| Ημέρα | Φάση |
|-------|------|
| Day 1 | Business Request → Data Understanding → Data Quality Report → Manager Feedback |
| Day 2 | Cleaning → Validation |
| Day 3 | EDA → Insights |
