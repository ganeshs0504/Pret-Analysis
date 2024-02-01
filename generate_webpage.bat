@echo off    
jupyter nbconvert PretAnalysis.ipynb --to python
python PretAnalysis.py
exit /b