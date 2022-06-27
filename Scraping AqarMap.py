# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:42:06 2021

@author: MohaMedFRy
"""
import requests 
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

cnt=1;
while(True):    
    #Definition 
    link = []
    print(cnt)
    # Open general link
    result = requests.get (f"https://aqarmap.com.eg/ar/for-sale/property-type/cairo/?photos=0&unitOnly=0&byOwnerOnly=0&default=4&page={cnt}")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    
    links = soup.find_all("div", {'class' : 'card-details-container'})
    #print (links)
    for i in range(len(links)):
        s = "https://aqarmap.com.eg" + links[i].find('a').attrs['href']
        link.append(s)
        
        # link.append(links[i].find('a').attrs['href'])
    ln = len(link)
    print(ln)
    titles = []
    
    floor = []
    year_of_delivery = []
    finish_type = []
    overlooking = []
    ad_num = []
    date_of_publication = []
    price = []
    price_of_meter = [] 
    advertiser_type = []
    payment_method = []
    
    ad_description = []
    sz = 0
    for i in link:
        print(sz)
        sz += 1
        result = requests.get(i)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        #print (i)
        # هنشيل الهاش ف الاخر    
        title_scr = soup.find('div', {'class' : "padding-md-zero"}).find('h1')
        titles.append(title_scr.text)
        x = soup.find("table", {'class' : "listing-info table-info"})
        al_tb = x.find("tbody").find_all("tr")
        for j in al_tb:
            descriptions = j.find_all("td")
            l=[]
            for k in descriptions:
                l.append(k.text)
            if l[0] == "سنة البناء / سنة التسليم":
                year_of_delivery.append(l[1])
            elif l[0] == "نوع التشطيب":
                finish_type.append(l[1])
            elif l[0] == 'تطل على':
                overlooking.append(l[1])
            elif l[0] == 'الطابق':
                floor.append(l[1])
                
        x = soup.find("table", {'class' : "listing-info collapse listingMoreInfo"})
        #print(x)
        al_tb = x.find("tbody").find_all("tr")
        for j in al_tb:
             descriptions = j.find_all("td")
             l=[]
             for k in descriptions:
                 l.append(k.text)
                 #print(l)   
             if l[0] == "رقم الإعلان":
                 ad_num.append(l[1])
           
             elif l[0] == "تاريخ النشر":
                   date_of_publication.append(l[1])
             elif l[0] == "السعر":
                   price.append(l[1])
             elif l[0] == "سعر المتر":
                 price_of_meter.append(l[1])
             elif l[0] == "نوع المعلن":
                 advertiser_type.append(l[1])
             elif l[0] == "طريقة الدفع":
                 payment_method.append(l[1])
        if len(floor) < sz :  floor.append("NA")
        if len(year_of_delivery) < sz : year_of_delivery.append("NA")
        if len(finish_type) < sz : finish_type.append("NA")
        if len(overlooking) < sz : overlooking.append("NA")     
        if len(ad_num) < sz : ad_num.append("NA")
        if len(date_of_publication) < sz : date_of_publication.append("NA")
        if len(price) < sz : price.append("NA")
        if len(price_of_meter) < sz : price_of_meter.append("NA")
        if len(advertiser_type) < sz : advertiser_type.append("NA")
        if len(payment_method) < sz : payment_method.append("NA")
    x = soup.find("div", {"class" : "listing-text large-element"})
    ad_description.append(x.text)
    stop = soup.find("span", {'class' : 'next'})
    if stop is None:
        break
    cnt += 1    
        
  
print("Scraping Done")
file_list = [titles, floor, year_of_delivery, finish_type, overlooking, ad_num, date_of_publication,
              price, price_of_meter, advertiser_type, payment_method, ad_description]
exported = zip_longest(*file_list)
        
with open("F:\Scraping\AqarMap\AqarMap in Cairo.csv", 'w' ,encoding='utf-8') as file:
    wr = csv.writer(file)
    wr.writerow(['Title', 'Floor Number', 'Year of Delivery', 'Finish Type', 'Overlooking',
                  'Advertise Number', 'Date of Publication', 'Price', 'Price of One Meter',
                  'Advertiser Type', 'Payment Method', 'Advertise Description'])
    wr.writerows(exported)

      
print("Done")


