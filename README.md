The CadQuery Workbench for FreeCAD
=======================
[![GitHub version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=2.0.0&x2=0)](https://github.com/CadQuery/cadquery-freecad-workbench/releases/tag/v2.0.0)

## Introduction

This is a revised  Cadquery workbench on FreeCAD that allows the Code Editor to execute and display CadQuery models (*.py not macro). 

![image](https://github.com/user-attachments/assets/b0a90445-0fde-4a16-877d-aad6aee22931)


### Documentation
- [Introduction](docs/index.md#introduction)
- [Installation methode 1](docs/installation.md)


  After install build123d/ Cadquery in path:
  C:\Users\AppData\Roaming\Python\\Python311\site-packages\
  then copy revised WB to folder path
  C:\Users\AppData\Roaming\FreeCAD\Mod\ or
  following sequence instruction from Jeremy Wright in main hub (cadquery-freecad-workbench)
  then replace cadquery WB content by files of this branch to folder path:  C:\Users\AppData\Roaming\FreeCAD\Mod\

  Restart Freecad  then run test:
  
  +write code in code editor
  
  +click Execute Script to show model (for Build123d click "Execute Script" button in twice)

- [Installation methode 2](docs/installation.md)
  If you already installed in python in another path folder eg: C:\Users\Admin\AppData\Local\Programs\Python\Python313\Lib\site-packages\
  and dont want to install cadquery/ build123d again then copy cadquery/ build123d package & dependancies from old path folder to
  C:\Users\Admin\AppData\Local\Programs\FreeCAD 1.0\bin\Lib\site-packages\ (* Note need checking requirement dependancies of cadquery/build123d, some packages may already got in Freecad)
  then copy revised WB to folder path
  C:\Users\AppData\Roaming\FreeCAD\Mod\ , now Freecad can call core cadquery/build123d functions.
  
- [Usage](docs/usage.md)
- [Developers](docs/developers.md)

### Testing result

![image](https://github.com/user-attachments/assets/839e098a-d243-4ddd-9a7a-a5d2a2b0074f)

![image](https://github.com/user-attachments/assets/256e63b6-958f-4b4c-8072-14f608b7fc91)

option using "from cadquery.vis import show" 

![image](https://github.com/user-attachments/assets/339ce7de-6faa-4ad8-9b1a-4e564bdb17bc)

in Freecad environment, Cadquery - Build123d now are more convenient in usage with dialog  

<img width="780" height="360" alt="image" src="https://github.com/user-attachments/assets/04b3cb07-c6b1-4fa0-9116-dccf331cdb20" />


### Update some functions
<img width="329" height="302" alt="image" src="https://github.com/user-attachments/assets/22d46b6a-c240-4c28-9cef-86860ff3cf07" />



