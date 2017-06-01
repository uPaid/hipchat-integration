# hipchat-integration

Integrations server for HipChat

## Table of Contents

* [Installation](#installation)
  * [Requirements](#requirements)
  * [Deployment](#deployment)
  * [Running the app](#running-the-app)
    * [Example](#example)
* [Building your own integration](#building-your-own-integration)
  * [Rules](#rules)
  * [Example integration](#example-integration)
  * [Data persistance](#data-persistance)
    * [Saving and loading the storage](#saving-and-loading-the-storage)
    * [Erasing the storage](#erasing-the-storage)
  * [Configuration in the HipChat UI](#configuration-in-the-hipchat-ui)

## Installation

### Requirements

The application requires following dependencies:

* [Python version 3.5+](https://www.python.org/downloads/)
* Python packages:
 * [http](https://docs.python.org/3/library/http.server.html) as a base for application
 * [importlib](https://docs.python.org/3/library/importlib.html) for dynamic calls to integrations
 * [requests](http://docs.python-requests.org/en/master/) for sending data to HipChat server
 * [json](https://docs.python.org/2/library/json.html) for serialization
 * [re](https://docs.python.org/2/library/re.html) for regex matching
 * [threading](https://docs.python.org/2/library/threading.html) to run integrations in parallel
* [zlib](https://docs.python.org/2/library/zlib.html) (optional) for easy application deployment
 * note that installation is tricky, see [this link](https://stackoverflow.com/a/15013895/5922757) for more info

### Deployment

If zlib is installed, deployment to a server is fairly easy.

1. compress cloned project to .zlib:
```bash
git clone "https://github.com/uPaid/hipchat-integration.git"
cd "hipchat-integration"
zip -r "hipchat-integration.zip" *
```

2. send the package to your server:
```bash
scp "hipchat-integration.zip" username@my.server.com:"/opt/app/hipchat-integration/"
```

3. run the application on your server ([ARGS] are application arguments):
```bash
ssh username@my.server.com "python3 /opt/app/hipchat-integration/hipchat-integration.zip [ARGS]"
```

### Running the app

If arguments are invalid, application will print the following message:

> Usage: python3 'hipchat-integration.zip' [PORT] [INTEGRATIONS_PATH] [INTEGRATION_NAME:INTEGRATION_TOKEN...]

Arguments must be provided in the following order:
* **PORT** - the port for application to listen on
* **INTEGRATIONS_PATH** - the path where integrations scripts are stored at
* **INTEGRATION_NAME:INTEGRATION_TOKEN...** - a list of tokens in one of the following formats:
 * **TOKEN_NAME:TOKEN_VALUE** - a global token
 * **ROOM_ID:INTEGRATION_NAME:TOKEN_VALUE** - integration-specific token (*ROOM_ID* must be numerical)

For more details please refer to the [HipChat dokumentation on tokens](https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens).

#### Example:

```bash
python3 hipchat-integration.zip 8000 ./integrations \
    1234:test:2YotnFZFEjr1zCsicMWpAA \
    send_message:2YotnFZFEjr1zCsicMWpAA
```

The application will:
* listen on port 8000
* look for available integrations in directory *integrations*
* store two tokens:
 * token assigned to a room with if *1234* and integration *test* in that room
 * global token called *send_message*

## Building your own integration:

### Rules

The integration must follow the rules below:
* must be in the **INTEGRATIONS_PATH** of application
* must be a Python script with name ending with *.py*
* must be interpretable by Python interpreter in version 3.5 or higher
* must define a **run_integration** function with the following arguments:
 * **notification** *(notification.Notification)* - the [object sent by HipChat API](https://www.hipchat.com/docs/apiv2/webhooks#room_message)
 * **query** *(str)* - integration command's contents
 * **all_tokens** *(dict)* - all tokens passed to the application
 * **token** *(str)* - token for the current
 * **storage** *(dict)* - volatile, integration-specific storage that can be used to persist data (note that it is kept in memory and will be erased if the application is killed, please refer to the [data persistance](#data-persistance) section of this manual for more details)
 * **log** *(server.Logger)* - a utility that can be used for printing the output in place of the *print()* function

### Example integration

An example integration can be found [here](https://github.com/uPaid/hipchat-integration/blob/master/example/example.py).

### Data persistance

Just like any Python script, your integration can save data to a local file.
Although if the data is not too important, it can be saved to the volatile application storage.

To put a variable in the storage, call `storage[key] = variable` from your integration.

To retrieve a variable from the storage, call `variable = storage[key]` from your integration.

Keep in mind that if the is is not found in the storage, a `KeyError` will be raised.

#### Saving and loading the storage

The storage can be saved or loaded to or from a file by sending a HTTP POST request to the application:
 * `save [FILE]` will save serialized storage to a given file
 * `load [FILE]` will load and deserialize storage from a given file

Example:
`curl -X POST -d "save storage.txt" "http://my.server.com:8000"`

Keep in mind that the data is serialized with the *json.dumps()* function, so if any non-persistable objects are in the storage, an error will be raised. Data is also deserialized using the *json.loads()* function, which means that any complex object will be casted to a *dict*.

#### Erasing the storage

The storage can also be easily erased by sending a HTTP POST request with only `erase` text to the application.

Example:
`curl -X POST -d "erase" "http://my.server.com:8000"`

### Configuration in the HipChat UI

You can configure your integration with just a few easy steps:
1. go to https://upaid.hipchat.com/addons
2. select your room
3. click "Build your own integration"
4. give a name to your integration
5. add a slash command to your integration
 * enter the name of your command, for example `/test`
 * add the url to your server, for example `http://my.server.com:8000`
6. press *Save*

All you have to do now is create your integration script, for example *integrations/test.py* and run the application with the token provided by HipChat.
