import json
import re

def chunk_text(text, chunk_size=500):
    """Splits text into smaller chunks."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def load_extracted_data(filepath):
    """Loads extracted data from the given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def process_refrigerator_data(refrigerator_data):
    """For refrigerator due to diff scraping technique and output structure"""
    print("Processing Refrigerator Data")
    chunks = []
    total_chunks = 0

    for brand, product_types in refrigerator_data.items():
        print(f"Checking brand: {brand}")
        brand_chunk_count = 0

        for product_type_url, products in product_types.items():
            product_type = product_type_url.split("/")[-1].replace(".htm", "").replace("-", " ")
            print(f"Checking product type: {product_type}")

            if isinstance(products, dict):
                product_found = False

                for product_page, product_text in products.items():
                    if isinstance(product_text, str) and product_text.strip():
                        product_found = True
                        text_chunks = chunk_text(product_text)
                        chunk_count = len(text_chunks)

                        for chunk in text_chunks:
                            chunks.append({
                                "text": chunk,
                                "appliance": "Refrigerator",
                                "brand": brand,
                                "product_type": product_type,
                                "product_page": product_page
                            })
                        
                        brand_chunk_count += chunk_count

                if product_found:
                    print(f"Found products for {product_type} ({brand}) → {brand_chunk_count} chunks")
                else:
                    print(f"No valid product descriptions found for {product_type} ({brand})")

        print(f"Total chunks for {brand}: {brand_chunk_count}")
        total_chunks += brand_chunk_count

    print(f"Refrigerator Data Chunking Completed! Total chunks: {total_chunks}")
    return chunks

def process_dishwasher_data(da):
 
    """
    For dishwashers as their data structure is different
    """
    print("Processing Dishwasher Data")

    

    
    data = da['Dishwasher']
    chunks = []
    chunk_counter = 0
    for brand_name, link in data['Brand Links'].items():
        
        brand = brand_name
        product_page = link
        category_links = []
        category_product_links = []
        indivisual_product_links = []
        # for key, item in da['Product Type Links'].items():
        #     print(key, item)
        #     if key == rf"(https://www.partselect.com/{brand_name}-Dishwasher)":
        #         category_links = item
        category_links = data['Product Type Links'][f"https://www.partselect.com/{brand_name}-Dishwasher-Parts.htm"]
        for i in category_links:
            
            # a = i[0]
            category_product_links = data['Individual Product Links'][f'https://www.partselect.com{i}']
            for product_link in category_product_links:
                
                descrip = data["Product Descriptions"][f"https://www.partselect.com{product_link}"]
                chunk = {
                    "text": descrip,
                    "appliance": "Dishwasher",
                    "brand": brand_name,
                    "product_type": f"{i}",
                    "product_page": f"https://www.partselect.com{product_link}",
                }
                chunks.append(chunk)
                chunk_counter += 1

    print(f"Total chunks created: {chunk_counter}")
    if chunks:
        print(f"Example chunk: {json.dumps(chunks[0], indent=4)}")

    return chunks


def save_chunks(chunks, output_file):
    """Saves chunked data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)
    print(f"hunked data saved to `{output_file}`.")

def main():
    """Main function to orchestrate chunking for both Refrigerator and Dishwasher."""
    input_file = "merged_appliances_data.json"  
    output_file = "chunks_data.json"

    print(f"Loading extracted data from `{input_file}`...")
    extracted_data = load_extracted_data(input_file)

    print("Processing Refrigerator and Dishwasher data separately...")

    refrigerator_chunks = process_refrigerator_data(extracted_data.get("Refrigerator", {}))
    dishwasher_chunks = process_dishwasher_data(extracted_data.get("Dishwasher", {}))

    all_chunks = refrigerator_chunks + dishwasher_chunks

    print(f"Saving all chunked data to `{output_file}`...")
    save_chunks(all_chunks, output_file)

if __name__ == "__main__":
    main()


