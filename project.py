from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import datetime
import csv



def main():
    credentials = creds()
    youtube = build("youtube", "v3", credentials=credentials)
    existing_channels = get_existing_channels()
    if existing_channels:
        remove_existing_channel(existing_channels)
    channels_id_title = add_new_channel(youtube)
    write_channels_to_file(channels_id_title, existing_channels)
    playlist_id = delete_previous_playlist(youtube)
    video_ids = search_videos(youtube)
    if not playlist_id:
        playlist_id = create_playlist(youtube)
    add_videos_to_playlist(playlist_id, video_ids, youtube)
    print(f"Added {len(video_ids)} videos to the playlist.")


# Get credentials to connect to the API 
def creds():
    # Path to secret file
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    # Check if secret file exists
    if os.path.exists(client_secrets_file):
        # Disable OAuthlib's HTTPS verification when running locally.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Get credentials and create an API client
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
        flow.run_local_server()
        credentials = flow.credentials
    else:
        print("'YOUR_CLIENT_SECRET_FILE.json' file does not exist. Please create the secret file!")
        print("Or if it is created place it in the root directory")
        exit(1)
    return credentials


# Delete the previous created playlist. (id stored in the .txt file)
def delete_previous_playlist(youtube):
    # Check if the previous playlist id is stored in txt file
    if not os.path.exists('Playlist_ID.txt'):
        return
    # If it is ask user if wants the previous playlist to be deleted
    else:
        # Read the playlist id from the file
        with open('Playlist_ID.txt') as file:
            previous_playlist_id = file.read()
        if previous_playlist_id:
            prompt = ""
            # Get user input to delete the playlist or not
            while prompt.lower() not in ["y", "n"]:
                prompt = input("Delete the previous playlist? (y/n)")
                
            # If yes delete the previous created playlist
            if prompt.lower() == "y":
                    request = youtube.playlists().delete(id = previous_playlist_id)
                    # Send the request to the API and handle the errors if the response returned an error
                    query_api(request)
                    # Let the user know that the playlist has been deleted
                    print("Previously created playlist was deleted...")
                    return

        # Else return the previous created playlist id
        return previous_playlist_id    


# Check if user already has saved channels to search for
def get_existing_channels():
    # Check if there are channels stored in txt file
    if os.path.exists("channels.csv"):
        # If txt file exists get the channels stored
        with open("channels.csv") as file:
            reader = csv.DictReader(file)
            existing_channels = [row["Title"] for row in reader]
        # Let the user know what channels if any there are stored in the file
        if len(existing_channels) == 0:
            print("Currently you have no channels in the list.")
        else:
            print(f"Currently you have these channels in the list:\n{existing_channels}")
        return existing_channels
    print("Currently you have no channels in the list.")
    return     


