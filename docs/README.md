# template-sphinx-docs
A template to quickly start a Sphinx documentation

# Install and build using venv

1. Create virtual environment
```
python3 -m venv venv
```
2. Source environment and install theme
```
source venv/bin/activate
pip3 install sphinx sphinx_rtd_theme
```
3. Clone repository in a `docs` folder
```
git clone git@github.com:rdesarz/template-sphinx-docs.git docs
```
4. Update `conf.py` with corresponding theme

5. Delete .git folder
```
rm -rf .git
```
6. Build docs
```
sphinx-build -b html source build
```

# (Optional) Use `plantuml`

Makefile is already updated to handle plantuml diagrams. You simply need to install plantuml
```
sudo apt-get install plantuml
```
