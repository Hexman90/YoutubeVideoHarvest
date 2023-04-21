# YoutubeVideoHarvest


## Video Demo:  <https://youtu.be/s51gnqLGHYQ>


## Description:
This Python program allows you to search for videos on YouTube and add them to a playlist. You can specify the channels to search for and the program will retrieve the most relevant videos and add them to a new or existing playlist.

## Usage
#### Adding Channels
The program will inform you whether or not you have channels in your list. If you have channels already in the list, the program will ask you if you want to delete a channel from the existing list. If you do not want to delete any channels from the list, you will be prompted to add channels by typing 'y'.

These channels will be stored in a file, so they can be used the next time you run the program.

The program will then ask if you want to add more channels. If you type 'n', and if you added channels, the program will continue and print the IDs of the channels to confirm that they have been found.

#### Deleting a Playlist
Next, if you previously created a playlist, the program will ask if you want to delete the playlist that you created the last time.

####Specifying Age of Videos
Next, the program will ask you for the maximum age of the videos you want to include in the playlist.

####Naming a Playlist
Then the program will ask you to name the playlist you want to create. If you haven’t created a playlist already or if you deleted the previously created playlist.

####Adding Videos to Playlist
Once you've provided a name, the program will create the playlist, search for videos that meet your criteria, sort them from newest to oldest, and add them to the playlist. Finally, the program will let you know how many videos have been added to the playlist.

## Prerequisites
### Youtube Api Key Configuration

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. If you're not already signed in, create an account and log in.
3. Create a new project by clicking on the "Select a Project" dropdown at the top of the page and clicking "New Project". Give it a name and click "Create".
4. Access the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard) and click "Enable APIs and Services". Search for "YouTube Data API v3" and enable it.
5. Head to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)  select "External", then click "Create". Provide your app's name, email address for "User support email", and email address for "Developer contact information". Finally, click "SAVE AND CONTINUE".
6. On the "Scopes" page select "ADD OR REMOVE SCOPES". Look for "YoutubeData API V3" and check the box next to ".../auth/youtube.force-ssl" scope. Click "UPDATE" and "SAVE AND CONTINUE".
7. On the "Test users" page, select "ADD USERS" and enter your email address. Then, click "ADD" and "SAVE AND CONTINUE".
8. Go to the [Credentials](https://console.cloud.google.com/apis/credentials) page and click "Create Credentials". Choose "OAuth client ID".
9. Pick "Web application" as the application type. Give it a name and add the authorized redirect URIs to your OAuth consent screen. For instance, enter "https://localhost:8080/" as the redirect URI. If you have a domain name, you can replace "localhost" with it. Click "Create".
10. Click "DOWNLOAD JSON" and save it in the root directory. Rename the file to "YOUR_CLIENT_SECRET_FILE.json".