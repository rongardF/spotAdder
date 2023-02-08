# Youtube liked videos adder into Spotify

This is code based on the tutorial from Youtube that teaches about Youtube and Spotify APIs.

This code does not function as it fails when trying to extract song and artist name. This is most likely because of
some changes in the `youtube_dl` library. Issue is not fixed.

If trying to use this code then two additional files are required for using both Youtube and Spotify APIs:
	- **secrets.py** that would contain the Spotify client ID and secret
	- **credentials.json** that would contain the Youtube API credentials

Tutorial youtube video link: https://www.youtube.com/watch?v=7J_qcttfnJA