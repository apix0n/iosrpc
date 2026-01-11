# iosrpc

A simple Flask server that receives API requests and sets the user's Discord Presence as the sent data.

## Installation

1. Clone the Git repository or download it from [here](https://github.com/apix0n/iosrpc/archive/main.zip)
2. Install the dependencies with `pip install -r .\requirements.txt`

## Usage

0. Create a Discord Application in the [Discord Developer Portal](https://discord.com/developers/applications)

1. Copy your Applicaiton ID and set it as the `CLIENT_ID` environment variable
    > You can also create a `.env` file with the content looking like `CLIENT_ID=0123456789`.

2. Start the Python server with `python .\presence.py`

3. Create an iOS Shortcut
   1. Add a `Get Current App` action
   2. Add a `Get Contents of URL` action
      1. Set the URL path as `http://yourcomputerip/update`
      2. Set the method as POST
      3. Add a `Content-Type` header with value `application/json`
      4. Add in the request body the values
        - `app_name` = Current App (Name)
        - `bundle_id` = Current App (Bundle Identifier) 
         > Will be used to fetch the icon from iTunes servers
        - `use_timer` (boolean) / Optional
        - `device_name` = Text / Optional

4. Create an Automation set to launch every time you open/close apps of your choice the shortcut you made

## More

- Note the server includes a `/clear` route that removes the current app presence

### made by [apix](https://github.com/apix0n) with ❤️