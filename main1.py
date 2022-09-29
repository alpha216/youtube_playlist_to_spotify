import spotipy, requests, json, urllib, asyncio, aiohttp
import logging, logging.config
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic



class hello():
    def __init__(self) -> None:
        self.fail = open('fail.txt', 'w')


    async def fetch(self, session, i, uris = None):
        try:
            logger.debug(f"{i[0]} by {i[1]}")
            
            if uris != None:
                api_link = f'https://api.spotify.com/v1/playlists/{info["Spotify_playlist"]}/tracks?uris={uris}'
                
                async with session.post(api_link, headers=header) as response:
                    if not response.status == 201:
                        logger.warn(f"{i} - Bad Request")
                                # Bad Request
                        await asyncio.sleep(2)
                        async with aiohttp.ClientSession() as session:
                            return await self.fetch(session, i, ids)
                    else: logger.debug(f"{i} {response.status}")
                return
                
            res = spotify.search(f"{i[0]} {i[1]}", type="track")

            if res is None or len(res.get("tracks", {}).get("items", [])) == 0:
                logger.debug(f'failed to finding {i}')
                self.fail.write(i)
            else:
                ids = res['tracks']['items'][0]['uri']
                logging.debug(f'added : {i} - {ids}')
                
                api_link = f'https://api.spotify.com/v1/playlists/{info["Spotify_playlist"]}/tracks?uris={ids}'
            
                async with session.post(api_link, headers=header) as response:
                    if not response.status == 201:
                        logger.warn(f"{i} - Bad Request")
                                # Bad Request
                        await asyncio.sleep(2)
                        async with aiohttp.ClientSession() as session:
                            return await self.fetch(session, i, ids)
                    else: logger.debug(f"{i} {response.status}")

        except Exception as e:  # Timeout
            logger.error(e)
            await asyncio.sleep(2)
            async with aiohttp.ClientSession() as session:
                await self.fetch(session, i, ids)

    def crowls(self, url: str):
        logger.debug('connecting to youtube music')
        ytmusic: YTMusic = YTMusic('headers_auth.json')
        logger.debug('connected')
        pl = ytmusic.get_watch_playlist(playlistId=url, limit=500)

        content = [[pl['tracks'][i]['title'], pl['tracks'][i]['artists'][0]['name']] for i in range(0, len(pl['tracks']))]
        logger.debug('finished')
        logger.debug(str(content))
        return content
    
    async def main(self):
        # [['Daydream', 'Kenshi Yonezu'], ['for lovers who hesitate', 'JANNABI']]
        loop = asyncio.get_event_loop()
        name_list = await loop.run_in_executor(None, self.crowls, info["Youtube_playlist"])
        # name_list = await self.crowls(info["Youtube_playlist"])
        logger.debug(str(name_list))
        logger.debug('Starting Requests')
        # Requests
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(
                    # feach(['Daydream', 'Kenshi Yonezu'])
                    *(self.fetch(session, i) for i in name_list)
                )


if __name__ == "__main__":
    # Logger Setup
    with open('logging.json', 'rt') as f: config = json.load(f)
    open("./info.log", 'w').close()
    logging.config.dictConfig(config)
    logger = logging.getLogger()

    new = hello()
    info = json.loads(open('./info.json').read())
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=info["client_id"], client_secret=info['client_secret']))
    header = {"Accept": "application/json", "Content-Type": "application/json",
              "Authorization": f"Bearer {info['token']}"}
    logger.debug('start')
    asyncio.run(new.main())
    logger.debug('finished')

