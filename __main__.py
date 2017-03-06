from flask import Flask, request, render_template
import tweepy
from textblob import TextBlob
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='lastps', api_key='cB0kWozoTEjQDZJpCUhP')


def Gauge_Printer():
    base_chart = {
        "values": [40, 10, 10, 10, 10, 10, 10],
        "labels": ["-", "0", "20", "40", "60", "80", "100"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }
    meter_chart = {
        "values": [50, 10, 10, 10, 10, 10],
        "labels": ["BS Level", "Minimal", "A Tad", "Skeptical", "A lot", "BULLS***"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(240,248,255)',
                'rgb(176,224,230)',
                'rgb(0,191,255)',
                'rgb(30,144,255)',
                'rgb(0,0,128)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }
    layout = {
        'xaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': 'M 0.235 0.5 L 0.24 0.65 L 0.245 0.5 Z',
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': '50',
                'showarrow': False
            }
        ]
    }

    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0

    fig = {"data": [base_chart, meter_chart],
           "layout": layout}
    py.iplot(fig, filename='gauge-meter-chart')
app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        search = request.form['search_query']
        if not search:
            return render_template('index.html')
        consumer_key = "8ncrufW2yEegl2KcjI8EwPBbM"
        consumer_secret = "TUcy90RkQDg34ovJxeSPfDTrfNRVunVRE8LkH44vSocwZs5Fiu"
        access_token = "726689466-rcGLxjPt7mu7DedKlsGFHJmJdfRh6GaVh6eXPF9E"
        access_token_secret = "uCYc0MuoKGpTaal6SdLXXFqLEu9OJbBvPKNtd13QjhFC4"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        tweets_not_subjective = []
        tweets_subjective = []
        tweets_positive = []
        tweets_negative = []
        overall_sentiment = ""
        overall_subjectivity = ""
        sentiment_array = []
        subjectivity_array = []
        count1, count2, counter_positive, counter_negative, counter_subjective, counter_objective = 0, 0, 0, 0, 0, 0
        search_term = ""
        tweets_public = api.search(q=search, count=100, lang ="en")
        for tweets in tweets_public:
            # print(tweets.text)
            # print(tweets.created_at)
            sent = TextBlob(tweets.text)
            # print(sent.sentiment)
            sentiment_array.append(sent.sentiment.polarity)
            subjectivity_array.append(sent.sentiment.subjectivity)
            if sent.sentiment.subjectivity < 0.5 and counter_objective <= 5:
                tweets_not_subjective.append(tweets)
                counter_objective += 1
            elif sent.sentiment.subjectivity > 0.5 and counter_subjective <= 5:
                tweets_subjective.append(tweets)
                counter_subjective += 1
            if sent.sentiment.polarity > 0.0 and counter_positive <= 5:
                tweets_positive.append(tweets)
                counter_positive += 1
            elif sent.sentiment.polarity < 0.0 and counter_positive <= 5:
                tweets_negative.append(tweets)
                counter_negative += 1
            count1 += sent.sentiment.subjectivity
            count2 += sent.sentiment.polarity

        average1 = count1 / 100.0
        average2 = count2 / 100.0
        if average1 > 0.5:
            overall_sentiment = "a lot of "
        elif average1 <0.5:
            overall_sentiment = "minimal"
        elif average1 == 0.5:
            overall_sentiment = "a bit of"
        if average2 > 0:
            overall_sentiment = "negatively"
        elif average2 <0:
            overall_sentiment = "positively"
        elif average2 == 0:
            overall_sentiment = "neutral"
        trace0 = go.Scatter(
            x=sentiment_array,
            y=subjectivity_array,
            mode='markers',
            name='markers'
        )

        layout = go.Layout(
            title='',
            xaxis=dict(
                title='Positivity',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Subjectivity',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
        # trace1 = go.Scatter(
        #   k = [0],
        #  f = [0.3]
        # )
        data = [trace0]
        # Plot and embed in ipython notebook!
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='', auto_open=False)
####        Gauge_Printer()
        return render_template('index.html', tweets_plus=tweets_positive, tweets_minus=tweets_negative, tweets_fact=tweets_not_subjective, tweets_unfact=tweets_subjective, sub_overall=overall_subjectivity, sent_overall=overall_sentiment)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)