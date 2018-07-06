curl -o tmp.json https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&TimeRange=LAST_3_DAYS
See https://github.com/HearthSim/HSReplay.net/blob/d35dcdaa00d00f275cebfbebc73defc53b78b64f/hsreplaynet/static/scripts/src/filters.d.ts for possible values
cp tmp.json lineupSolver/win_rates/{filename}.json
edit json_win_rates.py
python lineup_generator_conquest.py sim "Recruit Hunter, Shudderwock Shaman, Even Warlock, Taunt Druid" "Token Druid, Odd Paladin, Even Shaman, Zoo Warlock"
