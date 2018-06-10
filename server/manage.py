#!/usr/bin/env python
import os
import sys
sys.path.append('../backend/plots/')
from init_plot import plot_show

def insert_map():
    left_symbol = '<td class="map">'
    with open("./pages/templates/index.html", "r") as index:
        index_str = "".join(index.readlines())

    with open("../backend/plots/init_map.html", "r") as map:
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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverapp.settings")
    #plot_show()
    # insert_map()
    # insert_text('')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

