# Snake Game

A classic snake game implemented in python using pygame library

## Installation
``` shell
git clone https://github.com/Alireza2317/Snake_Python
cd Snake_Game
pip3 install -r requirements.txt
```

## Running the game

```
python3 app.py
```

## Screenshot

Here is the default look of the game:

![2](https://github.com/user-attachments/assets/14fe5359-1378-4f00-821c-f574c9f347eb)

## Features

- Change the speed
	- You can change `FPS` manually in the code, which will change the speed. The higher the `FPS` the faster the game.
	- You can also change the game speed inside the game by pressing `+` and `-` buttons, to increase and decrease the speed.

- Change the size
  	- Tweaking `WN` and `HN` will change the number of pixels for width and height respectively.
  	- Also changing `BLOCK_SIZE` will determine the size of each pixel in the game.
  	  
  		![4](https://github.com/user-attachments/assets/7e639013-d378-4693-86c7-8bb3b3586bd6)
		![1](https://github.com/user-attachments/assets/a039a5a1-28d6-42e3-a72d-d23c4ad4a17d)

- Change the pixel shape
  	- You can set `SHAPE = 'circle'` to change the pixel shape. Default is `SHAPE = 'square'`.
  	  
  		![3](https://github.com/user-attachments/assets/13d6a6ef-f883-4b16-9085-2ea31f71b916)
	- When `SHAPE = 'square'`, you can change `ROUNDNESS` to change the roundness of the snake's head.
   		By default `ROUNDNESS` is equal to `BLOCK_SIZE` which will make the head round.
   		You can set `ROUNDNESS` to `0` to make the head square-shaped.

  		Here is how it looks for `ROUNDNESS = 0`:
   
   		![8](https://github.com/user-attachments/assets/41f030d6-9112-447c-bd5b-a2d45bf8b131)

- Change the colors and ultimately change the theme of the game
  
	![6](https://github.com/user-attachments/assets/fb3d84d8-f84a-4507-8e4e-67d367df019b)
	![5](https://github.com/user-attachments/assets/4881ff0c-c303-4bbc-84cd-27c272443519)

- Change number of foods
  
	You can change `NUM_FOODS` to set the number of foods of the game. The default is of course `1`.

	Here is how it looks for `NUM_FOODS = 3`:

	![7](https://github.com/user-attachments/assets/68fcf5bd-35a8-4c86-82b6-dc53c63f119f)

## Thanks
Thank you for checking this project out. Hope you enjoy playing this classic game 🙂.

