{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Investigating Grandslam Tennis Tournements from 2014-2016."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Alana Woloshin <br>\n",
    "Data Gathering -> Used read_csv for base dataset and then scrapped off wikipedia using beautiful soup.<br>\n",
    "Data cleaning -> Used various regex's and grouped by in several places. Applied a handmade function, and used various other regex methods like to lower and replace. <br>\n",
    "Data manipulation -> Joined various dataframes as well as created an sql database to store the most relevant information. Also used various stack and unstack methods with aggregation functions <br> \n",
    "Data reporting -> Included three sophisticated graphs each delievering important information, built a computational narrative building in markdown cells with code. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### First off, we need to make sure we import all the correct modules needed to complete this analysis as well as connect to our local SQL server "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "%matplotlib inline\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "from urllib.request import urlopen\n",
    "import psycopg2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "##sql information\n",
    "%reload_ext sql\n",
    "#%load_ext sql\n",
    "%sql postgres://jovyan:si330studentuser@localhost:5432/si330\n",
    "host=\"localhost\"\n",
    "dbname=\"si330\"\n",
    "user=\"jovyan\"\n",
    "password=\"si330studentuser\"\n",
    "\n",
    "conn = psycopg2.connect(host=host,dbname=dbname, user=user, password=password)\n",
    "conn.autocommit=True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### In order to analyze the data and make interesting conclusions, I extract the desired years and find only the grand slam tournements. The data set was found on kaggle and will be read into a pandas dataframe"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "match = pd.read_csv(\"datasets/match_scores_project.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>tourney_slug</th>\n",
       "      <th>tourney_round_name</th>\n",
       "      <th>round_order</th>\n",
       "      <th>match_order</th>\n",
       "      <th>winner_name</th>\n",
       "      <th>winner_player_id</th>\n",
       "      <th>loser_name</th>\n",
       "      <th>loser_player_id</th>\n",
       "      <th>winner_seed</th>\n",
       "      <th>loser_seed</th>\n",
       "      <th>match_score_tiebreaks</th>\n",
       "      <th>winner_sets_won</th>\n",
       "      <th>loser_sets_won</th>\n",
       "      <th>winner_games_won</th>\n",
       "      <th>loser_games_won</th>\n",
       "      <th>winner_tiebreaks_won</th>\n",
       "      <th>loser_tiebreaks_won</th>\n",
       "      <th>year</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>year</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>2014</td>\n",
       "      <td>australian-open</td>\n",
       "      <td>Finals</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Stan Wawrinka</td>\n",
       "      <td>w367</td>\n",
       "      <td>Rafael Nadal</td>\n",
       "      <td>n409</td>\n",
       "      <td>8</td>\n",
       "      <td>1</td>\n",
       "      <td>63 62 36 63</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>21</td>\n",
       "      <td>14</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2014</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2014</td>\n",
       "      <td>australian-open</td>\n",
       "      <td>Semi-Finals</td>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>Rafael Nadal</td>\n",
       "      <td>n409</td>\n",
       "      <td>Roger Federer</td>\n",
       "      <td>f324</td>\n",
       "      <td>1</td>\n",
       "      <td>6</td>\n",
       "      <td>76(4) 63 63</td>\n",
       "      <td>3</td>\n",
       "      <td>0</td>\n",
       "      <td>19</td>\n",
       "      <td>12</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>2014</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2014</td>\n",
       "      <td>australian-open</td>\n",
       "      <td>Semi-Finals</td>\n",
       "      <td>2</td>\n",
       "      <td>2</td>\n",
       "      <td>Stan Wawrinka</td>\n",
       "      <td>w367</td>\n",
       "      <td>Tomas Berdych</td>\n",
       "      <td>ba47</td>\n",
       "      <td>8</td>\n",
       "      <td>7</td>\n",
       "      <td>63 67(1) 76(3) 76(4)</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>26</td>\n",
       "      <td>22</td>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>2014</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2014</td>\n",
       "      <td>australian-open</td>\n",
       "      <td>Quarter-Finals</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>Rafael Nadal</td>\n",
       "      <td>n409</td>\n",
       "      <td>Grigor Dimitrov</td>\n",
       "      <td>d875</td>\n",
       "      <td>1</td>\n",
       "      <td>22</td>\n",
       "      <td>36 76(3) 76(7) 62</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>23</td>\n",
       "      <td>20</td>\n",
       "      <td>2</td>\n",
       "      <td>0</td>\n",
       "      <td>2014</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2014</td>\n",
       "      <td>australian-open</td>\n",
       "      <td>Quarter-Finals</td>\n",
       "      <td>3</td>\n",
       "      <td>2</td>\n",
       "      <td>Stan Wawrinka</td>\n",
       "      <td>w367</td>\n",
       "      <td>Novak Djokovic</td>\n",
       "      <td>d643</td>\n",
       "      <td>8</td>\n",
       "      <td>2</td>\n",
       "      <td>26 64 62 36 97</td>\n",
       "      <td>3</td>\n",
       "      <td>2</td>\n",
       "      <td>26</td>\n",
       "      <td>25</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2014</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "         tourney_slug tourney_round_name  round_order  match_order  \\\n",
       "year                                                                 \n",
       "2014  australian-open             Finals            1            1   \n",
       "2014  australian-open        Semi-Finals            2            1   \n",
       "2014  australian-open        Semi-Finals            2            2   \n",
       "2014  australian-open     Quarter-Finals            3            1   \n",
       "2014  australian-open     Quarter-Finals            3            2   \n",
       "\n",
       "        winner_name winner_player_id       loser_name loser_player_id  \\\n",
       "year                                                                    \n",
       "2014  Stan Wawrinka             w367     Rafael Nadal            n409   \n",
       "2014   Rafael Nadal             n409    Roger Federer            f324   \n",
       "2014  Stan Wawrinka             w367    Tomas Berdych            ba47   \n",
       "2014   Rafael Nadal             n409  Grigor Dimitrov            d875   \n",
       "2014  Stan Wawrinka             w367   Novak Djokovic            d643   \n",
       "\n",
       "     winner_seed loser_seed match_score_tiebreaks  winner_sets_won  \\\n",
       "year                                                                 \n",
       "2014           8          1           63 62 36 63                3   \n",
       "2014           1          6           76(4) 63 63                3   \n",
       "2014           8          7  63 67(1) 76(3) 76(4)                3   \n",
       "2014           1         22     36 76(3) 76(7) 62                3   \n",
       "2014           8          2        26 64 62 36 97                3   \n",
       "\n",
       "      loser_sets_won  winner_games_won  loser_games_won  winner_tiebreaks_won  \\\n",
       "year                                                                            \n",
       "2014               1                21               14                     0   \n",
       "2014               0                19               12                     1   \n",
       "2014               1                26               22                     2   \n",
       "2014               1                23               20                     2   \n",
       "2014               2                26               25                     0   \n",
       "\n",
       "      loser_tiebreaks_won  year  \n",
       "year                             \n",
       "2014                    0  2014  \n",
       "2014                    0  2014  \n",
       "2014                    1  2014  \n",
       "2014                    0  2014  \n",
       "2014                    0  2014  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "match['year'] = match['tourney_year_id'].str.extract('(?P<Year>201[456])')\n",
    "filtered_match = match[match['year'].notnull()]\n",
    "#dropping columns I do not need for my analysis\n",
    "filtered_match = filtered_match.drop(['tourney_order','tourney_year_id','tourney_url_suffix',\n",
    "                                      'match_stats_url_suffix','winner_slug','loser_slug','match_id'], axis=1)\n",
    "filtered_match = filtered_match.set_index(filtered_match[\"year\"])\n",
    "grandslams = [\"australian-open\",\"roland-garros\", \"wimbledon\", \"us-open\"]\n",
    "\n",
    "grandslamdf = filtered_match[filtered_match[\"tourney_slug\"].isin(grandslams)]\n",
    "\n",
    "grandslamdf.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Something Interesting about Tennis is the occurance of upsets, I investigated the percentage of upsets per year and tournement to see if there was a specific combination that led to an increase of upsets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 3 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "def perc_upset(Y):\n",
    "    upsets = Y[Y['loser_seed'] < Y['winner_seed']]\n",
    "    return (len(upsets)/len(grandslamdf))\n",
    "upsets = grandslamdf.reset_index(drop=True).groupby([\"tourney_slug\",\"year\"]).apply(perc_upset).unstack().plot.bar(subplots = True)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Conclusion: It was found consistent that roland-garros and wimbeldon have the highest upset rates, but no specific year provided greater upsets. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Going to investigate the winners now and see if they preformed better on different surfaces, in order to investigate this I webscraped information off wikipedia using BeautifulSoup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Australian Open</th>\n",
       "      <th>French Open</th>\n",
       "      <th>Wimbeldon</th>\n",
       "      <th>US Open</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>year</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>2016</td>\n",
       "      <td>Novak Djokovic (11/16)</td>\n",
       "      <td>Novak Djokovic (12/16)</td>\n",
       "      <td>Andy Murray (3/3)</td>\n",
       "      <td>Stan Wawrinka (3/3)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2017</td>\n",
       "      <td>Roger Federer (18/20)</td>\n",
       "      <td>Rafael Nadal (15/19)</td>\n",
       "      <td>Roger Federer (19/20)</td>\n",
       "      <td>Rafael Nadal (16/19)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2018</td>\n",
       "      <td>Roger Federer (20/20)</td>\n",
       "      <td>Rafael Nadal (17/19)</td>\n",
       "      <td>Novak Djokovic (13/16)</td>\n",
       "      <td>Novak Djokovic (14/16)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019</td>\n",
       "      <td>Novak Djokovic (15/16)</td>\n",
       "      <td>Rafael Nadal (18/19)</td>\n",
       "      <td>Novak Djokovic (16/16)</td>\n",
       "      <td>Rafael Nadal (19/19)</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             Australian Open             French Open               Wimbeldon  \\\n",
       "year                                                                           \n",
       "2016  Novak Djokovic (11/16)  Novak Djokovic (12/16)       Andy Murray (3/3)   \n",
       "2017   Roger Federer (18/20)    Rafael Nadal (15/19)   Roger Federer (19/20)   \n",
       "2018   Roger Federer (20/20)    Rafael Nadal (17/19)  Novak Djokovic (13/16)   \n",
       "2019  Novak Djokovic (15/16)    Rafael Nadal (18/19)  Novak Djokovic (16/16)   \n",
       "\n",
       "                     US Open  \n",
       "year                          \n",
       "2016     Stan Wawrinka (3/3)  \n",
       "2017    Rafael Nadal (16/19)  \n",
       "2018  Novak Djokovic (14/16)  \n",
       "2019    Rafael Nadal (19/19)  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "url = \"https://en.wikipedia.org/wiki/List_of_Grand_Slam_men%27s_singles_champions\"\n",
    "r = requests.get(url)\n",
    "soup = BeautifulSoup(r.text,'html.parser')\n",
    "tables = soup.find(\"table\", class_=\"wikitable sortable\")\n",
    "\n",
    "table_rows = tables.find_all('tr')\n",
    "\n",
    "res = []\n",
    "for tr in table_rows:\n",
    "    td = tr.find_all('td')\n",
    "    row = [tr.text.strip() for tr in td if tr.text.strip()]\n",
    "    if row:\n",
    "        res.append(row)\n",
    "df = pd.DataFrame(res, columns=[\"year\", \"Australian Open\", \"French Open\", \"Wimbeldon\",\"US Open\"])\n",
    "df.set_index(\"year\").tail(4)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "###### Djovak can win anywhere, Nadal has increased wins in France and US."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Investigating the surfaces for each venue, using beautiful soup,"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "      tourney_slug                  time-period      venue surface\n",
      "0  australian-open              mid/lateJanuary  Melbourne    Hard\n",
      "1    roland-garros          late May/early June      Paris    Clay\n",
      "2        wimbledon         late June/early July     London   Grass\n",
      "3          us-open  late August/early September   New York    Hard\n"
     ]
    }
   ],
   "source": [
    "url = \"https://en.wikipedia.org/wiki/Grand_Slam_(tennis)\"\n",
    "r = requests.get(url)\n",
    "soup = BeautifulSoup(r.text,'html.parser')\n",
    "table = soup.find('table',{'class',\"wikitable\"})\n",
    "\n",
    "table_rows = table.find_all('tr')\n",
    "\n",
    "res = []\n",
    "for tr in table_rows:\n",
    "    td = tr.find_all('td')\n",
    "    row = [tr.text.strip() for tr in td if tr.text.strip()]\n",
    "    if row:\n",
    "        res.append(row)\n",
    "\n",
    "\n",
    "df = pd.DataFrame(res, columns=[\"tourney_slug\", \"time-period\", \"venue\", \"surface\",\"e\",\"f\",\"g\",\"h\",\"i\"])\n",
    "df = df.drop(['e','f','g','h','i'], axis=1)\n",
    "df['venue'] = df['venue'].str.extract(',(?P<venue>[A-Z][a-z]+ ?[A-Z]?[a-z]+)')\n",
    "df['tourney_slug'] = df['tourney_slug'].str.lower()\n",
    "df['tourney_slug'] = df['tourney_slug'].str.replace(\" \",\"-\")\n",
    "df['tourney_slug'] = df['tourney_slug'].str.replace(\"french-open\",\"roland-garros\")\n",
    "#in the original df french open was named roland-garros\n",
    "# must get the columns to match so we can merge them now.\n",
    "\n",
    "print(df)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### I merged the two tables and got the value counts for each winner per tournement. In order to see the disparites in tournement wins per player, I aggregated the sum and the standard deviation.\n",
    "#### I found it would be most interesting to investigate players that had over 15 wins, with a standard deviation greater than two. To visualize this data, I made a stacked horizantal bar chart"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x7f622bb09278>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "grandslamdf = pd.merge(grandslamdf,df,left_on='tourney_slug',right_on='tourney_slug', how=\"outer\")\n",
    "counts_table = grandslamdf.groupby('tourney_slug')['winner_name'].value_counts().transpose().unstack().fillna(0)\n",
    "new = counts_table.agg([np.sum,np.std]).transpose()\n",
    "new = new[(new[\"std\"] > 2) & (new[\"sum\"] > 15)]\n",
    "grandslamdf[(grandslamdf['winner_name']).isin(new.index)].groupby('tourney_slug')['winner_name'].value_counts().transpose().unstack().fillna(0).T.plot(kind='barh', stacked=True)\n",
    "#make sure to descirbe the narrative \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### I wanted to see the mean and std of winner sets,loser sets, winner games and loser games won per tournement. It is interesting to see how many more losers win at different tournements, and the standard deviations there. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x7f622ac07128>"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "tourney_s = grandslamdf.drop([\"round_order\",\"match_order\",\"winner_tiebreaks_won\",\"loser_tiebreaks_won\"],axis=1)\n",
    "tourney_s = tourney_s.set_index(grandslamdf[\"tourney_slug\"]).groupby(level = 0).agg([np.mean,np.std])\n",
    "tourney_s.plot()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### To conclude and make this project reusable, I entered all of the players data, along with games won to a database. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "winners = grandslamdf[\"winner_name\"].unique()\n",
    "count = grandslamdf[\"winner_name\"].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * postgres://jovyan:***@localhost:5432/si330\n",
      "Done.\n",
      "Done.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "%%sql\n",
    "DROP TABLE IF EXISTS players;\n",
    "CREATE TABLE IF NOT EXISTS players (player varchar(40),\n",
    "                        games_won integer, \n",
    "                        PRIMARY KEY (player));"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * postgres://jovyan:***@localhost:5432/si330\n",
      "355 rows affected.\n",
      " * postgres://jovyan:***@localhost:5432/si330\n",
      "10 rows affected.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table>\n",
       "    <tr>\n",
       "        <th>player</th>\n",
       "        <th>games_won</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Novak Djokovic</td>\n",
       "        <td>71</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Andy Murray</td>\n",
       "        <td>59</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Stan Wawrinka</td>\n",
       "        <td>52</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Roger Federer</td>\n",
       "        <td>47</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Tomas Berdych</td>\n",
       "        <td>42</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Milos Raonic</td>\n",
       "        <td>37</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Kei Nishikori</td>\n",
       "        <td>36</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Jo-Wilfried Tsonga</td>\n",
       "        <td>36</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Marin Cilic</td>\n",
       "        <td>34</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "        <td>Rafael Nadal</td>\n",
       "        <td>32</td>\n",
       "    </tr>\n",
       "</table>"
      ],
      "text/plain": [
       "[('Novak Djokovic', 71),\n",
       " ('Andy Murray', 59),\n",
       " ('Stan Wawrinka', 52),\n",
       " ('Roger Federer', 47),\n",
       " ('Tomas Berdych', 42),\n",
       " ('Milos Raonic', 37),\n",
       " ('Kei Nishikori', 36),\n",
       " ('Jo-Wilfried Tsonga', 36),\n",
       " ('Marin Cilic', 34),\n",
       " ('Rafael Nadal', 32)]"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "sql_string = \"insert into players(player,games_won) values\"\n",
    "for i in count.index:\n",
    "    sql_string +=\"('\"+i+\"',\" + str(count[i]) + '),'\n",
    "sql_string = sql_string[0:-1]\n",
    "%sql $sql_string\n",
    "%sql select * from players LIMIT 10; "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
