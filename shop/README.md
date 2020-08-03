## Online store
[drive with HWs](https://drive.google.com/drive/folders/1-pz_xoxf1lW6DwPubDBJ1L8k_fY-nlx-)

### start
to start the project run `docker-compose up`

### description
API for online store using PostgreSQL, Django

![data](/shop/scheme.png)

### API Documentation
[Postman](https://documenter.getpostman.com/view/10647848/SzRxV9su?version=latest)

## Product:
* **name** (max_lenght=200)
* **code** (max_lenght=200)
* **category** (max_lenght=200)

## API

### INFO
* **HTTP method**: GET
* **URL**: /database/product?code={code}
* **Response type**: JSON
* **Response**: Found product
* **Description**: return product description
* **Response example**:
``` json
{
  "name": "Lada",
  "code": "42",
  "category": "car",
  "create time": "2020-03-05T11:44:15.801Z",
  "modified time": "2020-03-05T11:44:15.801Z"
}
```

### CREATE
* **HTTP method**: POST
* **URL**: /database/product/create
* **Body parameters**: name, code, category
* **Description**: create product

### DELETE
* **HTTP method**: DELETE
* **URL**: /database/product/delete?code={code}
* **Description**: delete product by code

### EDIT
* **HTTP method**: PUT
* **URL**: /database/product/edit?code={code}
* **Body parameters**: name (oprional), category (optional)
* **Description**: edit product name or/and category by code

### LIST VIEW
* **HTTP method**: PUT
* **URL**: /database/products_list?list={number, optional, default=0}&&size={number, optional, default=50}
* **Response type**: JSON
* **Response**: list of products and (optional, if page isn't last) next-url like database/products_list?list={number}&&size={number}
* **Description**: list view of products, numbered from 0
* **Response example**:
``` json
{
  "products": [
    {
      "name": "Lada",
      "code": "42",
      "category": "car",
      "create time": "2020-03-05T11:44:15.801Z",
      "modified time": "2020-03-05T11:44:15.801Z"
    }
  ],
  "next-url": "database/products_list?list=2&&size=50"
}
```
