import argparse
from sys import argv
from bs4 import BeautifulSoup

def scrapPlaylist( html ):

    soup = BeautifulSoup( html, 'html.parser' )
    
    videoTags = soup.find_all('ytd-playlist-video-renderer')

    videos = []
    for videoTag in videoTags:
        title = videoTag.find(id="video-title").text.replace("\n          ", '').replace("\n        ", '')
        channel = videoTag.find(id="tooltip").text.replace("\n  \n    ", '').replace("\n  \n", '')

        videos.append( [title, channel] )

    return videos

if __name__ == "__main__":
    
    programDescriptor = "Create a .csv file with title and channel name from a .html file from a Youtube playlist"

    parser = argparse.ArgumentParser( description=programDescriptor )

    parser.add_argument( '-f', action='store', help='The .html file from the playlist', nargs=1)
    parser.add_argument( '-o', action='store', help='The output file name', nargs=1, default='playlist.csv' )
        
    args = parser.parse_args()
    
    if( args.f == None ):
        raise RuntimeError("An .html file from the playlist must be passed.")
    
    fileName = args.f[0]
    outputFileName = args.o[0] if type(args.o) == type([]) else args.o

    html = ""
    with open( fileName, 'r') as fileHtml:
        html = fileHtml.read()
    playlist = scrapPlaylist( html )

    with open( outputFileName, 'w') as playlistFile:
        playlistStr = '\n'.join( [ video[0] + " ("+ video[1]+ ")" for video in playlist ] )
        playlistFile.write( playlistStr )
