# Data Understanding

## Overview

Το dataset αποτελείται από 6 αρχεία CSV, σχεδιασμένα γύρω από ένα μοντέλο **star schema**: ένα κεντρικό fact table (`FactSales`) που συνδέεται με dimension tables (`DimCustomers`, `DimProducts`) και δύο επιπλέον αρχεία αναφοράς (`Budget`, `Expenses`, `Payments`).

## Entity Relationship Summary

```
DimCustomers (CustomerID) ──┐
                             ├──> FactSales (CustomerID, ProductID)
DimProducts (ProductID) ────┘

Payments (CustomerID) ──> DimCustomers (CustomerID)

Budget (Month)     ──┐
Expenses (Month)   ──┴──> ανεξάρτητα, συνδέονται με FactSales μέσω InvoiceDate → Month
```

## File-by-File Breakdown

### 1. `FactSales.csv` — Κεντρικό fact table
**Γραμμές:** 1.500 | **Στήλες:** 10

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `InvoiceID` | string | Μοναδικό αναγνωριστικό συναλλαγής (π.χ. `INV00001`) |
| `InvoiceDate` | date (YYYY-MM-DD) | Ημερομηνία πώλησης. Εύρος: 2024-01-01 έως 2024-12-31 |
| `CustomerID` | string | Foreign key → `DimCustomers.CustomerID` |
| `ProductID` | string | Foreign key → `DimProducts.ProductID` |
| `Quantity` | integer | Ποσότητα προϊόντων στη συναλλαγή |
| `Category` | string | Κατηγορία προϊόντος (φαίνεται να είναι denormalized αντιγραφή από `DimProducts.Category`) |
| `UnitPrice` | float | Τιμή μονάδας |
| `DiscountPct` | float (0–1) | Ποσοστό έκπτωσης |
| `NetSales` | float | Καθαρά έσοδα συναλλαγής |
| `Cost` | float | Κόστος συναλλαγής |

**Πρωτεύον κλειδί:** `InvoiceID` (μοναδικό, χωρίς duplicates)

### 2. `DimCustomers.csv` — Dimension πελατών
**Γραμμές:** 100 | **Στήλες:** 2

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `CustomerID` | string | Μοναδικό αναγνωριστικό πελάτη (π.χ. `C001`) |
| `Region` | string | Γεωγραφική περιοχή πελάτη |

**Τιμές `Region`:** Athens, Heraklion, Larisa, Patra, Thessaloniki (5 μοναδικές περιοχές)

### 3. `DimProducts.csv` — Dimension προϊόντων
**Γραμμές:** 30 | **Στήλες:** 3

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `ProductID` | string | Μοναδικό αναγνωριστικό προϊόντος (π.χ. `P001`) |
| `Category` | string | Κατηγορία προϊόντος |
| `ProductName` | string | Όνομα προϊόντος |

**Τιμές `Category`:** Accessories, Laptops, Monitors, Phones (4 μοναδικές κατηγορίες)

### 4. `Budget.csv` — Μηνιαίος στόχος πωλήσεων
**Γραμμές:** 12 (Ιαν–Δεκ 2024) | **Στήλες:** 2

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `Month` | string (YYYY-MM) | Μήνας αναφοράς |
| `BudgetSales` | integer | Στόχος πωλήσεων για τον μήνα |

### 5. `Expenses.csv` — Μηνιαία έξοδα
**Γραμμές:** 12 (Ιαν–Δεκ 2024) | **Στήλες:** 4

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `Month` | string (YYYY-MM) | Μήνας αναφοράς |
| `Marketing` | integer | Έξοδα marketing |
| `Payroll` | integer | Έξοδα μισθοδοσίας |
| `Rent` | integer | Έξοδα ενοικίου |

### 6. `Payments.csv` — Ταχύτητα πληρωμών πελατών
**Γραμμές:** 100 | **Στήλες:** 2

| Στήλη | Τύπος | Περιγραφή |
|-------|-------|-----------|
| `CustomerID` | string | Foreign key → `DimCustomers.CustomerID` |
| `DaysToPay` | integer | Μέσος αριθμός ημερών μέχρι την πληρωμή |

## Initial Observations (πριν το Data Quality Report)

- Όλα τα `CustomerID` και `ProductID` στο `FactSales` βρίσκουν αντιστοιχία στα dimension tables — καλή referential integrity σε πρώτη ανάγνωση.
- Τα `Budget.csv` και `Expenses.csv` καλύπτουν τους ίδιους 12 μήνες με το `FactSales` — άμεσα συγκρίσιμα.
- Η στήλη `Category` υπάρχει σε δύο σημεία (`FactSales` και `DimProducts`) — πρέπει να ελεγχθεί αν είναι πάντα συνεπής (redundancy check).
- Χρειάζεται περαιτέρω έλεγχος σε: missing values, αρνητικές τιμές, και consistency μεταξύ υπολογισμένων πεδίων (π.χ. αν `NetSales` ≈ `Quantity × UnitPrice × (1 − DiscountPct)`).

*(Λεπτομέρειες και ευρήματα στο `data_quality_report.md`)*
