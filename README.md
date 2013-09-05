KFC-Tour
========

Optimal tours of KFC locations, inspired by https://news.ycombinator.com/item?id=6324462

Tested on Ubuntu 12.10 64-bit.

Installation & usage:

```bash
pip install -r requirements.txt
wget http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/linux24/concorde.gz
gunzip concorde.gz 
chmod u+x concorde
python kfc_tour.py
```

The resulting .kml file can be plotted with http://www.gpsvisualizer.com
