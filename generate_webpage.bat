@echo off    
jupyter nbconvert PretAnalysis.ipynb --to python
python PretAnalysis.py
git add .
git commit -m "Version and Data Update"
git push origin master
exit /b