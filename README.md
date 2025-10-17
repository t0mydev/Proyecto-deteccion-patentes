# Proyecto-deteccion-patentes
Proyecto utilizando YOLO para reconocimiento de patentes automáticamente


This project uses [poetry](https://python-poetry.org/)

## Quickstart

1. Create a `videos` folder inside `ravinala_airports_parking` and copy the `entree_2ms.mp4` and `exit_2ms.mp4` videos
2. Create a `models` folder inside `ravinala_airports_parking` and copy the `best.pt` file
3. Run `poetry shell` to activate the virtual environment
4. Run `poetry install` to install depedencies. To install additional dependencies use `poetry add <dependency-name>`
5. Run `python main.py` to run the project 

*IMPORTANT NOTE*

This POC has been developed using state-of-art all purpose models. 

In production the best practice is to use fine-tuned efficient models tailored for the use case, on this case, a model trained to read plates from Madagascar.

Some interesting links: 

* https://github.com/stephanecharette/DarkPlate?tab=readme-ov-file#darkplate
* https://www.reddit.com/r/computervision/comments/ydxgeo/what_is_the_best_license_plate_recognition_ocr/
* https://www.youtube.com/watch?v=jz97_-PCxl4
