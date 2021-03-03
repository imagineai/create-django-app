<h1> Create Django App </h1>

One-line command to create a Django app with all the dependencies installed. 

<h2> Overview </h2>

- Run the following command in your terminal:
```
npm install -g imagine && imagine create -f django -n myapp 
```
(If you don't have npm installed, you'll need to [install this first](https://docs.npmjs.com/cli/v7/commands/npm-install).)

- You should see this:

```
abc
```


- You can now run your new Django app by running `cd myapp && imagine run`. 
- When you open http://127.0.0.1:8000/, you should see that the install worked successfully.

- Congrats! Your Django app is up and running!

- Now that you've created your new app, check out the `myapp.im` in your app directory - using this you can: 
  - easily change your app settings such as django server and package manager, API format etc.
  - add app functionality such as data models, APIs, storage etc using a simple config spec. 

- Learn more about how you can use Imagine to generate code at www.imagine.ai.

</br>
<h2> Detail </h2>

<h3> Easy to create </h3>

- Our one-line command allows your to get started with your Django app immediately, without worrying about installing dependencies or environment variables - we use commonly used env variables to help you get started with your app, so you can focusing on writing business logic.


- Our default environment variables when we create your django app are as follows: 
  - Server:                 dev
  - Package manager:        pipenv
  - Django models layout:   single-file
  - Project directory name: microservice
  - API format:             REST
  - Database:               sqlite
  - Database name:          myapp
       

<h3> Easy to configure </h3>

- If you want to change any of the above defaults for your app, its a piece of cake.

- Go to the myapp.im file in your directory, your should see the basic default settings here:

</br>

```
settings

app:
    # your application name
    name: myapp
    # choose one: [django, node]
    framework: django

django:
    # choose one: [pipenv, poetry]
    package-manager: pipenv
    # choose one: [gunicorn, uwsgi, dev]
    server: dev

    layout:
        # choose one: [single-file, separate-files]
        models: single-file
        # name of the project settings directory:
        project-dir: microservice

api:
    # choose one: [rest, graphql]
    format: rest

end settings

database taskmaster-db 
```
  
- You can replace the default settings with your preferences (based on the options allowed), and then run `imagine compile myapp.im` in your terminal. Your app and will be updated with the new settings


<h3> Easy to customize </h3>

- Not only can you change your app settings easily, you can also generated production-ready code using the `myapp.im` file. 


- Use Imagine's simple syntax to add [data models](www.imagine.ai/docs/model) and [CRUD APIs](www.imagine.ai/docs/api) to your Django app. 


- Run `imagine compile myapp.im` to see the generated code (PS - all our generated code has extensive coverage for end-to-end and unit tests).


- Enjoy!


