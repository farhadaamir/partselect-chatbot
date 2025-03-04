import json 
import regex

def chunker_dishwasher(data):
    da = data['Dishwasher']
    print("hello")
    # # print(da.items())
    # print(len(da["Brand Links"]))
    # print(da["Brand Links"][0])
    # print(len(da["Product Type Links"]))
    # print(da["Product Type Links"][0])
    # print(len(da["Individual Product Links"]))

    for brand_name, link in da['Brand Links'].items():
        print(brand_name)
        brand = brand_name
        product_page = link
        category_links = []
        category_product_links = []
        indivisual_product_links = []
        # for key, item in da['Product Type Links'].items():
        #     print(key, item)
        #     if key == rf"(https://www.partselect.com/{brand_name}-Dishwasher)":
        #         category_links = item
        category_links = da['Product Type Links'][f"https://www.partselect.com/{brand_name}-Dishwasher-Parts.htm"]
        for i in category_links:
            print(f'https://www.partselect.com{i}')
            # a = i[0]
            category_product_links = da['Individual Product Links'][f'https://www.partselect.com{i}']
            # get product name using regex by getting the alphabets before .htm? 
            for product_link in category_product_links:
                print(f'https://www.partselect.com{product_link}')
                descrip = da["Product Descriptions"][f"https://www.partselect.com{product_link}"]
                print(descrip[:200])
        break
        
        break
# "Brand Links": {
            # "Admiral": "https://www.partselect.com/Admiral-Dishwasher-Parts.htm",
    # "Product Type Links": {
            # "https://www.partselect.com/Admiral-Dishwasher-Parts.htm": [
                # "/Admiral-Dishwasher-Hardware.htm", 
    # "Individual Product Links": {
#             "https://www.partselect.com/Admiral-Dishwasher-Hardware.htm": [
#                 "/PS11740613-Whirlpool-WP285655-Hose-Clamp.htm?SourceCode=18",
# "Product Descriptions": {
            # "https://www.partselect.com/PS11740613-Whirlpool-WP285655-Hose-Clamp.htm?SourceCode=18
    
if __name__ == "__main__":
    with open("parts_data_dishwasher.txt", "r", encoding="utf-8") as file:
        dishwasher_data = json.load(file)
    
    dishwasher_chunks = chunker_dishwasher(dishwasher_data)
    # print(f"🚀 Dishwasher Data Chunking Completed! Total chunks: {len(dishwasher_chunks)}")
