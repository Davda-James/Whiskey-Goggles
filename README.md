## 📚 Table of Contents
- [Requirements](#requirements)
- [Data Preparation](#data-preparation)
- [Demo](#demo)
  - [Demo1](#demo1)
  - [Demo2](#demo2)

## Requirements
```python
pip install -r requirements.txt
```

## Data Preparation
- As baxus image has 501 images, so I have stored it and baxus_data.csv in data but if it scales and becomes more, then make **data** folder in root directory and download the google sheets as csv and store it in **data** folder.
```bash 
mkdir data
```
- Download the csv file of baxus where data is stored.
- Then run the download_baxus_data.py
```bash
python donwload_baxus_data.py
```

**If data is 501 there is no need to do anything and proceed further** 

## Demo 

### Demo1
This image is downloaded from internet and is not same as given in images.
<img src="./public/images/demo1.py.jpg">

### Backend Response (tried using postman)
```json
{
    "result": [
        {
            "name": "Jack Daniel's Coy Hill Barrelhouse 8 2024 Special Release Single Barrel Whiskey",
            "size": 750,
            "proof": 135.0,
            "abv": 67.5,
            "spirit_type": "Whiskey",
            "brand_id": 231.0,
            "popularity": 100062.0,
            "image_url": "https://d1w35me0y6a2bb.cloudfront.net/newproducts/af93f8d7-8ca7-45fb-8a24-4d6da26c74e6",
            "avg_msrp": 79.99,
            "fair_price": 252.21,
            "shelf_price": 549.99,
            "total_score": 893,
            "wishlist_count": 381,
            "vote_count": 222,
            "bar_count": 290,
            "ranking": 437,
            "id": 46347,
            "confidence_score": 0.6705087125301361
        }
    ]
}
```
#### Response on frontend




