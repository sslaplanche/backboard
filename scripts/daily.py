import pandas as pd
import isodate

from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.live.nba.endpoints import scoreboard, boxscore

from utils import cacheify, fp

@cacheify(cache_filename="DailySummary.json")
def fetch_data():
    # Fetch: Entire league player averages
    player_averages = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed='PerGame').get_data_frames()[0]

    # Fetch: Todays games boxscores
    todays_game_ids = [ game['gameId'] for game in scoreboard.ScoreBoard().games.get_dict() ]
    boxscores = [
        boxscore.BoxScore(game_id=game_id).get_dict()['game']
        for game_id in todays_game_ids
    ]

    # CLEAN DATA
    players = []
    for box in boxscores: 
        for team in [box['homeTeam'], box['awayTeam']]:
            player_team = {
                'id': team['teamId'],
                'name': team['teamName'],
                'tricode': team['teamTricode'],
                'score': team['score'],
            }
            opp_team = {
                'id': box['awayTeam']['teamId'] if player_team['name'] == box['homeTeam']['teamName'] else box['homeTeam']['teamId'],
                'name': box['awayTeam']['teamName'] if player_team['name'] == box['homeTeam']['teamName'] else box['homeTeam']['teamName'],
                'tricode': box['awayTeam']['teamTricode'] if player_team['name'] == box['homeTeam']['teamName'] else box['homeTeam']['teamTricode'],
                'score': box['awayTeam']['score'] if player_team['name'] == box['homeTeam']['teamName'] else box['homeTeam']['score'],
            }

            for today_player in team['players']:
                
                new_player = {
                    'id': today_player['personId'],
                    'first_name': today_player['firstName'],
                    'last_name': today_player['familyName'],
                    'game_status': box['gameStatusText'] if box['gameStatus'] == 2 else '',
                    'team': player_team,
                    'opp_team': opp_team,
                    'holder': None,
                }

                new_player.update({
                    'sec': isodate.parse_duration(today_player['statistics']['minutes']).total_seconds(),
                    'min': "{:02d}:{:02d}".format(int(isodate.parse_duration(today_player['statistics']['minutes']).total_seconds() / 60), int(isodate.parse_duration(today_player['statistics']['minutes']).total_seconds() % 60)),
                    'pts': today_player['statistics']['points'],
                    'reb': today_player['statistics']['reboundsTotal'],
                    'ast': today_player['statistics']['assists'],
                    'stl': today_player['statistics']['steals'],
                    'blk': today_player['statistics']['blocks'],
                    'tov': today_player['statistics']['turnovers'],
                })
                new_player.update({ 'fp': round(fp(new_player), 2) })

                season_player_df = player_averages[player_averages['PLAYER_ID'] == int(today_player['personId'])]
                if len(season_player_df) > 0:
                    new_player.update({
                        'sec_pg': season_player_df['MIN'].values[0] * 60,
                        'pts_pg': season_player_df['PTS'].values[0],
                        'reb_pg': season_player_df['REB'].values[0],
                        'ast_pg': season_player_df['AST'].values[0],
                        'stl_pg': season_player_df['STL'].values[0],
                        'blk_pg': season_player_df['BLK'].values[0],
                        'tov_pg': season_player_df['TOV'].values[0],
                        'fp_pg': round(fp({
                            'pts': season_player_df['PTS'].values[0],
                            'reb': season_player_df['REB'].values[0],
                            'ast': season_player_df['AST'].values[0],
                            'stl': season_player_df['STL'].values[0],
                            'blk': season_player_df['BLK'].values[0],
                            'tov': season_player_df['TOV'].values[0],
                        }), 2)
                    })

                players.append(new_player)

    # ORGANISE DATA
    players = sorted(players, key=lambda x: x['fp'], reverse=True)

    # Add new column for fp/sec
    for player in players:
        if player['sec'] == 0:
            player['fp_min'] = None
        else:
            player['fp_min'] = round(player['fp'] / player['sec'] * 60, 2)

    df = pd.DataFrame(players)

    df = df[df['sec'] > 900] # Only players who played at least 15 minutes

    return df.to_dict(orient='records')