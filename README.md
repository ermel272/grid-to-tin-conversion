# Grid to TIN Conversion

This project implements two known Raster (grid) to Triangle Irregular Network (TIN) 
conversion algorithms. The goal of the project is to compare the speed and error
performance of both algorithms. The results of the experimentation can be seen [here][paper]. 
The project was written with Python 2.7.

### Installation
In the project root directory, run the following command:

```bash
python -m pip install -r requirements.txt
```

### Running the code

The project contains an interactive script for testing out and visualizing the conversion
algorithms. From the project root directory, run

```bash
python -i main.py
```

then you can demo the conversion by calling

```python
convert(sidelength=30, algorithm='fjallstrom', error=0.3)
```

- The sidelength parameter controls the sidelength of the randomly generated raster image.
- The algorithm parameter controls the algorithm used to perform the conversion. Acceptable
inputs are 'fjallstrom' and 'lee'.
- The error parameter controls the maximum error for interpolation on the generated TIN. As
this value approaches zero, the runtime of the conversion approaches infinity.

#### Examples

Here is an example of a 30 x 30 Raster Image converted at 40% Maximum Error using the 
Fjallstrom Algorithm:

![original]
![converted]

[original]: examples/original.png
[converted]: examples/converted.png
[paper]: https://github.com/ermel272/grid-to-tin-conversion/blob/master/paper.pdf
