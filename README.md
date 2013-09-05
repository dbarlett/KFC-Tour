KFC-Tour
========
![Screenshot of tour plotted on OpenStreetMap basemap](http://i.imgur.com/20Mg7YI.png)

Optimal tours of KFC locations, via the [Concorde](http://www.math.uwaterloo.ca/tsp/concorde/index.html) cutting-plane-based exact TSP solver.
Inspired by a [Hacker News comment](https://news.ycombinator.com/item?id=6324462).

Tested on Ubuntu 12.10 64-bit.

Installation & usage:
```bash
pip install -r requirements.txt
wget http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/linux24/concorde.gz
gunzip concorde.gz 
chmod u+x concorde
python kfc_tour.py
```

The resulting .kml file can be plotted with Google Earth or [GPS Visualizer](http://www.gpsvisualizer.com).


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/dbarlett/kfc-tour/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

