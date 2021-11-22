this the rasa chatbot for iphone retail shop built on top of RasaHQ/retail-demo: Rasa's retail starter pack using Rasa 2.3.1,

repository : https://github.com/RasaHQ/retail-demo

I built this model using  FastAPI for the back end server,rasa for front end client,and MongoDB Atlas for the back end database server.

# Things you can ask the bot:

       1.Check the status of an order
       2.Return an item
       3.Cancel an item
       4.check Stock availability for iphone mobile
       5.Subscribe to product updates
       6.check the colors available for certain iphone model
       7.check the internal memory availability for certain iphone model
	
# Overview of the files:

- data/stories.yml- contains stories
- data/nlu.yml -  contains NLU training data
- data/rules.yml -  contains the rules upon which the bot responds to queries
- actions/actions.py -  contains custom action/api code
- domain.yml -  the domain file, including bot response templates
- config.yml -  training configurations for the NLU pipeline and policy ensemble
- tests/test_stories.yml -  end-to-end test stories

# overview of the dataset used:

there is two datasets used in the model orders and iphone dataset,

## orders dataset:
 containing details of the customer order including:

- order_date : "01/01/20"
- order_number : 1
- order_email : example@rasa.com
- order_mobile : 01066301431
- brand : Apple
- model : iPhone 7 Plus
- colors : Jet Black
- capacity : 256GB
- payment : 900 
- status : returning




### MongoDB Document overview of orders collections:

{"_id":{"$oid":"6191982f47f17cf4d4d0e242"},"order_date":"01/01/20","order_number":"1","order_email":"example@rasa.com","order_mobile":"01066301431","brand":"Apple","model":"iPhone 7 Plus","colors":"Jet Black","capacity":"256GB","payment":"900","status":"returning"}


## iphone dataset:
containing details the iphone mobile stock available and mobile specifications:

- brand : Apple
- model : iPhone13ProMax
- announced : 2021september
- size_height_width_deth : 160.8x78.1x7.65mm
- weight_g : 240grams
- colors : SierraBlue
- capacity : 128GB
- ram : 6GB
- approx_price_USD : 1099
- img_url :"https://freephonestores.com/wp-content/uploads/2021/09/iphone-13-pro-family-hero.png"
- stock : 5

### MongoDB Document overview of iphone collections:

{"_id":{"$oid":"619408ed0c50ef973a30b8c2"},"brand":"Apple","model":"iPhone13ProMax","announced":"2021september","size_height_width_deth":"160.8x78.1x7.65mm","weight_g":"240grams","colors":"SierraBlue","capacity":"128GB","ram":"6GB","approx_price_USD":"1099","img_url":"https://freephonestores.com/wp-content/uploads/2021/09/iphone-13-pro-family-hero.png","stock":"5"}

the database hosted in MongoDB Atlas as non-relational databases, or NoSQL,

in order to connect to the MongoDB Database we created API app to get data from you database.



# Overview of the API application:


## api application built using FastAPI, 

Fast API is a modern and fast web framework for building API’s created by Sebastian Ramirez, and this uses ASCII, 
and ASCII stands for asynchronouse server gateway interface.

And this is just the interface between your application and the server.
The response time is lightning fast,and this is one of the big advantages of having ASCII server implementation on your,

fast api also has interactive API documentation and it helps you to test the different HTTP requests like get post put and delete visually using open API,
which is itself based on json schema.

So I built two API applications one for the orders dataset and one for iphone dataset the booth deployed to heroku, 
Heroku is a platform as a service (PaaS) that enables developers to build, run,and operate applications entirely in the cloud.

