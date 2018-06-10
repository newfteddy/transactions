from django.shortcuts import render
from django.views.generic import TemplateView
import sys
sys.path.append('../backend/plots/')
from plot import plot_show


# Create your views here.

def insert_map():
    left_symbol = '<td class="map">'
    with open("./pages/templates/index.html", "r") as index:
        index_str = "".join(index.readlines())

    with open("../backend/plots/map.html", "r") as map:
        map_str = "".join(map.readlines())

    map_str = map_str[map_str.index("<script type"):map_str.index("</body></html>")]
    left = index_str[:index_str.index(left_symbol)+len(left_symbol)]
    tmp = index_str[index_str.index(left_symbol)+len(left_symbol):]
    right = tmp[tmp.index("</td>"):]
    index_str = left+'\n'+map_str+'\n'+right
    with open("./pages/templates/index.html", "w") as index:
        index.write(index_str)
    index.close()

def insert_text(text):
    left_symbol = '<div id="text_field">'
    with open("./pages/templates/index.html", "r") as index:
        index_str = "".join(index.readlines())

    left = index_str[:index_str.index(left_symbol)+len(left_symbol)]
    tmp = index_str[index_str.index(left_symbol)+len(left_symbol):]
    right = tmp[tmp.index("</div>"):]
    index_str = left+'\n'+text+'\n'+right
    with open("./pages/templates/index.html", "w") as index:
        index.write(index_str)

    index.close()

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    def post(self, request, **kwargs):
        data = request.POST

        if ('arrival' in data) and ('destination' in data) and ('date' in data) and (len(data['date']) > 0):
            arrival, destination, date, thresholds = data['arrival'], data.getlist('destination'), data['date'], data['thr']
            d, m, y = date.split('.')
            config = {
                "airport_from": destination,
                "airport_to": arrival,
                "date": "{}-{}-{}".format(y, m, d),
                "thr": thresholds
            }
            # try:
            text = plot_show(config)
            # insert_map()
            # insert_text(text)
            # #except: pass

            return render(request, 'index.html', context=None)

        return render(request, 'index.html', context=None)