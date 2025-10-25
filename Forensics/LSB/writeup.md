In this challenge i have hidden the flag in LSB (Least Significant Bit) of the png file so you have many methodes to extract the flag :
First method : command linux : zsteg file.png (extract to you something hidden in the pixels of the image)
Second Method : make a script python to read the rgb channels of every pixels and read only the 8éme bit of every byte and concaten it and convert it to string you will see the flag then
Third method : you use stegsolve and project in the 0éme bits of RGB of the image and you will see the flag in the data , this will automatically concatenate the 8éme bit of every channel of every pixel to string
