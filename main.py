import tkinter as tk
from tkinter import ttk
import requests
from lxml import html

def on_submit():
    selected_site = site_var.get()
    user_input = input_field.get()
    base_urls = {
        "emag.bg": f"https://www.emag.bg/search/{user_input}?ref=effective_search",
        "ardes.bg": f"https://ardes.bg/products?q={user_input}",
        "technomarket.bg": f"https://www.technomarket.bg/search?query={user_input}"
    }
    xpath_selectors = {
        "emag.bg": '//*[@id="card_grid"]//h2/a',
        "ardes.bg": '//*[@id="ajax_content"]//div[@class="title"]',
        "technomarket.bg": '//tm-product-item//div/a'
    }
    if selected_site not in base_urls: 
        print("Selected site is not supported.")
        return

    full_url = base_urls[selected_site]
    try:
        response = requests.get(full_url)
        print(f"Request sent to: {full_url}")
        print(f"Response status code: {response.status_code}")
        tree = html.fromstring(response.content)
        elements = tree.xpath(xpath_selectors[selected_site])
        product_titles = [''.join(el.xpath('.//text()')).strip() for el in elements]
        result_text.delete('1.0', tk.END)
        for title in product_titles:
            result_text.insert(tk.END, title + '\n')

    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")

root = tk.Tk()
root.title("Web Scraper")
root.geometry("1280x720") 

frame = tk.Frame(root)
frame.pack(fill='both', expand=True, padx=20, pady=20)

site_label = tk.Label(frame, text="Select Site:", anchor="w")
site_label.pack(fill='x')

site_var = tk.StringVar(value="emag.bg")
site_dropdown = ttk.Combobox(frame, textvariable=site_var, state="readonly")
site_dropdown['values'] = ("emag.bg", "ardes.bg", "technomarket.bg")
site_dropdown.pack(fill='x', pady=(0, 10))

input_label = tk.Label(frame, text="Enter search term:", anchor="w")
input_label.pack(fill='x')

input_field = tk.Entry(frame)
input_field.pack(fill='x', pady=(0, 10))

submit_button = tk.Button(frame, text="Submit", command=on_submit)
submit_button.pack()

result_text = tk.Text(frame, height=15)
result_text.pack(fill='both', expand=True, pady=(10, 0))

root.mainloop()

