texasmaps
=========

I made some maps like this:

https://drive.google.com/drive/folders/1vcfPCNVYbI_p5rNHyYOthMEAPveMXzOs?usp=sharing

make your own
=============

Probably like:

	pipenv install
        pipenv shell
	./map.py --level 0 --start -73 -17
	xdg-open map.png  # or something more Cupertino friendly


get some city names
===================

Assuming the above worked, maybe like:

	sudo apt install tesseract-ocr
	./find_cities.py map.png out.png
	xdg-open out.png
