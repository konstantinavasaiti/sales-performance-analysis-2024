import pandas as pd

# Φόρτωση των δύο αρχείων
fact = pd.read_csv("../data/raw/FactSales.csv")
prod = pd.read_csv("../data/raw/DimProducts.csv")


# ─────────────────────────────────────────────────────────────
# ΒΗΜΑ 0: Απομόνωση των 10 προβληματικών γραμμών
# ─────────────────────────────────────────────────────────────

missing = fact[fact["Category"].isna()].copy()

print("Πλήθος γραμμών με κενό Category:", len(missing))
# → 10


# ─────────────────────────────────────────────────────────────
# ΒΗΜΑ 1: Φτιάχνουμε ένα set() με όλα τα ProductID που υπάρχουν στο DimProducts.
# ─────────────────────────────────────────────────────────────

valid_product_ids = set(prod["ProductID"])

# .isin() ελέγχει, για κάθε ProductID στο missing, αν υπάρχει
# μέσα στο valid_product_ids. Επιστρέφει True/False ανά γραμμή.
missing["ProductID_valid"] = missing["ProductID"].isin(valid_product_ids)

print("Όλα τα ProductID είναι έγκυρα;", missing["ProductID_valid"].all())
# → True  (όλα τα 10 ProductID υπάρχουν στο DimProducts)


# ─────────────────────────────────────────────────────────────
# ΒΗΜΑ 2: "LEFT JOIN με το DimProducts στο ProductID"
# ─────────────────────────────────────────────────────────────

merged = missing.merge(
    prod,
    on="ProductID",
    how="left",
    suffixes=("_fact", "_dim")
)

print(merged[["InvoiceID", "ProductID", "Category_fact", "Category_dim"]])


print("Γραμμές χωρίς αντιστοίχιση μετά το join:", merged["Category_dim"].isna().sum())


# ─────────────────────────────────────────────────────────────
# ΒΗΜΑ 3: "Επιβεβαίωση ότι επιστρέφεται μία και μόνο μία κατηγορία"
# ─────────────────────────────────────────────────────────────

duplicate_keys = prod["ProductID"].duplicated().sum()
print("Διπλά ProductID στο DimProducts:", duplicate_keys)
# → 0

# (β) Έλεγχος εάν υπάρχει κάποιο ProductID που αντιστοιχεί σε ΠΕΡΙΣΣΟΤΕΡΕΣ
#     από μία διαφορετικές τιμές Category.

category_per_product = prod.groupby("ProductID")["Category"].nunique()
ambiguous_products = (category_per_product > 1).sum()
print("ProductID με >1 διαφορετική κατηγορία:", ambiguous_products)
# → 0

# (γ) Τελικός έλεγχος "fan-out"
no_fanout = len(missing) == len(merged)
print("Γραμμές πριν == γραμμές μετά το join;", no_fanout)


# ─────────────────────────────────────────────────────────────
# ΤΕΛΟΣ: όλα τα κριτήρια πληρούνται 
# ─────────────────────────────────────────────────────────────
all_checks_passed = (
    missing["ProductID_valid"].all()
    and merged["Category_dim"].notna().all()
    and duplicate_keys == 0
    and ambiguous_products == 0
    and no_fanout
)
print("\n100% επιτυχής, ασφαλής αντιστοίχιση:", all_checks_passed)
# → True