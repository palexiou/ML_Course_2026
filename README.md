# Machine learning for bioinformatics

Hands-on notebooks and a group project. Open notebooks locally or in Google Colab and run the cells in order.

| Exercise | Topic | Colab |
| --- | --- | --- |
| [Exercise 1](exercise_1.ipynb) | Generate a synthetic motif dataset | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_1.ipynb) |
| [Exercise 2](exercise_2.ipynb) | Logistic regression with k-mers | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_2.ipynb) |
| [Exercise 3](exercise_3.ipynb) | Logistic regression on real promoters | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_3.ipynb) |
| [Exercise 4](exercise_4.ipynb) | Decision trees and random forests | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_4.ipynb) |
| [Exercise 5](exercise_5.ipynb) | Gradient boosting | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_5.ipynb) |
| [Exercise 6](exercise_6.ipynb) | Compare models on real promoters | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_6.ipynb) |
| [Exercise 7](exercise_7.ipynb) | Motif XOR: perceptron, random forest, and MLP | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_7.ipynb) |
| [Exercise 8](exercise_8.ipynb) | Positional motifs with a CNN | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_8.ipynb) |
| [Exercise 9](exercise_9.ipynb) | Learn CNN filters on real promoters | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_9.ipynb) |
| [Exercise 10](exercise_10.md) | Group project: miRNA target prediction · [2D CNN example](exercise_10.ipynb) | [Open](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_10.ipynb) |

Exercises 2, 4, and 5 use the CSV from Exercise 1; set `ifile` to its path.
In Colab, upload that CSV first. Other notebooks generate or download their data.
Colab links open the version on GitHub's `main` branch.

For local use, install dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate the Exercise 1 dataset from the command line:

```bash
python exercise_1.py --ofile exercise_1_output/dataset.csv
```

Run checks with `python -m unittest discover -s tests`.
