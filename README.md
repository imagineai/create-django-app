<h1> Create Django App </h1>

Single line command to create a Django app with all the dependencies installed. 

<h2> Overview </h2>

Run the following command in your terminal:
```
npm install -g imagine && imagine create -f django -n myapp 
```

(If you don't have npm installed, you'll need to install this first)

- You can run your new Django app by running `cd myapp && imagine run`. You can open the url http://127.0.0.1:8000/ in your browser - you should see a page that shows the install worked successfully.

- Congrats! Your Django app is up and running! 

- Now that you've created your new app, check out the myapp.im in your app directory - using this you can easily: 
  - easily change your app settings such as django server and package manager, API format etc.
  - add app functionality such as data models, APIs, storage etc using a simple config spec. 
