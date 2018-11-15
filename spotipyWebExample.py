import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError


# In order to run this, you need to run the following in the terminal:
# 
# export SPOTIPY_CLIENT_ID='e72315dd83024d248af8f29c4819852f'
# export SPOTIPY_CLIENT_SECRET='af4478f67fa740e8ac1af99a6ab5c894'
# export SPOTIPY_REDIRECT_URI='http://localhost/'
#
# Then you call the program with username like:
#
# python3 spotipywebexample.py 1259108252


# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# User ID:   	   1259108252
# Client ID:  	   e72315dd83024d248af8f29c4819852f
# Client Secret:   af4478f67fa740e8ac1af99a6ab5c894


# Erase cache and prompt for user permission
try:
	token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

# Create our spotifyObject with permissions
spotifyObject = spotipy.Spotify(auth=token)

# Get current device
devices = spotifyObject.devices()
deviceID = devices['devices'][0]['id']

# Current track information
track = spotifyObject.current_user_playing_track()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

if artist != "":
	print("Currently playing " + artist + " - " + track)

# User information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

# Loop
while True:
	# Main Menu
	print()
	print(">>> Welcome to Spotipy " + displayName + "!")
	print()
	print("0 - Exit")
	print("1 - Search for an artist")
	print()
	choice = input("Your choice: ")

	# Search for the artist
	if choice == '0':
		break


	# End the program
	if choice == '1':
		print()
		searchQuery = input("Ok, what's their name?: ")
		print()

		# Get search results
		searchResults = spotifyObject.search(searchQuery,1,0,"artist")

		# Artist details
		artist = searchResults['artists']['items'][0]
		print(artist['name'])
		print(str(artist['followers']['total']) + " followers")
		print(artist['genres'][0])
		print()
		webbrowser.open(artist['images'][0]['url'])
		artistID = artist['id']

		# Album Details
		trackURIs = []
		trackArt = []
		z = 0

		# Extract Album Data
		albumResults = spotifyObject.artist_albums(artistID)
		albumResults = albumResults['items']

		for item in albumResults:
			print("ALBUM " + item['name'])
			albumID = item['id']
			albumArt = item['images'][0]['url']

			# Extract track data
			trackResults = spotifyObject.album_tracks(albumID)
			trackResults = trackResults['items']

			for item in trackResults:
				print(str(z) + ": " + item['name'])
				trackURIs.append(item['uri'])
				trackArt.append(albumArt)
				z += 1
			print()

		# See album art
		while True:
			songSelection = input("Enter a song number to see the album art and play the song (x to exit)")
			if songSelection == 'x':
				break
			trackSelectionList = []
			trackSelectionList.append(trackURIs[int(songSelection)])
			spotifyObject.start_playback(deviceID, None, trackSelectionList) 
			webbrowser.open(trackArt[int(songSelection)])	


# print(json.dumps(VARIABLE, sort_keys=True, indent=4))