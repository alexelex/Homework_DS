## Homework_DS
[drive with HWs](https://drive.google.com/drive/folders/1-pz_xoxf1lW6DwPubDBJ1L8k_fY-nlx-)

### start
to start the project run `docker-compose up`

### description
API for online store using SQLite, Django

### API Documentation
[Postman](https://documenter.getpostman.com/view/10647848/SzRxV9su?version=latest)

## Product:
* **name** (max_lenght=200)
* **code** (max_lenght=200)
* **category** (max_lenght=200)

## API

### INFO
* **HTTP method**: GET
* **URL**: /database/product&code={code}
* **Response type**: JSON
* **Response**: Created item.
* **Description**: return product description.
