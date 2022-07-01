# Deploy a Python (Django) web app with PostgreSQL, Blob Storage, and Managed Identity in Azure

https://github.com/vmagelo/msdocs-django-three-azure-services

This is a Python web app using the Django framework with three Azure services: Azure App Service, Azure Database for PostgreSQL relational database service, and Azure Blob Storage. This app is designed to be run locally and then deployed to Azure. Related: [Flask version](https://github.com/vmagelo/msdocs-flask-three-azure-services).

| Function      | Local Dev | Azure Hosted |
| ------------- | --------- | ------------ |
| Web app | runs locally, e.g., http://127.0.0.1:8000 | runs in App Service, e.g., https://\<app-name>.azurewebsites.net  |
| Database | Local PostgreSQL instance | Azure Database for PostgreSQL |
| Storage | Azure Blob Storage<sup>1</sup> or local emulator like [Azurite emulator for local Azure storage development](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite) | Azure Blob Storage |


<sup>1</sup>Current code can work with Azure Blob Storage accessed from local environment or Azurite (local storage emulator). The same environment variables STORAGE_ACCOUNT_NAME and STORAGE_CONTAINER_NAME in *.env* are used for both cases. The code figures out what to do for each case. And AzureDefaultCredential is used in both cases. Note: to use Azurite emulator, we need to run Django with SSL, which would require a certificate and adding some libraries. See [Tip 13](#tip-13-using-ssl) for using SSL. See [Tip 14](#tip-14-using-azurite) for using Azurite.

The Python app code doesn't change when moving from dev to Azure-hosted. All that changes is how the environment variables are set. With that in mind, there are two patterns for dealing with authentication:

|   | Local dev | Azure-hosted |
| - | --------- | ------------ |
| pattern&nbsp;1 | app service principal <br> add AZURE_CLIENT_ID, AZURE_TENANT_ID, and AZURE_CLIENT_SECRET to the *.env* file | app service principal <br> configure app settings for AZURE_CLIENT_ID, AZURE_TENANT_ID, and AZURE_CLIENT_SECRET |
| pattern&nbsp;2 | AD group, developer account<br> login in with `az login` | managed identity<br> configure as shown in [Authentication Azure-hosted app to Azure resources](https://docs.microsoft.com/en-us/azure/developer/python/sdk/authentication-azure-hosted-apps) |

The code doesn't change between pattern 1 and 2, only what goes into *.env* file in local dev case. We are primarily interested in pattern 2 and showing local authentication to Azure with developer account and authentication in Azure with a managed identity.

See [Tip 7](#tip-7) below for something to watch out for when using developer account.

Example screenshot:

![Example review list with images](/static/images/Example-reviews.png)

## Propagate Django changes?

Propagate changes in restaurant review app back to previous Django tutorials, including:

* csrf token use, don't use exempt in [views.py](./restaurant_review/views.py)
* use message passing to forms when there is an error (for add review and restaurant), see [views.py](./restaurant_review/views.py) for an example. Temporary error message is stored in session data.
* add check of forms looking for blank fields and raise error (for add review and restaurant)
* check render() lookup on url and make sure they are correct for error conditions, in some cases just use reverse()
* pull all CSS to [restaurants.css](./static/restaurant.css) and link to from base.html, should be no CSS in other templates

## Deployment

Create all Azure resources in the same group.

1. Set up App Service.
    * Set managed identity following [Auth from Azure-hosted apps](https://review.docs.microsoft.com/en-us/azure/developer/python/sdk/authentication-azure-hosted-apps)
    * Set managed identity as system-assigned
    * Assign role as "Storage Blob Data Contributor", so app service can connect to storage

1. Set up PostgreSQL
    * Add firewall rule so local machine can connect (necessary if you are creating table in VS Code, otherwise optional)
    * "Allow public access from any Azure service" as we did in previous tutorial. See [Tip 8](#tip-8-postgresql---firewalls)
    * Configure managed identity. ** See [Tip 9](#tip-9-managed-identity-with-azure-postgresql)

1. Set up Azure Storage.
    * Create container "photos".
    * Set container to "public read". This doesn't mean public write. The web app can write because of the assigned role.

1. Deploy the app with one of the methods: VS Code, local git, ZIP.
    * set app service configuration variables for: DBNAME, DBHOST, DBUSER, STORAGE_ACCOUNT_NAME, STORAGE_CONTAINER_NAME
    * ssh into app service
    * create the databases with `python manage.py migrate`

## Requirements

The [requirements.txt](./requirements.txt) has the following packages:

| Package | Description |
| ------- | ----------- |
| [Django](https://pypi.org/project/Django/) | Web application framework. |
| [pyscopg2-binary](https://pypi.org/project/psycopg-binary/) | PostgreSQL database adapter for Python. |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Read key-value pairs from .env file and set them as environment variables. In this sample app, those variables describe how to connect to the database locally. <br><br> This package is used in the [manage.py](./manage.py) file to load environment variables. |
| [whitenoise](https://pypi.org/project/whitenoise/) | Static file serving for WSGI applications, used in the deployed app. <br><br> This package is used in the [azureproject/production.py](./azureproject/production.py) file, which configures production settings. |
| [azure-blob-storage](https://pypi.org/project/azure-storage/) | Microsoft Azure Storage SDK for Python |
| [azure-identity](https://pypi.org/project/azure-identity/) | Microsoft Azure Identity Library for Python |

## How to run locally (without SSL)

Create a virtual environment. For SSL work, 3.9 version is best, especially with python-certifi-win32 package.

```dos
py -3.9 -m venv .venv
.venv/scripts/activate
```

In the virtual environment, install the dependencies.

```dos
pip install -r requirements.txt
```

Create the `restaurant` and `review` tables.

```dos
python manage.py migrate
```

Run the app.

```dos
python manage.py runserver
```

See [Tip 13](#tip-13-using-ssl) for running locally with SSL.

## Tips and tricks learned during development

### Tip 1: Migrations

When making [model.py](./restaurant_review/models.py) changes run `python manage.py makemigrations` to pick up those changes. For more information, see [django-admin and manage.py](https://docs.djangoproject.com/en/4.0/ref/django-admin/#makemigrations). Run `python manage.py migrate` after `makemigrations`.

### Tip 2: PostgreSQL commands

When creating a new PostgreSQL locally, for example with [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio/what-is-azure-data-studio?view=sql-server-ver15):

```dos
CREATE DATABASE <database-name>;
```

Or, with [psql.exe](https://www.postgresql.org/download/):

```dos
psql --username=<user-name> --password <password>

postgres=# CREATE DATABASE <database-name>;
postgres=# \c <database-name>
postgres=# \l
postgres=# \du
postgres=# \q
```

### Tip 3: Creating a GUID

To create an GUID in Python, use [UUIDField](https://docs.djangoproject.com/en/1.8/ref/models/fields/#uuidfield), which creates a universally unique identifier. When used with PostgreSQL, this stores in a **uuid** datatype.

```python
import uuid
from django.db import models

# model table column example
image_name = models.CharField(max_length=100, null=True)    

# create a uuid
uuid_str = str(uuid.uuid4()) 
```

CharField could be max length 32 (size of uuid) but doesn't hurt to make it bigger in case some other uuid that is longer is used.

### Tip 4: Storage container read access

To work with the Python SDK and Azure Blob Storage, see [Quickstart: Manage blobs with Python v12 SDK](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python).

Create container called *restaurants* and set access level to *Blob (anonymous read access for blobs only)*. It makes this example easier to have images public when **reading**. Could set up the example so that images are accessed through web app and not public, but this would require more coding and would complicate the presentation.

When **writing**, this should be done authenticated. Locally with authenticated Azure AD User or App service principal (registered app) with role. Deployed, with App service principal or managed identity.

### Tip 5: HTML input file

To work with the HTML input file, make sure the form tag has *encytype*.

```html
<form method="POST" action="{% url 'add_review' restaurant.id %}" enctype="multipart/form-data">
    <label for="reviewImage" class="form-label">Add a photo</label>
    <input type="file" class="form-control" id="reviewImage" 
           name="reviewImage" accept="image/png, image/jpeg">                    
</form>
```

The input tag *accept* attribute only filters what can be uploaded in the upload dialog box. It can easily be circumvented by changing the filter. A more rigorous check would be to use a library like [Pillow](https://pillow.readthedocs.io/en/stable/) in Python, or do some other checking in JavaScript before upload. This is beyond the scope of this sample app.

### Tip 6: Python message framework

This sample app uses the Django [messages framework](https://docs.djangoproject.com/en/4.0/ref/contrib/messages/). For example, to pass a message back if there is an error in a form submission (add restaurant, add review), do this:

```python
messages.add_message(request, messages.INFO, 
    'Restaurant not added. Include at least a restaurant name and description.')
return HttpResponseRedirect(reverse('create_restaurant'))  
```

In the template redirected to put:

```html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

The message backend is set in [settings.py](./azureproject/settings.py) with:

```python
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
```

This storage messages in session data. The default is cookie if the `MESSAGE_STORAGE` variable is not set.

Todo: Go back to simple passing of "error_message" variable to template. Should be sufficient and have less coding.

### Tip 7: Shared token cache issue

A big gotcha (that some may hit, I did) with using developer account in local dev is that you could get "SharedTokenCacheCredential: Azure Active Directory error '(invalid_grant) AADSTS500200" error even following instructions in how to use login in with developer account and `DefaultAzureCredential()`. It seems that there can be problems with SharedTokenCacheCredential in Visual Studio and this is the recommended solution:

```python
azure_credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
``` 
After doing that, I could sign in to Visual Studio code or use `az login` and my developer account worked. There looks to be a way to clear out your msal.cache but that seems extreme. References: [issue 16306](https://github.com/Azure/azure-sdk-for-net/issues/16306#issuecomment-724189313), [issue 16828](https://github.com/Azure/azure-sdk-for-python/issues/16828)

Another workaround, not recommended in general, is to just add to *.env* file AZURE_USERNAME and AZURE_PASSWORD to directly pass the values in. DefaultAzureCredential() without exclude flag will find the values in the *.env* file and use them.

Is there any harm on keeping `exclude_shared_token_cache_credential=True` when deploying?

### Tip 8: PostgreSQL - firewalls

We connect to PostgreSQL with DBNAME, DBHOST, and DBUSER passed as environment variables and used in [development.py](./azureproject/development.py) and [production.py](./azureproject/production.py) to set the [DATABASES variable expected by Django](https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-DATABASES). This is how we connect, but we must first be able to access the server. That's where networking and firewall rules come into play.

Some ways to deal with networking:

* **THIS IS WE WILL SHOW in TUTORIAL*** To allow code in App Service to access PostgreSQL, we set the "Allow public access from any Azure service" networking setting, which works but is a bit loose in terms of security. It allows access to all Azure services.

* Create a firewall rule to explicitly add all the outbound IPs of the Azure App Service. See [Create a firewall rule to explicitly allow outbound IPs](https://docs.microsoft.com/en-us/azure/mysql/howto-connect-webapp#solution-2---create-a-firewall-rule-to-explicitly-allow-outbound-ips). This is not a bad fallback to show or mention.

* There is a new way to create a PostgreSQL in it's own VPN and deal with security that way. This isn't generally available at this time.

### Tip 9: Managed Identity with Azure PostgreSQL

It's tricky. Trickier than managed identity with storage. The goal is to avoid having to specify a password and let Azure take care of it. Think about the previous App Service / PostgreSQL tutorial where we set DBPASS as a configuration parameter for the App Service. We want to avoid that.

Some references:

* [Azure databases](https://docs.microsoft.com/azure/app-service/tutorial-connect-msi-azure-database) in App Service documentation. Some things to watch out for:
   
     * Only seems to work with PostgeSQL single server. **Managed identity not supported for flexible?**
     * Commands in step 2 where you use psql to login in we never got to work. We did get access with Azure Data Studio. It could be that the token is too big for password field.

* [Configure Azure AD Integration](https://docs.microsoft.com/azure/postgresql/howto-configure-sign-in-aad-authentication) in the PostgreSQL documentation.

    * This article gives hint that [PGPASSWORD](https://www.postgresql.org/docs/current/libpq-envars.html) needs to be used when passing tokens for password because they are too long.
    * This article show how to set Azure Active Directory admin for PostgreSQL in the portal. So, in a tutorial, we would have at least instructions for portal and CLI.

* [Connect with Managed Identity](https://docs.microsoft.com/azure/postgresql/howto-connect-with-managed-identity) shows an C# example and gives insight into how the tokens are generated and what endpoint you call to get token.

The general challenge/problem with the references  is that they show manually creating connection strings. For Python, that is using package `psycopg2-binary` and calling `psycopg2.connect(conn_string)`. When we use frameworks like Django or Flask, the connection to the database is abstracted and handled for us via `DATABASES` global variable. This means a little more code to deal with tokens to refresh the password part of the `DATABASES` variable.  For example,

```python
import os
from azure.identity import DefaultAzureCredential
import django.conf as conf

def get_token():
    if 'WEBSITE_HOSTNAME' in os.environ:   
        azure_credential = DefaultAzureCredential()
        token = azure_credential.get_token("https://ossrdbms-aad.database.windows.net")
        conf.settings.DATABASES['default']['PASSWORD'] = token.token
    else:
        # Locally, read password from environment variable.
        conf.settings.DATABASES['default']['PASSWORD'] = os.environ['DBPASS']
    return
```

Then, there is the complicated process of setting up of PostgreSQL to use managed ID, which goes something like this (from the first reference above):

1. Grant a user account to be Active Directory Admin. (Portal or CLI)
1. Get application ID of the system-assigned identity. (Portal or CLI). 
    * In portal, you have to go to Active Directory resource, find the web application, and get this value.
1. Log in to the PostgreSQL database with the Active Directory Admin and create a new user and role. (Start from Portal or CLI)
    ```sql
    SET aad_validate_oids_in_tenant = off;
    CREATE ROLE <postgresql-user-name> WITH LOGIN PASSWORD '<application-id-of-system-assigned-identity>' IN ROLE azure_ad_user;
    ```
    For example, create a username like "webappuser" with the password as the application id of the system-assigned identity. This isn't at all obvious or intuitive, but that's how it works.

    You can log in with psql (via cloud shell is easiest), Azure Data Studio, or any tool that manages PostgreSQL.

    In the connection string, be careful with username. It has to be webappuser@postgresql-server-name.

1. In the App Service set the configuration setting `DBUSER=webappuser`. There is no `DBPASS` setting. (Portal, VS Code, or CLI)

### Tip 10: Refactor settings files

Before, we had just settings.py and production.py. Now, we have [settings.py](./azureproject/settings.py) - common to all environments, [development.py](./azureproject/development.py) - for the dev or local environment, and [production.py](./azureproject/production.py) - for production / deployment. 

> **_NOTE:_**  In the process of doing this, a circular reference was introduced but not noticed. So, debug=true for local environment was fine. But only debug=true would work in production, which is a no-no. With debug=false, kept getting 500 error with no explanation in the logs.  `ALLOWED_HOSTS` not set appropriately can be a common 500 error in production. But after ruling that out, we were at wits' end until we found this [StackOverflow answer](https://stackoverflow.com/questions/4970489/what-could-cause-a-django-error-when-debug-false-that-isnt-there-when-debug-tru) about circular references, which saved the day.

### Tip 11: WhiteNoise static file serving

We decided to use WhiteNoise for both local and deployed web app. See [Using WhiteNoise in development](http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development). It makes it easier to have all `INSTALLED_APPS` and `MIDDLEWARE` in the base settings.py file.

With WhiteNoise, you may see this kind of warning in the deployment logs: "/tmp/8da29e2cb651a79/antenv/lib/python3.9/site-packages/whitenoise/base.py:115: UserWarning: No directory at: /tmp/8da29e2cb651a79/staticfiles/". This isn't a blocker as explained by this [GitHub issue](https://github.com/evansd/whitenoise/issues/215). 

When running WhiteNoise, you could spend a lot of time troubleshooting errors and missing images. In particular, when `Debug=True` used in production (a no-no, but just for testing), certain errors are masked and the web app works fine. Set `Debug=False` and suddenly you have a broken web app returning 500.

* `STATICFILES_STORAGE` has a bunch of possible options. When set to `whitenoise.storage.CompressedStaticFilesStorage` you are using WhiteNoise and `python manage.py collectstatic` needs to be run. When deploying through Visual Studio Code, that is the case. The `SCM_DO_BUILD_DURING_DEPLOYMENT` setting is `1/true` in this case.

     * See [Customize build automation](https://docs.microsoft.com/azure/app-service/configure-language-python#customize-build-automation): when manage.py is found, then `manage.py collectstatic` is run unless `DISABLE_COLLECTSTATIC` is set to `true`.

* When running locally, you can also use `whitenoise.storage.CompressedStaticFilesStorage` but you have to then run `python manage collectstatic` yourself. Locally, it's easier to just use `django.contrib.staticfiles.storage.StaticFilesStorage`.

* See the [Troubleshooting WhiteNoise backend](http://whitenoise.evans.io/en/stable/django.html#troubleshooting-the-whitenoise-storage-backend) for more tips.

* If you get the error 'ValueError: Missing staticfiles manifest entry for …' try running `python manage.py findstatic --verbosity 2 filename` in the SSH of the App Service.

* For `STATICFILES_STORAGE` we don't need the `Manifest` part, which is overkill for sample. The `Compressed` part of class name just create .gz files in static file location. 

### Tip 12: Troubleshooting deployment

Here are things to try:

* Test first locally `python manage.py runserver` if you've made coding changes, even if you think they are not a problem. It will save a bad deploy and time wasted if you have a syntax error or coding problem.

* After deployment (say from Visual Studio Code, which is generally the easiest), check the deployment logs. At first, you see two entries for "pending". When those become one "success" entry the deployment is done. This is generally the same time that Visual Studio Code reports back that the deployment is done. However, it still may take an additional few minutes for the code to really make it to the App Service. 

* Keep the log stream open in a browser tab. Check that the container creation didn't fail, which happens if you have a coding error. If container builds, hit the web site and then check the log stream. Print statements can help here.

* Note that for troubleshooting [DEBUG_PROPAGATE_EXCEPTIONS](https://docs.djangoproject.com/en/4.0/ref/settings/#debug-propagate-exceptions) can be useful to switch to True.

* `Debug = False` should be always on for production settings, but for troubleshooting, setting to `True` may help if you're stuck. In particular, if your code has a circular import, it will only be flagged when `Debug=False`. 

* Read the Django tips on the [Oryx GitHub page](https://github.com/microsoft/Oryx/wiki/Django-Tips). Oryx is the build system used to compile Django source code into runnable artifacts in App Service.

### Tip 13: Using SSL

The steps for getting SSL to run are roughly this:

Step 1: Install [mkcert](https://github.com/FiloSottile/mkcert). Run it and create a certificate. The alternative if you don't use it is that your browser will keep showing warning.

```
mkcert --install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 
```

Step 2: Add TLS (SSL) capabilities to the local development environment, add the [django-sslserver](https://pypi.org/project/django-sslserver/) package:

```
pip install django-sslserver
```

Step 3: Use machine CA certificates. (Only do this with Python 3.9 or perhaps earlier. Did not work in Python 3.10)

```
pip install python-certifi-win32
```

Step 4: Change the run command to:

```
 python manage.py runsslserver --certificate cert.pem --key key.pem
```
### Tip 14: Using Azurite

We recommend using [Azurite](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite) from the command line to emulate blob storage that can be used by the web app. (Using it from Visual Studio Code with an extension is easier, but couldn't get past SSL problems. Plus, running from command line is more general and can potentially reach more users.)

```dos
azurite-blob ^
    --location "<folder-path>" ^
    --debug "<folder-path>\debug.log" ^
    --oauth basic ^
    --cert "<project-root>\cert.pem" ^
    --key "<project-root\key.pem"
```
