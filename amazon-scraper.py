from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import myproduct
import time
import functools
import sys

#Config
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)

#Parse search product name
search_product = ""
for i in range(1, len(sys.argv)):
  search_product += sys.argv[i] + " "

PRODUCT = search_product.strip()

#Open amazon and wait
print("Visiting amazon")
driver.get("https://amazon.com")
driver.implicitly_wait(2)

#Search for desired product
print("Searching for product")
search_box = driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
search_box.clear()
search_box.send_keys(PRODUCT)
search_box.send_keys(Keys.RETURN)

print("Getting and processing data")

#A function to create a Set of words in the title
def create_word_set(title):
  title_words = title.split(" ")
  title_words_set = set()
  for word in title_words:
    title_words_set.add(word.lower())
  
  return title_words_set

#A function to check whether the given key word is a prefix of any word in the given set
def prefix_search(key_word, title_words):
  n = len(key_word)
  for title_word in title_words:
    title_word_prefix = title_word[0: n]
    if title_word_prefix == key_word:
      return True
  
  #If none of the words in the given set have a prefix equal to the key word
  return False

#A function to check whether a given title is valid(has all the required key words)
def is_valid_title(title):
  key_words = PRODUCT.split(" ")

  #Used a Set for constance time search
  title_words = create_word_set(title)
  for key_word in key_words:
    #Only trying for a prefix match if word doesn't exist
    if not key_word.lower() in title_words:
      if not prefix_search(key_word.lower(), title_words):
        return False
  
  return True

#A function to get all the data on the page and process it
def process_data_on_page():
  products_main = driver.find_element_by_class_name("s-main-slot")
  amazon_products = products_main.find_elements_by_class_name("s-result-item")
  my_products = []
  for product in amazon_products:
      lines = product.text.split("\n")

      #Looking for title(skipping all Sponsored, and Best Seller lines)
      title = ""
      for line in lines:
        if (line.lower() != "sponsored" and line.lower() != "best seller"):
          title = line
          break
      
      #If title is valid, creating a product object and storing in my products list
      if is_valid_title(title):
        try:
          #Get discount price
          discount_price_element = WebDriverWait(product, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price")))
          discount_price_info = discount_price_element.text.split("\n")
          discount_price = float(discount_price_info[0][1:] + "." + discount_price_info[1])
        except:
          continue

        try:
          #Get previous price
          previous_price_element = WebDriverWait(product, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price[data-a-strike='true']")))
          previous_price = float(previous_price_element.text[1:])
        except:
          previous_price = discount_price
        
        #Create product object and add to list
        my_products.append(myproduct.Product(title, previous_price, discount_price))
  
  return my_products

#Retreiving amazon's non customized search results
time.sleep(3)
my_products = process_data_on_page()

#Check all the deals checkboxes to load the pages with the best deals
driver.implicitly_wait(2)
try:
  deals_container = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[aria-labelledby=p_n_specials_match-title]")))
  deals = deals_container.find_elements_by_tag_name("a")

  for deal in deals:
    deal.click()
except:
  #do nothing if no deals
  pass

#Retreiving amazon's deals search results
my_products.extend(process_data_on_page())

#Finding cheapest product and product with best deal
print("Finding best deal and cheapest product")

cheapest_product = None
cheapest_price = 0
best_deal_product = None
best_discount = -1

for product in my_products:
  if not cheapest_product or product.get_price() < cheapest_product.get_price():
    cheapest_product = product
    cheapest_price = product.get_price()
  
  if not best_deal_product or product.get_discount() > cheapest_product.get_discount():
    best_deal_product = product
    best_discount = product.get_discount()

print("Finished!")
print("---------------------------------------")
print("Here are your results!")
if not my_products:
  print("Sorry, no available results match... try lowering the number of key words")
else:
  print("Cheapest product: {0}, Price: ${1}".format(cheapest_product.get_title(), cheapest_price))
  print("Best deal: {0}, Previous Price: ${1}, Discount: ${2}".format(best_deal_product.get_title(), best_deal_product.get_previous_price(), best_discount))

  
