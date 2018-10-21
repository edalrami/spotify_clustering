import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import pandas as pd
from pandas import DataFrame

username = sys.argv[1];

print(username)

try: 
	token = util.prompt_for_user_token(username)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username)

spotifyObject = spotipy.Spotify(auth=token)

category_ids = []
category_names = []
playlist_ids = [] 
playlist_names = []


playlist_song_names = []
playlist_song_popularities = []
playlist_song_ids = []
playlist_song_dates_added_to_playlist = []
playlist_song_durations = []


playlist_song_artist_names = []
playlist_song_artist_ids = []

playlist_song_album_names = []
playlist_song_album_release_dates = []
playlist_song_album_ids = []


## audio features

audio_acousticnesses = []
audio_danceabilities = []
audio_energies = []
audio_instrumentalnesses = []
audio_keys = []
audio_livenesses = []
audio_loudnesses = []
audio_modes = []
audio_speechinesses = []
audio_tempos = []
audio_time_signatures = []
audio_valences = []


user = spotifyObject.current_user()
displayName = user['display_name']

followers = user['followers']['total']

while True:
  print()
  print(">>> Welcome to Spotipy " + displayName + "!")
  print(">>> You have " + str(followers) + " followers!")
  print()
  print("1 - Search for an artist")
  print("2 - Create csv of category plalists")
  print("3 - exit")
  print()
  choice = input("Your choice: ")
  if choice == "1":
    print("1")
    searchQuery = input("Ok, what is the artist's name?:")
    print()

    # get search results
    searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
    #print(json.dumps(searchResults, sort_keys=True, indent=4))

    artist = searchResults['artists']['items'][0]
    artist_name = artist['name']
    artist_followers = artist['followers']['total']
    artist_genres = artist['genres']
    artist_album_artwork_urls = artist['images'][0]['url']
    artist_id = artist['id']

    print(f"We found {artist_name}.\n{artist_name} has {artist_followers} followers\n{artist_name} creates music with {artist_genres} genres.")
    webbrowser.open(artist_album_artwork_urls)
    # search for 1 artist with an offest of 0

    # album and track details
    trackURIs = []
    trackArt = []
    ii = 0
    # extract album data
    albumResults = spotifyObject.artist_albums(artist_id)
    albumResults = albumResults['items']
    #print(json.dumps(albumResults, sort_keys=True, indent=4))


    for album in albumResults:
      print(album['name'])
      album_id = album['id']
      album_art = album['images'][0]['url']

      # Extract Track data
      trackResults = spotifyObject.album_tracks(album_id)
      #print(json.dumps(trackResults, sort_keys=True, indent=4))
      trackResults = trackResults['items']
      for track in trackResults:
        track_info = spotifyObject.audio_features([track['id']])
        #print(json.dumps(track_info, sort_keys=True, indent=4))
        print(f"{ii} : {track['name']}")
        trackURIs.append(track['uri'])
        trackArt.append(album_art)
        ii+=1
      print()

    # View album art
    while True:
      songSelection = input("Enter a song number to see the album art or x to exit")
      if songSelection == "x":
        break;
      webbrowser.open(trackArt[int(songSelection)]);
  if choice == "2":
    print("2")
    categories = spotifyObject.categories(limit = 50)
    categories = categories['categories']['items'];

    ## Get all categories 
    for ii, category in enumerate(categories):
      category_id = category['id']
      category_name = category['name']
      category_ids.append(category_id)
      category_names.append(category_name)
      ii += 1
      if ii < 10:
        print(f"{ii}  : {category_name}")
      else:
        print(f"{ii} : {category_name}")
    ## Get all playlists from each category
    for ii, category_id in enumerate(category_ids):
      category_playlists = spotifyObject.category_playlists(
        category_id = category_id,
        limit = 50)
      category_playlists = category_playlists['playlists']['items']
      for category in category_playlists:
        playlist_id = category['id']
        owner_id = category['owner']['id']
        playlist_name = category['name']
        playlist_ids.append(playlist_id)
        playlist_names.append(playlist_name)
        if ii < 10:
          print(f"{ii}  : {playlist_name}")
        else:
          print(f"{ii} : {playlist_name}")
        if ii == 7 or ii == 18:
          continue;
    next_playlist = False;
    for ii, playlist_id in enumerate(playlist_ids):
      if ii < 10:
        print(f"{ii}  : Fetching {playlist_names[ii]}")
      else:
        print(f"{ii} : Fetching {playlist_names[ii]}")
      playlist = spotifyObject.user_playlist_tracks(
        owner_id,
        playlist_id = playlist_id)
      playlist = playlist['items']
      for track in playlist:
        #print(json.dumps(track, sort_keys=True, indent=4))
        # try:
        track_name = track['track']['name']
        # except ValueError:
        #   next_playlist = True;
        #   break;
        playlist_song_names.append(track_name)
        playlist_song_popularities.append(track['track']['popularity'])
        playlist_song_ids.append(track['track']['id'])
        playlist_song_dates_added_to_playlist.append(track['added_at'])
        playlist_song_durations.append(track['track']['duration_ms'])
        playlist_song_artist_names.append(track['track']['artists'][0]['name'])
        #playlist_song_artist_ids.append(track['track']['artists'][0]['id'])
        playlist_song_album_names.append(track['track']['album']['name'])
        playlist_song_album_release_dates.append(track['track']['album']['release_date'])
        #playlist_song_album_ids.append(track['track']['album']['id'])
      if next_playlist:
        continue
      #print(f"playlist_song_ids:\n{playlist_song_ids}")
      audio_features = spotifyObject.audio_features(playlist_song_ids)
      
      if audio_features is None:
        print(f"This one is broken")
        continue;

      for audio_feature in audio_features:
        if audio_feature is None:
          next_playlist = True;
          break;
        #print(json.dumps(audio_feature, sort_keys=True, indent=4))
        if audio_feature.get('acousticness'):
          audio_acousticness = audio_feature['acousticness']         
        else:
          next_playlist = True;        

        if audio_feature['danceability'] is None:
          next_playlist = True;
        else:
          audio_danceability = audio_feature['danceability']

        if audio_feature['energy'] is None:
          next_playlist = True;
        else:
          audio_energy = audio_feature['energy']

        if audio_feature['instrumentalness'] is None:
          next_playlist = True;
        else:
          audio_instrumentalness = audio_feature['instrumentalness']

        if audio_feature['key'] is None:
          next_playlist = True
        else:
          audio_key = audio_feature['key']

        if audio_feature['liveness'] is None:
          next_playlist = True;
        else:
          audio_liveness = audio_feature['liveness']

        if audio_feature['loudness'] is None:
          next_playlist = True;
        else:
          audio_loudness = audio_feature['loudness']

        if audio_feature['mode'] is None:
          next_playlist = True
        else:
          audio_mode = audio_feature['mode']

        if audio_feature['speechiness'] is None:
          next_playlist = True;
        else:
          audio_speechiness = audio_feature['speechiness']

        if audio_feature['tempo'] is None:
          next_playlist = True;
        else:
          audio_tempo = audio_feature['tempo']

        if audio_feature['time_signature'] is None:
          next_playlist = True;
        else:
          audio_time_signature = audio_feature['time_signature']
        
        if audio_feature['valence'] is None:
          next_playlist = True;
        else:
          audio_valence = audio_feature['valence']

        if next_playlist:
          break;
        audio_acousticnesses.append(audio_acousticness)
        audio_danceabilities.append(audio_danceability)
        audio_energies.append(audio_energy)
        audio_instrumentalnesses.append(audio_instrumentalness)
        audio_keys.append(audio_key)
        audio_livenesses.append(audio_liveness)
        audio_loudnesses.append(audio_loudness)
        audio_modes.append(audio_mode)
        audio_speechinesses.append(audio_speechiness)
        audio_tempos.append(audio_tempo)
        audio_time_signatures.append(audio_time_signature)
        audio_valences.append(audio_valence)
      if not next_playlist:
        if ii < 10:
          print(f"{ii}  : Finished {playlist_names[ii]}")
        else:
          print(f"{ii} : Finished {playlist_names[ii]}")

        print(f"\tsong_name              : {len(playlist_song_names)}")
        print(f"\tsong_popularity        : {len(playlist_song_popularities)}")
        print(f"\tdate_added_to_playlist : {len(playlist_song_dates_added_to_playlist)}")
        print(f"\tsong_duration_ms       : {len(playlist_song_durations)}")
        print(f"\tartist_name            : {len(playlist_song_artist_names)}")
        print(f"\talbum_names            : {len(playlist_song_album_names)}")
        print(f"\talbum_release_date     : {len(playlist_song_album_release_dates)}")
        print(f"\tacousticness           : {len(audio_acousticnesses)}")
        print(f"\tdanceability           : {len(audio_danceabilities)}")
        print(f"\tenergy                 : {len(audio_energies)}")
        print(f"\tinstrumentalness       : {len(audio_instrumentalnesses)}")
        print(f"\tkey                    : {len(audio_keys)}")
        print(f"\tliveness               : {len(audio_livenesses)}")
        print(f"\tloudness               : {len(audio_loudnesses)}")
        print(f"\tmode                   : {len(audio_modes)}")
        print(f"\tspeechiness            : {len(audio_speechinesses)}")
        print(f"\ttempo                  : {len(audio_tempos)}")
        print(f"\ttime_signature         : {len(audio_time_signatures)}")
        print(f"\tvalence                : {len(audio_valences)}")

        playlist_df = DataFrame(data={
          'song_name'              : playlist_song_names,
          'song_popularity'        : playlist_song_popularities,
          'date_added_to_playlist' : playlist_song_dates_added_to_playlist,
          'song_duration_ms'       : playlist_song_durations,
          'artist_name'            : playlist_song_artist_names,
          'album_names'            : playlist_song_album_names,
          'album_release_date'     : playlist_song_album_release_dates,
          'acousticness'           : audio_acousticnesses,
          'danceability'           : audio_danceabilities,
          'energy'                 : audio_energies,
          'instrumentalness'       : audio_instrumentalnesses,
          'key'                    : audio_keys,
          'liveness'               : audio_livenesses,
          'loudness'               : audio_loudnesses,
          'audio_mode'             : audio_modes,
          'speechiness'            : audio_speechinesses,
          'tempo'                  : audio_tempos,
          'time_signature'         : audio_time_signatures,
          'audio_valence'          : audio_valences
          })
        # Save the data to a csv
        file_name  = str(playlist_names[ii]).replace("/" , "")
        file_name_and_path = f"playlists/{file_name}"
        playlist_df.to_csv(file_name_and_path)

      playlist_song_names = []
      playlist_song_popularities = []
      playlist_song_ids = []
      playlist_song_dates_added_to_playlist = []
      playlist_song_durations = []
      playlist_song_artist_names = []
      playlist_song_album_names = []
      playlist_song_album_release_dates = []
      audio_acousticnesses = []
      audio_danceabilities = []
      audio_energies = []
      audio_instrumentalnesses = []
      audio_keys = []
      audio_livenesses = []
      audio_loudnesses = []
      audio_modes = []
      audio_speechinesses = []
      audio_tempos = []
      audio_time_signatures = []
      audio_valences = []

  if choice == "3":
    break