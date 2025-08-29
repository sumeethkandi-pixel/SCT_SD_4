import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from scrapers import REGISTRY

def scrape():
    provider = provider_var.get()
    query = query_var.get().strip()
    pages = int(pages_var.get())
    if not query:
        messagebox.showwarning("Input", "Please enter a search query.")
        return

    scraper = REGISTRY[provider]
    # clear table
    for row in tree.get_children():
        tree.delete(row)

    scraped = 0
    try:
        for p in range(1, pages+1):
            status_var.set(f"Fetching page {p}/{pages} from {provider}…")
            root.update_idletasks()

            for item in scraper.search(query, p):
                tree.insert("", "end", values=(item["name"], item["price"], item["rating"], item["url"]))
                scraped += 1

        status_var.set(f"Done. {scraped} items.")
        if scraped == 0:
            messagebox.showinfo("No Results", "No products found. Try a different keyword or fewer pages.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to scrape: {e}")
        status_var.set("Idle")

def export_csv():
    if not tree.get_children():
        messagebox.showwarning("Export", "No data to export.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="products.csv")
    if not path:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Price", "Rating", "URL"])
        for iid in tree.get_children():
            writer.writerow(tree.item(iid)["values"])
    messagebox.showinfo("Export", f"Saved to {path}")

root = tk.Tk()
root.title("E‑commerce Product Scraper")

# Controls frame
frm = ttk.Frame(root, padding=10)
frm.pack(fill="x")

ttk.Label(frm, text="Provider:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
provider_var = tk.StringVar(value=list(REGISTRY.keys())[0])
ttk.Combobox(frm, textvariable=provider_var, values=list(REGISTRY.keys()), state="readonly", width=12).grid(row=0, column=1, padx=4, pady=4)

ttk.Label(frm, text="Search:").grid(row=0, column=2, sticky="w", padx=4, pady=4)
query_var = tk.StringVar()
ttk.Entry(frm, textvariable=query_var, width=30).grid(row=0, column=3, padx=4, pady=4)

ttk.Label(frm, text="Pages:").grid(row=0, column=4, sticky="w", padx=4, pady=4)
pages_var = tk.StringVar(value="1")
ttk.Spinbox(frm, from_=1, to=5, textvariable=pages_var, width=5).grid(row=0, column=5, padx=4, pady=4)

ttk.Button(frm, text="Scrape", command=scrape).grid(row=0, column=6, padx=6, pady=4)
ttk.Button(frm, text="Export CSV", command=export_csv).grid(row=0, column=7, padx=6, pady=4)

# Table
cols = ("Product", "Price", "Rating", "URL")
tree = ttk.Treeview(root, columns=cols, show="headings", height=18)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="w", width=200 if c=="Product" else 100)
tree.pack(fill="both", expand=True, padx=10, pady=6)

# Status bar
status_var = tk.StringVar(value="Idle")
status = ttk.Label(root, textvariable=status_var, anchor="w", relief="sunken")
status.pack(fill="x", padx=10, pady=(0,10))

root.mainloop()