# Delete or get the previous playlist
def remove_existing_channel(existing_channels):
    # Ask user if wants to delete a channel from the existing list
    while True:
        prompt = input("Would you like to delete an existing channel? (y/n): ")
        if prompt.lower() == "y":
            # Prompt user for the name/s of the channel/s the be removed from the existing list
            name = input("Name of the channel/s to be deleted from the list (separated by comma): ")
            # Split the input string by comma and remove any whitespace
            names = [n.strip() for n in name.split(',')]
            # Check if the channels exist in the list of existing channels
            invalid_channels = [n for n in names if n not in existing_channels]
            if invalid_channels:
                print(f"The following channels do not exist in the list: {', '.join(invalid_channels)}.")
            else:
                # Read the channels from the file, and store the channels that don't 
                with open("channels.csv") as file:
                    reader = csv.DictReader(file)
                    channels = [row for row in reader if row["Title"] not in names]

                # Write the updated list of channels to the file
                with open("channels.csv", "w", newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Title", "ID"])
                    writer.writeheader()
                    writer.writerows(channels)
                # Let user know that the channels have been deleted
                print(f"The following channels have been deleted from the list: {', '.join(names)}")
        # If user doesn't want to delete a channel from the existing list break
        elif prompt.lower() == "n":
            break
        else:
            print("Invalid input. Please enter y/n.")


 
# If user wants to add more channels to search get the channels
def add_new_channel(youtube):
    channels_id_title = {}
    # Ask user if wants to add more channels to the list
    while True:
        prompt = input("Would you like to add more channels? (y/n): ")
        # If the user wants to add a channel to the list:
        if prompt.lower() == "y":
            # Prompt user for the name of the channel to be added to the list
            name = input("Name of the channel/s (separated by comma): ")
            # Split the input string by comma and remove any whitespace
            names = [n.strip() for n in name.split(',')]
            # Api request variable
            for name in names:
                request = youtube.search().list(
                    q=name,
                    type='channel',
                    part='id,snippet',
                    maxResults=1
                    )
                # Send the request to the API
                response = query_api(request)
                # If a channel is found, get the title and it's id
                if response["items"]:
                    title_id = {response["items"][0]["snippet"]["title"]: response['items'][0]['id']['channelId']}
                    channels_id_title.update(title_id) 
                # Else let the user know that the channel has not been found               
                else:
                    print(f'No channels found with username: {name}')
        # If the user doesn't want to add a channel to the list return the channels already added
        elif prompt.lower() == "n":
            if channels_id_title:
                added_channels = [channel for date, channel in channels_id_title.items()]
                print(added_channels)
            return channels_id_title
        else:
            print("Invalid input. Please enter y/n.")


# Write all channels to the csv file
def write_channels_to_file(channels_id_title, existing_channels):
    # If there are channels that have to be added to the list add them
    if channels_id_title:
        # Add to the file, or if the file doesn't exist create it
        with open("channels.csv", "a+", newline="") as file:
            file.seek(0)
            rows = len(file.read().strip())
            # Initiate the variable to store the header of the file
            writer = csv.DictWriter(file, fieldnames=["Title", "ID"])
            # Chack if the file is empty. and if it is write the header
            if rows == 0:  
                writer.writeheader()
            # Write the channels to the csv file it the channel doesn't exist already
            for title, id in channels_id_title.items():
                if existing_channels and title not in existing_channels:
                        writer.writerow({"Title": title, "ID": id})
                else:
                    writer.writerow({"Title": title, "ID": id})
    return



# Search for videos in the channels listed above, and adds them all up in a sorted order, from the latest video uploaded.
def search_videos(youtube):
    # Searches for videos no more than n days old in every channel.
    video_age = prompt_age()
    age = (datetime.datetime.now() - datetime.timedelta(days=video_age)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Get the channels ids
    all_channels = get_channels_id()
    # Initiate a variable to stroe the uploading dates and the videos ids
    dates_and_ids = {}
    # Loop trough all the channels and request the ip for the videos that have no more than the "age"
    for channel in all_channels:
        request = youtube.search().list(
            part="snippet",
            channelId= channel,
            maxResults=25,
            order="date",
            publishedAfter=age,
            type="video",
            videoType="any"
        )
        # Send the request to the API
        response = query_api(request)
        # Get the date and id of the videos from the api response
        date_and_id = {items["snippet"]['publishedAt']: items["id"]["videoId"] for items in response["items"]}
        # Store all the dates and ids of the videos from the api response to the dictionary above
        dates_and_ids.update(date_and_id)
    # Sorting the videos by uploading date in decreasing order.
    sorted_dates_ids = sorted(dates_and_ids.items(), key=lambda x: x[0], reverse=True)
    # Get just the video id's from the sorted list
    vid_id = [item[1] for item in sorted_dates_ids]
    return vid_id


# Get the channels ids 
def get_channels_id():
    # Open the file and read the ids of the channels
    with open("channels.csv") as file:
            reader = csv.DictReader(file)
            # Store the channels ids
            all_channels = [row["ID"] for row in reader]
    return all_channels

# Prompt user for the age of the videos
def prompt_age():
    while True:
        try:
            age = int(input("Enter maximum age of videos to search for (in days): "))
            if age >= 0:
                return age
            else:
                print("Please enter a number greather than 0.")
        except ValueError:
            print("Please enter a number.")
        return age


# Create new playlist
def create_playlist(youtube):
    # Prompt user for the name of the playlist
    playlist_name = input("Name of the Playlist to be created: ")
    # Send a request to the API to create the playlist
    request = youtube.playlists().insert(
        part="snippet",
        body={"snippet": {
                "title": playlist_name,
                "description": "A new playlist created using the YouTube API"
            }
        }
    )
    # Send the request to the API
    response = query_api(request)
    # Get the playlist id from the response
    playlist_id = response['id']
    # Write the PlaylistId in 'Playlist_ID.txt' file.
    with open('Playlist_ID.txt', 'w') as file:
        file.write(playlist_id)
    return playlist_id


# Add the videos to the playlist
def add_videos_to_playlist(playlist_id, video_ids, youtube):
    print("Adding videos to the playlist...")
    # For every video in the video_ids list send a request to the API to add the video to the playlist
    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        # Send the request to the API
        query_api(request)


# Send the request to the API and handle the errors if the response returned an error
def query_api(request):
    
    try:      
        response = request.execute()
    except HttpError as error:
        if "quotaexceeded" in str(error).lower():
            print("\n\u001b[44mAPI usage limit for the day exceeded.\u001b[0m\n")
            exit(1)
        else:
            print(str(error))
            exit(1)
    return response



if __name__ == "__main__":
    main()






